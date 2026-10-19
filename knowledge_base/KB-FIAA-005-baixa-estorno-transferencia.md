---
id: KB-FIAA-005
titulo: Baixa, estorno e transferência de ativos
area: Transactions
status: RASCUNHO para revisão (ilustrativo)
fontes: [HELP, S4F17, DD, TS07]
revisado_por: <preencher>
data_revisao: <preencher>
---

## Quando se aplica
Baixa com erro, pedido de estorno de baixa, transferência entre ativos ou empresas, correção de classe.

## Baixa (retirada)

| Tipo | Observação | Fonte |
|---|---|---|
| Venda com cliente | Lança a receita e a baixa em um passo | HELP p.173 |
| Venda sem cliente (ABAON) | Receita contra conta de compensação | HELP p.179 |
| Sucata (ABAVN) | Baixa sem receita | HELP p.180 |
- Os tipos de movimento padrão criam lançamentos de ganho ou perda automaticamente [HELP p.173].
- Não se lança com data de valor anterior à última baixa; antes é preciso estornar as baixas posteriores [HELP p.174].
- Baixa completa exige que todos os movimentos tenham data de valor anterior; adiantamentos e subvenções devem ser compensados ou estornados [HELP p.174].
- Baixa parcial refere-se a aquisições de anos anteriores **ou** do ano corrente [HELP p.174].
- **Ativo incompleto não pode ser baixado** [HELP p.221].

- A **data de desativação (DEAKT)** registra a data de valor da baixa **total** [TS07]. Em ativos transferidos, a **data de aquisição original (ORIG_ACQ_DATE)** guarda a capitalização do ativo de origem, como o imobilizado em andamento; o valor original (ORIG_VALUE) **não é preenchido automaticamente** no template [TS07].

## Estorno
- Deve ser feito pela **transação da aplicação de origem** (por exemplo, fatura de compras ou contas a receber) [HELP p.181].
- Se o movimento seguinte for negativo, pode ser preciso estornar esse também, pois o valor contábil poderia ficar negativo [HELP p.181].
- Estorno específico de FI-AA: AB08 [S4F17 Ex.15].

## Transferência
- Mudança de classe exige transferência para um novo registro, separando aquisições de anos anteriores e do corrente [HELP p.84, p.147].
- Dentro da empresa: ABUMN [S4F17 Ex.18]. Entre empresas: ABT1N com variante de transferência [S4F17 Ex.19; HELP p.148-155].
- Na capitalização de AuC, usar variante com tipos de movimento 348 e 349 [HELP p.138].

## Verificações recomendadas (somente leitura)
Exibir o ativo e seus itens (AW01N); localizar o documento de origem; conferir movimentos posteriores e datas de valor; conferir se o ano está fechado [HELP p.86, p.190].

## Exige validação humana
**Sempre**: baixa, estorno e transferência são ações contábeis (ver KB-FIAA-010).

## Referências
HELP p.84, 138, 147-155, 173-182, 190, 221; S4F17 Ex.15, 17-19.
