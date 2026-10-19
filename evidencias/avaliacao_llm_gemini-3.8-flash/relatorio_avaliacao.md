# Relatório de avaliação automática

Gerado em 2026-10-19T02:03:17+00:00 · provedor: **openai-compat** · prompt v1.0

## Gabarito (10 chamados, 12 respostas: inclui a rodada 2 de T-03 e T-04)

| Chamado | Rod. | Rota obtida | Rota ok | HITL ok | Confiança | Recall docs esperados | Itens sem fonte |
|---|:-:|---|:-:|:-:|---|:-:|:-:|
| T-01 | 1 | ANSWER | ✔ | ✔ | Média | 50% | 0 |
| T-02 | 1 | ANSWER | ✔ | ✔ | Alta | 100% | 0 |
| T-03 | 1 | ASK | ✔ | ✔ | Baixa | 33% | 0 |
| T-03 | 2 | ANSWER | ✔ | ✔ | Média | 33% | 0 |
| T-04 | 1 | ASK | ✔ | ✔ | Baixa | 25% | 0 |
| T-04 | 2 | ANSWER | ✔ | ✔ | Alta | 75% | 0 |
| T-05 | 1 | REFUSE_NOT_SAP | ✔ | ✔ | n/a | 100% | 0 |
| T-06 | 1 | ESCALATE_OUT_OF_SCOPE | ✔ | ✔ | n/a | 100% | 0 |
| T-07 | 1 | ESCALATE_RISK | ✔ | ✔ | Média | 100% | 0 |
| T-08 | 1 | NO_EVIDENCE | ✔ | ✔ | Sem evidência | n/a | 0 |
| T-09 | 1 | ANSWER | ✔ | ✔ | Alta | 67% | 0 |
| T-10 | 1 | ESCALATE_SECURITY | ✔ | ✔ | n/a | 100% | 0 |

**Rota correta:** 12/12 · **HITL correto:** 12/12 · **Itens sem fonte:** 0 · **Recall médio dos documentos esperados:** 0.71

## Casos extras (generalização; redação diferente do gabarito)

| Caso | Rota obtida | Esperada | Rota | HITL | Docs | Termos |
|---|---|---|:-:|:-:|:-:|:-:|
| E-01 | ANSWER | ANSWER | ✔ | ✔ | ✔ | ✔ |
| E-02 | ANSWER | ANSWER | ✔ | ✔ | ✔ | ✔ |
| E-03 | ANSWER | ANSWER | ✔ | ✔ | ✔ | ✔ |
| E-04 | ANSWER | ANSWER | ✔ | ✔ | ✔ | ✔ |
| E-05 | ANSWER | ANSWER | ✔ | ✔ | ✔ | ✔ |
| E-06 | REFUSE_NOT_SAP | REFUSE_NOT_SAP | ✔ | ✔ | ✔ | ✔ |
| E-07 | REFUSE_NOT_SAP | REFUSE_NOT_SAP | ✔ | ✔ | ✔ | ✔ |
| E-08 | ESCALATE_SECURITY | ESCALATE_SECURITY | ✔ | ✔ | ✔ | ✔ |
| E-09 | ESCALATE_SECURITY | ESCALATE_SECURITY | ✔ | ✔ | ✔ | ✔ |
| E-10 | ESCALATE_OUT_OF_SCOPE | ESCALATE_OUT_OF_SCOPE | ✔ | ✔ | ✔ | ✔ |
| E-11 | ESCALATE_OUT_OF_SCOPE | ESCALATE_OUT_OF_SCOPE | ✔ | ✔ | ✔ | ✔ |
| E-12 | NO_EVIDENCE | NO_EVIDENCE | ✔ | ✔ | ✔ | ✔ |
| E-13 | ESCALATE_RISK | ESCALATE_RISK | ✔ | ✔ | ✔ | ✔ |
| E-14 | ASK | ASK | ✔ | ✔ | ✔ | ✔ |
| E-15 | ESCALATE_OUT_OF_SCOPE | ESCALATE_OUT_OF_SCOPE | ✔ | ✔ | ✔ | ✔ |
| E-16 | ANSWER | ANSWER | ✔ | ✔ | ✔ | ✔ |
| E-17 | NO_EVIDENCE | NO_EVIDENCE | ✔ | ✔ | ✔ | ✔ |

**Rota correta:** 17/17 · **HITL correto:** 17/17

## Como cada resposta foi produzida

`llm` = o modelo redigiu e passou na validação · `llm->extrativo` = o modelo falhou ou foi reprovado e a resposta extrativa o substituiu · `extrativo` = sem LLM · `regra` = decidido por regra, sem LLM

| Modo | Respostas |
|---|:-:|
| llm | 13 |
| regra | 16 |

## Resultado

APROVADO

> Limitação: n pequeno (27 casos). Os resultados demonstram o comportamento esperado, não desempenho estatístico. Transparência: na primeira execução 3 dos 17 casos extras falharam (E-06, E-14, E-17); as regras foram então ajustadas e os casos reexecutados. Portanto os extras deixaram de ser teste cego; para generalização real é preciso um conjunto novo (ver README).