"""
SELF-AUDIT: verify the IR metric implementations against HAND-COMPUTED values.

Every downstream number depends on these five functions. If they are wrong, the
entire results section is wrong. Each case below is computed by hand in the
docstring so a reviewer can check the expected value without running code.
"""
from __future__ import annotations
import math, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from evaluation.metrics.ir_metrics import (
    recall_at_k, precision_at_k, reciprocal_rank, ndcg_at_k, hit_at_k)

FAIL = []
def check(name, got, want, tol=1e-9):
    ok = (math.isnan(got) and math.isnan(want)) or abs(got - want) <= tol
    print(f"  {'PASS' if ok else 'FAIL'}  {name}: got {got:.6f} want {want:.6f}")
    if not ok: FAIL.append(name)

print("recall@k")
# ranked [a,b,c,d,e]; relevant {a,c,x}. 3 relevant total.
r, rel = [1,2,3,4,5], {1:1.0, 3:1.0, 99:1.0}
check("recall@1 = 1/3", recall_at_k(r, rel, 1), 1/3)
check("recall@3 = 2/3", recall_at_k(r, rel, 3), 2/3)
check("recall@5 = 2/3 (99 unretrievable)", recall_at_k(r, rel, 5), 2/3)
check("recall with empty rel = nan", recall_at_k(r, {}, 5), float("nan"))

print("precision@k")
check("p@1 = 1/1", precision_at_k(r, rel, 1), 1.0)
check("p@3 = 2/3", precision_at_k(r, rel, 3), 2/3)
check("p@5 = 2/5", precision_at_k(r, rel, 5), 2/5)

print("reciprocal rank")
check("first relevant at rank 1 -> 1.0", reciprocal_rank([1,2,3], {1:1.0}), 1.0)
check("first relevant at rank 3 -> 1/3", reciprocal_rank([7,8,1], {1:1.0}), 1/3)
check("no relevant -> 0.0", reciprocal_rank([7,8,9], {1:1.0}), 0.0)

print("nDCG@k  (binary gains)")
# ranked [1,2,3]; rel {1,3}. DCG = 1/log2(2) + 0 + 1/log2(4) = 1 + 0.5 = 1.5
# ideal   = 1/log2(2) + 1/log2(3)               = 1 + 0.63093 = 1.63093
check("ndcg@3 = 1.5/1.63093", ndcg_at_k([1,2,3], {1:1.0,3:1.0}, 3),
      1.5 / (1 + 1/math.log2(3)), 1e-9)
check("perfect ranking -> 1.0", ndcg_at_k([1,2], {1:1.0,2:1.0}, 2), 1.0)
check("no relevant -> nan", ndcg_at_k([1,2], {}, 2), float("nan"))

print("nDCG@k  (graded gains)")
# ranked [1,2]; gains {1:1, 2:2}. DCG = 1/1 + 2/log2(3) = 1 + 1.26186 = 2.26186
# ideal (2 then 1)                  = 2/1 + 1/log2(3) = 2 + 0.63093 = 2.63093
check("graded ndcg@2", ndcg_at_k([1,2], {1:1.0,2:2.0}, 2),
      (1 + 2/math.log2(3)) / (2 + 1/math.log2(3)), 1e-9)

print("hit@k")
check("hit@1 true", hit_at_k([1,2], {1:1.0}, 1), 1.0)
check("hit@1 false", hit_at_k([9,1], {1:1.0}, 1), 0.0)

print("\nedge cases")
check("empty ranking, recall", recall_at_k([], {1:1.0}, 5), 0.0)
check("empty ranking, mrr", reciprocal_rank([], {1:1.0}), 0.0)
check("k larger than ranking", recall_at_k([1], {1:1.0}, 100), 1.0)

print(f"\n{'ALL METRIC TESTS PASSED' if not FAIL else 'FAILURES: ' + ', '.join(FAIL)}")
sys.exit(1 if FAIL else 0)
