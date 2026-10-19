---
id: KB-FIAA-014
titulo: Dicionário de campos: áreas de depreciação, valores acumulados, lançados e movimentos
area: Depreciation
status: RASCUNHO para revisão (ilustrativo; campos gerados a partir do template SAP)
fontes: [TS07; HELP]
revisado_por: <preencher>
data_revisao: <preencher>
---

## Quando se aplica
Dúvidas sobre termos de depreciação por área, valores acumulados e lançados, ou campos de movimento (tipo, data de valor, valor).

> Versão do template: **S4CORE 103, de 04.10.2019**, objeto de migração "Fixed asset (incl. balances and transactions)". É material de **carga de dados**, mais antigo que a documentação de 2025 usada nos demais KBs. Tipos e tamanhos são os do **template**; em divergência com o sistema do cliente, prevalece o sistema [VALIDAR].

## Regras de formato do template [TS07 aba Introduction]
- **Texto:** letras, números e caracteres especiais. Em campos de texto com tamanho 80, o template permite **mapear valores** de origem para valores de destino; portanto o "80" **não é necessariamente o comprimento técnico do campo no SAP** [VALIDAR].
- **Número:** o tamanho informado **inclui os decimais**. Exemplo do template: tamanho 8 com 3 decimais admite 12345.678. Decimais são opcionais. Negativos levam o sinal "-" imediatamente antes do número.
- **Data:** no formato regional (por exemplo 31.12.1998 ou 12/31/1998).
- Campo com asterisco no template é **obrigatório**; as chaves (empresa e número do ativo) são obrigatórias em todas as folhas.
- Folhas obrigatórias: dados mestre, informações de lançamento e dados dependentes do tempo; as demais são opcionais conforme o escopo.

## Conceitos por campo
- **Vida útil (NDJAR e NDPER):** os dois campos são **aditivos**. Exemplo do template: 3,5 anos = 3 em anos + 6 em períodos [TS07].
- **Data de início da depreciação (AFABG):** em regra o sistema a determina pela **data de valor do primeiro lançamento de aquisição**. Se for informada manualmente no mestre, o sistema **ignora** a data de valor da aquisição. É guardada como data de calendário, mesmo em ano fiscal não calendário [TS07].
- **Data de prontidão operacional (INBDA):** se não informada na capitalização, o sistema usa a data de valor da capitalização [TS07].
- **Valor residual (SCHRW):** valor absoluto que não é depreciado na área (valor de memória). Quando informado, o percentual da chave de depreciação não é considerado, e a depreciação para ao atingi-lo [TS07].
- **Área desativada (XAFBE):** mantém a área definida no plano de amortização, mas inativa no ativo ou na classe [TS07].
- **Valores negativos permitidos (XNEGA):** necessário, por exemplo, para subvenção de investimento gerida como ativo negativo e para estorno posterior em imobilizado em andamento já totalmente liquidado [TS07].
- **Ativo de grupo (ANLGR e ANLGR2):** com a atribuição, a depreciação passa a ser determinada no **nível do ativo de grupo**, não do ativo individual [TS07].
- **Ano de troca da chave (UMJAR):** se diferente de zero, deixa de ser atualizado automaticamente quando os termos mudam [TS07].
- **Parcela variável (APROP):** percentual da depreciação que varia com o fator de turnos [TS07].
- **Valores acumulados × lançados:** os acumulados (prefixo K, por exemplo KANSW e KNAFA) são **saldos até o exercício**; os lançados (por exemplo NAFAG) são a **depreciação lançada no exercício**. No template, a depreciação acumulada deve ser **negativa** (exemplo -1267,00) [TS07].
- **Data de referência (VALUEDATE):** é a **data de valor do ativo**; pode divergir da data de lançamento e cair em período já fechado na contabilidade financeira, mas o **ano do lançamento e o ano da data de valor devem ser o mesmo**. O sistema cria um valor padrão quando possível, conforme a configuração [TS07; HELP p.91].
- **Exercício (GJAHR):** exercício ativo no sistema; pode coincidir ou não com o ano civil [TS07].
- **Depreciação lançada até o período (LAST_POSTED_DEPR_PERIOD):** relevante para carga **durante** o exercício; indica o último período com depreciação lançada no legado [TS07].
- **Regra do template:** as folhas de valores lançados e de movimentos aceitam apenas as áreas 01 e 32 "por construção do sistema" [TS07]. Trata-se de regra do template, não de regra geral do FI-AA [VALIDAR].

## Dicionário de campos

