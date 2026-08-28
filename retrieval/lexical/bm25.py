"""
BM25 Okapi — self-contained, no external dependency.

Implemented in-repo rather than via `rank_bm25` so the baseline is fully
reproducible with zero install step and the exact scoring formula is auditable.

Reference formula (Robertson & Zaragoza 2009), standard Okapi BM25:

    score(q,d) = sum_{t in q} IDF(t) * ( f(t,d)*(k1+1) ) / ( f(t,d) + k1*(1-b + b*|d|/avgdl) )
    IDF(t)     = ln( 1 + (N - n(t) + 0.5) / (n(t) + 0.5) )
"""
from __future__ import annotations
import math, re
from collections import Counter
from typing import List, Tuple

_TOKEN = re.compile(r"[a-z0-9]+")

# Minimal English stoplist. Kept small and explicit so it can be audited.
STOP = {
    "the","a","an","and","or","of","to","in","is","was","were","are","be","been","being",
    "for","on","at","by","with","as","that","this","these","those","it","its","from",
    "which","who","whom","what","when","where","how","why","not","no","but","if","then",
    "than","so","such","have","has","had","do","does","did","can","could","would","should",
    "may","might","must","will","shall","there","their","they","them","he","she","his","her",
    "we","our","you","your","i","also","into","about","over","under","between","during",
}

def tokenize(text: str, drop_stop: bool = True) -> List[str]:
    toks = _TOKEN.findall(text.lower())
    return [t for t in toks if not (drop_stop and t in STOP)]


class BM25:
    """
    idf_variant:
      "lucene"    log(1 + (N - n + 0.5)/(n + 0.5))    - default; always positive
      "robertson" log(N - n + 0.5) - log(n + 0.5)     - classic RSJ; can go negative,
                  so an epsilon floor (as in rank_bm25) is applied to negative values.

    Both are published Okapi BM25 variants. "lucene" is the default because it needs
    no epsilon hack. The "robertson" option exists so the implementation can be
    cross-validated against rank_bm25 exactly (tests/metrics/test_bm25_crossvalidation.py).
    """

    def __init__(self, corpus_tokens: List[List[str]], k1: float = 1.5, b: float = 0.75,
                 idf_variant: str = "lucene", epsilon: float = 0.25):
        self.k1, self.b = k1, b
        self.idf_variant, self.epsilon = idf_variant, epsilon
        self.docs = corpus_tokens
        self.N = len(corpus_tokens)
        self.doc_len = [len(d) for d in corpus_tokens]
        self.avgdl = sum(self.doc_len) / self.N if self.N else 0.0
        self.tf = [Counter(d) for d in corpus_tokens]

        df: Counter = Counter()
        for tfd in self.tf:
            df.update(tfd.keys())
        if idf_variant == "lucene":
            self.idf = {t: math.log(1 + (self.N - n + 0.5) / (n + 0.5)) for t, n in df.items()}
        elif idf_variant == "robertson":
            self.idf = {t: math.log(self.N - n + 0.5) - math.log(n + 0.5)
                        for t, n in df.items()}
            avg = sum(self.idf.values()) / len(self.idf) if self.idf else 0.0
            floor = self.epsilon * avg
            for t, v in list(self.idf.items()):
                if v < 0:
                    self.idf[t] = floor
        else:
            raise ValueError(f"unknown idf_variant: {idf_variant}")
        # inverted index: term -> [doc ids]
        self.inv: dict[str, list[int]] = {}
        for i, tfd in enumerate(self.tf):
            for t in tfd:
                self.inv.setdefault(t, []).append(i)

    def search(self, query: str, top_k: int = 10) -> List[Tuple[int, float]]:
        q = tokenize(query)
        scores: dict[int, float] = {}
        for t in q:
            if t not in self.inv:
                continue
            idf = self.idf[t]
            for i in self.inv[t]:
                f = self.tf[i][t]
                denom = f + self.k1 * (1 - self.b + self.b * self.doc_len[i] / self.avgdl)
                scores[i] = scores.get(i, 0.0) + idf * (f * (self.k1 + 1)) / denom
        ranked = sorted(scores.items(), key=lambda kv: -kv[1])[:top_k]
        return ranked
