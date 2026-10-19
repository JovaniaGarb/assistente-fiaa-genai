# Métricas e medição de ganho

> Nenhum ganho de tempo é afirmado neste protótipo: não há linha de base real. O que existe é o **método** para medi-lo no piloto.

## 1. Linha de base (antes do piloto, 2 a 4 semanas)

| Indicador | Como medir | Fonte |
| --- | --- | --- |
| Tempo até a 1ª resposta útil | Amostra de 30 a 50 chamados FI-AA por consultor, cronometrada | Ferramenta de chamados + amostra |
| Taxa de devolução por informação incompleta | % de chamados que voltam ao solicitante | Ferramenta de chamados |
| Retrabalho | % de respostas corrigidas por outro consultor | Revisão por amostragem |
| Qualidade da resposta | Nota 1-5 por revisor cego, com os 5 critérios do gabarito | Revisão por amostragem |

## 2. Indicadores durante o piloto (do próprio log `audit.jsonl`)

| Indicador | Cálculo | Meta de partida (a calibrar) |
| --- | --- | --- |
| Taxa de aceite | recomendações aceitas ÷ apresentadas | definir com Champions |
| Respostas sem fonte | itens sem citação ÷ itens | **0** (inegociável) |
| Violações bloqueadas pelo validador | contagem de `validacao.ok_final = false` | acompanhar tendência |
| Taxa de "Sem evidência" | `NO_EVIDENCE` ÷ chamados | alimenta a fila de melhoria da base |
| Perguntas por chamado | rodadas até resposta | reduzir ao longo do piloto |
| Ações de risco com validação humana | `hitl = true` com decisão registrada ÷ total | **100%** |
| Tempo de decisão humana | `decisao.em` − `criado_em` na fila | monitorar gargalo |

## 3. Ganho de produtividade
Ganho = (tempo médio da linha de base − tempo médio com o assistente) × volume, **descontado** o tempo de revisão humana. Reportar sempre com intervalo e tamanho da amostra; sem amostra suficiente, reportar "não conclusivo".

## 4. Gate de regressão
Toda alteração em base, prompt ou limiares reexecuta `python -m assistente_fiaa avaliar` e `pytest`. Falha em qualquer caso bloqueia a publicação.
