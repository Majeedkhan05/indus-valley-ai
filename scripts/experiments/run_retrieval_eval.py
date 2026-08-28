"""
PHASE 4 + 5 - Final retrieval evaluation with statistical validation.

Systems : bm25 | dense | hybrid_rrf   (+ legacy_dense for the Phase-6 comparison)
Metrics : Recall@{1,3,5,10}, MRR, nDCG@{5,10}, Precision@5
Stats   : bootstrap 95% CIs, PAIRED bootstrap significance vs dense, threshold sweep

Judgments: uses research/annotations/qrels_human.json IF IT EXISTS, otherwise the
automatic proxy judge (clearly labelled). Never fabricates labels.

Outputs (research/results/):
  raw/<system>_run.json          full ranked lists
  raw/qrels_<judge>.json         judgments actually used
  processed/metrics.json         all metrics + CIs + significance
  processed/per_question.json    per-question scores (for error analysis)
"""
from __future__ import annotations
import json, os, pathlib, platform, sys, time
from datetime import datetime, timezone
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np, faiss

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from retrieval.lexical.bm25 import BM25, tokenize
from evaluation.metrics.ir_metrics import recall_at_k, precision_at_k, reciprocal_rank, ndcg_at_k

SEED = 42
rng = np.random.default_rng(SEED)
IDX  = ROOT / "backend" / "data" / "index_v2"
LEG  = ROOT / "backend" / "data" / "index"
BENCH = ROOT / "research" / "benchmark" / "iva80_latest.json"
HUMAN = ROOT / "research" / "annotations" / "qrels_human.json"
RES  = ROOT / "research" / "results"
KS = (1, 3, 5, 10)
NDCG_KS = (5, 10)
DEPTH = 10
N_BOOT = 10000
SELECTIVITIES = (0.03, 0.05, 0.10, 0.20)
PRIMARY = 0.05


