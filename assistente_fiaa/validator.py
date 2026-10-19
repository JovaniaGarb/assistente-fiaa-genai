"""Validação pós-geração: barreira contra alucinação e promessas indevidas.

Verifica: (1) citações existem entre os trechos recuperados; (2) cada item tem fonte;
(3) códigos técnicos citados (transações, campos, mensagens) constam nos trechos ou no chamado;
(4) ausência de linguagem de execução ou de garantia; (5) não pede dados sensíveis.
Em caso de violação, a resposta do LLM é descartada.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .models import Item

# Tokens em maiúsculas que NÃO são códigos técnicos de SAP.
PERMITIDOS = {
    "SAP", "FI", "AA", "FIAA", "FI-AA", "HITL", "RAG", "IA", "API", "PDF", "XML", "KB", "HELP", "DD", "TS07",
    "S4F17", "APC", "AUC", "PEP", "OKOF", "NÃO", "SIM", "ILUSTRATIVO", "VALIDAR", "IFRS", "GAAP", "UTC", "ID",
    "MM", "SD", "CO", "HR", "AP", "AR", "GL", "S4CORE", "TEXTO", "DATA", "NUMERO", "OK", "BR", "PT",
}
_RE_TOKEN = re.compile(r"\b[A-Z][A-Z0-9_]{2,}\b")
_PROIBIDAS = [
    r"\b(eu\s+)?(executei|estornei|liquidei|lancei|alterei|baixei|reabri|fechei|excluí|exclui|bloqueei|corrigi)\b",
    r"\b(foi|foram)\s+(executad|estornad|liquidad|lancad|alterad|baixad|reaberto|fechad)\w*\s+(com sucesso|por mim)",
    r"\b(isso|isto)\s+(vai\s+)?resolve\w*\b",
    r"\bgaranto\b|\bgarantido\b|\bcom certeza\b|\bsem duvida\b|\b100%\b",
    r"\bproblema\s+resolvido\b",
]
_SENSIVEL = r"\b(senha|password|token|credencial|cpf|cartao de credito)\b"


@dataclass
class Resultado:
    ok: bool = True
    violacoes: list[str] = field(default_factory=list)

    def falha(self, msg: str):
        self.ok = False
        self.violacoes.append(msg)


def _norm(s: str) -> str:
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def validar(itens_por_secao: dict[str, list[Item]], textos_extras: list[str], ids_permitidos: set[str],
            contexto: str, chamado: str, exigir_fonte: bool = True) -> Resultado:
    r = Resultado()
    base = contexto + "\n" + chamado
    for secao, itens in itens_por_secao.items():
        for it in itens:
            if not it.texto:
                r.falha(f"[{secao}] item vazio")
                continue
            if exigir_fonte and not it.fontes:
                r.falha(f"[{secao}] item sem fonte: {it.texto[:50]}")
            for f in it.fontes:
                if f not in ids_permitidos:
                    r.falha(f"[{secao}] citação inexistente nos trechos recuperados: {f}")
            for tok in set(_RE_TOKEN.findall(it.texto)):
                if tok in PERMITIDOS or tok.upper() in PERMITIDOS:
                    continue
                if tok not in base:
                    r.falha(f"[{secao}] código técnico ausente das fontes (possível alucinação): {tok}")
            n = _norm(it.texto)
            for p in _PROIBIDAS:
                if re.search(p, n):
                    r.falha(f"[{secao}] linguagem proibida (execução ou garantia): {it.texto[:60]}")
            if re.search(_SENSIVEL, n):
                r.falha(f"[{secao}] menção a dado sensível")
    for t in textos_extras:
        for p in _PROIBIDAS:
            if re.search(p, _norm(t)):
                r.falha(f"[texto] linguagem proibida: {t[:60]}")
    return r
