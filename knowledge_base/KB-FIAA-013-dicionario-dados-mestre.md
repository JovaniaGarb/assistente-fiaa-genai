---
id: KB-FIAA-013
titulo: Dicionário de campos: dados mestre, datas e atribuições organizacionais
area: Asset Master Records
status: RASCUNHO para revisão (ilustrativo; campos gerados a partir do template SAP)
fontes: [TS07 = EN_Fixed_asset_TS07.xlsx (template SAP de migração, S4CORE 103); HELP; DD]
revisado_por: <preencher>
data_revisao: <preencher>
---

## Quando se aplica
Dúvidas sobre o significado, o tipo, o tamanho ou o formato de um campo do cadastro do ativo (dados mestre, datas de lançamento e atribuições organizacionais).

> Versão do template: **S4CORE 103, de 04.10.2019**, objeto de migração "Fixed asset (incl. balances and transactions)". É material de **carga de dados**, mais antigo que a documentação de 2025 usada nos demais KBs. Tipos e tamanhos são os do **template**; em divergência com o sistema do cliente, prevalece o sistema [VALIDAR].

## Regras de formato do template [TS07 aba Introduction]
- **Texto:** letras, números e caracteres especiais. Em campos de texto com tamanho 80, o template permite **mapear valores** de origem para valores de destino; portanto o "80" **não é necessariamente o comprimento técnico do campo no SAP** [VALIDAR].
- **Número:** o tamanho informado **inclui os decimais**. Exemplo do template: tamanho 8 com 3 decimais admite 12345.678. Decimais são opcionais. Negativos levam o sinal "-" imediatamente antes do número.
- **Data:** no formato regional (por exemplo 31.12.1998 ou 12/31/1998).
- Campo com asterisco no template é **obrigatório**; as chaves (empresa e número do ativo) são obrigatórias em todas as folhas.
- Folhas obrigatórias: dados mestre, informações de lançamento e dados dependentes do tempo; as demais são opcionais conforme o escopo.

## Conceitos por campo
- **Número do ativo (ANLN1):** identificador único do ativo; no template é o número do sistema legado, e os ativos migrados recebem numeração interna [TS07].
- **Classe (ANLKL):** um subnúmero deve ter a **mesma classe do ativo principal** [TS07].
- **Data de capitalização (AKTIV):** o sistema guarda a data de referência do lançamento que capitaliza o ativo; é **obrigatória** na folha de informações de lançamento [TS07].
- **Data de desativação (DEAKT):** o sistema registra a data de valor da baixa quando a baixa é **total** [TS07].
- **Gerenciado historicamente (HISTORY):** indicador "X" [TS07].
- **Centro de custo (KOSTL):** obrigatório no template; o **centro de custo responsável (KOSTLV)** responde pelo ativo, mas não arca com a depreciação [TS07]. Só se atribui um centro de custo por ativo [HELP p.24].
- **Ativo paralisado (XSTIL):** usado quando o ativo está em conservação e **não há depreciação** [TS07].
- **Fator de múltiplos turnos (SHIFT_FACT):** multiplica a **parcela variável** da depreciação ordinária [TS07].
- **Local do ativo (STORT) e centro (WERKS):** o centro é necessário para determinar o local [TS07].
- **Elemento PEP (PS_PSP_PNR2):** necessário para atribuir depreciação, juros e ganho ou perda a um PEP [TS07].
- **Dados dependentes do tempo:** campos de atribuição organizacional têm validade por período; ver tratamento de alteração em KB-FIAA-002 [HELP p.83].

## Dicionário de campos

