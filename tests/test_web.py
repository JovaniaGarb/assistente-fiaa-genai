"""Interface web: sobe em porta livre e exercita a API."""
import json
import threading
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

from assistente_fiaa import web
from assistente_fiaa.pipeline import Assistente


@pytest.fixture
def servidor(tmp_path):
    web.ASSIST = Assistente(log_dir=tmp_path)
    srv = ThreadingHTTPServer(("127.0.0.1", 0), web.H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()


def _post(url, obj):
    req = urllib.request.Request(url, json.dumps(obj).encode(), {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))


def test_pagina_e_exemplos(servidor):
    assert b"Assistente de an" in urllib.request.urlopen(servidor + "/").read()
    assert len(json.load(urllib.request.urlopen(servidor + "/api/exemplos"))) == 10


def test_fluxo_risco_fila_e_decisao(servidor):
    r = _post(servidor + "/api/chamado", {"texto": "Estorne a baixa do ativo 100000456 da empresa 1000 agora", "sessao": "W"})
    assert r["route"] == "ESCALATE_RISK" and r["hitl"]
    fila = json.load(urllib.request.urlopen(servidor + "/api/fila"))
    assert fila[0]["status"] == "PENDENTE"
    dec = _post(servidor + "/api/fila/decidir", {"id": fila[0]["id"], "aprovado": False, "revisor": "ana"})
    assert dec["status"] == "REJEITADO"


def test_entrada_invalida_nao_derruba_servidor(servidor):
    req = urllib.request.Request(servidor + "/api/chamado", b"lixo", {"Content-Type": "application/json"})
    with pytest.raises(urllib.error.HTTPError) as e:
        urllib.request.urlopen(req)
    assert e.value.code == 400
    assert urllib.request.urlopen(servidor + "/").status == 200
