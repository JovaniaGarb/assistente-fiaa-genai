---
id: KB-FIAA-002
titulo: Dados mestre do ativo, alterações e ativo incompleto
area: Asset Master Records
status: RASCUNHO para revisão (ilustrativo)
fontes: [HELP, S4F17, DD, TS07]
revisado_por: <preencher>
data_revisao: <preencher>
---

## Quando se aplica
Ativo criado ou alterado com dado errado, ativo incompleto, dúvida sobre data de incorporação, classe, centro de custo ou termos de depreciação.

## Conceitos
- A chave do ativo é **empresa + número + subnúmero** (BUKRS, ANLN1, ANLN2) [DD].
- O registro mestre contém dados gerais, atribuições organizacionais (muitas dependentes do tempo) e **termos de depreciação por área** (chave de depreciação, vida útil, data de início) [HELP p.81-82; DD].
- Só é possível atribuir **um centro de custo** por ativo [HELP p.24].
- O layout de tela por classe define campos obrigatórios, opcionais ou ocultos [S4F17 Ex.5; HELP p.72].
- Verificar a cronologia entre aquisição, data de incorporação (AKTIV) e início da depreciação (AFABG) [DD].

## Conceitos de campo (detalhes em KB-FIAA-013)
- **Data de capitalização (AKTIV):** data de referência do lançamento que capitaliza o ativo; obrigatória no cadastro [TS07].
- **Subnúmero:** deve ter a mesma classe do ativo principal [TS07].
- **Ativo paralisado (XSTIL):** em conservação, sem depreciação [TS07].
- **Área de depreciação desativada (XAFBE):** a área existe no plano, mas fica inativa no ativo [TS07].
- **Formato:** número do ativo com até 12 caracteres; descrição com até 50; datas no formato regional [TS07].

## Como cada tipo de alteração é tratada

| Tipo | Tratamento | Fonte |
|---|---|---|
| Campo comum | Altera-se diretamente no registro | HELP p.83 |
| Unidade organizacional não relevante ao balanço | Altera-se com intervalo de tempo | HELP p.83 |
| Centro de lucro ou segmento | Novo intervalo gera **transferência automática** | HELP p.83 |
| Classe do ativo | Exige **transferência** para novo registro | HELP p.84; S4F17 Ex.18 |
| Termos de depreciação | Afetam a depreciação planejada dos exercícios abertos | HELP p.204 |

## Ativo incompleto
- Nele **não se lança depreciação**, não se pode baixar e **não se fecha o exercício** da empresa [HELP p.221].
- Relatório de ativos incompletos (AUVA) lista o motivo [HELP p.194, p.221].
- Pode surgir quando a visão do ativo limita o acesso a campos [HELP p.71].

## Verificações recomendadas (somente leitura)
Exibir o ativo (AW01N); conferir classe, datas, chave de depreciação, vida útil, indicadores de paralisação e de área desativada; rodar o relatório de ativos incompletos; consultar documentos de alteração [S4F17 Ex.11].

## Exige validação humana quando
Troca de classe, mudança de centro de lucro ou segmento, alteração de termos de depreciação, bloqueio, desativação ou exclusão [HELP p.83-85].

## Informações mínimas
Empresa, número e subnúmero, campo e valor correto, se é dependente do tempo, mensagem exata (ver KB-FIAA-011).

## Não fazer
Não propor alteração sem saber o campo; não indicar exclusão física sem validação humana [HELP p.85].

## Referências
HELP p.24, 71-72, 81-85, 194, 204, 221; S4F17 Ex.5, 10-11, 18; DD; TS07 abas Master Details, Posting Information e Depreciation Areas.
