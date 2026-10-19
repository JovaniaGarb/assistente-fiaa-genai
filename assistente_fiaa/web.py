"""Interface web local (somente biblioteca padrão). Uso: python -m assistente_fiaa web
Escuta apenas em 127.0.0.1. Sem autenticação: é um protótipo local."""
from __future__ import annotations

import json
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import config
from .pipeline import Assistente

LOCK = threading.Lock()
ASSIST: Assistente | None = None


def _exemplos() -> list[dict]:
    d = json.loads((config.TICKETS_DIR / "chamados.json").read_text(encoding="utf-8"))["chamados"]
    out = [{"id": c["id"], "titulo": c["titulo"], "categoria": c["categoria"], "texto": c["texto"],
            "rodada_2": c.get("rodada_2", {}).get("resposta_usuario")} for c in d]
    return out


def _resumo_avaliacao() -> dict:
    arqs = sorted(config.EVIDENCE_DIR.glob("avaliacao_*/resultados.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return json.loads(arqs[0].read_text(encoding="utf-8")) if arqs else {}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):  # silencioso
        pass

    def _send(self, code: int, body: bytes, ctype="application/json; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj, ensure_ascii=False).encode("utf-8"))

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self._send(200, PAGINA.encode("utf-8"), "text/html; charset=utf-8")
        if self.path == "/api/exemplos":
            return self._json(_exemplos())
        if self.path == "/api/fila":
            with LOCK:
                return self._json(ASSIST.fila.listar())
        if self.path == "/api/auditoria":
            with LOCK:
                return self._json(ASSIST.audit.ler()[-30:][::-1])
        if self.path == "/api/avaliacao":
            return self._json(_resumo_avaliacao())
        self._send(404, b'{"erro":"nao encontrado"}')

    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length", "0"))
            if n > 20000:
                return self._json({"erro": "texto muito longo"}, 413)
            dados = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._json({"erro": "requisição inválida"}, 400)
        with LOCK:
            if self.path == "/api/chamado":
                texto = str(dados.get("texto", ""))[:5000]
                sessao = str(dados.get("sessao", "WEB-1"))[:40]
                r = ASSIST.processar(texto, sessao)
                d = r.to_dict()
                d["markdown"] = r.to_markdown()
                d["hitl"] = r.hitl
                return self._json(d)
            if self.path == "/api/fila/decidir":
                try:
                    item = ASSIST.fila.decidir(str(dados.get("id")), bool(dados.get("aprovado")),
                                               str(dados.get("revisor") or "consultor.humano")[:60],
                                               str(dados.get("comentario") or "")[:300])
                except KeyError:
                    return self._json({"erro": "item inexistente"}, 404)
                ASSIST.audit.registrar({"evento": "decisao_humana", "hitl_id": item["id"], "ticket_id": item["ticket_id"],
                                        "status": item["status"], "revisor": item["decisao"]["revisor"]})
                return self._json(item)
        self._send(404, b'{"erro":"nao encontrado"}')


def servir(provider=None, porta: int = 8765, abrir: bool = True):
    global ASSIST
    ASSIST = Assistente(provider=provider)
    srv = ThreadingHTTPServer(("127.0.0.1", porta), H)
    url = f"http://127.0.0.1:{porta}"
    print(f"Assistente FI-AA no ar em {url}  (Ctrl+C para encerrar)")
    if abrir:
        try:
            webbrowser.open(url)
        except Exception:
            pass
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrado.")


PAGINA = r"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Assistente FI-AA</title>
<style>
:root{--bg:#f6f7f9;--card:#fff;--tx:#1d2330;--mut:#667085;--bd:#e3e6ec;--pri:#0b5cad;--ok:#13795b;--warn:#b54708;--warnbg:#fff4e5;--bad:#b42318;--badbg:#fdecea;--okbg:#e8f6f0;--info:#175cd3;--infobg:#eaf1fd}
@media(prefers-color-scheme:dark){:root{--bg:#12151c;--card:#1b2030;--tx:#e8ebf2;--mut:#98a2b3;--bd:#2d3447;--pri:#6aa8f5;--ok:#5fd0a5;--warn:#f5b05a;--warnbg:#3a2a12;--bad:#ff8f84;--badbg:#3b1b19;--okbg:#12342a;--info:#8ab4ff;--infobg:#172743}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:15px/1.5 system-ui,Segoe UI,Roboto,sans-serif}
header{padding:16px 24px;border-bottom:1px solid var(--bd);background:var(--card)}header h1{margin:0;font-size:18px}header p{margin:2px 0 0;color:var(--mut);font-size:13px}
nav{display:flex;gap:4px;padding:0 24px;background:var(--card);border-bottom:1px solid var(--bd)}
nav button{border:0;background:none;color:var(--mut);padding:12px 14px;font:inherit;cursor:pointer;border-bottom:2px solid transparent}
nav button.on{color:var(--pri);border-color:var(--pri);font-weight:600}
main{max-width:1180px;margin:0 auto;padding:20px 24px 60px}
.grid{display:grid;grid-template-columns:minmax(300px,420px) 1fr;gap:20px}@media(max-width:860px){.grid{grid-template-columns:1fr}}
.grid>*{min-width:0}.card{background:var(--card);border:1px solid var(--bd);border-radius:10px;padding:16px}
h2{font-size:14px;margin:0 0 10px;text-transform:uppercase;letter-spacing:.04em;color:var(--mut)}
textarea{width:100%;min-height:130px;border:1px solid var(--bd);border-radius:8px;padding:10px;font:inherit;background:var(--bg);color:var(--tx);resize:vertical}
.btn{border:1px solid var(--pri);background:var(--pri);color:#fff;border-radius:8px;padding:8px 14px;font:inherit;cursor:pointer}
.btn.sec{background:none;color:var(--pri)}.btn.ok{background:var(--ok);border-color:var(--ok)}.btn.bad{background:var(--bad);border-color:var(--bad)}
.btn:disabled{opacity:.5;cursor:wait}
.row{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;align-items:center}
.ex{display:block;width:100%;text-align:left;border:1px solid var(--bd);background:none;color:var(--tx);border-radius:8px;padding:8px 10px;margin-bottom:6px;cursor:pointer;font:inherit}
.ex:hover{border-color:var(--pri)}.ex small{color:var(--mut);display:block}
.badge{display:inline-block;padding:3px 10px;border-radius:999px;font-size:12px;font-weight:600}
.b-ANSWER{background:var(--okbg);color:var(--ok)}.b-ASK{background:var(--infobg);color:var(--info)}
.b-ESCALATE_RISK,.b-ESCALATE_OUT_OF_SCOPE,.b-ESCALATE_INFO,.b-NO_EVIDENCE{background:var(--warnbg);color:var(--warn)}
.b-ESCALATE_SECURITY{background:var(--badbg);color:var(--bad)}.b-REFUSE_NOT_SAP{background:var(--bd);color:var(--mut)}
.meta{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:12px}
.chip{font:12px ui-monospace,Consolas,monospace;background:var(--bg);border:1px solid var(--bd);color:var(--mut);border-radius:6px;padding:1px 6px;margin-left:4px;white-space:normal;word-break:break-all;display:inline-block}
.sec{margin:14px 0}.sec h3{margin:0 0 6px;font-size:14px}ul{margin:0;padding-left:20px}li{margin-bottom:6px}
.human{background:var(--warnbg);border:1px solid var(--warn);border-radius:8px;padding:10px 12px}.human h3{color:var(--warn)}
.policy{background:var(--infobg);border-left:4px solid var(--info);padding:10px 12px;border-radius:6px;margin-bottom:12px}
.aviso{color:var(--mut);font-size:13px;font-style:italic}
table{width:100%;border-collapse:collapse;font-size:13px}th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--bd);vertical-align:top}
.empty{color:var(--mut);padding:30px;text-align:center}
.hidden{display:none}input[type=text]{border:1px solid var(--bd);border-radius:8px;padding:7px 9px;font:inherit;background:var(--bg);color:var(--tx)}
details{margin-top:12px}summary{cursor:pointer;color:var(--mut);font-size:13px}pre{white-space:pre-wrap;font-size:12px;background:var(--bg);padding:10px;border-radius:8px;overflow:auto}
</style></head><body>
<header><h1>Assistente de análise de chamados SAP FI-AA</h1>
<p>Protótipo com dados fictícios. O assistente recomenda; nunca executa ações no SAP. Decisões de risco vão para validação humana.</p></header>
<nav><button class="on" data-t="chamado">Analisar chamado</button><button data-t="fila">Fila de validação humana <span id="nfila"></span></button><button data-t="audit">Auditoria</button><button data-t="aval">Avaliação</button></nav>
<main>
<section id="t-chamado" class="grid">
 <div>
  <div class="card"><h2>Chamado</h2>
   <textarea id="txt" placeholder="Descreva o chamado, ou escolha um exemplo abaixo."></textarea>
   <div class="row"><button class="btn" id="enviar">Analisar</button><button class="btn sec" id="novo">Novo chamado</button><span id="rodada" class="aviso"></span></div>
  </div>
  <div class="card" style="margin-top:16px"><h2>Exemplos do gabarito</h2><div id="exs"></div></div>
 </div>
 <div class="card" id="res"><div class="empty">A resposta aparece aqui.</div></div>
</section>
<section id="t-fila" class="card hidden"><h2>Itens aguardando decisão de uma pessoa</h2>
 <div class="row" style="margin:0 0 12px"><label>Revisor: <input type="text" id="revisor" value="seu.nome"></label></div><div id="filaconteudo"></div></section>
<section id="t-audit" class="card hidden"><h2>Últimos registros (audit.jsonl)</h2><div id="auditconteudo"></div></section>
<section id="t-aval" class="card hidden"><h2>Resultado da avaliação automática</h2><div id="avalconteudo"></div></section>
</main>
<script>
const $=s=>document.querySelector(s);
function el(tag,attrs={},...kids){const e=document.createElement(tag);for(const[k,v]of Object.entries(attrs)){if(k==='class')e.className=v;else if(k==='text')e.textContent=v;else e.setAttribute(k,v)}for(const c of kids.flat()){if(c==null)continue;e.append(c.nodeType?c:document.createTextNode(c))}return e}
let sessao='WEB-'+Date.now(), exemploAtual=null;
async function api(p,body){const r=await fetch(p,body?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}:{});return r.json()}
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{document.querySelectorAll('nav button').forEach(x=>x.classList.toggle('on',x===b));
 ['chamado','fila','audit','aval'].forEach(t=>$('#t-'+t).classList.toggle('hidden',t!==b.dataset.t));
 if(b.dataset.t==='fila')carregaFila();if(b.dataset.t==='audit')carregaAudit();if(b.dataset.t==='aval')carregaAval()});
const ROTAS={ANSWER:'Resposta fundamentada',ASK:'Preciso de mais informações',ESCALATE_RISK:'Ação de risco: encaminhado a humano',ESCALATE_OUT_OF_SCOPE:'Fora do escopo: encaminhado a humano',ESCALATE_INFO:'Dados insuficientes: encaminhado a humano',ESCALATE_SECURITY:'Tentativa bloqueada',NO_EVIDENCE:'Sem evidência na base',REFUSE_NOT_SAP:'Fora do domínio SAP'};
function itens(titulo,lst,cls){if(!lst||!lst.length)return null;const ul=el('ul');lst.forEach(i=>ul.append(el('li',{},i.texto,...(i.fontes||[]).map(f=>el('span',{class:'chip',text:f})))));
 return el('div',{class:'sec '+(cls||'')},el('h3',{text:titulo}),ul)}
function render(r){const box=$('#res');box.replaceChildren();
 box.append(el('div',{class:'meta'},el('span',{class:'badge b-'+r.route,text:ROTAS[r.route]||r.route}),el('span',{class:'chip',text:'confiança: '+r.confianca}),
  el('span',{class:'chip',text:'encaminhamento humano: '+(r.hitl?'sim':'não')}),r.area?el('span',{class:'chip',text:r.area}):null));
 if(r.mensagem_politica)box.append(el('div',{class:'policy',text:r.mensagem_politica.replace(/\*\*/g,'')}));
 if(r.entendimento)box.append(el('p',{},el('b',{text:'Entendimento: '}),r.entendimento));
 if(r.perguntas.length){const ol=el('ol');r.perguntas.forEach(p=>ol.append(el('li',{text:p})));box.append(el('div',{class:'sec'},el('h3',{text:'Para analisar, preciso destas informações'}),ol))}
 [itens('O que a documentação indica',r.conteudo),itens('Causas possíveis',r.causas),itens('Verificações recomendadas (somente leitura)',r.verificacoes),itens('Ação que depende de autorização humana (a IA não executa)',r.acoes_humanas,'human')].forEach(x=>x&&box.append(x));
 r.avisos.forEach(a=>box.append(el('p',{class:'aviso',text:'Aviso: '+a})));
 if(r.fontes.length)box.append(el('div',{class:'sec'},el('h3',{text:'Fontes consultadas'}),...r.fontes.map(f=>el('span',{class:'chip',text:f.id+' · '+f.titulo}))));
 box.append(el('details',{},el('summary',{text:'Detalhes técnicos (guardrails e validação)'}),el('pre',{text:JSON.stringify({flags:r.flags,validacao:r.validacao,provider:r.provider,rodada:r.rodada},null,2)})));
 $('#rodada').textContent=r.route==='ASK'?'Responda às perguntas e clique em Analisar de novo (rodada '+(r.rodada+1)+').':'';
 if(r.route==='ASK'&&exemploAtual&&exemploAtual.rodada_2){$('#txt').value='';$('#txt').placeholder='Dica de resposta (exemplo do gabarito): '+exemploAtual.rodada_2}
 atualizaFila()}
$('#enviar').onclick=async()=>{const t=$('#txt').value.trim();if(!t){$('#txt').focus();return}
 $('#enviar').disabled=true;try{render(await api('/api/chamado',{texto:t,sessao}))}catch(e){$('#res').textContent='Erro ao consultar o servidor.'}$('#enviar').disabled=false};
$('#novo').onclick=()=>{sessao='WEB-'+Date.now();exemploAtual=null;$('#txt').value='';$('#txt').placeholder='Descreva o chamado.';$('#rodada').textContent='';$('#res').replaceChildren(el('div',{class:'empty',text:'A resposta aparece aqui.'}))};
async function exemplos(){const ex=await api('/api/exemplos');ex.forEach(e=>{const b=el('button',{class:'ex'},el('b',{text:e.id+' '}),e.titulo,el('small',{text:e.categoria.replace('EXCECAO_','exceção: ').replace('SUCESSO','sucesso').toLowerCase()}));
 b.onclick=()=>{sessao='WEB-'+e.id+'-'+Date.now();exemploAtual=e;$('#txt').value=e.texto;$('#rodada').textContent='';$('#txt').focus()};$('#exs').append(b)})}
async function atualizaFila(){const f=await api('/api/fila');const n=f.filter(i=>i.status==='PENDENTE').length;$('#nfila').textContent=n?'('+n+')':''}
async function carregaFila(){const f=await api('/api/fila');const box=$('#filaconteudo');box.replaceChildren();atualizaFila();
 if(!f.length){box.append(el('div',{class:'empty',text:'Nenhum item. Analise um chamado de risco (ex.: T-07) para gerar um.'}));return}
 f.slice().reverse().forEach(i=>{const c=el('div',{class:'card',style:'margin-bottom:10px'},el('div',{class:'meta'},el('b',{text:i.id+' · '+i.ticket_id}),el('span',{class:'badge b-'+i.rota,text:ROTAS[i.rota]||i.rota}),el('span',{class:'chip',text:i.status})));
  const ul=el('ul');(i.acoes_propostas||[]).forEach(a=>ul.append(el('li',{text:a})));c.append(ul);
  if(i.status==='PENDENTE'){const com=el('input',{type:'text',placeholder:'Comentário (opcional)',style:'flex:1;min-width:200px'});
   const dec=async ok=>{await api('/api/fila/decidir',{id:i.id,aprovado:ok,revisor:$('#revisor').value,comentario:com.value});carregaFila()};
   const a=el('button',{class:'btn ok',text:'Aprovar'});a.onclick=()=>dec(true);const r=el('button',{class:'btn bad',text:'Rejeitar'});r.onclick=()=>dec(false);
   c.append(el('div',{class:'row'},com,a,r))}
  else c.append(el('p',{class:'aviso',text:'Decisão: '+i.status+' por '+i.decisao.revisor+(i.decisao.comentario?' — '+i.decisao.comentario:'')}));
  box.append(c)})}
async function carregaAudit(){const a=await api('/api/auditoria');const box=$('#auditconteudo');box.replaceChildren();
 if(!a.length){box.append(el('div',{class:'empty',text:'Sem registros ainda.'}));return}
 const t=el('table',{},el('tr',{},...['Hora (UTC)','Chamado','Rota','Confiança','HITL','Fontes'].map(h=>el('th',{text:h}))));
 a.forEach(x=>t.append(el('tr',{},x.ts||'',x.ticket_id||'',x.route||x.evento||'',x.confianca||'',x.hitl===undefined?(x.status||''):(x.hitl?'sim':'não'),(x.fontes_citadas||[]).map(f=>f.id).join(', '))));
 box.append(t)}
async function carregaAval(){const d=await api('/api/avaliacao');const box=$('#avalconteudo');box.replaceChildren();
 if(!d.resumo){box.append(el('div',{class:'empty',text:'Rode: python -m assistente_fiaa avaliar'}));return}
 const g=d.resumo.gabarito,x=d.resumo.extras;
 box.append(el('p',{},'Gabarito: rotas corretas ',el('b',{text:g.rota_ok+'/'+g.respostas}),' · encaminhamento humano correto ',el('b',{text:g.hitl_ok+'/'+g.respostas}),' · itens sem fonte ',el('b',{text:String(g.itens_sem_fonte)}),' · recall médio dos documentos esperados ',el('b',{text:String(g.recall_medio_docs_esperados)})));
 box.append(el('p',{},'Casos extras: rotas corretas ',el('b',{text:x.rota_ok+'/'+x.casos}),'. Falhas: ',el('b',{text:d.resumo.falhas.length?d.resumo.falhas.join('; '):'nenhuma'})));
 const t=el('table',{},el('tr',{},...['Chamado','Rodada','Rota obtida','Rota ok','HITL ok','Confiança'].map(h=>el('th',{text:h}))));
 d.gabarito.forEach(l=>t.append(el('tr',{},l.id,String(l.rodada),l.rota,l.rota_ok?'✔':'✘',l.hitl_ok?'✔':'✘',l.confianca)));box.append(t);
 box.append(el('p',{class:'aviso',text:'Amostra pequena: demonstra comportamento, não desempenho estatístico.'}))}
exemplos();atualizaFila();
</script></body></html>
"""
