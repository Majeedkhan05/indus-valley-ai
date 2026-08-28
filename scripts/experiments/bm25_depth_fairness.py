"""
Red-team #7 follow-up: BM25 returns SHORT ranked lists.

BM25 only scores documents sharing at least one query term, so on some queries it
returns fewer than DEPTH candidates while dense always returns DEPTH. A shorter
list can only LOWER Recall@10. This biases the comparison AGAINST BM25 - i.e.
against the system that currently outranks our deployed dense retriever.

We quantify the effect three ways and report all of them:
  (a) how often it happens and how short
  (b) metrics restricted to queries where BM25 returned a FULL list (fair subset)
  (c) an upper bound: BM25 credited with recall it could not have achieved
"""
from __future__ import annotations
import json, os, pathlib, sys
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from evaluation.metrics.ir_metrics import recall_at_k, reciprocal_rank, ndcg_at_k

RAW = ROOT / "research" / "results" / "raw"
OUT = ROOT / "research" / "results" / "processed"
BENCH = ROOT / "research" / "benchmark" / "iva80_latest.json"
DEPTH = 10
rng = np.random.default_rng(42)

qs = json.load(BENCH.open())["questions"]
runs = {s: json.loads((RAW / f"{s}_run.json").read_text())
        for s in ("bm25", "dense", "hybrid_rrf")}
qrels = {int(k): {int(c): 1.0 for c in v} for k, v in
         json.loads((RAW / "qrels_used.json").read_text())["qrels"].items()}

lens = {int(q): len(runs["bm25"].get(str(q), [])) for q in [x["id"] for x in qs]}
short = {q: l for q, l in lens.items() if l < DEPTH}
judged = [q["id"] for q in qs if qrels.get(q["id"])]
short_judged = [q for q in judged if lens[q] < DEPTH]

print("=== (a) HOW OFTEN ===")
print(f"  queries where BM25 returned < {DEPTH}: {len(short)}/{len(lens)}")
print(f"  ... among JUDGED queries            : {len(short_judged)}/{len(judged)}")
print(f"  list lengths observed               : {sorted(set(lens.values()))}")
print(f"  mean length                         : {np.mean(list(lens.values())):.2f}")

def metrics(qids, run):
    r5, r10, mr, nd = [], [], [], []
    for q in qids:
        rel = qrels.get(q, {})
        if not rel: continue
        rl = run.get(str(q), [])
        r5.append(recall_at_k(rl, rel, 5)); r10.append(recall_at_k(rl, rel, 10))
        mr.append(reciprocal_rank(rl, rel)); nd.append(ndcg_at_k(rl, rel, 10))
    return {"recall@5": float(np.nanmean(r5)), "recall@10": float(np.nanmean(r10)),
            "mrr": float(np.nanmean(mr)), "ndcg@10": float(np.nanmean(nd)), "n": len(r5)}

full = [q for q in judged if lens[q] == DEPTH]
print("\n=== (b) FAIR SUBSET - queries where BM25 returned a full list ===")
print(f"{'system':<12}{'n':>4}{'R@5':>9}{'R@10':>9}{'MRR':>9}{'nDCG@10':>10}")
fair_res = {}
for s in runs:
    m = metrics(full, runs[s]); fair_res[s] = m
    print(f"{s:<12}{m['n']:>4}{m['recall@5']:>9.3f}{m['recall@10']:>9.3f}"
          f"{m['mrr']:>9.3f}{m['ndcg@10']:>10.3f}")
all_res = {s: metrics(judged, runs[s]) for s in runs}
print("\n  all judged queries (for comparison):")
for s in runs:
    m = all_res[s]
    print(f"{s:<12}{m['n']:>4}{m['recall@5']:>9.3f}{m['recall@10']:>9.3f}"
          f"{m['mrr']:>9.3f}{m['ndcg@10']:>10.3f}")

# (c) upper bound: give BM25 perfect recall on the slots it never filled
ub = []
for q in judged:
    rel = qrels.get(q, {})
    rl = runs["bm25"].get(str(q), [])
    got = recall_at_k(rl, rel, 10)
    missing_slots = max(0, DEPTH - len(rl))
    unfound = [c for c in rel if c not in rl]
    bonus = min(missing_slots, len(unfound)) / max(len(rel), 1)
    ub.append(min(1.0, got + bonus))
print("\n=== (c) UPPER BOUND on BM25 Recall@10 if short lists were filled perfectly ===")
print(f"  observed  : {all_res['bm25']['recall@10']:.3f}")
print(f"  upper bnd : {float(np.nanmean(ub)):.3f}")
print(f"  dense     : {all_res['dense']['recall@10']:.3f}")

order_full = sorted(fair_res, key=lambda s: -fair_res[s]["recall@5"])
order_all = sorted(all_res, key=lambda s: -all_res[s]["recall@5"])
print(f"\n  ordering on fair subset : {' > '.join(order_full)}")
print(f"  ordering on all judged  : {' > '.join(order_all)}")
print(f"  ordering unchanged      : {order_full == order_all}")

res = {"issue": "BM25 returns fewer than DEPTH candidates when few documents share a "
                "query term; dense always returns DEPTH. Shorter lists can only lower "
                "Recall@10, biasing the comparison AGAINST BM25.",
       "direction_of_bias": "against BM25 - i.e. against the system that outranks our "
                            "deployed dense retriever, so it does not flatter our narrative",
       "frequency": {"queries_short": len(short), "of": len(lens),
                     "judged_short": len(short_judged), "of_judged": len(judged),
                     "lengths_observed": sorted(set(lens.values())),
                     "mean_length": float(np.mean(list(lens.values())))},
       "fair_subset_full_lists_only": {"n": len(full), "metrics": fair_res},
       "all_judged": all_res,
       "bm25_recall10_upper_bound": float(np.nanmean(ub)),
       "ordering_fair_subset": order_full, "ordering_all": order_all,
       "ordering_unchanged": order_full == order_all,
       "resolution": "Reported, not patched. Padding BM25 with zero-score documents would "
                     "invent an ordering it does not have. The honest statement is that "
                     "BM25 Recall@10 is a LOWER BOUND.",
       "seed": 42}
(OUT / "bm25_depth_fairness.json").write_text(json.dumps(res, indent=2))
print(f"\nwrote {(OUT/'bm25_depth_fairness.json').relative_to(ROOT)}")
