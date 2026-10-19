# Plano de adoção: Assistente Inteligente para Análise de Chamados - Onda 1 - SAP FI-AA

**Documento para validação do cliente**

> Prazos, volumes e metas deste plano são propostas iniciais. Serão confirmados com os Delivery Leads após a medição da linha de base (fase de diagnóstico) no cliente.

## 1. Sumário executivo

**Objetivo.** Reduzir o tempo de análise e aumentar a consistência no atendimento de chamados SAP de Contabilidade de Ativo Imobilizado (FI-AA), usando IA Generativa fundamentada em base de conhecimento controlada, com decisão final sempre humana.

**Abordagem.** Implantação em três ondas (piloto, expansão e escala), com critérios objetivos de passagem. Cada onda só avança quando produtividade e qualidade melhoram juntas e os controles de segurança se mantêm.

**Princípios.**
- O assistente **recomenda**; o consultor **decide**. Nenhuma ação é executada no SAP pelo assistente.
- Toda resposta indica **fontes** e **nível de confiança**. Sem evidência nas fontes, o caso é encaminhado a um consultor.
- Ações com impacto contábil reforçam **dupla validação humana**.

**O que solicitamos ao cliente.** Patrocínio dos Delivery Leads, 1 ou 2 equipes para o piloto, um Champion por equipe com tempo protegido, e acesso a uma amostra de chamados para a linha de base.

## 2. Visão das ondas

|  | **Onda 1: Piloto** | **Onda 2: Expansão** | **Onda 3: Escala** |
| --- | --- | --- | --- |
| **Foco** | Provar valor e segurança | Ampliar equipes e profundidade | Incorporar à rotina de entrega |
| **Escopo** | Dados mestre, transações, depreciação, fechamento e integração com o razão | Novas equipes; acesso somente leitura ao SAP; áreas adicionais conforme priorização | Demais equipes e novos casos de uso com evidência de ganho |
| **Equipes** | 1 ou 2 | Equipes adicionais com Champions treinados pela onda 1 | Todas as equipes elegíveis |
| **Modo de operação** | Assistente sugere, consultor decide | Idem, com consulta segura a dados reais | Idem, com governança permanente |
| **Critério de passagem** | Aceite das recomendações acima da meta; nenhuma ação de risco sem escalonamento; ganho de tempo medido | Resultados sustentados em mais equipes; conector aprovado por Segurança; base com responsável por documento | Ganho sustentado de produtividade e qualidade; nenhuma regressão de segurança |

## 3. Fase de diagnóstico (antes da onda 1)

1. **Entrevistas** com Delivery Leads e Champions para entender onde o tempo se perde, quais chamados retornam por falta de informação e onde as respostas variam entre consultores.
2. **Amostra de chamados** para medir a linha de base (tempo de primeira resposta e de resolução, retrabalho) e classificar por área.
3. **Inventário de atividades candidatas**, priorizadas por valor, viabilidade e risco.

| Atividade | Tratamento |
| --- | --- |
| Triagem e primeira análise de chamados FI-AA | Incluída no piloto |
| Solicitação de dados faltantes ao usuário | Incluída no piloto |
| Consulta à documentação para orientar o usuário | Incluída no piloto |
| Checklist de pré-fechamento do exercício | Candidata à onda 2 |
| Revisão de dados mestre incompletos | Candidata à onda 2 |
| Decisões contábeis (baixa, estorno, ajuste) | **Permanecem humanas** |

## 4. Governança e responsabilidades

| Papel | Responsabilidade |
| --- | --- |
| **Delivery Lead** | Seleciona as equipes, libera tempo dos consultores, decide a passagem entre ondas e remove impedimentos |
| **Champion** | Utiliza o assistente em chamados reais, registra feedback, valida respostas e documentos, apoia os colegas |
| **Consultor funcional FI-AA** | Mantém e revisa a base de conhecimento; valida as recomendações |
| **Time AI Advanced Assets e Funcional SAP** | Conduz a estratégia de adoção, treinamentos e acompanhamento; mantém a solução técnica (recuperação, prompts, registros e avaliação) |
| **Segurança e Basis** | Aprovam o acesso somente leitura ao SAP na onda 2 |
| **Controladoria e Auditoria** | Definem o que é risco contábil e validam as regras de validação humana |

**Ritos.** Semanal com Champions e time técnico (feedback e melhorias). Quinzenal com Delivery Leads (indicadores e decisões). Relatório de uma página ao final de cada onda.

## 5. Modelo operacional

**Treinamento (45 minutos, prático, com chamados reais).** O que o assistente faz e não faz; como escrever um bom chamado; como ler fontes e confiança; como dar feedback; quando escalar. Material de apoio: guia de uma página e três exemplos (sucesso, dados incompletos e escalonamento). Plantão semanal de dúvidas durante o piloto.

**Feedback.** Cada resposta pode ser classificada como útil, parcialmente útil ou incorreta, com o motivo.

