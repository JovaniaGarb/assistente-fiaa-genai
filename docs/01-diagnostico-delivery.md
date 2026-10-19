# Diagnóstico de delivery: processo atual × processo futuro

**LUME SAP AI** · Assistente Inteligente para Análise de Chamados SAP

| Tipo | Duração | Orçamento | Responsável | Data |
| --- | --- | --- | --- | --- |
| Prova de Conceito (PoC) | 3 dias | R$ 0 | Jovania Garbelotto Pancieri | 16/10/2026 |

## 1. Contexto do diagnóstico

Este diagnóstico avalia o processo de análise de chamados SAP e define como o **LUME SAP AI** será inserido no processo. O foco é tornar explícito, etapa a etapa, **onde a IA atua** (interpretação, busca de evidências via RAG e recomendação) e **onde o humano decide** (validação, escalonamento e ação no SAP). Premissa: a decisão final é sempre humana.

## 2. Processo atual (AS-IS)

### 2.1 Mapa do processo atual

| # | Etapa | Quem executa | Como é feito hoje | Dor identificada |
| --- | --- | --- | --- | --- |
| 1 | **Abertura do chamado** | Usuário de Negócio | Descreve o problema em texto livre | Chamados com informações insuficientes |
| 2 | **Interpretação da solicitação** | Consultor SAP | Leitura e interpretação manual do chamado | Atividade repetitiva e dependente do consultor |
| 3 | **Identificação de processo e módulo SAP** | Consultor SAP | Classificação baseada na experiência individual | Variação de critério entre consultores |
| 4 | **Coleta de dados complementares** | Consultor ↔ Usuário | Novas interações para obter dados faltantes | Múltiplas idas e vindas; tempo elevado |
| 5 | **Pesquisa de conhecimento** | Consultor SAP | Consulta manual a documentações e à equipe | Conhecimento disperso e pouco escalável |
| 6 | **Análise e orientação** | Consultor SAP | Formula a causa provável e redige a orientação | Risco de respostas inconsistentes ou incorretas |
| 7 | **Resposta e encerramento** | Consultor SAP | Envia a orientação e encerra o chamado | Sem registro estruturado de fontes e decisões |

*No processo atual, 100% das etapas são executadas manualmente pelo consultor; não há ponto formal de apoio por IA.*

### 2.2 Diagnóstico: principais gargalos

- **Processo manual e repetitivo:** interpretação, classificação e pesquisa consomem o tempo do consultor.
- **Conhecimento concentrado em pessoas:** dificuldade de escalar a especialização SAP.
- **Retrabalho na coleta de dados:** múltiplas interações para complementar chamados.
- **Qualidade variável e baixa rastreabilidade:** respostas sem evidências explícitas e sem histórico reutilizável.

## 3. Processo futuro (TO-BE) com LUME SAP AI

### 3.1 Visão geral do fluxo

| Usuário | IA | IA | IA | ◆ Humano | ◆ Humano | ◆ Humano |
| --- | --- | --- | --- | --- | --- | --- |
| Abre o chamado ► | Interpreta e classifica ► | Checa escopo e dados ► | RAG + recomendação ► | Valida / ajusta ► | Escala se crítico ► | Responde e age |

Legenda: **IA** recomenda (executa a análise) · **◆ Humano** decide (ponto de controle) · **Usuário** abre o chamado.

### 3.2 Mapa do processo futuro

