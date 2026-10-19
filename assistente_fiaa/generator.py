"""Geração da resposta fundamentada: modo extrativo (offline) e modo LLM.

O modo extrativo monta a resposta SÓ com linhas da base (fundamentada por construção).
O modo LLM redige a partir dos trechos, mas passa pelo validador; se falhar, usa o extrativo.
"""
from __future__ import annotations

import re

from . import config, prompts
from .kb import Chunk
from .llm import Provider, parse_json
from .models import Item
from .retriever import Retriever
from .text import tokenize


def _limpa(linha: str) -> str:
    l = linha.strip()
    if not re.search(r"\s2\.\s", l):          # mantém "1." quando a linha é uma sequência numerada
        l = re.sub(r"^(\d+\.|[-*])\s+", "", l)
    else:
        l = re.sub(r"^[-*]\s+", "", l)
    return l.replace("**", "").strip()


_RE_FONTE = re.compile(r"^(HELP|S4F17|TS07|DD)\b")


def _formata_linha(linha: str) -> str | None:
    """Converte linhas de tabela em texto legível; descarta cabeçalhos e vazios."""
    l = linha.strip()
    if not l or l.startswith("#"):
        return None
    if l.startswith("|"):
        cols = [c.strip() for c in l.strip("|").split("|")]
        if not any(cols[1:]):
            return None   # linha de separador de folha
        if cols[0] in ("Campo", "Tipo", "Ação", "Nível", "Forma", "Erro", "Classe", "Termo", "Área", "Atividade", "Papel", "Risco"):
            return None
        if len(cols) == 6 and cols[2] in ("Texto", "Número", "Data"):
            return (f"Campo {cols[0]} ({cols[1]}): tipo {cols[2]}, tamanho {cols[3]}, decimais {cols[4]}, "
                    f"obrigatório na folha: {cols[5]} [TS07]")
        cols = [c for c in cols if c]
        fonte = ""
        if len(cols) > 1 and _RE_FONTE.match(cols[-1]):
            fonte = f" [{cols[-1]}]"
            cols = cols[:-1]
        if len(cols) == 1:
            return _limpa(cols[0] + fonte)
        return _limpa(f"{cols[0]}: {' — '.join(cols[1:])}{fonte}")
    return _limpa(l)


def _unidades(chunk: Chunk) -> list[str]:
    out = []
    for ln in chunk.texto.splitlines():
        f = _formata_linha(ln)
        if f and len(f) > 12:
            out.append(f)
    return out


def _score(retr: Retriever, termos: list[str], unidade: str) -> tuple[float, int]:
    toks = set(tokenize(unidade))
    casados = [t for t in termos if t in toks and t in retr.idf]
    return sum(retr.idf[t] for t in casados), len(casados)


GOVERNANCA = {"KB-FIAA-010", "KB-FIAA-011", "KB-FIAA-012"}
TRANSVERSAIS = {"KB-FIAA-001"}   # mapa e glossário: só entram quando não há foco definido por regra


def selecionar_docs(hits, docs_foco: list[str], max_docs: int = 4) -> list[str]:
    """Documentos de domínio usados na resposta: os do foco (intenção e ações detectadas por regra) e os
    demais só se forem muito relevantes. Governança (010-012) nunca entra como conteúdo."""
    docs = [d for d in docs_foco if d not in GOVERNANCA]
    for h in hits:
        if h.chunk.doc_id in GOVERNANCA or h.chunk.doc_id in docs:
            continue
        if docs_foco and h.chunk.doc_id in TRANSVERSAIS:
            continue
        limite = config.LIMIAR_ALTO if docs_foco else config.LIMIAR_RELEVANCIA * 0.6
        if h.relevancia >= limite:
            docs.append(h.chunk.doc_id)
        if len(docs) >= max_docs:
            break
    return docs[:max_docs]


