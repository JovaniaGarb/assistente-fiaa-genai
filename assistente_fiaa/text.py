"""Normalização de texto, tokenização leve e expansão por glossário (ontologia leve)."""
import re
import unicodedata

STOP = set(
    "a o as os um uma uns umas de da do das dos em na no nas nos por para com sem e ou que se ao aos "
    "como mais mas foi ser sao e esta estao ja tem pode podem preciso precisamos meu minha nosso nossa "
    "isso essa esse este esta aqui la sobre entre ate quando qual quais the of and to is are in for on".split()
)

_SUFIXOS = ("coes", "cao", "mente", "oes", "ais", "eis", "res", "es", "s")


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def normalize(s: str) -> str:
    return strip_accents(s).lower()


def stem(tok: str) -> str:
    """Stemming leve. Identificadores técnicos (com dígito ou _) ficam intactos."""
    if re.search(r"[0-9_]", tok):
        return tok
    if len(tok) > 5:
        for suf in _SUFIXOS:
            if tok.endswith(suf) and len(tok) - len(suf) >= 4:
                tok = tok[: -len(suf)]
                break
    return tok[:7] if len(tok) > 7 else tok


def tokenize(s: str, keep_stop: bool = False) -> list[str]:
    toks = re.findall(r"[a-z0-9_]+", normalize(s))
    return [stem(t) for t in toks if keep_stop or t not in STOP]


# Glossário PT <-> termos técnicos das fontes. Funciona como ontologia leve:
# frases do usuário disparam termos que aparecem nos documentos da base.
EXPANSAO = {
    "depreciacao": "afab afar deprecia",
    "imobilizado em andamento": "auc andamento liquida aiab",
    " auc ": "andamento liquida aiab",
    "fechamento": "faa_cmp encerramento",
    "encerramento": "faa_cmp encerramento",
    "estorno": "estorno ab08 aplicacao origem",
    "estornar": "estorno ab08 aplicacao origem",
    "baixa": "retirada abaon abavn baixa",
    "vida util": "ndjar ndper",
    "data de incorporacao": "aktiv capitaliza",
    "data de capitalizacao": "aktiv capitaliza",
    "inicio da depreciacao": "afabg",
    "chave de depreciacao": "afasl",
    "area de depreciacao": "afabe",
    "paralis": "xstil",
    "ativo de grupo": "anlgr",
    "incompleto": "incompleto auva",
    "saldo": "razao integra conciliacao",
    "razao": "integra conciliacao",
    "tipo e tamanho": "tipo tamanho template ts07",
    "tamanho": "tipo tamanho template ts07",
}


def expand_query(q: str) -> list[str]:
    n = " " + normalize(q) + " "
    extra: list[str] = []
    for gatilho, termos in EXPANSAO.items():
        if gatilho in n:
            extra += [stem(t) for t in termos.split()]
    return extra
