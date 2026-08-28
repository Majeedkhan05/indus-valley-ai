"""
SELF-AUDIT / red-team #13: is our in-repo BM25 correct?

Cross-validates against `rank_bm25` (an independent implementation) on the real
corpus and the real benchmark queries. If our BM25 were wrong, every lexical and
hybrid result would be wrong.

Both are Okapi BM25 with k1=1.5, b=0.75 and the SAME tokenisation, so scores
should agree to floating-point tolerance and rankings should agree exactly.

Matched configuration: we instantiate our BM25 with idf_variant="robertson" so the
IDF formula is identical to rank_bm25's. Any remaining difference would be a real
bug in our scoring loop. (Production uses the "lucene" variant by default.)
"""
from __future__ import annotations
import json, pathlib, sys
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from retrieval.lexical.bm25 import BM25, tokenize

IDX = ROOT / "backend" / "data" / "index_v2"
BENCH = ROOT / "research" / "benchmark" / "iva80_latest.json"

chunks = [json.loads(l) for l in (IDX / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
toks = [tokenize(c["text"]) for c in chunks]
qs = json.load(BENCH.open())["questions"]

ours = BM25(toks, k1=1.5, b=0.75, idf_variant="robertson")
try:
    from rank_bm25 import BM25Okapi
except ImportError:
    print("rank_bm25 not installed - cannot cross-validate"); sys.exit(2)
theirs = BM25Okapi(toks, k1=1.5, b=0.75)

max_abs_diff, rank_mismatches, checked = 0.0, 0, 0
top10_jaccard = []
for q in qs:
    qt = tokenize(q["question"])
    if not qt: continue
    checked += 1
    ours_scores = np.zeros(len(toks))
    for d, s in ours.search(q["question"], top_k=len(toks)):
        ours_scores[d] = s
    theirs_scores = np.asarray(theirs.get_scores(qt), dtype=float)
    max_abs_diff = max(max_abs_diff, float(np.abs(ours_scores - theirs_scores).max()))
    a = set(np.argsort(-ours_scores)[:10].tolist())
    b = set(np.argsort(-theirs_scores)[:10].tolist())
    top10_jaccard.append(len(a & b) / len(a | b))
    if a != b: rank_mismatches += 1

print(f"queries cross-validated      : {checked}")
print(f"max |score difference|       : {max_abs_diff:.3e}")
print(f"mean top-10 Jaccard          : {np.mean(top10_jaccard):.4f}")
print(f"queries with differing top-10: {rank_mismatches}/{checked}")

TOL = 1e-6
ok = max_abs_diff < TOL and rank_mismatches == 0
print(f"\nBM25 CROSS-VALIDATION: {'PASS' if ok else 'FAIL'}"
      f"  (tolerance {TOL:.0e}, identical rankings required)")
sys.exit(0 if ok else 1)
