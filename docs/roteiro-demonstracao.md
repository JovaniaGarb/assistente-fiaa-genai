# Roteiro da demonstração (18 min + 2 min de folga)

Chamados usados são do gabarito (`tickets/chamados.json`); na interface web aparecem como botões em "Exemplos do gabarito".

## Antes de começar (5 min de preparação)
- [ ] Terminal na pasta do projeto; variáveis do Gemini definidas (`LLM_BASE_URL`, `LLM_MODEL`, `LLM_API_KEY`) e `python -m assistente_fiaa --provider openai web` rodando em http://127.0.0.1:8765.
- [ ] Abas prontas: diagrama (`docs/diagrama-arquitetura.png`), uma KB (`knowledge_base/KB-FIAA-006-depreciacao.md`), a interface web.
- [ ] Rodar T-01 uma vez antes (aquece o serviço e confirma a chave).
- [ ] **Plano B**: se o serviço do modelo devolver 429/503, o sistema cai sozinho no modo extrativo (aparece `llm->extrativo` em "Detalhes técnicos"). Isso também é parte da demonstração: mostre como controle. Mantenha `evidencias/demo_saida.md` aberto como último recurso.

## Roteiro

| Min | Bloco | O que mostrar | O que dizer (ideia central) |
|---|---|---|---|
| 0–2 | Problema e escopo | `docs/00-escopo-fi-aa.md` (5 áreas do índice) | Atividade transformada: triagem e primeira análise de chamados de ativo fixo. O que o assistente **não** faz: executar no SAP. |
| 2–5 | Arquitetura | Diagrama, faixa por faixa | Três faixas: regras determinísticas decidem a rota (sem LLM); recuperação e geração só com trechos da base, validadas depois; saída separa recomendação da IA de ação humana. "O LLM redige; quem decide risco e rota são regras." |
| 5–7 | A base | KB-FIAA-006 e a tabela de fontes (Help PDF, S4F17, TS07) | Documentos curados com seções padronizadas (causa, verificação, ação humana); cada afirmação tem página ou fonte. Base não validada por especialista: está nas limitações. |
| 7–10 | **Sucesso 1: T-01** (depreciação não lançada) | Interface web: resposta, chips de fonte, confiança, bloco laranja "ação que depende de autorização humana"; abrir "Detalhes técnicos" | Recomendação fundamentada com citação; verificações são só leitura; a execução real fica como ação humana. Confiança é calculada por regra, não pedida ao modelo. |
| 10–11 | **Sucesso 2: T-02 ou T-09** (rápido) | Mesma tela | Outra área (imobilizado em andamento ou vida útil), mesma estrutura de resposta. |
| 11–12 | **Exceção: dados incompletos, T-03** | Resposta pede dados; digitar a resposta da rodada 2 | Não afirma causa sem dados; máx. 5 perguntas por rodada; após 2 rodadas sem dados, escala. |
| 12–14 | **Exceção: ação de risco, T-07** (estorno de baixa e reabertura) | Resposta de política + aba "Fila de validação humana": rejeitar ou aprovar com revisor e comentário | "Não executo." O pedido vira item PENDENTE; só um humano decide, e a decisão fica registrada. |
| 14–15 | **Exceções rápidas: T-08, T-10 e T-05** | T-08 (erro ZXX_998 inexistente), T-10 (injeção), T-05 (receita de bolo) | Sem evidência: declara que não encontrou, não inventa. Injeção: recusa e registra. Fora do domínio: recusa cordial. |
| 15–16 | Auditoria | Aba "Auditoria" e `logs/audit.jsonl` | Cada chamado grava rota, trechos recuperados com score, fontes, validação e latência; e-mail/CPF mascarados. |
| 16–17 | Resultados e honestidade | Aba "Avaliação" | 12/12 e 17/17 em rota e HITL; mas recall de documentos 0,65 e 3 dos 17 extras falharam na primeira execução e depois ajustei as regras: amostra pequena e não é teste cego. |
| 17–18 | Riscos, próximos passos, medição | `README` §6–§8 | Dados reais só em modo leitura com usuário de menor privilégio; validação por consultor; busca híbrida e conjunto de teste cego; medir ganho com linha de base (nenhum ganho é afirmado hoje). |
| 18–20 | Perguntas | | Folga. |

## Frases de segurança
- "Os dados são fictícios; o que mostro é comportamento, não desempenho estatístico."
- "Se o modelo falhar na validação, o sistema responde só com o que está na base: é de propósito."
- Se perguntarem por que BM25 e não embeddings: base pequena, em português, cheia de identificadores; busca lexical é auditável (o log mostra os termos que casaram). Embeddings entram como evolução.

## Ordem de corte se faltar tempo
Cortar primeiro T-02/T-09 e as exceções rápidas T-05; manter T-01, T-03, T-07, T-08 e a aba de auditoria, que cobrem os requisitos (sucesso, exceções, HITL, logs).
