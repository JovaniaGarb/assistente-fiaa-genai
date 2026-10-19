"""Estruturas de dados da resposta do assistente."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

ROTAS = (
    "ANSWER",                 # resposta fundamentada
    "ASK",                    # pede dados faltantes
    "REFUSE_NOT_SAP",         # fora do domínio SAP: recusa cordial
    "ESCALATE_OUT_OF_SCOPE",  # área FI-AA fora do escopo: encaminha sem diagnosticar
    "ESCALATE_RISK",          # pedido de execução de ação de risco: orienta e encaminha
    "ESCALATE_SECURITY",      # tentativa de burlar regras: recusa, registra e encaminha
    "ESCALATE_INFO",          # dados mínimos não obtidos após 2 rodadas
    "NO_EVIDENCE",            # sem evidência na base: não responde, encaminha
)


@dataclass
class Item:
    texto: str
    fontes: list[str] = field(default_factory=list)   # ids de trechos (ex.: KB-FIAA-006#regras-da-execucao)


@dataclass
class Resposta:
    ticket_id: str
    rodada: int
    route: str
    area: str = ""
    entendimento: str = ""
    perguntas: list[str] = field(default_factory=list)
    causas: list[Item] = field(default_factory=list)
    conteudo: list[Item] = field(default_factory=list)
    verificacoes: list[Item] = field(default_factory=list)
    acoes_humanas: list[Item] = field(default_factory=list)
    fontes: list[dict] = field(default_factory=list)
    confianca: str = "n/a"
    encaminhar_humano: bool = False
    acao_humana_necessaria: bool = False
    mensagem_politica: str = ""
    avisos: list[str] = field(default_factory=list)
    flags: dict = field(default_factory=dict)
    validacao: dict = field(default_factory=dict)
    provider: str = ""
    fallback: bool = False

    @property
    def hitl(self) -> bool:
        return self.encaminhar_humano or self.acao_humana_necessaria

    def texto_completo(self) -> str:
        partes = [self.entendimento, self.mensagem_politica, *self.perguntas, *self.avisos]
        for lst in (self.causas, self.conteudo, self.verificacoes, self.acoes_humanas):
            partes += [i.texto for i in lst]
        return "\n".join(p for p in partes if p)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_markdown(self) -> str:
        o = [f"### Resposta ({self.route})", ""]
        if self.mensagem_politica:
            o += [f"> {self.mensagem_politica}", ""]
        if self.entendimento:
            o += [f"**Entendimento:** {self.entendimento}", ""]
        if self.perguntas:
            o += ["**Preciso destas informações para analisar:**"] + [f"{i}. {p}" for i, p in enumerate(self.perguntas, 1)] + [""]
        def bloco(titulo, itens):
            if itens:
                o.extend([f"**{titulo}**"] + [f"- {i.texto}  `{', '.join(i.fontes)}`" if i.fontes else f"- {i.texto}" for i in itens] + [""])
        bloco("O que a documentação indica", self.conteudo)
        bloco("Causas possíveis", self.causas)
        bloco("Verificações recomendadas (somente leitura)", self.verificacoes)
        if self.acoes_humanas:
            o += ["**Ação que depende de autorização humana (a IA não executa)**"]
            o += [f"- {i.texto}  `{', '.join(i.fontes)}`" for i in self.acoes_humanas] + [""]
        for a in self.avisos:
            o.append(f"_Aviso: {a}_")
        if self.fontes:
            o += ["", "**Fontes consultadas:** " + "; ".join(f["id"] for f in self.fontes)]
        o += [f"**Confiança:** {self.confianca}",
              f"**Encaminhamento humano:** {'sim' if self.hitl else 'não'}"]
        return "\n".join(o)
