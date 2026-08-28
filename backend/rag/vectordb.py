"""
FAISS vector store — persistent on disk.
========================================
Uses inner-product on L2-normalized vectors == cosine similarity.
Stores:
  • faiss.index        — the FAISS index file
  • chunks.jsonl       — chunk metadata (one per line, in insertion order)

CITATION INTEGRITY INVARIANT
============================
search() resolves a FAISS id `i` to `metadata[i]` POSITIONALLY. That mapping is
only meaningful when the two stores are the same length and were written by the
same ingest run. If they diverge, every citation past the divergence point names
the wrong document and page — silently, because the id is still in range.

This module therefore refuses to serve retrieval unless:

    index.ntotal == len(metadata)   and   index.d == dim

See docs/bug-index-metadata-misalignment.md for the incident this guards against.

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


class IndexIntegrityError(RuntimeError):
    """Raised when the vector store cannot guarantee citation integrity.

    Retrieval MUST NOT proceed after this is raised. Metadata is never
    truncated, vectors are never dropped, and no attempt is made to guess the
    correct mapping — any of those would produce plausible-looking but wrong
    citations, which is worse than refusing to serve.
    """


class VectorDB:
    def __init__(self, index_dir: Path, dim: int):
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.faiss_path = self.index_dir / "faiss.index"
        self.meta_path  = self.index_dir / "chunks.jsonl"
        self.dim = dim
        self.index = None
        self.metadata: List[Dict] = []
        self.integrity_ok: bool = False

    # ───────────────────────────────────────────
    def load_or_init(self):
        """Load the index and HARD-FAIL if citation integrity cannot be guaranteed."""
        import faiss
        self.integrity_ok = False
        if self.faiss_path.exists() and self.meta_path.exists():
            log.info(f"Loading existing index from {self.faiss_path}")
            self.index = faiss.read_index(str(self.faiss_path))
            with self.meta_path.open(encoding="utf-8") as f:
                self.metadata = [json.loads(line) for line in f if line.strip()]
            log.info(f"  loaded {self.index.ntotal} vectors, {len(self.metadata)} metadata rows")
            self.verify_integrity()          # raises IndexIntegrityError on mismatch
        else:
            log.info(f"Initialising new IndexFlatIP (dim={self.dim})")
            self.index = faiss.IndexFlatIP(self.dim)
            self.integrity_ok = True

    # ───────────────────────────────────────────
    def verify_integrity(self) -> None:
        """Enforce the citation-integrity invariant. Raises IndexIntegrityError.

        Checks, in order:
          1. an index is loaded
          2. index.ntotal == len(metadata)
          3. index.d == self.dim  (embedder output must match index geometry)
          4. every metadata row carries the fields citations are built from
        """
        if self.index is None:
            raise IndexIntegrityError("no FAISS index loaded")

        n_vec, n_meta = int(self.index.ntotal), len(self.metadata)
        if n_vec != n_meta:
            raise IndexIntegrityError(
                f"CITATION INTEGRITY FAILURE in {self.index_dir}: "
                f"{n_vec} vectors but {n_meta} metadata rows. "
                f"search() maps FAISS id -> metadata[id] positionally, so this "
                f"mismatch makes citations point at the wrong source/page. "
                f"Refusing to serve retrieval. "
                f"Rebuild with scripts/data_ingestion/rebuild_index.py; see "
                f"docs/bug-index-metadata-misalignment.md"
            )

        if int(self.index.d) != int(self.dim):
            raise IndexIntegrityError(
                f"DIMENSION MISMATCH in {self.index_dir}: index.d={self.index.d} "
                f"but embedder dim={self.dim}. The index was built with a different "
                f"embedding model. Refusing to serve retrieval."
            )

        required = ("text", "source", "page")
        for i, m in enumerate(self.metadata):
            missing = [k for k in required if k not in m]
            if missing:
                raise IndexIntegrityError(
                    f"METADATA SCHEMA FAILURE in {self.index_dir}: row {i} is missing "
                    f"{missing}. Citations cannot be constructed. Refusing to serve."
                )

        self.integrity_ok = True
        log.info(f"  integrity OK: {n_vec} vectors == {n_meta} metadata rows, dim={self.index.d}")

    def count(self) -> int:
        return 0 if self.index is None else self.index.ntotal

    def add(self, vectors: np.ndarray, metadata: List[Dict]):
        if vectors.shape[0] != len(metadata):
            raise IndexIntegrityError(
                f"add() refused: {vectors.shape[0]} vectors vs {len(metadata)} metadata rows"
            )
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
        # Post-write check: the two files on disk must agree before we call it saved.
        if int(self.index.ntotal) != len(self.metadata):
            raise IndexIntegrityError(
                f"save() produced an inconsistent store: {self.index.ntotal} vectors "
                f"vs {len(self.metadata)} metadata rows in {self.index_dir}"
            )

    # ───────────────────────────────────────────
    def search(self, query_vec: np.ndarray, top_k: int = 6) -> List[Dict]:
        if not self.integrity_ok:
            raise IndexIntegrityError(
                "refusing to search: index integrity was never verified. "
                "call load_or_init() (which verifies) before searching."
            )
        if self.index is None or self.index.ntotal == 0:
            return []
        if query_vec.ndim == 1:
            query_vec = query_vec[None, :]
        if query_vec.dtype != np.float32:
            query_vec = query_vec.astype(np.float32)
        scores, idx = self.index.search(query_vec, min(top_k, self.index.ntotal))
        out = []
        for s, i in zip(scores[0], idx[0]):
            if i < 0:
                continue
            if i >= len(self.metadata):
                # Unreachable while the invariant holds; loud rather than silent.
                raise IndexIntegrityError(
                    f"FAISS returned id {i} but metadata has {len(self.metadata)} rows"
                )
            m = dict(self.metadata[i])
            m["score"] = float(s)            # IP on normalized vecs == cosine
            out.append(m)
        return out