def load_index(d):
    rows = [json.loads(l) for l in (d / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
    idx = faiss.read_index(str(d / "faiss.index"))
    return rows, np.asarray(idx.reconstruct_n(0, idx.ntotal), dtype=np.float32)


def rrf(lists, k=60):
    s = {}
    for l in lists:
        for r, d in enumerate(l, 1): s[d] = s.get(d, 0.0) + 1.0 / (k + r)
    return [d for d, _ in sorted(s.items(), key=lambda kv: -kv[1])]


def boot_ci(v, alpha=0.05):
    v = np.asarray([x for x in v if not np.isnan(x)], float)
    if len(v) < 2: return [float("nan")] * 2
    idx = rng.integers(0, len(v), size=(N_BOOT, len(v)))
    mu = v[idx].mean(axis=1)
    return [float(np.percentile(mu, 100 * alpha / 2)), float(np.percentile(mu, 100 * (1 - alpha / 2)))]


def paired_boot(a, b):
    """Paired bootstrap: P(mean(a) > mean(b)) and CI of the difference."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = ~(np.isnan(a) | np.isnan(b)); a, b = a[ok], b[ok]
    if len(a) < 2: return {"diff": float("nan"), "ci95": [float("nan")] * 2, "p_two_sided": float("nan")}
    idx = rng.integers(0, len(a), size=(N_BOOT, len(a)))
    d = (a[idx] - b[idx]).mean(axis=1)
    p = 2 * min((d <= 0).mean(), (d >= 0).mean())
    return {"diff": float(a.mean() - b.mean()),
            "ci95": [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))],
            "p_two_sided": float(min(p, 1.0))}


def main():
    t0 = time.time()
    for sub in ("raw", "processed", "tables", "figures"):
        (RES / sub).mkdir(parents=True, exist_ok=True)

    chunks, V = load_index(IDX)
    texts = [c["text"] for c in chunks]
    leg_meta, LV = load_index(LEG)
    leg2cor = np.argmax(LV @ V.T, axis=1)          # legacy id -> true corrected chunk

    bench = json.load(BENCH.open())
    qs = bench["questions"]
    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer("BAAI/bge-small-en-v1.5")
    enc = lambda xs: m.encode(xs, normalize_embeddings=True, convert_to_numpy=True,
                              show_progress_bar=False).astype(np.float32)
    QV = enc([q["question"] for q in qs]); GV = enc([q["reference_answer"] for q in qs])
    bm25 = BM25([tokenize(t) for t in texts])

    runs = {"bm25": [], "dense": [], "hybrid_rrf": [], "legacy_dense": [],
            "legacy_dense_slotwaste": []}
    for i, q in enumerate(qs):
        bm = [d for d, _ in bm25.search(q["question"], top_k=DEPTH)]
        dn = np.argsort(-(V @ QV[i]))[:DEPTH].tolist()
        # BUG FIX (self-audit): mapping legacy ids to corrected chunks collapses
        # duplicates, which truncated 17/80 lists below DEPTH and biased legacy
        # recall@10 LOW - i.e. in favour of our own "the repair helped" narrative.
        # Two defensible variants are now reported:
        #   legacy_dense          - backfilled to DEPTH (isolates the MISALIGNMENT)
        #   legacy_dense_slotwaste- truncated (shows real duplicate slot waste)
        leg_order = np.argsort(-(LV @ QV[i]))
        lg_full, seen = [], set()
        for j in leg_order:
            c = int(leg2cor[j])
            if c not in seen:
                seen.add(c); lg_full.append(c)
            if len(lg_full) >= DEPTH:
                break
        lg = lg_full
        lg_waste = list(dict.fromkeys(int(leg2cor[j]) for j in leg_order[:DEPTH]))
        runs["bm25"].append(bm); runs["dense"].append(dn)
        runs["hybrid_rrf"].append(rrf([bm, dn])[:DEPTH]); runs["legacy_dense"].append(lg)
        runs["legacy_dense_slotwaste"].append(lg_waste)

    # ---------- judgments -------------------------------------------------
    if HUMAN.exists():
        hq = json.load(HUMAN.open())
        judge_kind = "HUMAN (adjudicated)"
        def qrels_at(_sel):
            return {int(k): {int(c): float(g) for c, g in v.items() if g > 0}
                    for k, v in hq.items()}, float("nan")
        sels = (PRIMARY,)
    else:
        judge_kind = "AUTOMATIC PROXY (no human labels exist)"
        pools, lex, sem = [], [], []
        for i in range(len(qs)):
            pool = sorted(set().union(*[set(runs[s][i]) for s in runs]))
            ref = set(tokenize(qs[i]["reference_answer"]))
            cos = V[pool] @ GV[i]
            for j, d in enumerate(pool):
                lex.append(len(ref & set(tokenize(texts[d]))) / len(ref) if ref else 0.0)
                sem.append(float(cos[j]))
            pools.append(pool)
        lex, sem = np.array(lex), np.array(sem)
        flat = [(i, d) for i, p in enumerate(pools) for d in p]
        def qrels_at(sel):
            la = (lex >= np.quantile(lex, 1 - sel)).astype(int)
            sa = (sem >= np.quantile(sem, 1 - sel)).astype(int)
            qr = {}
            for n, (i, d) in enumerate(flat):
                qr.setdefault(qs[i]["id"], {})
                if la[n] or sa[n]: qr[qs[i]["id"]][d] = 1.0
            po = (la == sa).mean()
            pe = la.mean() * sa.mean() + (1 - la.mean()) * (1 - sa.mean())
            return qr, float((po - pe) / (1 - pe))
        sels = SELECTIVITIES

    def per_question(qr):
        out = {}
        for s, rl in runs.items():
            rows = []
            for i, q in enumerate(qs):
                rel = qr.get(q["id"], {})
                if not rel: continue
                r = {"qid": q["id"], "category": q["category"], "flags": q["flags"],
                     "retrieval_types": q["retrieval_types"], "mrr": reciprocal_rank(rl[i], rel)}
                for k in KS: r[f"recall@{k}"] = recall_at_k(rl[i], rel, k)
                for k in NDCG_KS: r[f"ndcg@{k}"] = ndcg_at_k(rl[i], rel, k)
                r["precision@5"] = precision_at_k(rl[i], rel, 5)
                rows.append(r)
            out[s] = rows
        return out

    metric_names = [f"recall@{k}" for k in KS] + ["mrr"] + [f"ndcg@{k}" for k in NDCG_KS] + ["precision@5"]
    sweep, primary_pq, primary_qr = {}, None, None
    for sel in sels:
        qr, kap = qrels_at(sel)
        pq = per_question(qr)
        block = {"judge_kappa": kap,
                 "n_questions_with_relevant": sum(1 for v in qr.values() if v),
                 "systems": {}}
        for s in runs:
            block["systems"][s] = {mn: {"mean": float(np.nanmean([r[mn] for r in pq[s]])),
                                        "ci95": boot_ci([r[mn] for r in pq[s]]),
                                        "n": len(pq[s])} for mn in metric_names}
        # paired significance vs dense
        block["paired_vs_dense"] = {
            s: {mn: paired_boot([r[mn] for r in pq[s]], [r[mn] for r in pq["dense"]])
                for mn in metric_names}
            for s in runs if s != "dense"}
        sweep[f"{sel:.2f}"] = block
        if abs(sel - PRIMARY) < 1e-9 or len(sels) == 1:
            primary_pq, primary_qr = pq, qr

    rank_orders = {k: sorted([s for s in runs if s != "legacy_dense"],
                             key=lambda s: -v["systems"][s]["recall@5"]["mean"])
                   for k, v in sweep.items()}
    stable = len(set(tuple(v) for v in rank_orders.values())) == 1

    for s in runs:
        (RES / "raw" / f"{s}_run.json").write_text(json.dumps(
            {qs[i]["id"]: runs[s][i] for i in range(len(qs))}, indent=2))
    (RES / "raw" / "qrels_used.json").write_text(json.dumps(
        {"judge": judge_kind, "primary_selectivity": PRIMARY,
         "qrels": {str(k): {str(c): g for c, g in v.items()} for k, v in primary_qr.items()}}, indent=2))
    (RES / "processed" / "per_question.json").write_text(json.dumps(primary_pq, indent=2))
    (RES / "processed" / "metrics.json").write_text(json.dumps({
        "judge": judge_kind, "primary_selectivity": PRIMARY, "depth": DEPTH,
        "bootstrap_resamples": N_BOOT, "seed": SEED,
        "benchmark": {"name": bench["benchmark"], "version": bench["version"],
                      "questions": bench["n_questions"]},
        "corpus": bench["corpus"],
        "sweep": sweep, "ranking_by_selectivity": rank_orders,
        "ranking_stable": stable,
        "environment": {"python": platform.python_version(), "platform": platform.platform(),
                        "numpy": np.__version__, "faiss": faiss.__version__},
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }, indent=2))

    p = sweep[f"{PRIMARY:.2f}"]
    print(f"judge: {judge_kind}   kappa={p['judge_kappa']:.3f}   "
          f"n={p['systems']['dense']['recall@5']['n']}")
    cols = ["recall@1", "recall@5", "recall@10", "mrr", "ndcg@10"]
    print(f"\n{'system':<14}" + "".join(f"{c:>22}" for c in cols))
    for s in ("bm25", "dense", "hybrid_rrf", "legacy_dense", "legacy_dense_slotwaste"):
        cells = []
        for mn in cols:
            e = p["systems"][s][mn]
            cells.append(f"{e['mean']:.3f} [{e['ci95'][0]:.2f},{e['ci95'][1]:.2f}]".rjust(22))
        print(f"{s:<14}" + "".join(cells))
    print("\npaired bootstrap vs dense (recall@5 and mrr):")
    for s, d in p["paired_vs_dense"].items():
        for mn in ("recall@5", "mrr"):
            x = d[mn]
            sig = "SIGNIFICANT" if x["p_two_sided"] < 0.05 else "not significant"
            print(f"  {s:<13} {mn:<9} diff={x['diff']:+.3f} "
                  f"CI[{x['ci95'][0]:+.3f},{x['ci95'][1]:+.3f}] p={x['p_two_sided']:.3f}  {sig}")
    print(f"\nranking stable across thresholds: {stable}")
    for k, v in rank_orders.items(): print(f"  sel={k}: {' > '.join(v)}")
    print(f"\nwrote research/results/  ({time.time()-t0:.1f}s)")


if __name__ == "__main__":
    main()
