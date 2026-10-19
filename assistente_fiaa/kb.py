"""Carga e divisão (chunking) da base de conhecimento em Markdown."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from . import config
from .text import normalize

MAX_CHARS = 1100


@dataclass
class Chunk:
    id: str            # ex.: KB-FIAA-006#causas-possiveis-de-depreciacao-nao-lancada
    doc_id: str        # ex.: KB-FIAA-006
    titulo_doc: str
    area: str
    secao: str
    tipo: str          # causas | verificacoes | acoes | minimas | conteudo
    texto: str
    paginas: list[str] = field(default_factory=list)   # citações HELP p.N encontradas no texto


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", normalize(s)).strip("-")[:60]


def _tipo_secao(titulo: str) -> str:
    t = normalize(titulo)
    if t.startswith("causas"):
        return "causas"
    if t.startswith("verificacoes"):
        return "verificacoes"
    if t.startswith("exige validacao"):
        return "acoes"
    if t.startswith("informacoes minimas") or t.startswith("dados minimos") or t.startswith("dados adicionais"):
        return "minimas"
    return "conteudo"


def _front_matter(md: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", md, re.S)
    if not m:
        return {}, md
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, m.group(2)


def load_chunks(kb_dir: Path | None = None) -> list[Chunk]:
    kb_dir = Path(kb_dir or config.KB_DIR)
    chunks: list[Chunk] = []
    for f in sorted(kb_dir.glob("KB-FIAA-*.md")):
        meta, body = _front_matter(f.read_text(encoding="utf-8"))
        doc_id = meta.get("id", f.stem)
        titulo = meta.get("titulo", doc_id)
        area = meta.get("area", "")
        secoes = re.split(r"^## ", body, flags=re.M)
        for sec in secoes[1:]:
            nome, _, corpo = sec.partition("\n")
            corpo = corpo.strip()
            if not corpo or nome.strip().lower().startswith("referências"):
                continue
            tipo = _tipo_secao(nome)
            buf, n = [], 0
            partes: list[str] = []
            for line in corpo.splitlines():
                if line.startswith("|---"):
                    continue
                if n + len(line) > MAX_CHARS and buf:
                    partes.append("\n".join(buf)); buf, n = [], 0
                buf.append(line); n += len(line)
            if buf:
                partes.append("\n".join(buf))
            for i, p in enumerate(partes):
                cid = f"{doc_id}#{_slug(nome)}" + (f"-{i+1}" if len(partes) > 1 else "")
                paginas = sorted(set(re.findall(r"(?:HELP|S4F17|TS07|DD)[^\]]*", p)))
                chunks.append(Chunk(cid, doc_id, titulo, area, nome.strip(), tipo, p.strip(), paginas))
    return chunks
