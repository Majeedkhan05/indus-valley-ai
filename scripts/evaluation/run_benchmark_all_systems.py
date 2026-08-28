"""
E003 - Retrieval evaluation across ALL systems, with confidence intervals.

Systems (each written to its OWN result file, per directive S7):
  legacy_vector    the deployed dense retriever on the MISALIGNED legacy index
  corrected_vector the same retriever on the validated index_v2
  bm25             lexical baseline
  hybrid_rrf       reciprocal-rank fusion of bm25 + corrected_vector

Legacy hits are mapped into the corrected id space by vector identity, so all
systems are judged against the same relevance labels. That isolates RETRIEVAL
quality; CITATION correctness is measured separately in E002.

Judgments are automatic proxies (see evaluation/benchmarks/relevance.py).
Confidence intervals are non-parametric bootstrap over questions (10k resamples).

Usage: backend/venv/bin/python scripts/evaluation/run_benchmark_all_systems.py
"""
from __future__ import annotations
import json, os, pathlib, platform, sys, time
from datetime import datetime, timezone
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np, faiss

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from retrieval.lexical.bm25 import BM25, tokenize
from evaluation.metrics.ir_metrics import (
    recall_at_k, precision_at_k, reciprocal_rank, ndcg_at_k)
from evaluation.benchmarks.relevance import cohens_kappa

SEED = 42
rng = np.random.default_rng(SEED)
LEG = ROOT / "backend" / "data" / "index"
COR = ROOT / "backend" / "data" / "index_v2"
BENCH = ROOT / "paper" / "eval" / "benchmark_questions.json"
OUT = ROOT / "experiments" / "results"
POOL_DEPTH, KS, N_BOOT = 20, (1, 5, 10), 10000
SELECTIVITIES = (0.03, 0.05, 0.10, 0.20)
PRIMARY = 0.05


