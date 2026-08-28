"""
Standard IR metrics. Binary relevance (graded optional for nDCG).

All functions take:
    ranked : list of doc ids in rank order (best first)
    rel    : dict {doc_id: gain}, gain > 0 means relevant
"""
from __future__ import annotations
import math
from typing import Dict, List


def recall_at_k(ranked: List[int], rel: Dict[int, float], k: int) -> float:
    total = sum(1 for g in rel.values() if g > 0)
    if total == 0:
        return float("nan")
    hit = sum(1 for d in ranked[:k] if rel.get(d, 0) > 0)
    return hit / total


def precision_at_k(ranked: List[int], rel: Dict[int, float], k: int) -> float:
    if k == 0:
        return float("nan")
    return sum(1 for d in ranked[:k] if rel.get(d, 0) > 0) / k


def reciprocal_rank(ranked: List[int], rel: Dict[int, float]) -> float:
    for i, d in enumerate(ranked, start=1):
        if rel.get(d, 0) > 0:
            return 1.0 / i
    return 0.0


def ndcg_at_k(ranked: List[int], rel: Dict[int, float], k: int) -> float:
    dcg = sum(
        (rel.get(d, 0.0)) / math.log2(i + 1)
        for i, d in enumerate(ranked[:k], start=1)
    )
    ideal = sorted((g for g in rel.values() if g > 0), reverse=True)[:k]
    idcg = sum(g / math.log2(i + 1) for i, g in enumerate(ideal, start=1))
    return dcg / idcg if idcg > 0 else float("nan")


def hit_at_k(ranked: List[int], rel: Dict[int, float], k: int) -> float:
    return 1.0 if any(rel.get(d, 0) > 0 for d in ranked[:k]) else 0.0
