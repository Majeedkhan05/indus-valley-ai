"""
E001 - Retrieval baseline comparison on IVA-80 (retrieval only, no LLM).

Systems:
  BM25           lexical baseline (in-repo Okapi BM25)
  VECTOR         the deployed retriever: bge-small-en-v1.5 + FAISS IndexFlatIP
  VECTOR+PREFIX  same, with the BGE query-instruction prefix
  HYBRID_RRF     reciprocal-rank fusion of BM25 + VECTOR

RELEVANCE JUDGMENTS: automatic proxy, TREC-style pooling. NOT human, NOT expert,
NOT "ground truth". Two independent judges (lexical coverage / semantic cosine)
are QUANTILE-CALIBRATED to identical selectivity so their agreement is
interpretable, and the operating point is swept to test whether the ranking of
systems is stable rather than an artifact of one threshold.

Usage: IVAI_INDEX=index_v2 backend/venv/bin/python scripts/evaluation/run_retrieval_experiments.py
"""
from __future__ import annotations
import json, os, platform, sys, time, pathlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import numpy as np, faiss

from retrieval.lexical.bm25 import BM25, tokenize
from evaluation.metrics.ir_metrics import (
    recall_at_k, precision_at_k, reciprocal_rank, ndcg_at_k, hit_at_k)
from evaluation.benchmarks.relevance import cohens_kappa

SEED = 42
np.random.seed(SEED)
INDEX_NAME = os.environ.get("IVAI_INDEX", "index_v2")
INDEX_DIR  = ROOT / "backend" / "data" / INDEX_NAME
BENCH      = ROOT / "paper" / "eval" / "benchmark_questions.json"
OUT        = ROOT / "experiments" / "results"
POOL_DEPTH = 20
KS = (1, 3, 5, 10)
SELECTIVITIES = (0.03, 0.05, 0.10, 0.20)   # fraction of pooled pairs judged relevant
PRIMARY_SEL = 0.05
BGE_PREFIX = "Represent this sentence for searching relevant passages: "


def rrf(rank_lists, k=60):
    s = {}
    for lst in rank_lists:
        for r, d in enumerate(lst, 1):
            s[d] = s.get(d, 0.0) + 1.0 / (k + r)
    return [d for d, _ in sorted(s.items(), key=lambda kv: -kv[1])]