def load(d):
    rows = [json.loads(l) for l in (d / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
    idx = faiss.read_index(str(d / "faiss.index"))
    return rows, np.asarray(idx.reconstruct_n(0, idx.ntotal), dtype=np.float32)


def boot_ci(vals, n_boot=N_BOOT, alpha=0.05):
    v = np.asarray([x for x in vals if not np.isnan(x)], float)
    if len(v) < 2:
        return (float("nan"), float("nan"))
    idx = rng.integers(0, len(v), size=(n_boot, len(v)))
    means = v[idx].mean(axis=1)
    return (float(np.percentile(means, 100 * alpha / 2)),
            float(np.percentile(means, 100 * (1 - alpha / 2))))


def main():
    t0 = time.time()
    leg_meta, LV = load(LEG)
    cor_meta, CV = load(COR)
    texts = [c["text"] for c in cor_meta]
    questions = json.load(BENCH.open())["questions"]

    # legacy vector id -> corrected chunk id (by vector identity)
    leg2cor = np.argmax(LV @ CV.T, axis=1)

    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer("BAAI/bge-small-en-v1.5")
    enc = lambda xs: m.encode(xs, normalize_embeddings=True, convert_to_numpy=True,
                              show_progress_bar=False).astype(np.float32)
    QV = enc([q["q"] for q in questions])
    GT = enc([q["ground_truth"] for q in questions])
    bm25 = BM25([tokenize(t) for t in texts])

    def rrf(ls, k=60):
        s = {}
        for l in ls:
            for r, d in enumerate(l, 1):
                s[d] = s.get(d, 0.0) + 1.0 / (k + r)
        return [d for d, _ in sorted(s.items(), key=lambda kv: -kv[1])]

    runs = {"legacy_vector": [], "corrected_vector": [], "bm25": [], "hybrid_rrf": []}
    for i in range(len(questions)):
        lg = [int(leg2cor[j]) for j in np.argsort(-(LV @ QV[i]))[:POOL_DEPTH]]
        cv = np.argsort(-(CV @ QV[i]))[:POOL_DEPTH].tolist()
        bm = [d for d, _ in bm25.search(questions[i]["q"], top_k=POOL_DEPTH)]
        runs["legacy_vector"].append(list(dict.fromkeys(lg)))
        runs["corrected_vector"].append(cv)
        runs["bm25"].append(bm)
        runs["hybrid_rrf"].append(rrf([bm, cv])[:POOL_DEPTH])

    # pooled proxy judgments, quantile-calibrated
    pools, lex, sem = [], [], []
    for i in range(len(questions)):
        pool = sorted(set().union(*[set(runs[s][i]) for s in runs]))
        ref = set(tokenize(questions[i]["ground_truth"]))
        cos = CV[pool] @ GT[i]
        for j, d in enumerate(pool):
            lex.append(len(ref & set(tokenize(texts[d]))) / len(ref) if ref else 0.0)
            sem.append(float(cos[j]))
        pools.append(pool)
    lex, sem = np.array(lex), np.array(sem)
    flat = [(i, d) for i, p in enumerate(pools) for d in p]

    def qrels_at(sel):
        la = (lex >= np.quantile(lex, 1 - sel)).astype(int)
        sa = (sem >= np.quantile(sem, 1 - sel)).astype(int)
        q = {}
        for n, (i, d) in enumerate(flat):
            q.setdefault(questions[i]["id"], [])
            if la[n] or sa[n]:
                q[questions[i]["id"]].append(d)
        return q, cohens_kappa(la.tolist(), sa.tolist())

    print(f"pooled pairs judged: {len(lex)}")
    sweep = {}
    for sel in SELECTIVITIES:
        qr, kap = qrels_at(sel)
        row = {}
        for s, rl in runs.items():
            per = {f"recall@{k}": [] for k in KS}
            per.update({f"ndcg@{k}": [] for k in KS}); per["mrr"] = []
            per["precision@5"] = []
            for i, q in enumerate(questions):
                rel = {d: 1.0 for d in qr.get(q["id"], [])}
                if not rel:
                    continue
                for k in KS:
                    per[f"recall@{k}"].append(recall_at_k(rl[i], rel, k))
                    per[f"ndcg@{k}"].append(ndcg_at_k(rl[i], rel, k))
                per["precision@5"].append(precision_at_k(rl[i], rel, 5))
                per["mrr"].append(reciprocal_rank(rl[i], rel))
            row[s] = {mm: {"mean": float(np.nanmean(v)),
                           "ci95": boot_ci(v), "n": int(len(v))}
                      for mm, v in per.items()}
        sweep[f"{sel:.2f}"] = {"cohens_kappa": kap, "systems": row}

    p = sweep[f"{PRIMARY:.2f}"]["systems"]
    n = p["bm25"]["recall@5"]["n"]
    print(f"\n=== PRIMARY (selectivity={PRIMARY}, kappa={sweep[f'{PRIMARY:.2f}']['cohens_kappa']:.3f}, n={n}) ===")
    print(f"{'system':<18}{'R@1':>16}{'R@5':>16}{'R@10':>16}{'MRR':>16}{'nDCG@10':>16}")
    for s in runs:
        f = lambda k: f"{p[s][k]['mean']:.3f}[{p[s][k]['ci95'][0]:.2f},{p[s][k]['ci95'][1]:.2f}]"
        print(f"{s:<18}{f('recall@1'):>16}{f('recall@5'):>16}{f('recall@10'):>16}"
              f"{f('mrr'):>16}{f('ndcg@10'):>16}")

    env = {"python": platform.python_version(), "platform": platform.platform(),
           "numpy": np.__version__, "faiss": faiss.__version__}
    for s in runs:
        d = OUT / f"E003_{s}"; d.mkdir(parents=True, exist_ok=True)
        (d / "config.json").write_text(json.dumps({
            "experiment_id": f"E003_{s}", "system": s,
            "index": "legacy (MISALIGNED, ids mapped to true content)" if s == "legacy_vector"
                     else "index_v2 (validated)",
            "corpus_chunks": len(cor_meta), "questions": len(questions),
            "embedder": "BAAI/bge-small-en-v1.5", "pool_depth": POOL_DEPTH,
            "judgments": "AUTOMATIC PROXY - quantile-calibrated dual judge. NOT human, NOT expert.",
            "bootstrap_resamples": N_BOOT, "seed": SEED, "environment": env,
            "timestamp": datetime.now(timezone.utc).isoformat()}, indent=2))
        (d / "metrics.json").write_text(json.dumps({
            "primary_selectivity": PRIMARY,
            "primary": p[s],
            "sweep": {k: v["systems"][s] for k, v in sweep.items()},
            "kappa_by_selectivity": {k: v["cohens_kappa"] for k, v in sweep.items()}}, indent=2))
        (d / "predictions.json").write_text(json.dumps(
            {questions[i]["id"]: runs[s][i] for i in range(len(questions))}, indent=2))

    (OUT / "E003_comparison.json").write_text(json.dumps(
        {"primary_selectivity": PRIMARY, "sweep": sweep,
         "note": "legacy_vector is judged on the TRUE content its vectors encode; "
                 "its citation failure is quantified separately in E002."}, indent=2))
    print(f"\nwrote {len(runs)} per-system result dirs + E003_comparison.json  ({time.time()-t0:.1f}s)")


if __name__ == "__main__":
    main()
