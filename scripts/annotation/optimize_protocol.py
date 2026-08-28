"""
Reduce the human annotation burden WITHOUT weakening the experimental design.

The 1,382 tasks are (question x pooled-candidate) pairs: the union of top-10 from
BM25, dense and hybrid over 80 questions. This script determines how much of that
is redundant for the metrics we actually report, and designs a stratified
minimum set.

Principle: a pair that every system ranks identically carries little information
for DISCRIMINATING systems. Pairs where systems disagree are worth more per unit
of human effort. But metrics still need coverage of each system's own top-k.

Nothing is discarded: the full candidate set is preserved. This only decides what
humans look at FIRST.
"""
from __future__ import annotations
import collections, json, os, pathlib, sys
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
ANN = ROOT / "research" / "annotations"
RES = ROOT / "research" / "results" / "raw"
BENCH = ROOT / "research" / "benchmark" / "iva80_latest.json"
IDX = ROOT / "backend" / "data" / "index_v2"
rng = np.random.default_rng(42)

tasks = [json.loads(l) for l in (ANN / "tasks.jsonl").open(encoding="utf-8") if l.strip()]
bench = {q["id"]: q for q in json.load(BENCH.open())["questions"]}
chunks = [json.loads(l) for l in (IDX / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
runs = {s: json.loads((RES / f"{s}_run.json").read_text())
        for s in ("bm25", "dense", "hybrid_rrf")}

# ---- structure analysis --------------------------------------------------
by_q = collections.defaultdict(list)
for t in tasks: by_q[t["qid"]].append(t)

def rank_of(sysname, qid, cid):
    lst = runs[sysname].get(str(qid), [])
    return lst.index(cid) + 1 if cid in lst else None

enriched = []
for t in tasks:
    ranks = {s: rank_of(s, t["qid"], t["chunk_id"]) for s in runs}
    present = [s for s, r in ranks.items() if r is not None]
    best = min([r for r in ranks.values() if r is not None], default=99)
    enriched.append({**t, "ranks": ranks, "n_systems": len(present), "best_rank": best})

n_all3 = sum(1 for e in enriched if e["n_systems"] == 3)
n_one = sum(1 for e in enriched if e["n_systems"] == 1)
top5 = [e for e in enriched if e["best_rank"] <= 5]
top10only = [e for e in enriched if e["best_rank"] > 5]

print("=== STRUCTURE OF THE 1,382 TASKS ===")
print(f"  total pairs                       : {len(enriched)}")
print(f"  questions                         : {len(by_q)}  (mean {len(enriched)/len(by_q):.1f} pairs/question)")
print(f"  retrieved by ALL 3 systems        : {n_all3} ({100*n_all3/len(enriched):.1f}%)")
print(f"  retrieved by exactly ONE system   : {n_one} ({100*n_one/len(enriched):.1f}%)")
print(f"  in some system's top-5            : {len(top5)} ({100*len(top5)/len(enriched):.1f}%)")
print(f"  only in ranks 6-10                : {len(top10only)} ({100*len(top10only)/len(enriched):.1f}%)")
print("\n  => the pairs are NOT redundant duplicates; they are genuine")
print("     (question, candidate) judgments. But they are NOT equally informative.")

# ---- tiering -------------------------------------------------------------
# Tier 1: any system's top-5  -> determines Recall@1/@5, MRR, nDCG@5 (headline metrics)
# Tier 2: ranks 6-10          -> only affects Recall@10 / nDCG@10
tier1 = top5
tier2 = top10only

# stratify tier 2 so every stratum stays represented
def strat_key(e):
    q = bench[e["qid"]]
    src = "tabular" if _numeric_rate(chunks[e["chunk_id"]]["text"]) >= 0.30 else "prose"
    flag = ("contested" if "contested_interpretation" in q["flags"]
            else "ambiguous" if "possibly_ambiguous" in q["flags"] else "plain")
    return (q["category"], flag, src, e["n_systems"])

def _numeric_rate(t):
    toks = t.lower().split()
    return sum(1 for w in toks if any(c.isdigit() for c in w)) / max(len(toks), 1)

strata = collections.defaultdict(list)
for e in tier2: strata[strat_key(e)].append(e)
SAMPLE_PER_STRATUM = 2
tier2_sample = []
for k, v in strata.items():
    idx = rng.permutation(len(v))[:min(SAMPLE_PER_STRATUM, len(v))]
    tier2_sample += [v[i] for i in idx]

minimum = tier1 + tier2_sample
hours = len(minimum) * 15 / 3600

print("\n=== OPTIMISED PROTOCOL ===")
print(f"  Tier 1 (any system top-5, MUST annotate) : {len(tier1)}")
print(f"  Tier 2 (ranks 6-10) total                : {len(tier2)}")
print(f"  Tier 2 stratified sample ({SAMPLE_PER_STRATUM}/stratum)    : {len(tier2_sample)} "
      f"across {len(strata)} strata")
print(f"  MINIMUM SET                              : {len(minimum)} "
      f"({100*len(minimum)/len(enriched):.0f}% of full pool)")
print(f"  effort per annotator                     : {hours:.1f} h  (was "
      f"{len(enriched)*15/3600:.1f} h)")
print(f"  two annotators                           : {2*hours:.1f} h total")

print("\n=== WHAT THIS COSTS SCIENTIFICALLY ===")
print("  FULLY preserved : Recall@1, Recall@5, MRR, nDCG@5, kappa, all system comparisons")
print("  DEGRADED        : Recall@10 and nDCG@10 become estimates on a stratified")
print("                    sample of ranks 6-10, with wider uncertainty")
print("  NOT AFFECTED    : the citation-integrity results (direct counts, no judging)")

cov = collections.Counter()
for e in minimum:
    for s, r in e["ranks"].items():
        if r is not None and r <= 5: cov[s] += 1
print("\n  top-5 coverage per system in the minimum set:")
for s in runs: print(f"    {s:<12} {cov[s]} pairs")

with (ANN / "tasks_minimum.jsonl").open("w", encoding="utf-8") as f:
    for e in minimum:
        rec = {k: v for k, v in e.items() if not k.startswith("_")}
        rec["tier"] = 1 if e in tier1 else 2
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

decision = {
    "question": "Must all 1,382 tasks be annotated before useful research continues?",
    "answer": "No. They are not redundant, but they are not equally informative.",
    "structure": {"total_pairs": len(enriched), "questions": len(by_q),
                  "retrieved_by_all_3": n_all3, "retrieved_by_one": n_one,
                  "in_some_top5": len(tier1), "ranks_6_to_10": len(tier2)},
    "protocol": {"tier1_all_top5": len(tier1),
                 "tier2_stratified_sample": len(tier2_sample),
                 "strata": len(strata), "per_stratum": SAMPLE_PER_STRATUM,
                 "minimum_set": len(minimum),
                 "reduction": 1 - len(minimum) / len(enriched),
                 "hours_per_annotator": round(hours, 1),
                 "annotators": 2},
    "stratification_axes": ["question category", "contested/ambiguous flag",
                            "source chunk type (prose/tabular)",
                            "number of systems retrieving the pair"],
    "preserved_metrics": ["Recall@1", "Recall@5", "MRR", "nDCG@5", "Cohen's kappa",
                          "all pairwise system comparisons"],
    "degraded_metrics": ["Recall@10", "nDCG@10 (estimated on stratified sample)"],
    "unaffected": ["citation correctness (direct count, no relevance judging)"],
    "rule": "The FULL machine-generated candidate set is preserved in tasks.jsonl. "
            "Unannotated machine judgments are NEVER converted into human ground truth.",
    "seed": 42,
}
(ANN / "protocol_decision.json").write_text(json.dumps(decision, indent=2))
print(f"\nwrote tasks_minimum.jsonl ({len(minimum)} tasks) + protocol_decision.json")
