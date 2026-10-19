"""Qualidade do RAG, integridade da base e auditoria / HITL."""
import re

from assistente_fiaa import config
from assistente_fiaa.kb import load_chunks
from assistente_fiaa.retriever import Retriever


def test_base_tem_14_documentos_com_secoes_obrigatorias():
    chunks = load_chunks()
    assert len({c.doc_id for c in chunks}) == 14
    for c in chunks:
        assert c.texto.strip() and c.id.startswith("KB-FIAA-")


def test_paginas_help_citadas_existem_no_pdf_de_221_paginas():
    for c in load_chunks():
        for p in re.findall(r"HELP p\.(\d+)", c.texto):
            assert 1 <= int(p) <= 221, (c.id, p)


def test_ids_de_chunk_sao_unicos():
    ids = [c.id for c in load_chunks()]
    assert len(ids) == len(set(ids))


PERGUNTAS_RECUPERACAO = [
    ("depreciação não lançada execução AFAB log", "KB-FIAA-006"),
    ("imobilizado em andamento liquidação AIAB", "KB-FIAA-004"),
    ("encerramento do exercício FAA_CMP", "KB-FIAA-008"),
    ("estorno de baixa AB08", "KB-FIAA-005"),
    ("tamanho do campo número do ativo template", "KB-FIAA-013"),
    ("divergência saldo razão ativo conta de reconciliação", "KB-FIAA-007"),
]


def test_recuperacao_traz_documento_correto_no_top_k():
    r = Retriever(load_chunks())
    for q, doc in PERGUNTAS_RECUPERACAO:
        docs = [h.chunk.doc_id for h in r.search(q, config.TOP_K)]
        assert doc in docs[:3], (q, docs)


def test_consulta_fora_do_dominio_tem_relevancia_baixa():
    r = Retriever(load_chunks())
    hits = r.search("receita de bolo de cenoura com cobertura de chocolate", 3)
    assert not hits or hits[0].relevancia < config.LIMIAR_RELEVANCIA


def test_termos_casados_sao_explicaveis():
    r = Retriever(load_chunks())
    h = r.search("execução da depreciação AFAB", 1)[0]
    assert h.termos and h.bm25 > 0


def test_log_de_auditoria_contem_campos_exigidos(assistente):
    assistente.processar("Estorne a baixa do ativo 100000456 da empresa 1000.", "A1")
    reg = assistente.audit.ler()[-1]
    for k in ("ts", "ticket_id", "chamado", "route", "confianca", "hitl", "fontes_citadas", "resposta", "recuperados", "prompt_version", "validacao"):
        assert k in reg, k
    assert reg["fontes_citadas"] and reg["recuperados"]


def test_fila_hitl_so_cria_pendente_e_humano_decide(assistente):
    assistente.processar("Estorne a baixa do ativo 100000456 da empresa 1000.", "A2")
    item = assistente.fila.listar("PENDENTE")[0]
    assert item["status"] == "PENDENTE" and item["decisao"] is None
    dec = assistente.fila.decidir(item["id"], aprovado=False, revisor="maria.silva", comentario="aguardar fechamento")
    assert dec["status"] == "REJEITADO" and dec["decisao"]["revisor"] == "maria.silva"


def test_resposta_sem_acao_de_risco_nao_cria_item_na_fila(assistente):
    assistente.processar("Qual é o tipo e o tamanho do campo de número do ativo no template de migração?", "A3")
    assert not assistente.fila.listar()


def test_aviso_obrigatorio_de_tipo_e_tamanho_ts07(assistente):
    r = assistente.processar("Qual é o tipo e o tamanho do campo de número do ativo nos dados mestre do template de migração?", "A4")
    assert any("TS07" in a and "validados" in a for a in r.avisos)


def test_aviso_integration_modo_orientacao(assistente):
    assistente.processar("O saldo do imobilizado no razão não bate com o do módulo de ativos.", "A5")
    r = assistente.processar("Empresa 1000, conta de custo de aquisição de máquinas, data-chave 30/09/2026, ledger 0L. O razão está 12.500 acima dos ativos.", "A5")
    assert any("não leu saldos reais" in a for a in r.avisos)
