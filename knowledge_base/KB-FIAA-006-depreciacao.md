---
id: KB-FIAA-006
titulo: Depreciação: cálculo, lançamento e erros
area: Depreciation
status: RASCUNHO para revisão (ilustrativo)
fontes: [HELP, S4F17, DD, TS07]
revisado_por: <preencher>
data_revisao: <preencher>
---

## Quando se aplica
Depreciação não calculada ou não lançada, valor diferente do esperado, erro no log da execução, necessidade de recalcular.

## Conceitos
- A depreciação planejada é **calculada** a cada alteração do registro mestre ou lançamento no ativo (AFAR) e **lançada** pela execução periódica (AFAB) [HELP p.183].
- A execução lança **documentos coletivos**, não um por ativo [HELP p.26].
- A depreciação depende dos termos por área: **chave de depreciação (AFASL), vida útil (NDJAR, NDPER) e data de início (AFABG)** [DD; HELP p.36].
- A data de valor, ajustada pelo controle de período da chave, define o início [HELP p.91].
- Ciclo de lançamento (mensal, trimestral etc.) e tipo de documento são configurados por empresa e área [HELP p.27].
- Se a variante do ano fiscal do FI-AA diferir da do razão, o período lançado pode mudar [HELP p.28].

## Regras da execução
- A execução real **só roda em segundo plano**; o teste em diálogo tem limite de 1000 ativos [HELP p.184].
- A empresa precisa estar disponível para lançamento durante a execução [HELP p.184].
- O status aparece no log ou no Schedule Manager (erros, lançado, nada a lançar) [HELP p.184].
- Erros em ativos individuais não impedem o fechamento do período, mas devem ser corrigidos até o fim do ano [HELP p.183].
- Ativo **incompleto** não recebe depreciação [HELP p.221].

## Causas possíveis de "depreciação não lançada"
Erro de cálculo (chave de depreciação incorreta); ativo incompleto; data de incorporação não definida; execução não rodada ou com erro no log; ciclo de lançamento diferente do período esperado; empresa indisponível durante a execução [HELP p.184, p.194, p.221].

**Causas ligadas aos termos do ativo** [TS07; ver KB-FIAA-014]: ativo paralisado (XSTIL), que não recebe depreciação; área de depreciação desativada no ativo (XAFBE); data de início da depreciação informada manualmente (AFABG), que faz o sistema ignorar a data de valor da aquisição; valor residual (SCHRW) atingido, que interrompe a depreciação; ativo pertencente a um **ativo de grupo** (ANLGR), cuja depreciação é determinada no nível do grupo; vida útil mal informada, pois anos (NDJAR) e períodos (NDPER) são **aditivos**.

## Verificações recomendadas (somente leitura)
Consultar o log ou Schedule Manager; exibir o ativo (AW01N) e conferir termos, datas e completude; rodar o relatório de ativos incompletos (AUVA); simular a depreciação do período [HELP p.195-199; S4F17 Ex.27, 36].

## Recalcular
O recálculo usa os termos vigentes e só vale para exercícios abertos; deve rodar em segundo plano [HELP p.214]. Alterar termos de depreciação afeta o planejado dos exercícios abertos [HELP p.204].

## Exige validação humana quando
Execução real (AFAB), recálculo em massa, alteração de termos, depreciação não planejada (ABAA) [HELP p.204; S4F17 Ex.22].

## Referências
HELP p.26-28, 36, 91, 183-184, 194-199, 204, 214, 221; S4F17 Ex.22, 27, 36; DD; TS07 aba Depreciation Areas e Time-Dependent Data.
