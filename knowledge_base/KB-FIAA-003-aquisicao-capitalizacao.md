---
id: KB-FIAA-003
titulo: Aquisição e capitalização de ativos
area: Transactions
status: RASCUNHO para revisão (ilustrativo)
fontes: [HELP, S4F17, DD, TS07]
revisado_por: <preencher>
data_revisao: <preencher>
---

## Quando se aplica
Aquisição não lançada, ativo não capitalizado, valor ou data de valor divergentes, aquisição vinda de compras.

## Formas de aquisição

| Forma | Descrição | Fonte |
|---|---|---|
| **Integrada com contas a pagar** | Lança o ativo e a dívida na mesma transação; o subledger fica sempre conciliado com o razão | HELP p.104, 106 |
| **Não integrada** | Lança a aquisição contra conta de compensação; pode ser antes ou depois da fatura | HELP p.103, 113; S4F17 Ex.15 |
| **Via compras (MM)** | Pedido com categoria de atribuição A (ativo); capitaliza no recebimento da mercadoria ou da fatura | HELP p.116-120; S4F17 Ex.16 |
| **Atividade interna** | Liquidação de ordem de produção ou manutenção para o ativo | HELP p.121 |

## Pontos de atenção
- Na aquisição integrada, o tipo de documento define lançamento bruto (AA) ou líquido (AN) [HELP p.106].
- É necessária a conta de compensação técnica da aquisição integrada [HELP p.105].
- Com pedido de compra, nenhum valor é atualizado no ativo até o recebimento [HELP p.117].
- Recebimento valorado capitaliza antes da fatura; não valorado só na fatura [HELP p.119-120].
- A **data de valor** determina o início da depreciação; seu padrão depende do tipo de movimento [HELP p.91]. Ela pode diferir da data de lançamento e cair em período já fechado na contabilidade financeira, mas o **ano do lançamento e o da data de valor devem ser o mesmo** [TS07].
- Se a data de início da depreciação foi informada manualmente no cadastro, o sistema **ignora** a data de valor da aquisição [TS07].
- Ativo **bloqueado** não aceita aquisição [HELP p.85]. Ativo **incompleto** aceita aquisição, desde que a área de negócios esteja informada ou a empresa não use balanço por área de negócios; ele precisa ser completado depois [HELP p.116, p.221].
- Após o encerramento do exercício, não se lança no ano fechado [HELP p.190].
- Não se lança com data de valor anterior à última baixa do ativo [HELP p.174].

## Causas possíveis de "aquisição não capitalizou"
Ativo bloqueado; ano fechado; data de valor inválida; categoria de atribuição do pedido sem tratamento de ativo; recebimento não valorado aguardando fatura.

## Verificações recomendadas (somente leitura)
Exibir o ativo e seus itens de linha (AW01N); conferir o documento de origem; consultar o pedido e o status de entrega [HELP p.86, p.118].

## Exige validação humana quando
Qualquer lançamento, estorno ou correção de valor [HELP p.181].

## Referências
HELP p.85-86, 91, 103-106, 113, 116-121, 174, 181, 190; S4F17 Ex.13-16.
