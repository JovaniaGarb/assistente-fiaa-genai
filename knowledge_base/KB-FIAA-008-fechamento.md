---
id: KB-FIAA-008
titulo: Fechamento do período e do exercício
area: Closing Operations
status: RASCUNHO para revisão (ilustrativo)
fontes: [HELP, S4F17]
revisado_por: <preencher>
data_revisao: <preencher>
---

## Quando se aplica
Fechamento que não avança, erro no encerramento do exercício, dúvida sobre pré-requisitos, lançamento bloqueado no ano seguinte.

## Regras
- Só se fecha o exercício **posterior ao último fechado**; o exercício corrente não pode ser fechado [HELP p.190].
- Depois do fechamento, **não se lança nem se altera valores** no ano [HELP p.190].
- Só **dois exercícios** podem estar abertos ao mesmo tempo; para abrir o exercício seguinte (YYYY+1) é preciso antes fechar o exercício YYYY-1 [HELP p.201].
- Para lançar no novo exercício é preciso a **transferência de saldos** e os períodos de lançamento abertos (responsabilidade do razão) [HELP p.200-201].
- Um erro de fechamento (por exemplo FAA_CMP078) ocorre quando a depreciação do ano não foi calculada e lançada por completo para todos os ativos [HELP p.204].

## Verificações que o sistema faz
Não há erro de cálculo de depreciação; a depreciação planejada foi lançada por completo no razão; todos os ativos adquiridos no ano foram capitalizados (AuC pode ser dispensado por classe); não há ativos incompletos [HELP p.190-191].

## Sequência recomendada
1. Identificar a empresa e o último exercício fechado; 2. conferir inconsistências de estoque entre FI e MM; 3. capitalizar ativos de baixo valor; 4. liquidar AuC concluídos; 5. recalcular depreciação; 6. rodar a última execução de depreciação; 7. analisar os valores; 8. executar o encerramento (FAA_CMP); 9. emitir relatórios [HELP p.191-192].

## Erros comuns e tratamento

| Erro | Tratamento | Fonte |
|---|---|---|
| Erro no cálculo de depreciação | Recalcular o ativo e rodar nova execução | HELP p.194 |
| Depreciação não lançada por completo | Nova execução (mesmo período ou especial) | HELP p.194 |
| Data de capitalização não definida | Conferir classes de AuC; senão, definir a data no registro e rodar depreciação | HELP p.194 |
| Ativos incompletos | Completar pelo relatório de ativos incompletos | HELP p.194, p.221 |

## Desfazer o encerramento
É possível reabrir o último exercício fechado por empresa ou por área; **exercícios anteriores à migração para S/4HANA não podem ser reabertos** [HELP p.191].

## Exige validação humana
Executar ou desfazer o encerramento, rodar depreciação, liquidar AuC, transferir saldos. Sempre.

## Referências
HELP p.190-194, 200-204; S4F17 Ex.28 e Problema-solução (exercício fechado = ano corrente menos 1).
