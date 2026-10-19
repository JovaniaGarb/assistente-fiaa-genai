"""Guardrails determinísticos aplicados ANTES de qualquer chamada a LLM.

Princípio: decisões de segurança e de roteamento não ficam a cargo do modelo. O LLM só redige
dentro dos limites que estas regras e o Retriever definem.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .text import normalize

# ------------------------------------------------------------------ injeção de prompt
_INJECAO = [
    r"ignore\w*\s+(todas?\s+)?(as\s+)?(suas\s+|as\s+)?(regras|instrucoes|instrucao|politicas)",
    r"desconsidere\w*\s+(todas?\s+)?(as\s+)?(suas\s+|as\s+)?(regras|instrucoes|anteriores)",
    r"esqueca\w*\s+(as\s+|todas\s+as\s+)?(regras|instrucoes)",
    r"ignore\s+(all|previous|prior)\s+(the\s+)?(rules|instructions)",
    r"(voce|tu)\s+agora\s+e\b",
    r"\bmodo\s+(desenvolvedor|admin|deus)\b",
    r"(revele|mostre|exiba)\s+.*(prompt|instrucoes internas|regras internas)",
    r"system\s*prompt",
    r"responda\s+apenas\s+['\"“]?\w+",
    r"sem\s+(verificar|consultar)\s+(a\s+)?(base|fontes)",
    r"\bjailbreak\b",
]

# ------------------------------------------------------------------ fora do escopo (áreas)
_AREAS_FORA = {
    "Parallel Accounting (contabilidade paralela)": [
        r"contabilidade paralela", r"\bledgers?\b.*\b(ifrs|gaap|local|paralel)", r"\b(ifrs|gaap)\b.*\bledgers?\b",
        r"ledgers? diferentes", r"parallel accounting"],
    "Leasing": [r"\bleasing\b", r"\barrendamento\b", r"ativo arrendado"],
    "Migração / carga de legado": [
        r"migra(cao|r)\b.*\b(legado|template|cockpit)", r"carga de (dados|legado)", r"migration cockpit",
        r"transferencia de dados legados", r"\bmigrar\b.*\bativos?\b"],
    "Configuração (customizing)": [
        r"\bcustomizing\b", r"configura(r|cao)\s+(a\s+|o\s+)?(chave|area|plano|classe|tela)",
        r"criar (uma\s+)?(nova\s+)?(chave|area) de depreciacao",
        r"configur\w+\s+(uma?\s+)?(nov[ao]s?\s+)?(chave|area|plano|classe|tela)"],
    "Reporting (relatórios)": [r"\bcriar (um\s+)?relatorio\b", r"relatorio (customizado|personalizado|z)", r"\bquery\b"],
    "APIs / integração técnica": [r"\bapis?\b", r"\bodata\b", r"web ?service"],
    "Outro módulo SAP (fora do FI-AA)": [r"\bmodulo\s+(mm|sd|co|pp|qm|pm|ps|hr|hcm|fi-?gl)\b", r"pedidos? de compras?\b.*\bcriar|criar\s+(um\s+)?pedido", r"ordem de venda", r"\bcontas a (pagar|receber)\b.*\b(criar|configur)"],
}

# ------------------------------------------------------------------ temas vizinhos SEM cobertura na base
# Assuntos contábeis/fiscais próximos do ativo imobilizado, mas sem documento na base (KB-FIAA-012).
# O assistente não improvisa: declara ausência de evidência e encaminha.
_TEMAS_SEM_COBERTURA = {
    "tributação / imposto diferido": [r"\bimposto\w*", r"\btribut\w+", r"\bdiferid\w+", r"\bsped\b", r"\bnota fiscal\b|\bnf-?e\b"],
    "orçamento / planejamento": [r"\borcament\w+", r"\bbudget\b"],
}

# ------------------------------------------------------------------ ações de risco (KB-FIAA-010)
_ACOES = {
    "estorno": r"\bestorn\w+",
    "baixa": r"\bbaix(a|ar|ado)\b|\bsucat\w+|\bretirad\w+",
    "reabertura_exercicio": r"reabr\w+|desfaz\w*\s+(o\s+)?(encerramento|fechamento)",
    "encerramento": r"\bencerr\w+|\bfechar\s+o\s+exercicio",
    "liquidacao_auc": r"\bliquid\w+",
    "execucao_depreciacao": r"(execut\w+|rod\w+|lanc\w+)\s+.{0,25}deprecia\w+|deprecia\w+.{0,25}(execut\w+|rod\w+)",
    "transferencia": r"\btransfer\w+",
    "alteracao_mestre": r"\b(alter\w+|corrig\w+|muda\w*|trocar?)\b.{0,40}\b(ativo|classe|data|campo|centro)\b",
    "exclusao_bloqueio": r"\bexclu\w+|\bbloque\w+|\bdesativ\w+",
    "ajuste_saldo": r"\bajust\w+\s+.{0,20}(saldo|valor)",
    "concessao_acesso": r"\blibera\w*\b.{0,20}(acesso|usuario)|\bconced\w+\s+acesso",
}
# pedido direto ao assistente para executar/fazer algo
_PEDIDO_EXECUCAO = [
    r"\bpode\s+(executar|rodar|estornar|reabrir|liberar|lancar|ajustar|excluir|bloquear|baixar|liquidar|transferir|fazer)",
    r"\b(execute|rode|estorne|reabra|libere|lance|ajuste|exclua|bloqueie|baixe|liquide|transfira|faca)\b",
    r"\b(pode|consegue)\s+.{0,20}\bagora\b",
    r"\bexecut\w+\s+agora\b",
]

_INCIDENTE = r"\b(erro|nao\s+(foi|foram|houve|saiu|sairam)\b|nao\s+(lancad|bate|avanca|aparece|consigo|funciona|roda|calcul)\w*|ficaram?\s+sem|diverg\w+|problema|falha|bloquead\w+|errad\w+|incorret\w+|impede|corrigir|trat\w+)\b"

_DOMINIO_SAP = set(normalize(
    "ativo ativos imobilizado depreciacao sap fi-aa fiaa empresa fechamento exercicio periodo razao conta classe "
    "capitaliza aquisicao baixa estorno transferencia andamento auc liquidacao saldo ledger mestre cadastro "
    "centro custo vida util lancamento documento chamado erro mensagem transacao campo modulo mm sd co pp hcm").split())

# identificadores tipo código de erro (ex.: ZXX_998, FAA_CMP078)
_RE_CODIGO = re.compile(r"\b[A-Z]{2,}[A-Z0-9]*[_-]?[A-Z]*\d{2,}[A-Z0-9_]*\b")

SLOTS = {
    "empresa": r"\bempresa\s*\d{3,4}\b|\bcompany\s*code\b|\bbukrs\b|\bempresa\b.{0,15}\b\d{4}\b|\bcia\s*\d{3,4}\b",
    "ativo": r"\b\d{9,12}\b|\bativo\s*(n[oº.]*\s*)?\d{5,}\b",
    "periodo": r"\b(0?[1-9]|1[0-2])/(19|20)\d{2}\b|\b\d{1,2}/\d{1,2}/(19|20)\d{2}\b|\b(exercicio|periodo|ano)\s*(de\s*)?(19|20)\d{2}\b|\b(19|20)\d{2}\b",
    "conta_ou_classe": r"\bconta\b|\bclasse\b|\banln\w*\b|\bkansw\b",
    "ledger_ou_area": r"\bledger\b|\barea\s+de\s+(deprecia\w+|avaliacao)\b|\bafabe\b|\bprincipio\b|\b0l\b",
    "valor_diferenca": r"\b\d[\d\.,]*\s*(a mais|a menos|acima|abaixo|de diferenca)|diferenca\s+de\s+\d|\b\d{1,3}(\.\d{3})+(,\d+)?\b|\b\d+[\.,]\d{2}\b",
    "campo": r"\b(campo|data de (incorporacao|capitalizacao|inicio)|centro de custo|classe|vida util|chave de deprecia\w+|descricao|dado)\b.{0,60}(errad|incorret|deveria|correto|mudar|alterar)|(errad|incorret).{0,60}\b(campo|data|centro|classe|vida)\b|\b(data de (incorporacao|capitalizacao|inicio)|centro de custo|vida util|classe)\b",
}

# slots exigidos por intenção (KB-FIAA-011)
EXIGIDOS = {
    "integracao": ["empresa", "conta_ou_classe", "periodo", "ledger_ou_area", "valor_diferenca"],
    "mestre": ["empresa", "ativo", "campo"],
    "depreciacao": ["empresa", "periodo"],
    "fechamento": ["empresa", "periodo"],
    "transacao": ["empresa"],
    "informativa": [],
}
PERGUNTAS = {
    "empresa": "Qual é a empresa (company code)?",
    "ativo": "Qual é o número do ativo (e o subnúmero, se houver)?",
    "periodo": "Qual é o período ou o exercício (e a data-chave, se aplicável)?",
    "conta_ou_classe": "Qual é a conta do razão ou a classe de ativo envolvida?",
    "ledger_ou_area": "Qual é o ledger ou a área de depreciação considerada?",
    "valor_diferenca": "Qual é o valor da diferença e se ela é de custo de aquisição ou de depreciação?",
    "campo": "Qual campo está errado, qual é o valor atual e qual deveria ser?",
}


@dataclass
class Analise:
    injecao: list[str] = field(default_factory=list)
    area_fora: str | None = None
    tema_sem_cobertura: str | None = None
    parece_sap: bool = True
    acoes_mencionadas: list[str] = field(default_factory=list)
    pediu_execucao: bool = False
    incidente: bool = False
    intencao: str = "informativa"
    slots_presentes: list[str] = field(default_factory=list)
    slots_faltantes: list[str] = field(default_factory=list)
    codigos_citados: list[str] = field(default_factory=list)
    codigos_desconhecidos: list[str] = field(default_factory=list)


def detectar_injecao(texto: str) -> list[str]:
    n = normalize(texto)
    return [p for p in _INJECAO if re.search(p, n)]


def detectar_area_fora(texto: str) -> str | None:
    n = normalize(texto)
    for area, pads in _AREAS_FORA.items():
        if any(re.search(p, n) for p in pads):
            return area
    return None


def detectar_tema_sem_cobertura(texto: str) -> str | None:
    n = normalize(texto)
    for tema, pads in _TEMAS_SEM_COBERTURA.items():
        if any(re.search(p, n) for p in pads):
            return tema
    return None


def detectar_acoes(texto: str) -> list[str]:
    n = normalize(texto)
    return [a for a, p in _ACOES.items() if re.search(p, n)]


def pediu_execucao(texto: str) -> bool:
    n = normalize(texto)
    return any(re.search(p, n) for p in _PEDIDO_EXECUCAO)


def parece_dominio_sap(texto: str) -> bool:
    toks = set(re.findall(r"[a-z0-9_\-]+", normalize(texto)))
    return len(toks & _DOMINIO_SAP) >= 1


def classificar_intencao(texto: str) -> str:
    n = normalize(texto)
    if re.search(r"\b(saldo|razao|concilia\w+|nao bate)\b", n) and re.search(r"\b(razao|saldo)\b", n) and re.search(r"diverg|nao bate|diferen", n):
        return "integracao"
    if re.search(r"(fechar|fechamento|encerra\w+|reabr\w+)", n) and re.search(r"exercicio|periodo|fechamento", n):
        return "fechamento"
    if re.search(r"deprecia", n) and re.search(_INCIDENTE, n):
        return "depreciacao"
    if re.search(r"\b(criei|criado|cadastr\w+)\b.*\b(ativo)\b|dado errad|corrigir|campo", n) and re.search(r"ativo", n) and re.search(_INCIDENTE, n):
        return "mestre"
    if re.search(r"\b(baix\w+|estorn\w+|transfer\w+|aquisi\w+|andamento|liquid\w+)\b", n) and re.search(_INCIDENTE, n):
        return "transacao"
    return "informativa"


def extrair_slots(texto: str) -> list[str]:
    n = normalize(texto)
    return [s for s, p in SLOTS.items() if re.search(p, n)]


def extrair_codigos(texto: str) -> list[str]:
    return list(dict.fromkeys(_RE_CODIGO.findall(texto)))


def analisar(texto: str, retriever=None) -> Analise:
    a = Analise()
    a.injecao = detectar_injecao(texto)
    a.area_fora = detectar_area_fora(texto)
    a.tema_sem_cobertura = detectar_tema_sem_cobertura(texto)
    a.parece_sap = parece_dominio_sap(texto)
    a.acoes_mencionadas = detectar_acoes(texto)
    a.pediu_execucao = pediu_execucao(texto)
    a.incidente = bool(re.search(_INCIDENTE, normalize(texto)))
    a.intencao = classificar_intencao(texto)
    a.slots_presentes = extrair_slots(texto)
    a.slots_faltantes = [s for s in EXIGIDOS[a.intencao] if s not in a.slots_presentes]
    a.codigos_citados = extrair_codigos(texto)
    if retriever is not None:
        a.codigos_desconhecidos = [c for c in a.codigos_citados if not retriever.termo_na_base(c)]
    return a