**Melhoria contínua da base de conhecimento.**
1. Captura de chamados sem evidência, respostas incorretas e perguntas repetidas.
2. Priorização pelo Champion e pelo consultor funcional.
3. Redação e revisão por pares.
4. Teste com o conjunto padrão de chamados.
5. Publicação versionada e comunicação aos usuários.
6. Medição da taxa de respostas "sem evidência".

## 6. Gestão de qualidade e riscos

**Controles.**
- Base de conhecimento com fonte, revisor e data em cada documento.
- Conjunto padrão de 10 chamados executado **antes de qualquer mudança** na base ou nas instruções do assistente; a mudança só é publicada se nenhum critério regredir.
- Verificação automática de que transações, campos e mensagens citados constam nas fontes.
- Registro de cada atendimento: chamado, resposta, fontes, confiança e decisão humana.

**Registro de riscos.**

| ID | Risco | Severidade | Mitigação |
| --- | --- | --- | --- |
| R01 | Resposta com transação, campo ou mensagem inexistente (alucinação) | Alto | RAG restrito à base curada; fonte obrigatória; declarar falta de evidência |
| R02 | Documentação 2025 FPS02 diferente do ambiente real (customizing, notas, desenvolvimentos próprios) | Alto | Validar toda recomendação no ambiente do cliente |
| R03 | Consultor executar recomendação sem validação humana | Alto | Regras de Human-in-the-Loop e aviso explícito em ações de risco |
| R04 | Conteúdo exportado do SAP Help Portal incompleto | Médio | Consultar o conteúdo original; não usar em produção |
| R05 | Base curada desatualizada (novos FPS, notas, processos) | Médio | Responsável por documento, revisão em cadência fixa e versionamento dos documentos |
| R06 | Curadoria dependente de uma só pessoa (substituição da KBA 1500066) | Médio | Critérios de curadoria documentados e revisão cruzada com o Consultor SAP do cliente |
| R07 | Classificação errada da área (ex.: Depreciação × Contabilidade paralela) | Médio | Exibir nível de confiança e escalar quando for baixo |
| R08 | Exposição de dados reais em piloto futuro | Alto | Dados fictícios no protótipo; mascaramento, anonimização, acesso mínimo e adequação à LGPD antes do uso real |
| R09 | Notas da matriz sem base em dados reais levarem a priorização errada | Médio | Validar com o cliente (ver [priorização, seção 5](02-priorizacao-casos-de-uso.md)) antes de investir |
| R10 | Baixa confiança dos consultores no assistente | A definir | Fontes visíveis, nível de confiança explícito e Champions como referência entre pares |
| R11 | Uso do assistente como "fonte da verdade", sem revisão crítica | A definir | Treinamento e mensagem fixa: o assistente recomenda, o consultor decide |
| R12 | Resposta incorreta em tema de risco contábil | A definir | Regras de validação humana e revisão de casos pela Controladoria |
| R13 | Sobrecarga dos Champions | A definir | Tempo protegido pelo Delivery Lead e escopo reduzido no piloto |
| R14 | Adoção alta com qualidade baixa | A definir | Critério de qualidade obrigatório na passagem de onda |

**Limitações desta fase.** O assistente opera com as restrições abaixo, agrupadas por tema.

- **Acesso e ações no SAP**
  - Não lê dados reais nem saldos do SAP.
  - Acesso a dados reais só na onda 2, em modo somente leitura e após aprovação de Segurança.
  - Não executa transações, lançamentos, estornos, liquidações nem alterações de customizing.
  - Agentes com ferramentas ficam fora do escopo inicial.
- **Escopo e base de conhecimento**
  - Cobre apenas as 5 áreas da onda 1.
  - Operações de fechamento e integração com o razão funcionam apenas em modo orientação.
  - A base é pequena (14 documentos).
  - As respostas se limitam ao que está na base; sem evidência, o caso vai para um consultor.
  - A KBA 1500066 não é consultada diretamente.
- **Fontes e versão**
  - Os trechos do SAP Help Portal são incompletos e inadequados para uso em produção.
  - O conteúdo vale apenas para o S/4HANA 2025 FPS02.
  - Fontes em inglês e chamados em português podem gerar diferenças de terminologia.
- **Maturidade do protótipo**
  - Os dados são fictícios.
  - Não há medidas reais da linha de base disponíveis.
  - Prazos, volumes e metas são hipóteses até a medição da linha de base.
  - Os ganhos de tempo ainda não foram medidos.

## 7. Indicadores e comunicação de resultados

| Dimensão | Indicadores |
| --- | --- |
| **Produtividade** | Tempo de primeira resposta; tempo de resolução; retrabalho por dados faltantes |
| **Qualidade** | Taxa de aceite das recomendações; qualidade avaliada por amostra de consultores; taxa de respostas "sem evidência" |
| **Segurança** | Ações de risco escaladas corretamente; respostas sem fonte |
| **Adoção** | Usuários ativos e chamados atendidos com apoio do assistente |

