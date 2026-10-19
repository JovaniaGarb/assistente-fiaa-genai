# Escopo do protótipo: Assistente de Análise de Chamados SAP (FI-AA)

> Protótipo de prova de conceito. Dados, documentos e respostas do SAP são **fictícios ou simulados**. Transações e conceitos devem ser validados no ambiente do cliente antes de qualquer uso real.

## 1. Problema e atividade transformada
Consultores analisam manualmente chamados de Contabilidade de Ativo Imobilizado: interpretam o texto, identificam o processo, consultam documentação e orientam o usuário. O trabalho é repetitivo, depende da experiência individual e gera respostas inconsistentes.

**O que o assistente transforma:** a triagem e a primeira análise do chamado (classificar, recuperar evidências, sugerir causas e verificações, pedir dados faltantes). A decisão e qualquer ação no sistema continuam humanas.

## 2. Critério de escopo
O escopo segue as áreas do índice (Table of Contents) de **Asset Accounting (FI-AA)**. Foram selecionadas 5 áreas mais comuns em chamados; as demais ficam fora.

## 3. Dentro do escopo (5 áreas do índice)

| Área do menu | Processos e exemplos de chamado |
| --- | --- |
| **Asset Master Records** | Ativo criado com classe, centro de custo ou campos incorretos; dados mestre incompletos |
| **Transactions** | Aquisição não lançada ou ativo não capitalizado; imobilizado em andamento sem liquidação; baixa com erro; transferência entre ativos |
| **Depreciation** | Depreciação não calculada ou não lançada no período; valor de depreciação divergente do esperado |
| **Closing Operations** | Pendências que impedem o fechamento do período ou do exercício; erros em rotinas de fechamento |
| **Integration** | Divergência de saldo entre FI-AA e contabilidade geral; lançamento do ativo que não reflete na contabilidade. Nesta versão o assistente **orienta com base na documentação**; não lê saldos reais |

Transversal (não é área do menu): **erro de autorização** do usuário nas transações das áreas acima.

## 4. Fora do escopo (10 áreas não selecionadas, mais APIs for Asset Accounting)
- Organizational Elements and Structures
- Basic Functions for Asset Valuation
- Parallel Accounting in Asset Accounting
- Special Valuations
- Manual Depreciation and Transferred Reserves
- Investment Support and Revaluation
- Reporting
- Tools
- Legacy Data Transfer and Preparations for Going Live
- Migration to New Asset Accounting (FI-AA (New))
- APIs for Asset Accounting (item técnico, não selecionado para este protótipo)

Também fora: outros módulos (MM, SD, CO, HR), exceto como causa provável mencionada; qualquer alteração de configuração (customizing); execução de lançamento, estorno ou liquidação; perguntas gerais sem relação com FI-AA.

**Regra de tratamento:** chamado sobre área fora do escopo é reconhecido como "SAP FI-AA, fora do escopo deste assistente" e encaminhado para consultor humano, sem tentar responder. Exemplo: divergência de depreciação entre ledgers ou áreas de avaliação é tratada como Parallel Accounting e escalada.

## 5. O que o assistente faz em cada chamado
1. Interpreta o chamado e identifica a área e o processo
2. Verifica se há informação suficiente; se não, **pergunta** (empresa, ativo, período, mensagem de erro, área de avaliação)
3. Recupera trechos da base de conhecimento (RAG)
4. Lista causas possíveis e verificações recomendadas
5. Informa **fontes** e **nível de confiança**
6. Encaminha para humano quando houver risco ou evidência insuficiente

## 6. Regras de Human-in-the-Loop
Validação humana **obrigatória** quando houver: estorno, baixa, liquidação, alteração de dados mestre, fechamento de período, impacto contábil ou fiscal, confiança baixa, ou ausência de fonte. O assistente **recomenda**; nunca executa.

## 7. Cenários de teste (8 chamados fictícios)
- **Sucesso (2):** depreciação não lançada no período (Depreciation); imobilizado em andamento sem liquidação (Transactions)
- **Exceção, chamado incompleto (2):** informação insuficiente, assistente deve perguntar (ex.: divergência de saldo sem informar período, conta ou ativo)
- **Exceção, fora do escopo (2):** pergunta não relacionada a SAP; chamado de área FI-AA não selecionada (ex.: relatório ou contabilidade paralela)
- **Exceção, ação de risco (1):** pedido de estorno, baixa ou fechamento, deve escalar
- **Exceção, sem evidência na base (1):** deve declarar que não sabe

## 8. Base de conhecimento (14 documentos curtos)
Dados mestre de ativo, fluxo de aquisição e capitalização, imobilizado em andamento, baixa e transferência, depreciação, fechamento de período, autorizações, glossário e política de escalonamento.

## 9. Critérios de sucesso do protótipo
- Toda resposta cita fonte ou declara ausência de evidência
- Nenhuma resposta inventa transação, campo ou mensagem não presente na base
- Ações de risco sempre vão para validação humana
- Todo atendimento fica registrado (chamado, resposta, fontes, decisão)

## 10. Premissas
Ambiente simulado, uso somente leitura, sem dados reais. Linha de base de tempo e qualidade **a medir** em um piloto real.
