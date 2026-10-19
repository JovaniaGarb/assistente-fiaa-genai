---
id: KB-FIAA-011
titulo: Informações mínimas por tipo de chamado e política de perguntas
area: Governança (transversal)
status: RASCUNHO para revisão (ilustrativo)
fontes: [HELP, S4F17, DD, TS07]
revisado_por: <preencher>
data_revisao: <preencher>
---

## Quando se aplica
Sempre que o chamado chega sem os dados necessários para a análise.

## Quando perguntar
Se o chamado não tem os dados mínimos abaixo, o assistente **pergunta antes de concluir**. Pode listar direções gerais com **confiança baixa**, mas não afirma causa.

## Regras
- No máximo **5 perguntas por rodada**, em linguagem simples, numeradas.
- Depois de **2 rodadas** sem os dados, escalar (KB-FIAA-010).
- Nunca pedir senha, token ou dados pessoais.
- Pedir a **mensagem de erro exata** (texto e identificador), não uma descrição.
- Pedir identificadores no formato do sistema: empresa (BUKRS), número e subnúmero do ativo (ANLN1, ANLN2), área de depreciação (AFABE), exercício (GJAHR) [DD].
- **Formatos esperados** [TS07]: número do ativo até 12 caracteres; exercício com 4 dígitos; datas no formato regional; valores com até 2 decimais e sinal "-" para negativos; vida útil em anos **e** períodos (aditivos).

## Dados mínimos comuns
Empresa, ativo (número e subnúmero), período ou data-chave, transação ou app, mensagem exata, o que mudou recentemente, impacto e urgência.

## Dados adicionais por área

| Área | Perguntar também | Por quê (fonte) |
|---|---|---|
| **Depreciation** | Ledger ou princípio contábil, área de depreciação, se foi teste ou execução real, resultado do log; data de incorporação (AKTIV), chave de depreciação (AFASL), vida útil e início da depreciação (AFABG) | Execução por empresa e princípio; termos por área [HELP p.184; DD] |
| **Asset Master Records** | Qual campo está errado, valor atual e desejado, se o campo é dependente do tempo, se o ativo aparece como incompleto | Tratamento muda por tipo de campo [HELP p.83-84, p.221] |
| **Transactions** | Tipo de movimento (aquisição, AuC, baixa, transferência), data de valor, se foi integrada com compras ou contas a pagar, documento de origem | Tratamento depende do tipo e da integração [HELP p.91, p.103-104, p.181] |
| **Closing Operations** | Exercício ou período, último exercício fechado, mensagem do log do fechamento, se depreciação do ano foi calculada e lançada, AuC concluídos | Pré-requisitos do fechamento [HELP p.191-192, p.204] |
| **Integration** | Conta ou classe, data-chave, ledger, valor e tipo da diferença (custo de aquisição ou depreciação) | Áreas lançam de formas distintas [HELP p.19, p.26-27] |

## Exemplo de pergunta bem formada
"Para analisar a divergência preciso saber: (1) empresa, (2) conta do razão ou classe de ativo, (3) data-chave, (4) ledger ou área de depreciação, (5) valor da diferença e se é custo de aquisição ou depreciação."

## Referências
HELP p.19, 26-27, 83-84, 91, 103-104, 181, 184, 191-192, 204, 221; DD; TS07 aba Field List.
