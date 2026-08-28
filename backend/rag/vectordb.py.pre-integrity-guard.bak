"""
FAISS vector store — persistent on disk.
========================================
Uses inner-product on L2-normalized vectors == cosine similarity.
Stores:
  • faiss.index        — the FAISS index file
  • chunks.jsonl       — chunk metadata (one per line, in insertion order)

Designed for:
  • Multiple documents (incremental add)
  • Idempotent reload across server restarts
  • Reasonable memory: 1M chunks × 384-dim float32 ≈ 1.5 GB
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import List, Dict, Optional

import numpy as np

log = logging.getLogger("ivai.vectordb")


class VectorDB:
    def __init__(self, index_dir: Path, dim: int):
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.faiss_path = self.index_dir / "faiss.index"
        self.meta_path  = self.index_dir / "chunks.jsonl"
        self.dim = dim
        self.index = None
        self.metadata: List[Dict] = []

    # ───────────────────────────────────────────
    def load_or_init(self):
        import faiss
        if self.faiss_path.exists() and self.meta_path.exists():
            log.info(f"Loading existing index from {self.faiss_path}")
            self.index = faiss.read_index(str(self.faiss_path))
            with self.meta_path.open(encoding="utf-8") as f:
                self.metadata = [json.loads(line) for line in f if line.strip()]
            log.info(f"  loaded {self.index.ntotal} vectors, {len(self.metadata)} metadata rows")
        else:
            log.info(f"Initialising new IndexFlatIP (dim={self.dim})")
            self.index = faiss.IndexFlatIP(self.dim)

    def count(self) -> int:
        return 0 if self.index is None else self.index.ntotal

    def add(self, vectors: np.ndarray, metadata: List[Dict]):
        assert vectors.shape[0] == len(metadata), "vectors / metadata mismatch"
        if vectors.dtype != np.float32:
            vectors = vectors.astype(np.float32)
        self.index.add(vectors)
        self.metadata.extend(metadata)

    def save(self):
        import faiss
        faiss.write_index(self.index, str(self.faiss_path))
        # rewrite metadata fully (cheap; one JSON per chunk)
        with self.meta_path.open("w", encoding="utf-8") as f:
            for m in self.metadata:
                f.write(json.dumps(m, ensure_ascii=False) + "\n")

    # ───────────────────────────────────────────
    def search(self, query_vec: np.ndarray, top_k: int = 6) -> List[Dict]:
        if self.index is None or self.index.ntotal == 0:
            return []
        if query_vec.ndim == 1:
            query_vec = query_vec[None, :]
        if query_vec.dtype != np.float32:
            query_vec = query_vec.astype(np.float32)
        scores, idx = self.index.search(query_vec, min(top_k, self.index.ntotal))
        out = []
        for s, i in zip(scores[0], idx[0]):
            if i < 0 or i >= len(self.metadata):
                continue
            m = dict(self.metadata[i])
            m["score"] = float(s)            # IP on normalized vecs == cosine
            out.append(m)
        return out