| Campo | Descrição | Tipo | Tamanho | Decimais | Obrigatório na folha |
|---|---|---|---|---|---|
| **Folha: Depreciation Areas** | | | | | |
| BUKRS | Empresa (company code) | Texto | 80 | n/a | Sim |
| ANLN1 | Número do ativo (externo/legado) | Texto | 12 | n/a | Sim |
| AFABE | Área de depreciação | Texto | 80 | n/a | Sim |
| XAFBE | Área de depreciação desativada | Texto | 1 | n/a | Não |
| AFASL | Chave de depreciação | Texto | 80 | n/a | Não |
| NDJAR | Vida útil (anos) | Número | 3 | 0 | Não |
| NDPER | Vida útil (períodos) | Número | 3 | 0 | Não |
| NDABJ | Vida útil decorrida (anos) no início do exercício | Número | 3 | 0 | Não |
| NDABP | Vida útil decorrida (períodos) no início do exercício | Número | 3 | 0 | Não |
| ANDSJ | Anos decorridos (depreciação especial) | Número | 3 | 0 | Não |
| ANDSP | Períodos decorridos (depreciação especial) | Número | 3 | 0 | Não |
| UMJAR | Ano de troca da chave de depreciação | Número | 4 | 0 | Não |
| RSTCK | Unidades depreciadas (depreciação por produção) | Número | 15 | 0 | Não |
| AFABG | Data de início da depreciação | Data | n/a | n/a | Não |
| SAFBG | Início da depreciação especial | Data | n/a | n/a | Não |
| ZINBG | Início do cálculo de juros | Data | n/a | n/a | Não |
| INBDA | Data de prontidão operacional | Data | n/a | n/a | Não |
| WBIND | Série de índices (valores de reposição) | Texto | 5 | n/a | Não |
| ALIND | Série de índices por idade | Texto | 5 | n/a | Não |
| APROP | Parcela variável da depreciação | Número | 7 | 4 | Não |
| SCHRW | Valor residual (sucata) | Número | 23 | 2 | Não |
| XNEGA | Valores negativos permitidos | Texto | 1 | n/a | Não |
| ANLGR | Ativo de grupo | Texto | 12 | n/a | Não |
| ANLGR2 | Subnúmero do ativo de grupo | Texto | 4 | n/a | Não |
| VYEAR | Ano de aquisição (alterável) | Número | 4 | 0 | Não |
| VMNTH | Mês de aquisição na área | Número | 3 | 0 | Não |
| SCHRW_PROZ | Valor residual em % do APC | Número | 14 | 11 | Não |
| **Folha: Cumulative Values** | | | | | |
| AFABE | Área de depreciação | Texto | 80 | n/a | Sim |
| GJAHR | Exercício | Número | 4 | 0 | Sim |
| KANSW | Valor de aquisição acumulado | Número | 23 | 2 | Não |
| KAUFW | Reavaliação acumulada do valor de reposição | Número | 23 | 2 | Não |
| KINVZ | Subvenções de investimento acumuladas | Número | 23 | 2 | Não |
| KNAFA | Depreciação ordinária acumulada | Número | 23 | 2 | Não |
| KSAFA | Depreciação especial acumulada | Número | 23 | 2 | Não |
| KAAFA | Depreciação não planejada acumulada | Número | 23 | 2 | Não |
| KMAFA | Transferência de reservas acumulada | Número | 23 | 2 | Não |
| KZINW | Juros acumulados | Número | 23 | 2 | Não |
| KAUFN | Reavaliação acumulada da depreciação ordinária | Número | 23 | 2 | Não |
| KANZA | Adiantamentos acumulados | Número | 23 | 2 | Não |
| CURRENCY | Moeda | Texto | 80 | n/a | Não |
| **Folha: Posted Values** | | | | | |
| AFABE | Área de depreciação | Texto | 80 | n/a | Sim |
| GJAHR | Exercício | Número | 4 | 0 | Sim |
| AUFWB | Reavaliação do valor de reposição lançada | Número | 23 | 2 | Não |
| NAFAG | Depreciação ordinária lançada no exercício | Número | 23 | 2 | Não |
| SAFAG | Depreciação especial lançada no exercício | Número | 23 | 2 | Não |
| AAFAG | Depreciação não planejada lançada no exercício | Número | 23 | 2 | Não |
| MAFAG | Transferência de reservas lançada no exercício | Número | 23 | 2 | Não |
| DZINSG | Juros lançados no exercício | Número | 23 | 2 | Não |
| AUFNG | Reavaliação da depreciação acumulada lançada | Número | 23 | 2 | Não |
| CURRENCY | Moeda | Texto | 80 | n/a | Não |
| LAST_POSTED_DEPR_PERIOD | Depreciação lançada até o período | Número | 3 | 0 | Não |
| **Folha: Transactions** | | | | | |
| AFABE | Área de depreciação | Texto | 80 | n/a | Sim |
| ASSETTRTYP | Tipo de movimento | Texto | 80 | n/a | Sim |
| GJAHR | Exercício | Número | 4 | 0 | Sim |
| CURRENT_NO | Nº sequencial das linhas do ativo no exercício | Número | 5 | 0 | Sim |
| VALUEDATE | Data de referência (data de valor do ativo) | Data | n/a | n/a | Sim |
| AMOUNT | Valor lançado | Número | 23 | 2 | Sim |
| CURRENCY | Moeda | Texto | 80 | n/a | Sim |

## Exige validação humana
Qualquer alteração de termos de depreciação, recálculo ou lançamento (KB-FIAA-010; HELP p.204, p.214).

## Referências
TS07 abas Introduction, Field List, Depreciation Areas, Cumulative Values, Posted Values e Transactions; HELP p.91, 204, 214.