| # | Etapa | Quem atua | O que acontece | Ponto de controle |
| --- | --- | --- | --- | --- |
| 1 | **Abertura do chamado** | Usuário | Registra a solicitação no assistente | — |
| 2 | **Interpretação e classificação** | IA | LLM interpreta o chamado e identifica processo de negócio e módulo SAP | Classificação exibida ao consultor |
| 3 | **Verificação de escopo** | IA | Detecta solicitações fora do escopo e responde com mensagem padrão | Fora do escopo → encaminha ao consultor |
| 4 | **Verificação de completude** | IA | Identifica dados faltantes e solicita contexto adicional ao consultor | Sem dados mínimos → não gera diagnóstico |
| 5 | **Busca de evidências (RAG)** | IA | Recupera trechos relevantes da base de conhecimento SAP | Sem evidência → não responde e sinaliza |
| 6 | **Recomendação** | IA | Sugere causas prováveis, verificações e próximos passos, com fontes, nível de confiança e impacto contábil | Saída é sempre recomendação, nunca ação |
| 7 | **Validação (Human-in-the-Loop)** | **◆ HUMANO DECIDE**: Consultor SAP | Aprova, ajusta ou rejeita a recomendação da IA | Decisão obrigatória em todos os chamados |
| 8 | **Escalonamento** | **◆ HUMANO DECIDE**: Especialista Funcional | Analisa casos críticos ou de baixa confiança | **Gatilho: criticidade alta ou confiança baixa** |
| 9 | **Resposta e ação no SAP** | **◆ HUMANO DECIDE**: Consultor SAP | Envia a orientação final; qualquer transação SAP é executada por humano | **IA não executa transações** |
| 10 | **Registro e aprendizado** | Sistema + Humano | Registra solicitação, resposta, fontes e decisão; especialista aprova atualizações da base | Rastreabilidade e curadoria |

*Regra de autonomia da PoC: a IA interpreta, busca evidências e recomenda; nenhuma resposta chega ao usuário nem é executada no SAP sem validação humana.*

## 4. Onde a IA entra e onde o humano decide

| Decisão / atividade | IA recomenda | ◆ Humano decide | Gatilho |
| --- | --- | --- | --- |
| **Classificação do chamado** | Sugere processo e módulo SAP | Consultor confirma ou corrige | Toda validação |
| **Dados complementares** | Identifica lacunas e formula perguntas | Usuário fornece as informações | Dados mínimos ausentes |
| **Solicitação fora do escopo** | Detecta e responde com mensagem padrão | Consultor define o encaminhamento | Tema fora da base/escopo |
| **Causa e próximos passos** | Propõe hipóteses com fontes e confiança | Consultor aprova, ajusta ou rejeita | Sempre |
| **Casos críticos** | Sinaliza criticidade e baixa confiança | Especialista Funcional decide | Criticidade alta ou confiança baixa |
| **Ação no SAP** | Não executa transações | Consultor executa | Sempre |
| **Atualização da base** | Registra logs e evidencia lacunas | Especialista aprova a curadoria | Revisão periódica |

## 5. Comparativo AS-IS × TO-BE

| Dimensão | Atual (AS-IS) | Futuro (TO-BE) |
| --- | --- | --- |
| **Interpretação** | Manual, por consultor | IA interpreta e classifica; consultor confirma |
| **Coleta de dados** | Múltiplas interações | Solicitação automática de contexto adicional |
| **Conhecimento** | Disperso e individual | Base estruturada consultada via RAG |
| **Qualidade da resposta** | Variável, sem evidências explícitas | Fundamentada, com fontes e nível de confiança |
| **Controle e rastreabilidade** | Implícito; sem registro estruturado | Human-in-the-Loop explícito e log de solicitações, respostas e fontes |

## 6. Riscos de delivery e próximos passos

| Risco principal | Severidade | Mitigação no processo futuro |
| --- | --- | --- |
| Prazo reduzido de 3 dias | **Crítica** | Priorização do MVP |
| Alucinação do modelo / respostas sem evidências | **Alta** | RAG, exibição obrigatória de fontes e validação humana (etapa 7) |
| Informações insuficientes no chamado | **Alta** | Solicitação automática de contexto adicional (etapa 4) |
| Base de conhecimento limitada / falhas de recuperação | **Alta** | Controle de escopo da PoC e ajustes na estratégia de busca |

**Plano de entrega (marcos)**

- **◆ M1 (dia 1):** arquitetura definida, base de conhecimento e chamados fictícios criados.
- **◆ M2 (dia 2):** protótipo funcional com LLM, prompts e RAG (etapas 2 a 6 do TO-BE).
- **◆ M3 (dia 3):** Human-in-the-Loop (etapas 7 a 9), testes com 1 cenário de sucesso e 2 de exceção, e demonstração.

**Indicadores sugeridos para medir o ganho:** tempo de análise por chamado, nº de interações para complementar dados, taxa de aprovação das recomendações pelo consultor e taxa de escalonamento. A linha de base será medida em um piloto real.
