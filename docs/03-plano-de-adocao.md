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

| Risco | Resposta |
| --- | --- |
| Baixa confiança dos usuários | Fontes visíveis, nível de confiança explícito, Champions como referência |
| Uso sem revisão crítica | Treinamento e mensagem fixa: o assistente recomenda, o consultor decide |
| Base desatualizada | Responsável por documento e revisão em cadência fixa |
| Resposta incorreta em tema de risco contábil | Regras de validação humana e revisão pela Controladoria |
| Sobrecarga dos Champions | Tempo protegido pelo Delivery Lead e escopo reduzido no piloto |
| Dados sensíveis em chamados | Dados fictícios no protótipo; mascaramento e acesso mínimo antes do uso real |
| Adoção alta com qualidade baixa | Critério de qualidade na passagem de onda |

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
