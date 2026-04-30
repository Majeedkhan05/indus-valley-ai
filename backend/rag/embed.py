"""
Sentence-transformers embedding wrapper.
========================================
Uses 'BAAI/bge-small-en-v1.5' by default — 384-dim, fast on CPU,
and benchmarks well on retrieval tasks. Override via env var
IVAI_EMBED_MODEL if you have a GPU (e.g. 'BAAI/bge-base-en-v1.5').
"""
from __future__ import annotations

import os
import logging
from typing import List

import numpy as np

log = logging.getLogger("ivai.embed")

DEFAULT_MODEL = os.environ.get("IVAI_EMBED_MODEL", "BAAI/bge-small-en-v1.5")


class EmbeddingModel:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        from sentence_transformers import SentenceTransformer
        log.info(f"Loading embedding model: {model_name}")
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()
        log.info(f"  dim = {self.dim}")

    def encode(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        if not texts:
            return np.zeros((0, self.dim), dtype=np.float32)
        vecs = self.model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=True,        # cosine via inner-product
            show_progress_bar=len(texts) > 200,
            convert_to_numpy=True,
        )
        return vecs.astype(np.float32)

    def encode_one(self, text: str) -> np.ndarray:
        return self.encode([text])[0]
