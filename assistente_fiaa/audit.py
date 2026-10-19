"""Registro de auditoria (JSONL) e fila de validação humana (HITL)."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

_MASCARAS = [(re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "[EMAIL]"),
             (re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"), "[CPF]")]


def mascarar(txt: str) -> str:
    for rx, sub in _MASCARAS:
        txt = rx.sub(sub, txt)
    return txt


def agora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Audit:
    def __init__(self, log_dir: Path):
        self.dir = Path(log_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.arquivo = self.dir / "audit.jsonl"

    def registrar(self, registro: dict) -> None:
        registro = {"ts": agora(), **registro}
        with self.arquivo.open("a", encoding="utf-8") as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")

    def ler(self) -> list[dict]:
        if not self.arquivo.exists():
            return []
        return [json.loads(l) for l in self.arquivo.read_text(encoding="utf-8").splitlines() if l.strip()]


class FilaHITL:
    """Fila de itens que dependem de decisão humana. O assistente só cria itens PENDENTES."""

    def __init__(self, log_dir: Path):
        self.arquivo = Path(log_dir) / "hitl_queue.jsonl"
        self.arquivo.parent.mkdir(parents=True, exist_ok=True)

    def _todos(self) -> list[dict]:
        if not self.arquivo.exists():
            return []
        return [json.loads(l) for l in self.arquivo.read_text(encoding="utf-8").splitlines() if l.strip()]

    def _salvar(self, itens: list[dict]) -> None:
        self.arquivo.write_text("\n".join(json.dumps(i, ensure_ascii=False) for i in itens) + ("\n" if itens else ""),
                                encoding="utf-8")

    def adicionar(self, ticket_id: str, rota: str, motivo: str, acoes: list[str]) -> dict:
        itens = self._todos()
        item = {"id": f"HITL-{len(itens)+1:04d}", "ticket_id": ticket_id, "rota": rota, "motivo": motivo,
                "acoes_propostas": acoes, "status": "PENDENTE", "criado_em": agora(), "decisao": None}
        itens.append(item)
        self._salvar(itens)
        return item

    def listar(self, status: str | None = None) -> list[dict]:
        return [i for i in self._todos() if status is None or i["status"] == status]

    def decidir(self, item_id: str, aprovado: bool, revisor: str, comentario: str = "") -> dict:
        itens = self._todos()
        for i in itens:
            if i["id"] == item_id:
                i["status"] = "APROVADO" if aprovado else "REJEITADO"
                i["decisao"] = {"revisor": revisor, "comentario": comentario, "em": agora()}
                self._salvar(itens)
                return i
        raise KeyError(item_id)