| Campo | Descrição | Tipo | Tamanho | Decimais | Obrigatório na folha |
|---|---|---|---|---|---|
| **Folha: Master Details** | | | | | |
| BUKRS | Empresa (company code) | Texto | 80 | n/a | Sim |
| ANLN1 | Número do ativo (externo/legado) | Texto | 12 | n/a | Sim |
| ANLKL | Classe do ativo | Texto | 80 | n/a | Sim |
| TXT50 | Descrição do ativo | Texto | 50 | n/a | Sim |
| TXA50_MORE | Descrição adicional do ativo | Texto | 50 | n/a | Não |
| SERNR | Número de série | Texto | 18 | n/a | Não |
| INVNR | Número de inventário | Texto | 25 | n/a | Não |
| MENGE | Quantidade | Número | 13 | 3 | Não |
| MEINS | Unidade de medida base | Texto | 80 | n/a | Não |
| HISTORY | Ativo gerenciado historicamente | Texto | 1 | n/a | Não |
| MAIN_DESCRIPT | Texto do número principal do ativo | Texto | 50 | n/a | Não |
| **Folha: Posting Information** | | | | | |
| AKTIV | Data de capitalização | Data | n/a | n/a | Sim |
| DEAKT | Data de desativação | Data | n/a | n/a | Não |
| GPLAB | Data planejada de baixa | Data | n/a | n/a | Não |
| BSTDT | Data do pedido de compra do ativo | Data | n/a | n/a | Não |
| CAP_KEY | Chave de análise de resultados | Texto | 80 | n/a | Não |
| **Folha: Time-Dependent Data** | | | | | |
| GSBER | Área de negócios | Texto | 80 | n/a | Não |
| KOSTL | Centro de custo | Texto | 80 | n/a | Sim |
| KOSTLV | Centro de custo responsável | Texto | 80 | n/a | Não |
| LSTAR | Tipo de atividade | Texto | 80 | n/a | Não |
| CAUFN | Ordem interna | Texto | 80 | n/a | Não |
| IAUFN | Ordem de manutenção | Texto | 80 | n/a | Não |
| WERKS | Centro (planta) | Texto | 80 | n/a | Não |
| STORT | Local do ativo | Texto | 80 | n/a | Não |
| RAUMN | Sala | Texto | 8 | n/a | Não |
| KFZKZ | Placa do veículo | Texto | 15 | n/a | Não |
| PERNR | Número de pessoal | Texto | 80 | n/a | Não |
| SHIFT_FACT | Fator de múltiplos turnos | Número | 3 | 2 | Não |
| XSTIL | Ativo paralisado (shutdown) | Texto | 1 | n/a | Não |
| GEBER | Fundo | Texto | 80 | n/a | Não |
| GRANT_NBR | Subvenção (grant) | Texto | 20 | n/a | Não |
| FUNC_AREA_LONG | Área funcional (longa) | Texto | 16 | n/a | Não |
| FISTL | Centro de fundos | Texto | 80 | n/a | Não |
| GEBER2 | Fundo para atribuição de contas de APC | Texto | 80 | n/a | Não |
| FKBER2 | Área funcional para atribuição de APC | Texto | 80 | n/a | Não |
| GRANT_NBR2 | Subvenção para atribuição de APC | Texto | 80 | n/a | Não |
| FISTL2 | Centro de fundos para atribuição de APC | Texto | 80 | n/a | Não |
| PS_PSP_PNR2 | Elemento PEP (chave externa) | Texto | 80 | n/a | Não |
| TAXJURCODE | Jurisdição fiscal | Texto | 80 | n/a | Não |
| IMKEY | Chave interna de objeto imobiliário | Texto | 80 | n/a | Não |
| RL_EST_KEY_EXT | Objeto imobiliário (chave externa) | Texto | 40 | n/a | Não |
| BUDGET_PD | Período de orçamento | Texto | 80 | n/a | Não |
| BUDGET_PD2 | Período de orçamento para atribuição de APC | Texto | 80 | n/a | Não |
| SEGMENT | Segmento | Texto | 80 | n/a | Não |
| PRCTR | Centro de lucro | Texto | 80 | n/a | Não |

## Fora deste documento
Folhas Inventory, Allocations, Origin, Investment, Net worth, Real Estate, Leasing, Proportional Values e as folhas específicas de país (Rússia e Índia) existem no template, mas **estão fora do escopo do assistente** (KB-FIAA-012).

## Exige validação humana
Qualquer alteração de campo no sistema (KB-FIAA-010).

## Referências
TS07 abas Introduction, Field List, Master Details, Posting Information e Time-Dependent Data; HELP p.24, 83.