def main():
    t0 = time.time()
    chunks = [json.loads(l) for l in (INDEX_DIR / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
    index = faiss.read_index(str(INDEX_DIR / "faiss.index"))
    assert index.ntotal == len(chunks), (
        f"index/metadata mismatch: {index.ntotal} vs {len(chunks)} - see "
        "docs/bug-index-metadata-misalignment.md")
    cvecs = np.asarray(index.reconstruct_n(0, index.ntotal), dtype=np.float32)
    texts = [c["text"] for c in chunks]
    questions = json.load(BENCH.open())["questions"]
    print(f"index={INDEX_NAME}  corpus={len(chunks)}  questions={len(questions)}")

    bm25 = BM25([tokenize(t) for t in texts])
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    qs  = [q["q"] for q in questions]
    gts = [q["ground_truth"] for q in questions]
    enc = lambda xs: model.encode(xs, normalize_embeddings=True, convert_to_numpy=True,
                                  show_progress_bar=False).astype(np.float32)
    qv, qvp, gtv = enc(qs), enc([BGE_PREFIX + q for q in qs]), enc(gts)

    runs = {"BM25": [], "VECTOR": [], "VECTOR+PREFIX": [], "HYBRID_RRF": []}
    for i in range(len(questions)):
        bm = [d for d, _ in bm25.search(qs[i], top_k=POOL_DEPTH)]
        vs = np.argsort(-(cvecs @ qv[i]))[:POOL_DEPTH].tolist()
        vp = np.argsort(-(cvecs @ qvp[i]))[:POOL_DEPTH].tolist()
        runs["BM25"].append(bm); runs["VECTOR"].append(vs)
        runs["VECTOR+PREFIX"].append(vp); runs["HYBRID_RRF"].append(rrf([bm, vs])[:POOL_DEPTH])

    # ---- pooled pairs + raw judge scores ---------------------------------
    pools, lex_s, sem_s = [], [], []
    for i, q in enumerate(questions):
        pool = sorted(set().union(*[set(runs[s][i]) for s in runs]))
        ref = set(tokenize(gts[i]))
        cos = cvecs[pool] @ gtv[i]
        for j, d in enumerate(pool):
            doc = set(tokenize(texts[d]))
            lex_s.append(len(ref & doc) / len(ref) if ref else 0.0)
            sem_s.append(float(cos[j]))
        pools.append(pool)
    lex_s, sem_s = np.array(lex_s), np.array(sem_s)
    print(f"pooled (question,chunk) pairs judged: {len(lex_s)}")

    flat = [(i, d) for i, p in enumerate(pools) for d in p]

    def build_qrels(sel: float):
        """Quantile-calibrate BOTH judges to the same selectivity `sel`."""
        lt, st = np.quantile(lex_s, 1 - sel), np.quantile(sem_s, 1 - sel)
        la = (lex_s >= lt).astype(int); sa = (sem_s >= st).astype(int)
        strict, lenient = {}, {}
        for n, (i, d) in enumerate(flat):
            qid = questions[i]["id"]
            strict.setdefault(qid, []); lenient.setdefault(qid, [])
            if la[n] and sa[n]: strict[qid].append(d)
            if la[n] or sa[n]:  lenient[qid].append(d)
        return strict, lenient, cohens_kappa(la.tolist(), sa.tolist()), float(lt), float(st)

    def evaluate(qrel):
        per = {}
        for sysname, rl in runs.items():
            acc = {f"{m}@{k}": [] for k in KS for m in ("recall", "precision", "ndcg", "hit")}
            acc["mrr"] = []; n = 0
            for i, q in enumerate(questions):
                rel = {d: 1.0 for d in qrel.get(q["id"], [])}
                if not rel: continue
                n += 1
                for k in KS:
                    acc[f"recall@{k}"].append(recall_at_k(rl[i], rel, k))
                    acc[f"precision@{k}"].append(precision_at_k(rl[i], rel, k))
                    acc[f"ndcg@{k}"].append(ndcg_at_k(rl[i], rel, k))
                    acc[f"hit@{k}"].append(hit_at_k(rl[i], rel, k))
                acc["mrr"].append(reciprocal_rank(rl[i], rel))
            per[sysname] = {m: float(np.nanmean(v)) for m, v in acc.items()}
            per[sysname]["n_questions_evaluated"] = n
        return per

    sweep, primary_qrels = {}, None
    print(f"\n{'sel':>5} {'kappa':>6} {'nQ':>4} | " + " ".join(f"{s:>13}" for s in runs) + "   (Recall@5, lenient)")
    for sel in SELECTIVITIES:
        strict, lenient, kap, lt, st = build_qrels(sel)
        ev_s, ev_l = evaluate(strict), evaluate(lenient)
        sweep[f"{sel:.2f}"] = {
            "thresholds": {"lexical_coverage": lt, "semantic_cosine": st},
            "cohens_kappa": kap,
            "questions_with_relevant": {"strict": sum(1 for v in strict.values() if v),
                                        "lenient": sum(1 for v in lenient.values() if v)},
            "strict": ev_s, "lenient": ev_l,
        }
        nq = ev_l["BM25"]["n_questions_evaluated"]
        print(f"{sel:5.2f} {kap:6.3f} {nq:4d} | " +
              " ".join(f"{ev_l[s]['recall@5']:13.3f}" for s in runs))
        if abs(sel - PRIMARY_SEL) < 1e-9:
            primary_qrels = {"strict": strict, "lenient": lenient}

    # ranking stability across the sweep (lenient, Recall@5)
    orders = [tuple(sorted(runs, key=lambda s: -sweep[f'{sel:.2f}']["lenient"][s]["recall@5"]))
              for sel in SELECTIVITIES]
    stable = len(set(orders)) == 1
    print(f"\nsystem ranking stable across all operating points: {stable}")
    for sel, o in zip(SELECTIVITIES, orders):
        print(f"  sel={sel:.2f}: {' > '.join(o)}")

    exp_id = f"E001_retrieval_baselines_{INDEX_NAME}"
    d = OUT / exp_id; d.mkdir(parents=True, exist_ok=True)
    (d / "config.json").write_text(json.dumps({
        "experiment_id": exp_id,
        "research_question": "RQ1 - do lexical and hybrid retrieval outperform the deployed "
                             "dense retriever on IVA-80?",
        "index_dir": INDEX_NAME, "corpus_chunks": len(chunks), "questions": len(questions),
        "embedder": "BAAI/bge-small-en-v1.5", "systems": list(runs),
        "pool_depth": POOL_DEPTH, "selectivity_sweep": list(SELECTIVITIES),
        "judgments": "AUTOMATIC PROXY - quantile-calibrated dual judge. NOT human, NOT expert.",
        "seed": SEED,
        "environment": {"python": platform.python_version(), "platform": platform.platform(),
                        "numpy": np.__version__, "faiss": faiss.__version__},
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }, indent=2))
    (d / "metrics.json").write_text(json.dumps(
        {"sweep": sweep, "primary_selectivity": PRIMARY_SEL,
         "ranking_stable_across_sweep": stable,
         "rankings": {f"{s:.2f}": list(o) for s, o in zip(SELECTIVITIES, orders)}}, indent=2))
    (d / "predictions.json").write_text(json.dumps(
        {s: {questions[i]["id"]: runs[s][i] for i in range(len(questions))} for s in runs}, indent=2))
    (d / "qrels.json").write_text(json.dumps(
        {"selectivity": PRIMARY_SEL,
         "strict": {str(k): v for k, v in primary_qrels["strict"].items()},
         "lenient": {str(k): v for k, v in primary_qrels["lenient"].items()}}, indent=2))
    print(f"\nwrote {d}  ({time.time()-t0:.1f}s)")


if __name__ == "__main__":
    main()
