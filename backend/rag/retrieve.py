"""
Top-k retrieval with relevance threshold.
=========================================
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

MIN_RELEVANCE = 0.30   # cosine threshold below which we say "I don't know"


@dataclass
class RetrievedChunk:
    text:   str
    source: str
    page:   int
    score:  float


def retrieve(question: str, embedder, vectordb, top_k: int = 6) -> List[RetrievedChunk]:
    qvec = embedder.encode([question])
    raw = vectordb.search(qvec, top_k=top_k)
    return [
        RetrievedChunk(
            text=r["text"],
            source=r.get("source", "unknown"),
            page=r.get("page", 0),
            score=r.get("score", 0.0),
        )
        for r in raw
    ]
