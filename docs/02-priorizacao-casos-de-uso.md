# Priorização de casos de uso: valor × viabilidade × risco

> **Importante:** as notas abaixo são **hipóteses iniciais de consultoria**, baseadas no desenho do processo, e não em dados reais de chamados. Elas devem ser validadas com Delivery Leads e Champions (seção 5) antes de qualquer decisão de investimento.

## 1. Critérios (escala 1 a 5)

| Critério | O que mede | 5 significa |
| --- | --- | --- |
| **Valor** | Frequência esperada do chamado × tempo manual de análise × impacto no negócio | Alto valor |
| **Viabilidade** | Existe documentação textual para fundamentar a resposta? Dá para fazer sem acesso a dados reais do SAP? | Muito viável agora |
| **Risco** | Impacto contábil, fiscal e financeiro de uma resposta errada; reversibilidade; exposição de dados | Risco alto |

**Pontuação de prioridade = (Valor × Viabilidade) ÷ Risco.** Quanto maior, mais cedo entra. O risco divide porque ele não se compensa com valor: ele define o **nível de supervisão humana**, não apenas a ordem.

## 2. Matriz das áreas do FI-AA

| Área (índice FI-AA) | Valor | Viabilidade | Risco | Prioridade | Onda |
| --- | :-: | :-: | :-: | :-: | --- |
| Asset Master Records | 4 | 5 | 2 | **10,0** | 1 |
| Transactions (aquisição, imobilizado em andamento, baixa, transferência) | 5 | 4 | 3 | **6,7** | 1 |
| Depreciation | 4 | 4 | 3 | **5,3** | 1 |
| Closing Operations | 5 | 3 | 4 | **3,8** | 1, com supervisão reforçada |
| Integration (FI-AA × contabilidade geral) | 5 | 3 | 4 | **3,8** | 1, com supervisão reforçada; só orientação documental |
| Reporting | 3 | 2 | 2 | **3,0** | 2 |
| Parallel Accounting in Asset Accounting | 4 | 3 | 4 | **3,0** | 2 |
| Special Valuations, Investment Support and Revaluation | a validar | 3 | 3 a 4 | n/a | 3, só se o cliente usar com frequência |
| APIs for Asset Accounting | n/a | a avaliar | a avaliar | n/a | Avaliar como possível caminho de leitura segura (onda 2), validando na documentação oficial |
| Organizational Elements, Basic Functions (configuração), Manual Depreciation, Tools | baixo | baixo | alto | n/a | Fora do escopo |
| Legacy Data Transfer, Migration to New Asset Accounting | baixo (trabalho de projeto, não de chamado) | baixo | alto | n/a | Fora do escopo |

## 3. Por que começar pelas 5 áreas da onda 1

1. **Cobrem o ciclo de vida do ativo**: cadastro, movimentação, depreciação, fechamento e a conexão com a contabilidade geral. É o fluxo que gera a maioria das dúvidas recorrentes de usuário.
2. **São fundamentáveis em documentação textual.** Cada área tem fluxos e verificações descritos em documentos, o que permite RAG com fonte citável e reduz alucinação. Essa é a condição para a resposta ser confiável.
3. **Não exigem acesso a dados reais do SAP** para entregar valor na primeira onda. O assistente orienta e pede dados; não consulta o sistema.
4. **O risco é controlável com supervisão humana.** Em Transactions, Depreciation, Closing Operations e Integration, qualquer ação com impacto contábil (estorno, baixa, liquidação, fechamento, ajuste de saldo) é sempre encaminhada para dupla validação humana. O assistente só recomenda.
5. **Closing Operations e Integration entram com salvaguardas** por terem as menores notas da onda 1: valor alto, mas risco alto e viabilidade menor. Se o tempo apertar, são as primeiras a serem reduzidas para "orientar e escalar".

## 4. Por que as demais ficaram para depois ou fora

- **Parallel Accounting (onda 2):** valor relevante, pois diferenças entre ledgers e áreas de avaliação geram chamados de depreciação. Exige conhecer o desenho de contabilidade paralela do cliente, então começa só com escalonamento para humano.
- **Reporting (onda 2):** valor menor e mais difícil de fundamentar sem conhecer os relatórios usados pelo cliente.
- **Special Valuations e Investment Support (onda 3):** dependem de o cliente realmente usar essas funções. Sem dado de volume, não há como justificar investimento.
- **APIs for Asset Accounting:** dependem de o cliente usar Universal Parallel Accounting.
- **Configuração, estrutura organizacional, depreciação manual, ferramentas, migração e carga de legado (fora):** alteram o sistema ou são trabalho de projeto, não de atendimento de chamado. Validar com o cliente. À princípio, o risco de uma recomendação errada é alto e a decisão é essencialmente de consultor humano.

## 5. Como validar as notas com o cliente

| Pergunta | Fonte | Efeito na matriz |
| --- | --- | --- |
| Quantos chamados por área nos últimos 3 a 6 meses? | Ferramenta de chamados | Ajusta **Valor** |
| Tempo médio de análise e de resolução por área? | Ferramenta de chamados e amostra com consultores | Ajusta **Valor** e a linha de base de ganho |
| Quais chamados voltam por informação incompleta? | Amostra de chamados | Mostra onde o assistente deve **perguntar** |
| Existe documentação por área? Está atualizada? | Champions e consultores | Ajusta **Viabilidade** |
| Qual é o impacto de uma orientação errada? | Controladoria e auditoria | Ajusta **Risco** e as regras de supervisão |

## 6. Roteiro de ondas

| Onda | Escopo | Condição para avançar |
| --- | --- | --- |
| **1: piloto** | Master Records, Transactions, Depreciation, Closing Operations e Integration (as duas últimas com supervisão reforçada e só orientação) | Taxa de aceite das recomendações e ausência de resposta sem fonte |
| **2: expansão** | Integration com análise de saldos reais (acesso somente leitura), Parallel Accounting, Reporting | Conector validado com segurança; base de conhecimento ampliada pelos Champions |
| **3: escala** | Áreas de uso condicionado e outros módulos | Evidência de volume e ganho nas ondas anteriores |

Documentos relacionados: [escopo do FI-AA](00-escopo-fi-aa.md).
