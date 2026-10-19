"""Orquestração: guardrails -> recuperação -> política de rota -> geração -> validação -> auditoria."""
from __future__ import annotations

import time
from pathlib import Path

from . import config, guardrails
from .audit import Audit, FilaHITL, mascarar
from .generator import gerar_extrativo, gerar_llm, itens_de
from .kb import Chunk, load_chunks
from .llm import Provider
from .models import Item, Resposta
from .retriever import Hit, Retriever
from .validator import validar

POL_SEG = ("Não executo ações no SAP e não altero minhas regras com base em instruções escritas dentro do chamado. "
           "Registrei a tentativa e encaminhei o caso a um consultor humano (KB-FIAA-012 e KB-FIAA-010).")
POL_NAO_SAP = ("Este assunto não está relacionado a SAP FI-AA e está fora do escopo deste assistente (KB-FIAA-012). "
               "Posso ajudar com dúvidas de ativo fixo: dados mestre, transações, depreciação, fechamento e integração com o razão.")
POL_RISCO = ("Não executo ações no SAP. A ação solicitada tem impacto contábil e depende de autorização humana "
             "(KB-FIAA-010). Abaixo estão o que a documentação indica e verificações somente leitura; o caso foi encaminhado "
             "para validação humana.")
# Foco de documentos por intenção e por ação de risco detectada (decidido por regra, não pelo LLM)
DOCS_INTENCAO = {"integracao": ["KB-FIAA-007"], "mestre": ["KB-FIAA-002", "KB-FIAA-013"], "depreciacao": ["KB-FIAA-006"],
                 "fechamento": ["KB-FIAA-008"], "transacao": [], "informativa": []}
DOCS_ACAO = {"estorno": ["KB-FIAA-005"], "baixa": ["KB-FIAA-005"], "transferencia": ["KB-FIAA-005"],
             "reabertura_exercicio": ["KB-FIAA-008"], "encerramento": ["KB-FIAA-008"], "liquidacao_auc": ["KB-FIAA-004"],
             "execucao_depreciacao": ["KB-FIAA-006"], "alteracao_mestre": ["KB-FIAA-002"], "ajuste_saldo": ["KB-FIAA-007"],
             "concessao_acesso": ["KB-FIAA-009"], "exclusao_bloqueio": ["KB-FIAA-002"]}
# Linha da política KB-FIAA-010 correspondente a cada ação (ou intenção) detectada
PADRAO_ACAO = {"estorno": r"estorno", "baixa": r"^baixa|baixa e estorno", "transferencia": r"^transfer",
               "reabertura_exercicio": r"encerramento", "encerramento": r"encerramento", "liquidacao_auc": r"liquidar auc",
               "execucao_depreciacao": r"execu\w+ real da deprecia", "alteracao_mestre": r"alterar (centro|termos)|dados mestre",
               "ajuste_saldo": r"ajuste de saldo", "exclusao_bloqueio": r"excluir|desativar|bloquear",
               "concessao_acesso": r"acesso"}
PADRAO_INTENCAO = {"depreciacao": r"execu\w+ real da deprecia|termos de deprecia", "fechamento": r"encerramento",
                   "mestre": r"alterar (centro|termos)|dados mestre|excluir", "integracao": r"ajuste de saldo",
                   "transacao": r"^baixa|^transfer|liquidar auc"}
INTENCAO_ROTULO = {"integracao": "divergência entre FI-AA e razão (Integration)", "mestre": "dados mestre (Asset Master Records)",
                   "depreciacao": "depreciação (Depreciation)", "fechamento": "fechamento (Closing Operations)",
                   "transacao": "transações (Transactions)", "informativa": "dúvida sobre o módulo"}


ROTULO_SLOT = {"empresa": "empresa", "ativo": "ativo", "periodo": "período", "conta_ou_classe": "conta/classe",
               "ledger_ou_area": "ledger/área de depreciação", "valor_diferenca": "valor da diferença", "campo": "campo"}