Adoção só é considerada resultado quando acompanhada de melhora em produtividade **e** qualidade. Metas definidas após a linha de base. Método detalhado no documento de métricas.

## 8. Gestão de mudanças de prioridade

Novos pedidos entram no backlog e são pontuados pela mesma matriz de valor, viabilidade e risco; o Delivery Lead define o que prioriza. Em demandas urgentes, entrega-se uma versão mínima mantendo os mesmos controles de segurança e registra-se o que foi adiado.

## 9. Evolução da solução

| Tema | Posição | Justificativa |
| --- | --- | --- |
| Geração fundamentada em base curada (RAG) | Adotada | Permite citar fontes e limitar respostas ao que está documentado |
| Agentes com ferramentas | Avaliar na onda 2 | Aumentam pontos de falha; só se justificam com acesso seguro e leitura de dados reais |
| Ontologia formal | Não adotada agora | Glossário e vocabulário de campos já padronizam os termos; ontologia completa excede o escopo inicial |

## 10. Próximos passos (30 dias)

| Semana | Atividade | Responsável |
| --- | --- | --- |
| 1 | Alinhamento com Delivery Leads; escolha das equipes e Champions | Delivery Lead |
| 1 a 2 | Entrevistas e medição da linha de base | Time AI Advanced Assets e Funcional SAP |
| 2 | Treinamento das equipes piloto | Funcional SAP |
| 3 a 4 | Início do piloto com feedback e revisão semanal | Equipes piloto |
| 4 | Primeiro relatório e decisão sobre ajustes | Delivery Lead, Champions, AI Advanced Assets e Funcional SAP |

**Decisões solicitadas ao cliente:** equipes do piloto, Champions designados, acesso à amostra de chamados e patrocinador do plano.

## 11. Registro de decisões

Decisões tomadas pelo Consultor Funcional SAP e pelo Consultor AI Advanced Assets.

| ID | Decisão | Justificativa | Responsável |
| --- | --- | --- | --- |
| D01 | Limitar a onda 1 a 5 áreas do FI-AA | Maiores pontuações na matriz; base de conhecimento pequena e verificável | Funcional |
| D02 | Adotar S/4HANA 2025 FPS02 como referência única | Alinhar à versão do cliente e evitar recomendações de outras releases | Conjunta |
| D03 | Curadoria própria | Conteúdo revisado e adaptado ao cliente; KBA poderá ser avaliada no futuro | Funcional |
| D04 | SAP Help Portal como referência oficial complementar | Ancorar nomes de áreas, processos e conceitos na versão do cliente | Conjunta |
| D05 | RAG com citação obrigatória de fonte | Reduzir respostas inventadas e permitir auditoria | Conjunta |
| D06 | Integração só com orientação documental na onda 1 | Sem acesso ao sistema; saldos reais dependem de conector somente leitura (onda 2) | AI Advanced Assets |
| D07 | Erro de autorização como tema transversal | Causa frequente de chamados em todas as áreas da onda 1 | Funcional |
| D08 | Fora do escopo vai a consultor humano, sem resposta | Evitar orientação sem base (ex.: divergência entre ledgers) | Conjunta |
| D09 | O assistente recomenda ressalvando criticidade | Estorno, baixa, liquidação e fechamento têm impacto contábil e fiscal | Funcional |
| D10 | Registrar todo atendimento (chamado, resposta, fontes, decisão) | Rastreabilidade, avaliação de qualidade e melhoria da base | AI Advanced Assets |
| D11 | Priorizar por (Valor × Viabilidade) ÷ Risco, com notas como hipóteses | Ordenação transparente; risco define a supervisão; validação com Delivery Leads e Champions | Conjunta |
| D12 | Implantar em ondas com condição de avanço explícita | Avançar só com evidência de aceite, segurança do conector e volume | Conjunta |

## 12. Validação do protótipo

- **Cenários de teste:** 10 chamados fictícios com gabarito ([chamados](../tickets/chamados.md)) e 17 casos extras de generalização. Cobrem sucesso, dados incompletos (o assistente deve perguntar), fora do escopo e ação de risco (o assistente deve escalar), ausência de evidência e tentativa de burlar as regras. O erro de autorização (KB-FIAA-009) não tem chamado dedicado e é testado manualmente.
- **Base de conhecimento:** 14 documentos curtos, a partir da curadoria do Consultor Funcional SAP FI-AA e dos trechos do SAP Help Portal. Cobrem as 5 áreas da onda 1, autorização, glossário, política de escalonamento, informações mínimas, limites e dicionários de campos ([índice](../knowledge_base/README.md)).
- **Critérios de sucesso:**
  - classificar corretamente a área;
  - nenhuma resposta sem fonte citada;
  - pedir dados quando faltarem;
  - escalar 100% dos casos fora do escopo ou de risco;
  - recomendações aceitas pelo consultor na revisão.
- **Premissas:** dados e chamados fictícios; sem acesso ao SAP do cliente; key-users disponíveis para revisar respostas e validar as notas da matriz.
