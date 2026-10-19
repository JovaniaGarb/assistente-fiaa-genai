"""Recuperação lexical (BM25) com métrica de relevância explicável.

Escolha: BM25 em Python puro. A base é pequena, em português e cheia de identificadores
técnicos (AFAB, AFABG, FAA_CMP078). Busca lexical é auditável (mostra exatamente quais termos
casaram) e dispensa dependências e chamadas externas. Embeddings ficam como evolução (README).
"""
from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass

from .kb import Chunk
from .text import expand_query, tokenize

K1, B = 1.5, 0.75
BM25_REF = 15.0   # BM25 de referência: abaixo dele, a cobertura é atenuada (evita falso positivo em consultas curtas ou fora do domínio)


@dataclass
class Hit:
    chunk: Chunk
    bm25: float
    cobertura: float           # cobertura ponderada por IDF dos termos da consulta, em [0, 1]
    relevancia: float          # cobertura atenuada pelo BM25 absoluto, em [0, 1]
    termos: list[str]          # termos que casaram (explicabilidade)


class Retriever:
    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        self.docs = [tokenize(f"{c.titulo_doc} {c.secao} {c.texto}") for c in chunks]
        self.sets = [set(d) for d in self.docs]
        self.tf = [Counter(d) for d in self.docs]
        self.N = len(chunks)
        self.avgdl = sum(len(d) for d in self.docs) / max(self.N, 1)
        df = Counter()
        for s in self.sets:
            df.update(s)
        self.df = df
        self.idf = {t: math.log(1 + (self.N - n + 0.5) / (n + 0.5)) for t, n in df.items()}
        self.idf_max = max(self.idf.values())
        self.idf_med = sorted(self.idf.values())[len(self.idf) // 2]
        self.vocab = set(df)

    def termos_consulta(self, q: str) -> list[str]:
        base = tokenize(q)
        return list(dict.fromkeys(base + expand_query(q)))

    def search(self, query: str, k: int = 6) -> list[Hit]:
        q = self.termos_consulta(query)
        if not q:
            return []
        conhecidos = [t for t in q if t in self.vocab]
        # termos informativos: presentes na base em >= 2 trechos e não numéricos (ignora ruído como datas e nº de ativo)
        informativos = [t for t in conhecidos if self.df[t] >= 2 and not t.isdigit()]
        denom = sum(self.idf[t] for t in informativos)
        hits: list[Hit] = []
        for i, c in enumerate(self.chunks):
            tf, dl = self.tf[i], len(self.docs[i])
            score = 0.0
            casados: list[str] = []
            for t in conhecidos:
                f = tf.get(t, 0)
                if f:
                    casados.append(t)
                    score += self.idf[t] * f * (K1 + 1) / (f + K1 * (1 - B + B * dl / self.avgdl))
            if score > 0:
                cov = (sum(self.idf[t] for t in informativos if t in casados) / denom) if denom else 0.0
                cov = min(cov, 1.0)
                hits.append(Hit(c, score, cov, cov * min(1.0, score / BM25_REF), casados))
        hits.sort(key=lambda h: h.bm25, reverse=True)
        return hits[:k]

    def termo_na_base(self, token: str) -> bool:
        """Verifica se um identificador (ex.: ZXX_998) aparece literalmente em algum trecho."""
        t = token.lower()
        return any(t in c.texto.lower() for c in self.chunks)
