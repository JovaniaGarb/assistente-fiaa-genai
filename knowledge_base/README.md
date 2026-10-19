# Base de conhecimento FI-AA (simulada)

Documentos curtos e rastreáveis que fundamentam o assistente. Cada afirmação cita a fonte; o que veio de conhecimento geral é marcado **[VALIDAR]**.

## Fontes

| Código | Fonte | Observação |
| --- | --- | --- |
| HELP | SAP Help Portal, Asset Accounting (FI-AA), SAP S/4HANA 2025 FPS02 (PDF de 221 páginas) | Fonte principal. O próprio PDF declara ser versão incompleta e não para uso em produção. Números são páginas do PDF. |
| S4F17 | S4F17.xlsx (Asset Accounting), abas Exam Prep e Problema-solução\* | Apoio e códigos de transação. É material de treinamento, resumido por IA, não documentação oficial. |
| TS07 | EN_Fixed_asset_TS07.xlsx | **Fonte SAP de campos**: definição, tipo, tamanho e decimais. É material de carga de dados em migração para S/4HANA. |
| DD | FIAA_Data_Dictionary.xlsx | Vocabulário e validações recomendadas em migração. Em divergência, vale o TS07 |

\* A planilha S4F12 (GL, AP e AR) não foi usada como fonte, por não tratar de FI-AA.

## Índice

| ID | Documento | Área |
| --- | --- | --- |
| KB-001 | Mapa do FI-AA e glossário | Transversal |
| KB-002 | Dados mestre e ativo incompleto | Asset Master Records |
| KB-003 | Aquisição e capitalização | Transactions |
| KB-004 | Imobilizado em andamento | Transactions |
| KB-005 | Baixa, estorno e transferência | Transactions |
| KB-006 | Depreciação | Depreciation |
| KB-007 | Integração com o razão (orientação) | Integration |
| KB-008 | Fechamento do período e do exercício | Closing Operations |
| KB-009 | Erro de autorização | Transversal |
| KB-010 | Escalonamento e Human-in-the-Loop | Governança |
| KB-011 | Informações mínimas e perguntas | Governança |
| KB-012 | Limites, fora do escopo e anti-alucinação | Governança |
| KB-013 | Dicionário de campos: dados mestre, datas e atribuições (tipo e tamanho) | Asset Master Records |
| KB-014 | Dicionário de campos: áreas de depreciação, valores acumulados, lançados e movimentos (tipo e tamanho) | Depreciation |

## Chamados e documentos esperados

| Chamado | Documentos |
| --- | --- |
| T-01 depreciação não lançada | KB-006, KB-014, KB-002, KB-010 |
| T-02 AuC impede fechamento | KB-004, KB-008, KB-010 |
| T-03 divergência sem detalhes (2 rodadas) | KB-007, KB-011, KB-014 |
| T-04 dado errado sem detalhes (2 rodadas) | KB-002, KB-013, KB-011, KB-010 |
| T-05 fora do escopo (não SAP) | KB-012 |
| T-06 fora do escopo (contabilidade paralela) | KB-012, KB-001 |
| T-07 estorno e reabertura | KB-005, KB-008, KB-010 |
| T-08 erro inexistente | nenhum |
| T-09 vida útil, tipo e tamanho de campo | KB-014, KB-013, KB-012 |
| T-10 tentativa de burlar regras | KB-012, KB-010 |

O KB-009 (autorização) não tem chamado dedicado e pode ser testado manualmente. O limite de 10 chamados do desafio foi mantido.

## Checklist de revisão por documento

- [ ] Cada afirmação sobre processo SAP confere com a sua experiência ou com a página citada
- [ ] Nenhuma transação, campo ou mensagem fora das fontes (ou marcada [VALIDAR])
- [ ] Tipos e tamanhos citados sempre com a ressalva de que são do template TS07
- [ ] Nenhuma promessa de resultado ("isso resolve")
- [ ] Nenhuma instrução de executar ação no sistema (só recomendar)
- [ ] Dados fictícios, sem cliente ou valores reais
- [ ] Cabeçalho preenchido (revisado_por e data_revisao)