def gerar_extrativo(retr: Retriever, hits, consulta: str, incidente: bool, mostrar_acoes: bool,
                    docs_foco: list[str] | None = None, max_docs: int = 4, padroes_acao: list[str] | None = None) -> tuple[dict[str, list[Item]], list[Chunk]]:
    """Monta a resposta SÓ com linhas da base. Retorna seções e os trechos efetivamente usados."""
    termos = retr.termos_consulta(consulta)
    docs = selecionar_docs(hits, docs_foco or [], max_docs)
    usados = [c for c in retr.chunks if c.doc_id in docs]
    secoes: dict[str, list[tuple[float, Item]]] = {"conteudo": [], "causas": [], "verificacoes": [], "acoes": []}
    for c in usados:
        for u in _unidades(c):
            sc, n = _score(retr, termos, u)
            if c.tipo == "causas":
                if incidente:
                    secoes["causas"].append((sc + 1, Item(u, [c.id])))
            elif c.tipo == "verificacoes":
                if incidente:
                    secoes["verificacoes"].append((sc + 1, Item(u, [c.id])))
            elif c.tipo == "acoes":
                if mostrar_acoes:
                    secoes["acoes"].append((sc + 1, Item(u, [c.id])))
            elif c.tipo == "conteudo" and n >= 2 and c.secao.lower() not in ("quando se aplica",):
                secoes["conteudo"].append((sc, Item(u, [c.id])))
    if mostrar_acoes:   # linhas da política de HITL (KB-FIAA-010) que casam com a consulta
        for c in retr.chunks:
            if c.doc_id == "KB-FIAA-010" and c.secao.upper().startswith("AÇÕES QUE SEMPRE"):
                for u in _unidades(c):
                    sc, n = _score(retr, termos, u)
                    # a linha da política entra se casa com uma ação detectada por regra (ou, sem regra, com >=2 termos)
                    casa = (any(re.search(p, u, re.I) for p in padroes_acao) if padroes_acao else n >= 2)
                    if casa:
                        secoes["acoes"].append((sc + 2, Item(u, [c.id])))
                        if c not in usados:
                            usados.append(c)
    limites = {"conteudo": 5, "causas": 4, "verificacoes": 4, "acoes": 3}
    out: dict[str, list[Item]] = {}
    for k, lst in secoes.items():
        lst.sort(key=lambda x: -x[0])
        vistos, itens = set(), []
        for _, it in lst:
            if it.texto not in vistos:
                vistos.add(it.texto); itens.append(it)
            if len(itens) >= limites[k]:
                break
        out[k] = itens
    return out, usados


def _formata_trechos(chunks: list[Chunk]) -> str:
    return "\n\n".join(f"[{c.id}]\n{c.texto}" for c in chunks)


def gerar_llm(provider: Provider, chunks: list[Chunk], chamado: str, area: str, rota: str,
              pediu_execucao: bool) -> tuple[dict | None, str]:
    user = prompts.USER_TEMPLATE.format(trechos=_formata_trechos(chunks), area=area or "indefinida",
                                        rota=rota, pediu_execucao="sim" if pediu_execucao else "não",
                                        chamado=chamado)
    bruto = provider.complete(prompts.SYSTEM_PROMPT, user)
    parsed = parse_json(bruto)
    if not parsed:   # uma segunda tentativa, pedindo só o JSON compacto (corta texto antes/depois e respostas longas)
        bruto2 = provider.complete(prompts.SYSTEM_PROMPT, user + "\n\nResponda SOMENTE com o objeto JSON, compacto, sem texto antes ou depois e sem cercas de código.")
        parsed2 = parse_json(bruto2)
        if parsed2:
            return parsed2, bruto2
        bruto = bruto + "\n--- 2ª tentativa ---\n" + bruto2
    return parsed, bruto


def itens_de(lista) -> list[Item]:
    itens = []
    for x in lista or []:
        if isinstance(x, dict):
            itens.append(Item(str(x.get("texto", "")).strip(), [str(f) for f in x.get("fontes", [])]))
    return itens
