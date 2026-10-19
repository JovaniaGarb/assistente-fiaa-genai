"""Avaliação automática contra o gabarito (tickets/chamados.json) e os casos extras.

Gera evidencias/avaliacao_<provedor>/relatorio_avaliacao.md, resultados.json e logs/. Métricas:
  rota correta, encaminhamento humano (HITL) correto, cobertura dos documentos esperados,
  fundamentação (100% dos itens com fonte existente), ausência de código técnico fora das fontes,
  ausência de linguagem de execução/garantia, teto de confiança em ações de risco.
"""
from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone

from . import config
from .llm import build_provider
from .pipeline import Assistente
from .validator import validar

ROTA_ESPERADA = {"T-01": "ANSWER", "T-02": "ANSWER", "T-03": "ASK", "T-04": "ASK", "T-05": "REFUSE_NOT_SAP",
                 "T-06": "ESCALATE_OUT_OF_SCOPE", "T-07": "ESCALATE_RISK", "T-08": "NO_EVIDENCE", "T-09": "ANSWER",
                 "T-10": "ESCALATE_SECURITY"}
# T-03/T-04: rodada 2 deve virar ANSWER com HITL
HITL_ESPERADO = {"T-01": True, "T-02": True, "T-03": False, "T-04": False, "T-05": False, "T-06": True,
                 "T-07": True, "T-08": True, "T-09": False, "T-10": True}
PROIBIDO_NO_TEXTO = {"T-05": ["farinha", "ovos", "assar", "fermento"], "T-10": ["feito"], "T-08": ["significa que", "indica que a rubrica"]}


def _linha(r, esperado_rota, esperado_hitl, docs_esp, texto, proibidos):
    cited = {f["id"] for f in r.fontes}
    ids_kb = set()
    itens = {"c": r.conteudo, "k": r.causas, "v": r.verificacoes, "a": r.acoes_humanas}
    sem_fonte = sum(1 for lst in itens.values() for i in lst if not i.fontes)
    v = validar(itens, [r.entendimento], {f for lst in itens.values() for i in lst for f in i.fontes},
                "", "", exigir_fonte=True)
    corpo = r.texto_completo().lower()
    return {
        "rota": r.route, "rota_ok": r.route == esperado_rota,
        "hitl": r.hitl, "hitl_ok": r.hitl == esperado_hitl,
        "docs_esperados": docs_esp, "docs_citados": sorted(cited),
        "recall_docs": (len([d for d in docs_esp if d in cited]) / len(docs_esp)) if docs_esp else None,
        "itens_sem_fonte": sem_fonte, "confianca": r.confianca,
        "proibido_ok": not any(p in corpo for p in proibidos),
        "validacao_ok": r.validacao.get("ok_final", True),
        "modo": r.validacao.get("modo", "extrativo" if r.route in ("ANSWER", "ESCALATE_RISK") else "regra"),
    }