class Assistente:
    def __init__(self, provider: Provider | None = None, kb_dir: Path | None = None, log_dir: Path | None = None):
        self.chunks = load_chunks(kb_dir)
        self.retr = Retriever(self.chunks)
        self.provider = provider
        self.audit = Audit(log_dir or config.LOG_DIR)
        self.fila = FilaHITL(log_dir or config.LOG_DIR)
        self.historico: dict[str, list[str]] = {}
        self.perguntas_feitas: dict[str, int] = {}

    # ------------------------------------------------------------------ API pública
    def processar(self, texto: str, ticket_id: str = "T-000", sessao: str | None = None) -> Resposta:
        t0 = time.time()
        sessao = sessao or ticket_id
        previas = self.historico.get(sessao, [])
        combinado = "\n".join(previas + [texto])
        n_ask = self.perguntas_feitas.get(sessao, 0)
        a = guardrails.analisar(combinado, self.retr)
        hits = self.retr.search(combinado, config.TOP_K)
        top = hits[0].relevancia if hits else 0.0
        resp = Resposta(ticket_id=ticket_id, rodada=n_ask + 1, route="ANSWER",
                        provider=getattr(self.provider, "name", "extractive"))
        resp.flags = {"injecao": a.injecao, "area_fora": a.area_fora, "pediu_execucao": a.pediu_execucao,
                      "intencao": a.intencao, "slots_faltantes": a.slots_faltantes,
                      "codigos_desconhecidos": a.codigos_desconhecidos, "tema_sem_cobertura": a.tema_sem_cobertura, "relevancia_topo": round(top, 3),
                      "acoes_mencionadas": a.acoes_mencionadas}
        usados: list[Chunk] = []

        # 1) segurança: instrução maliciosa embutida
        if guardrails.detectar_injecao(texto):
            self._rota(resp, "ESCALATE_SECURITY", POL_SEG, encaminhar=True)
            resp.fontes = self._fontes_politica(["KB-FIAA-012", "KB-FIAA-010"])
        # 2) fora do domínio SAP
        elif not a.parece_sap and top < config.LIMIAR_ALTO:   # sem termo de domínio, só um casamento forte justifica seguir
            self._rota(resp, "REFUSE_NOT_SAP", POL_NAO_SAP)
            resp.fontes = self._fontes_politica(["KB-FIAA-012"])
        # 3) área FI-AA fora do escopo
        elif a.area_fora:
            self._rota(resp, "ESCALATE_OUT_OF_SCOPE",
                       f"O tema identificado é **{a.area_fora}**, que está fora do escopo deste assistente (KB-FIAA-012). "
                       "Não farei diagnóstico nem orientação de correção. Encaminhei o caso a um consultor humano com o resumo abaixo.",
                       encaminhar=True)
            resp.entendimento = "Resumo para o consultor: " + mascarar(combinado.strip())[:300]
            resp.area = a.area_fora
            resp.fontes = self._fontes_politica(["KB-FIAA-012", "KB-FIAA-001"])
        # 4) identificador (ex.: código de erro) que não existe na base
        elif a.codigos_desconhecidos:
            self._rota(resp, "NO_EVIDENCE",
                       f"Não encontrei evidência na base para o identificador {', '.join(a.codigos_desconhecidos)}. "
                       "Não vou inferir o significado nem uma solução (KB-FIAA-012). Encaminhei o caso a um consultor humano.",
                       encaminhar=True)
            resp.perguntas = ["Qual é o texto completo da mensagem e a transação em que ela aparece?",
                              "Qual é o número do ativo e a empresa envolvidos?"]
            resp.confianca = "Sem evidência"
            resp.fontes = self._fontes_politica(["KB-FIAA-012"])
        # 4b) tema vizinho (ex.: tributação) sem documento na base
        elif a.tema_sem_cobertura:
            self._rota(resp, "NO_EVIDENCE",
                       f"O tema **{a.tema_sem_cobertura}** não tem cobertura na base de conhecimento deste protótipo (KB-FIAA-012). "
                       "Não vou inferir transações nem regras. Encaminhei o caso a um consultor humano.", encaminhar=True)
            resp.perguntas = ["Pode detalhar o processo, a empresa e o ativo envolvidos para o consultor?"]
            resp.confianca = "Sem evidência"
            resp.fontes = self._fontes_politica(["KB-FIAA-012"])
        # 5) dados faltantes
        elif a.slots_faltantes and a.intencao != "informativa" and not a.pediu_execucao:
            if n_ask >= config.MAX_RODADAS_PERGUNTAS:
                self._rota(resp, "ESCALATE_INFO",
                           "Mesmo após duas rodadas de perguntas, ainda faltam dados mínimos (KB-FIAA-011). "
                           "Encaminhei o caso a um consultor humano.", encaminhar=True)
                resp.fontes = self._fontes_politica(["KB-FIAA-011"])
            else:
                self._rota(resp, "ASK", "")
                resp.perguntas = [guardrails.PERGUNTAS[s] for s in a.slots_faltantes][: config.MAX_PERGUNTAS_POR_RODADA]
                resp.confianca = "Baixa"
                resp.entendimento = f"Entendi o chamado como {INTENCAO_ROTULO[a.intencao]}, mas faltam dados para analisar."
                resp.area = INTENCAO_ROTULO[a.intencao]
                resp.fontes = self._fontes_politica(["KB-FIAA-011"])
                self.perguntas_feitas[sessao] = n_ask + 1
                self.historico[sessao] = previas + [texto]
        # 6) sem evidência suficiente
        elif top < config.LIMIAR_RELEVANCIA and not a.pediu_execucao:
            self._rota(resp, "NO_EVIDENCE",
                       "Não encontrei evidência suficiente na base para responder com segurança (KB-FIAA-012). "
                       "Encaminhei o caso a um consultor humano.", encaminhar=True)
            resp.perguntas = ["Pode informar o texto completo da mensagem, a transação e o número do ativo?"]
            resp.confianca = "Sem evidência"
            resp.fontes = self._fontes_politica(["KB-FIAA-012"])
        # 7) resposta fundamentada (inclui pedido de execução, que é orientado e escalado)
        else:
            usados = self._responder(resp, a, hits, combinado)

        resp.area = resp.area or (hits[0].chunk.area if hits else "")
        self._finalizar(resp, a, hits, usados, texto, combinado, t0)
        if resp.route not in ("ASK",):
            self.historico.pop(sessao, None)
            self.perguntas_feitas.pop(sessao, None)
        return resp

    # ------------------------------------------------------------------ internos
    @staticmethod
    def _rota(resp: Resposta, rota: str, msg: str, encaminhar: bool = False):
        resp.route, resp.mensagem_politica, resp.encaminhar_humano = rota, msg, encaminhar

    def _fontes_politica(self, docs: list[str]) -> list[dict]:
        return [{"id": d, "titulo": next((c.titulo_doc for c in self.chunks if c.doc_id == d), d), "trechos": []} for d in docs]

    def _responder(self, resp: Resposta, a, hits: list[Hit], consulta: str) -> list[Chunk]:
        incidente = a.incidente or a.pediu_execucao
        foco = list(DOCS_INTENCAO.get(a.intencao, []))
        for ac in a.acoes_mencionadas:
            foco += [d for d in DOCS_ACAO.get(ac, []) if d not in foco]
        mostrar = bool(incidente or a.acoes_mencionadas)
        padroes = [PADRAO_ACAO[x] for x in a.acoes_mencionadas if x in PADRAO_ACAO]
        if incidente and a.intencao in PADRAO_INTENCAO:
            padroes.append(PADRAO_INTENCAO[a.intencao])
        secs, usados = gerar_extrativo(self.retr, hits, consulta, incidente, mostrar_acoes=mostrar, docs_foco=foco,
                                       padroes_acao=padroes)
        ids = {c.id for c in usados}
        contexto = "\n".join(c.texto for c in usados)
        resp.area = hits[0].chunk.area if hits else ""
        resp.entendimento = (f"Chamado classificado como {INTENCAO_ROTULO[a.intencao]}"
                             + (f"; dados identificados: {', '.join(ROTULO_SLOT.get(s, s) for s in a.slots_presentes)}." if a.slots_presentes else "."))
        final = {"conteudo": secs["conteudo"], "causas": secs["causas"], "verificacoes": secs["verificacoes"], "acoes": secs["acoes"]}
        validacao = {"modo": "extrativo", "ok": True, "violacoes": []}

        if self.provider is not None:
            # o LLM recebe, em primeiro lugar, os trechos que a seleção por regra já usou como evidência
            citados = [f for lst in secs.values() for it in lst for f in it.fontes]
            ctx_llm = self._contexto_llm(hits, usados, citados)
            try:
                parsed, bruto = gerar_llm(self.provider, ctx_llm, consulta, resp.area, resp.route, a.pediu_execucao)
                erro_chamada = None
            except Exception as e:   # rede, chave, modelo ausente, timeout: nunca derruba o atendimento
                parsed, erro_chamada = None, f"{type(e).__name__}: {e}"[:200]
            if erro_chamada:
                resp.fallback = True
                validacao = {"modo": "llm->extrativo", "ok": False, "violacoes": [f"falha na chamada ao LLM: {erro_chamada}"]}
                resp.avisos.append("O LLM não respondeu; usei a resposta extrativa, fundamentada na base.")
            elif parsed:
                cand = {"conteudo": itens_de(parsed.get("conteudo")), "causas": itens_de(parsed.get("causas_possiveis")),
                        "verificacoes": itens_de(parsed.get("verificacoes_recomendadas")), "acoes": itens_de(parsed.get("acoes_humanas"))}
                v = validar(cand, [str(parsed.get("entendimento", ""))], {c.id for c in ctx_llm},
                            "\n".join(c.texto for c in ctx_llm), consulta)
                if v.ok:
                    # as ações humanas vêm sempre da base (seção 'Exige validação humana'); o LLM complementa
                    cand["acoes"] = (secs["acoes"] + [i for i in cand["acoes"] if i.texto not in {x.texto for x in secs["acoes"]}])[:4]
                    final = cand
                    if parsed.get("entendimento"):
                        resp.entendimento = str(parsed["entendimento"])
                    validacao = {"modo": "llm", "ok": True, "violacoes": []}
                    ids = {c.id for c in ctx_llm} | {c.id for c in usados}
                else:
                    resp.fallback = True
                    validacao = {"modo": "llm->extrativo", "ok": False, "violacoes": v.violacoes}
                    resp.avisos.append("A resposta do LLM não passou na validação de fundamentação e foi substituída pela resposta extrativa.")
            else:
                resp.fallback = True
                b = bruto or ""
                fim = getattr(self.provider, "ultimo_finish", "")
                diag = f"saída do LLM não é JSON válido (finish_reason={fim or 'n/d'}; {len(b)} caracteres; início: {b[:160]!r}; fim: {b[-80:]!r})"
                validacao = {"modo": "llm->extrativo", "ok": False, "violacoes": [diag]}
                resp.avisos.append("A saída do LLM não era válida e foi substituída pela resposta extrativa.")

        resp.conteudo, resp.causas, resp.verificacoes, resp.acoes_humanas = (
            final["conteudo"], final["causas"], final["verificacoes"], final["acoes"])
        # validação final (também cobre o modo extrativo)
        v2 = validar({"conteudo": resp.conteudo, "causas": resp.causas, "verificacoes": resp.verificacoes, "acoes": resp.acoes_humanas},
                     [resp.entendimento], ids, contexto if validacao["modo"] != "llm" else "\n".join(c.texto for c in self._contexto_llm(hits, usados)) + "\n" + contexto,
                     consulta)
        resp.validacao = {**validacao, "ok_final": v2.ok, "violacoes_finais": v2.violacoes}
        if not v2.ok:
            self._rota(resp, "NO_EVIDENCE", "A resposta gerada não passou na validação de fundamentação e foi bloqueada. "
                       "Encaminhei o caso a um consultor humano.", encaminhar=True)
            resp.conteudo = resp.causas = resp.verificacoes = resp.acoes_humanas = []
            resp.confianca = "Sem evidência"
            return usados

        # avisos obrigatórios (KB-FIAA-012)
        citados = {i.fontes[0].split("#")[0] for lst in (resp.conteudo, resp.causas, resp.verificacoes) for i in lst if i.fontes}
        if citados & {"KB-FIAA-013", "KB-FIAA-014"} or any("tamanho" in i.texto.lower() for i in resp.conteudo):
            resp.avisos.append("Tipos e tamanhos de campo são os do template SAP de migração (TS07, S4CORE 103, 2019) e devem ser validados no sistema do cliente.")
        if "KB-FIAA-007" in citados:
            resp.avisos.append("Em Integration o assistente apenas orienta com base na documentação; não leu saldos reais.")

        if a.pediu_execucao:
            self._rota(resp, "ESCALATE_RISK", POL_RISCO, encaminhar=True)
        resp.acao_humana_necessaria = bool(a.pediu_execucao or (a.incidente and a.intencao != "informativa"))
        resp.confianca = self._confianca(hits, a)
        return usados

    def _contexto_llm(self, hits: list[Hit], usados: list[Chunk], citados: list[str] | None = None) -> list[Chunk]:
        """Ordem de prioridade: (1) trechos citados pela seleção por regra, (2) melhores resultados da busca,
        (3) causas/verificações/ações dos documentos usados. Limite de 14 trechos e ~12.000 caracteres."""
        por_id = {c.id: c for c in self.chunks}
        ordem = [por_id[i] for i in (citados or []) if i in por_id] + [h.chunk for h in hits] + \
                [c for c in usados if c.tipo in ("causas", "verificacoes", "acoes")]
        vistos, ctx, total = set(), [], 0
        for c in ordem:
            if c.id in vistos or len(ctx) >= 14 or total + len(c.texto) > 12000:
                continue
            vistos.add(c.id); ctx.append(c); total += len(c.texto)
        return ctx

    def _confianca(self, hits: list[Hit], a) -> str:
        suportes = [h for h in hits if h.relevancia >= config.LIMIAR_RELEVANCIA]
        docs = {h.chunk.doc_id for h in suportes}
        if not suportes:
            return "Sem evidência"
        forte = any(h.relevancia >= config.LIMIAR_ALTO for h in suportes)
        nivel = "Alta" if (forte and len(suportes) >= 2 and len(docs) >= 2) else "Média"
        # KB-FIAA-010: teto Média quando há pedido de execução ou na área Integration (modo orientação)
        if nivel == "Alta" and (a.pediu_execucao or a.intencao == "integracao"):
            nivel = "Média"
        return nivel

    def _finalizar(self, resp: Resposta, a, hits, usados, texto, combinado, t0):
        cit: dict[str, set[str]] = {}
        for lst in (resp.conteudo, resp.causas, resp.verificacoes, resp.acoes_humanas):
            for it in lst:
                for f in it.fontes:
                    cit.setdefault(f.split("#")[0], set()).add(f)
        if cit:
            resp.fontes = [{"id": d, "titulo": next((c.titulo_doc for c in self.chunks if c.doc_id == d), d),
                            "trechos": sorted(t)} for d, t in sorted(cit.items())]
        # fila HITL
        if resp.hitl and resp.route not in ("ASK", "REFUSE_NOT_SAP"):
            acoes = [i.texto for i in resp.acoes_humanas] or [resp.mensagem_politica[:200]]
            motivo = resp.route if resp.route != "ANSWER" else "ação com impacto contábil recomendada na análise"
            self.fila.adicionar(resp.ticket_id, resp.route, motivo, acoes)
        self.audit.registrar({
            "ticket_id": resp.ticket_id, "rodada": resp.rodada, "chamado": mascarar(texto),
            "route": resp.route, "confianca": resp.confianca, "hitl": resp.hitl,
            "provider": resp.provider, "model": getattr(self.provider, "model", None),
            "prompt_version": config.PROMPT_VERSION, "fallback": resp.fallback, "flags": resp.flags,
            "recuperados": [{"id": h.chunk.id, "bm25": round(h.bm25, 2), "relevancia": round(h.relevancia, 3), "termos": h.termos}
                            for h in hits[:config.TOP_K]],
            "fontes_citadas": resp.fontes, "validacao": resp.validacao,
            "resposta": {"entendimento": resp.entendimento, "perguntas": resp.perguntas,
                         "causas": [i.__dict__ for i in resp.causas], "conteudo": [i.__dict__ for i in resp.conteudo],
                         "verificacoes": [i.__dict__ for i in resp.verificacoes],
                         "acoes_humanas": [i.__dict__ for i in resp.acoes_humanas], "avisos": resp.avisos,
                         "mensagem_politica": resp.mensagem_politica},
            "latencia_ms": int((time.time() - t0) * 1000)})
