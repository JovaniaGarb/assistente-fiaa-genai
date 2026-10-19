---
id: KB-FIAA-004
titulo: Imobilizado em andamento (AuC): ciclo, liquidação e adiantamentos
area: Transactions
status: RASCUNHO para revisão (ilustrativo)
fontes: [HELP, S4F17, DD]
revisado_por: <preencher>
data_revisao: <preencher>
---

## Quando se aplica
AuC concluído e ainda aberto, liquidação que não roda, bloqueio do fechamento por AuC, adiantamento sem fatura final.

## Conceitos
- O AuC acumula custos de forma técnica; a capitalização posterior é feita por **liquidação** ou **transferência** para o ativo concluído [HELP p.135-138].
- Com **gestão por item de linha**, cada aquisição fica em aberto e é distribuída por **regras de distribuição** (percentual ou números de equivalência) a receptores como ativos ou centros de custo [HELP p.135-136].
- Para liquidar por item de linha, a empresa precisa de **perfil de liquidação** [HELP p.135; S4F17 Ex.21].
- A classe de AuC típica (por exemplo 4000 no treinamento) é liquidada por item de linha, não em resumo [S4F17 Ex.8].
- Ordem de investimento e elemento PEP podem estar ligados ao AuC [DD: INVEST_ORD, WBS_ELEMENT; S4F17 Ex.20].

## Regras importantes
- Para centros de custo como receptor, só se liquidam aquisições do **exercício corrente** [HELP p.136].
- Subvenção de investimento lançada no AuC **não pode ser transferida** no ano da capitalização; deve ser estornada manualmente antes [HELP p.136].
- Adiantamentos em aberto devem ser compensados com uma **reserva** antes da liquidação no fechamento do ano [HELP p.128].
- No fechamento, **todos os AuC concluídos no exercício devem ser liquidados** [HELP p.192]. A verificação de data de capitalização pode ser dispensada para as classes de AuC [HELP p.191, p.194].

## Causas possíveis de "liquidação não funciona"
Perfil de liquidação ausente; regras de distribuição não criadas; receptor não permitido; adiantamento em aberto; subvenção a estornar.

## Verificações recomendadas (somente leitura)
Exibir o AuC e seus itens em aberto; conferir regras de distribuição e perfil de liquidação; a liquidação possui modo de teste, a ser executado somente por pessoa autorizada [HELP p.138]; relatório de origem dos valores (RAHERK01) [HELP p.137].

## Exige validação humana quando
Liquidar (AIAB), transferir ou estornar liquidação. O estorno desfaz os documentos da última liquidação e exige ordem cronológica; não vale para AuC gerenciado apenas para contabilidade de custos [HELP p.136, p.182].

## Referências
HELP p.128, 135-138, 182, 191-192, 194; S4F17 Ex.8, 20-21; DD.
