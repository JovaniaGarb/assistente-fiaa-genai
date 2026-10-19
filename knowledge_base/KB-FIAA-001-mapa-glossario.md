---
id: KB-FIAA-001
titulo: Mapa do FI-AA, escopo do assistente e glossário
area: Transversal
status: RASCUNHO para revisão (ilustrativo; validar com a documentação oficial SAP)
fontes: [HELP = SAP Help Portal FI-AA S/4HANA 2025 FPS02 (PDF); S4F17 = planilha de treinamento S4F17; DD = dicionário de dados FI-AA (engenharia reversa)]
revisado_por: <preencher>
data_revisao: <preencher>
---

## Quando se aplica
Orientar a identificação da área do chamado e o vocabulário, e confirmar se o tema está no escopo (ver KB-FIAA-012).

## Panorama
- O FI-AA é um **subledger do Financial Accounting**, como contas a pagar e a receber; os lançamentos atualizam o razão e o subledger em paralelo [HELP p.86].
- Cada empresa (company code) usa **um plano de amortização** (chart of depreciation) e um plano de contas; o plano de amortização reúne até **99 áreas de depreciação** [HELP p.2-3, S4F17 Problema-solução].
- Cada ativo pertence a **uma classe**, que traz valores padrão e determinação de contas [HELP p.12-15].
- Cada transação gera **linhas de item** por área, com tipo de movimento, data de valor e valor [HELP p.86].

## Áreas dentro do escopo do assistente
Asset Master Records (KB-002), Transactions (KB-003, KB-004, KB-005), Depreciation (KB-006), Integration (KB-007, só orientação) e Closing Operations (KB-008).

## Glossário (PT / EN / campo, tipo e tamanho no template [TS07])

| Termo | Inglês | Campo | Tipo | Tamanho |
|---|---|---|---|---|
| Empresa | Company code | BUKRS | Texto | 80 (mapeável) |
| Número do ativo | Asset number | ANLN1 | Texto | 12 |
| Subnúmero | Subnumber | ANLN2 (não consta no template; ver DD) | n/a | n/a |
| Classe do ativo | Asset class | ANLKL | Texto | 80 (mapeável) |
| Descrição do ativo | Asset description | TXT50 | Texto | 50 |
| Data de capitalização | Capitalization date | AKTIV | Data | n/a |
| Data de desativação | Deactivation date | DEAKT | Data | n/a |
| Área de depreciação | Depreciation area | AFABE | Texto | 80 (mapeável) |
| Chave de depreciação | Depreciation key | AFASL | Texto | 80 (mapeável) |
| Vida útil em anos e em períodos | Useful life | NDJAR, NDPER | Número | 3 cada |
| Início da depreciação | Depreciation start date | AFABG | Data | n/a |
| Exercício | Fiscal year | GJAHR | Número | 4 |
| Tipo de movimento | Transaction type | ASSETTRTYP | Texto | 80 (mapeável) |
| Valor lançado | Amount posted | AMOUNT | Número | 23, com 2 decimais |
| Custo de aquisição e produção | APC | n/a | n/a | n/a |
| Imobilizado em andamento | Asset under construction (AuC) | n/a | n/a | n/a |
| Data de valor do ativo | Asset value date | VALUEDATE (no template) | Data | n/a |
| Ativo incompleto | Incomplete asset | n/a | n/a | n/a [HELP p.221] |

Definições completas, tipos e tamanhos: KB-FIAA-013 e KB-FIAA-014.

## Transações citadas nas fontes
AS01/AS02 (criar e alterar ativo) e AW01N (valores do ativo) [S4F17 Ex.10-14]; AFAR (calcular) e AFAB (lançar depreciação) [HELP p.183]; AIAB (liquidar AuC) [HELP p.136]; FAA_CMP (encerramento) [HELP p.192]; AUVA (ativos incompletos) [HELP p.194]; ABAON e ABAVN (baixa) [HELP p.179-180]; ABZOL (aquisição não integrada) e AB08 (estorno) [S4F17 Ex.15]; ABUMN (transferência) [S4F17 Ex.18].

## Observação sobre as fontes de campos
O **TS07** é o template oficial SAP de migração (S4CORE 103, 2019) e traz tipo, tamanho e definição. O **DD** foi derivado por engenharia reversa e **não traz tipos nem tamanhos**; em divergência, vale o TS07 [VALIDAR contra o sistema do cliente].

## Referências
HELP p.2-3, 12-15, 86, 91, 136, 179-183, 192, 194, 221; S4F17 Ex.10-18; DD; TS07 aba Field List.
