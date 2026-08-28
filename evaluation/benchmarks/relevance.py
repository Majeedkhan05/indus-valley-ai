"""
Proxy relevance judgments for the IVA-80 benchmark.

⚠ IMPORTANT — SCIENTIFIC STATUS ⚠
These are AUTOMATIC judgments, not human/expert relevance judgments.
They must never be described as "ground truth", "expert-verified", or "gold".
They are a reproducible stand-in that lets baseline comparison proceed while a
human annotation effort (docs/annotation-protocol.md) is carried out.

Methodology: TREC-style POOLING.
  1. Pool = union of top-P results from every system under comparison.
  2. Only pooled documents are judged (judging 1,506 chunks x 80 questions by
     hand is not feasible; judging the pool is standard IR practice).
  3. Two INDEPENDENT judges vote:
       Judge L (lexical)  — content-word coverage of the reference answer
       Judge S (semantic) — embedding cosine to the reference answer
  4. Agreement between the two judges is reported, so the reader can see how
     stable the proxy is. Primary metrics use the STRICT (both-agree) set.

Because recall is measured against the pool, it is "pooled recall" and is an
upper-bound-relative measure. This limitation is stated in every report.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Set

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from retrieval.lexical.bm25 import tokenize


@dataclass
class JudgeConfig:
    lexical_coverage: float = 0.60   # fraction of reference content words present
    semantic_cosine: float = 0.70    # cosine(reference_answer, chunk)


def judge_lexical(reference: str, chunk_text: str, thresh: float) -> bool:
    ref = set(tokenize(reference))
    if not ref:
        return False
    doc = set(tokenize(chunk_text))
    return len(ref & doc) / len(ref) >= thresh


def judge_semantic(cos: float, thresh: float) -> bool:
    return cos >= thresh


def agreement(a: Set[int], b: Set[int]) -> Dict[str, float]:
    """Jaccard + Cohen's kappa over the judged pool."""
    inter, union = len(a & b), len(a | b)
    jac = inter / union if union else float("nan")
    return {"jaccard": jac, "both": inter, "only_lexical": len(a - b), "only_semantic": len(b - a)}


def cohens_kappa(labels_a: List[int], labels_b: List[int]) -> float:
    n = len(labels_a)
    if n == 0:
        return float("nan")
    po = sum(1 for x, y in zip(labels_a, labels_b) if x == y) / n
    pa1, pb1 = sum(labels_a) / n, sum(labels_b) / n
    pe = pa1 * pb1 + (1 - pa1) * (1 - pb1)
    return (po - pe) / (1 - pe) if pe != 1 else float("nan")
