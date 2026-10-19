---
id: KB-FIAA-007
titulo: Integração FI-AA × contabilidade geral (modo orientação)
area: Integration
status: RASCUNHO para revisão (ilustrativo; o assistente NÃO lê saldos reais)
fontes: [HELP, S4F17, DD, TS07]
revisado_por: <preencher>
data_revisao: <preencher>
---

## Quando se aplica
Divergência de saldo entre o módulo de ativos e o razão, lançamento de ativo que não aparece na contabilidade, dúvida sobre como cada área lança no razão.

## Limite
Nesta versão o assistente apenas **orienta** com base na documentação. Comparar saldos reais é tarefa humana ou da onda 2 (acesso somente leitura).

## Conceitos
- Toda movimentação em ativos e em fornecedores atualiza as contas do razão correspondentes; na aquisição integrada, os subledgers ficam sempre conciliados com o razão [HELP p.86, p.104].
- Cada área de depreciação tem uma opção de lançamento: não lança; lança tudo em tempo real e a depreciação periodicamente; lança só depreciação; ou lança o custo de aquisição na hora e a depreciação periodicamente [S4F17 Problema-solução; HELP p.19].
- A **depreciação é sempre lançada periodicamente** pela execução e em documentos coletivos [HELP p.26; S4F17].
- Todas as empresas do mesmo plano de amortização lançam as mesmas áreas [HELP p.27].
- Cada área precisa de princípio contábil; o vínculo com o ledger ocorre por ele [S4F17 Problema-solução].

## Valores acumulados e lançados (para interpretar a diferença)
O FI-AA distingue **valores acumulados** (saldos até o exercício, como valor de aquisição acumulado KANSW e depreciação ordinária acumulada KNAFA) e **valores lançados no exercício** (como NAFAG). A depreciação acumulada é registrada com sinal **negativo** [TS07; KB-FIAA-014]. Ao comparar com o razão, conferir se os dois lados usam a mesma base (saldo acumulado ou movimento do exercício).

## Direções possíveis para uma divergência (sempre com confiança limitada)
1. **Depreciação planejada não lançada por completo** no razão [HELP p.191, p.194].
2. **Área que lança periodicamente** versus saldo comparado em data intermediária [HELP p.26, p.19].
3. **Aquisição não integrada** com conta de compensação ainda não conciliada [HELP p.103, p.113].
4. **Diferença entre variantes de ano fiscal** do razão e do FI-AA, que desloca o período [HELP p.28].
5. **Documentos lançados manualmente** com o tipo de documento da depreciação, que deve ser reservado à execução [HELP p.27].
6. **Transporte de saldos** de contas de ativo na virada do ano [HELP p.189].

## Verificações recomendadas (somente leitura)
Identificar o tipo da diferença (custo de aquisição ou depreciação); comparar por conta, área e período; consultar a origem dos documentos; conferir o log da última execução de depreciação.

## Exige validação humana
Qualquer lançamento de ajuste, estorno ou alteração de configuração de áreas.

## Informações mínimas
Empresa, conta ou classe, data-chave, ledger ou área, valor e tipo da diferença (KB-FIAA-011).

## Referências
HELP p.19, 26-28, 86, 103-104, 113, 189, 191, 194; S4F17 Problema-solução (lançamento das áreas); TS07 abas Cumulative Values e Posted Values.