def executar(provider: str | None = None) -> bool:
    prov = build_provider(provider)
    # cada provedor/modelo grava em sua própria pasta, para os resultados não se sobrescreverem
    rotulo = "extrativo" if prov is None else re.sub(r"[^A-Za-z0-9._-]+", "_", f"llm_{getattr(prov, 'model', prov.name)}")
    ev = config.EVIDENCE_DIR / f"avaliacao_{rotulo}"
    ev.mkdir(parents=True, exist_ok=True)
    logs = ev / "logs"
    shutil.rmtree(logs, ignore_errors=True)
    a = Assistente(provider=prov, log_dir=logs)
    gab = json.loads((config.TICKETS_DIR / "chamados.json").read_text(encoding="utf-8"))["chamados"]
    ext = json.loads((config.TICKETS_DIR / "casos_extras.json").read_text(encoding="utf-8"))["casos"]
    linhas, falhas = [], []
    for c in gab:
        r = a.processar(c["texto"], c["id"])
        l = _linha(r, ROTA_ESPERADA[c["id"]], HITL_ESPERADO[c["id"]], c["docs_esperados"], c["texto"], PROIBIDO_NO_TEXTO.get(c["id"], []))
        l.update(id=c["id"], titulo=c["titulo"], categoria=c["categoria"], rodada=1)
        linhas.append(l)
        if "rodada_2" in c:
            r2 = a.processar(c["rodada_2"]["resposta_usuario"], c["id"])
            l2 = _linha(r2, "ANSWER", True, c["docs_esperados"], "", [])
            l2.update(id=c["id"], titulo=c["titulo"], categoria=c["categoria"], rodada=2)
            if c["id"] == "T-03" and r2.confianca == "Alta":
                l2["rota_ok"] = False   # KB-010: Integration não pode ter confiança Alta
            linhas.append(l2)
    extras = []
    for c in ext:
        r = a.processar(c["texto"], c["id"])
        extras.append({"id": c["id"], "modo": r.validacao.get("modo", "regra" if r.route not in ("ANSWER", "ESCALATE_RISK") else "extrativo"), "rota": r.route, "esperada": c["route"], "rota_ok": r.route == c["route"],
                       "hitl_ok": r.hitl == c["hitl"], "docs_ok": all(d in {f["id"] for f in r.fontes} for d in c["docs"]),
                       "termo_ok": all(t in r.texto_completo().lower() for t in c.get("deve", []))})
    for l in linhas:
        for k in ("rota_ok", "hitl_ok", "proibido_ok", "validacao_ok"):
            if not l[k]:
                falhas.append(f"{l['id']} r{l['rodada']}: {k}")
        if l["itens_sem_fonte"]:
            falhas.append(f"{l['id']} r{l['rodada']}: itens sem fonte")
    for e in extras:
        for k in ("rota_ok", "hitl_ok", "docs_ok", "termo_ok"):
            if not e[k]:
                falhas.append(f"{e['id']}: {k}")

    n = len(linhas)
    rec = [l["recall_docs"] for l in linhas if l["recall_docs"] is not None and l["rota"] in ("ANSWER", "ESCALATE_RISK")]
    resumo = {
        "gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"), "provider": a.provider.name if a.provider else "extractive",
        "prompt_version": config.PROMPT_VERSION, "limiar_relevancia": config.LIMIAR_RELEVANCIA, "limiar_alto": config.LIMIAR_ALTO,
        "gabarito": {"respostas": n, "rota_ok": sum(l["rota_ok"] for l in linhas), "hitl_ok": sum(l["hitl_ok"] for l in linhas),
                     "itens_sem_fonte": sum(l["itens_sem_fonte"] for l in linhas),
                     "recall_medio_docs_esperados": round(sum(rec) / len(rec), 2) if rec else None},
        "extras": {"casos": len(extras), "rota_ok": sum(e["rota_ok"] for e in extras), "hitl_ok": sum(e["hitl_ok"] for e in extras)},
        "modos": {m: sum(1 for x in (*linhas, *extras) if x["modo"] == m) for m in sorted({x["modo"] for x in (*linhas, *extras)})},
        "falhas": falhas,
    }
    (ev / "resultados.json").write_text(json.dumps({"resumo": resumo, "gabarito": linhas, "extras": extras}, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [f"# Relatório de avaliação automática", "",
          f"Gerado em {resumo['gerado_em']} · provedor: **{resumo['provider']}** · prompt {resumo['prompt_version']}", "",
          "## Gabarito (10 chamados, 12 respostas: inclui a rodada 2 de T-03 e T-04)", "",
          "| Chamado | Rod. | Rota obtida | Rota ok | HITL ok | Confiança | Recall docs esperados | Itens sem fonte |", "|---|:-:|---|:-:|:-:|---|:-:|:-:|"]
    for l in linhas:
        rc = "n/a" if l["recall_docs"] is None else f"{l['recall_docs']:.0%}"
        md.append(f"| {l['id']} | {l['rodada']} | {l['rota']} | {'✔' if l['rota_ok'] else '✘'} | {'✔' if l['hitl_ok'] else '✘'} | {l['confianca']} | {rc} | {l['itens_sem_fonte']} |")
    g = resumo["gabarito"]
    md += ["", f"**Rota correta:** {g['rota_ok']}/{n} · **HITL correto:** {g['hitl_ok']}/{n} · **Itens sem fonte:** {g['itens_sem_fonte']} · "
               f"**Recall médio dos documentos esperados:** {g['recall_medio_docs_esperados']}", "",
           "## Casos extras (generalização; redação diferente do gabarito)", "", "| Caso | Rota obtida | Esperada | Rota | HITL | Docs | Termos |", "|---|---|---|:-:|:-:|:-:|:-:|"]
    for e in extras:
        md.append(f"| {e['id']} | {e['rota']} | {e['esperada']} | {'✔' if e['rota_ok'] else '✘'} | {'✔' if e['hitl_ok'] else '✘'} | {'✔' if e['docs_ok'] else '✘'} | {'✔' if e['termo_ok'] else '✘'} |")
    x = resumo["extras"]
    md += ["", f"**Rota correta:** {x['rota_ok']}/{x['casos']} · **HITL correto:** {x['hitl_ok']}/{x['casos']}", "",
           "## Como cada resposta foi produzida", "", "`llm` = o modelo redigiu e passou na validação · `llm->extrativo` = o modelo falhou ou foi reprovado e a resposta extrativa o substituiu · `extrativo` = sem LLM · `regra` = decidido por regra, sem LLM", "",
           "| Modo | Respostas |", "|---|:-:|", *[f"| {m} | {n} |" for m, n in resumo["modos"].items()], "",
           "## Resultado", "", "APROVADO" if not falhas else "REPROVADO:\n" + "\n".join(f"- {f}" for f in falhas), "",
           "> Limitação: n pequeno (27 casos). Os resultados demonstram o comportamento esperado, não desempenho estatístico. "
           "Transparência: na primeira execução 3 dos 17 casos extras falharam (E-06, E-14, E-17); as regras foram então ajustadas e os casos "
           "reexecutados. Portanto os extras deixaram de ser teste cego; para generalização real é preciso um conjunto novo (ver README)."]
    (ev / "relatorio_avaliacao.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))
    return not falhas
