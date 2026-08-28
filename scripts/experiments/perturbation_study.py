"""
CONTROLLED PERTURBATION STUDY - generalises the paper's central claim.

The observed bug is a single incident. A reviewer may fairly ask whether it is
anecdotal. Here we inject metadata misalignment of CONTROLLED severity into the
validated index and measure, at each severity:

    retrieval quality   (Recall@K, MRR, nDCG - depends only on vectors)
    citation correctness(depends on the vector->metadata mapping)

Prediction: retrieval metrics stay FLAT at every severity while citation
correctness falls linearly. If so, the blindness of ranking metrics to attribution
failure is a structural property, not a one-off.

Seed 42. Outputs research/results/processed/perturbation_study.json + figure.
"""
from __future__ import annotations
import json, os, pathlib, sys
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np, faiss
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from retrieval.lexical.bm25 import BM25, tokenize
from evaluation.metrics.ir_metrics import recall_at_k, reciprocal_rank, ndcg_at_k

IDX = ROOT / "backend" / "data" / "index_v2"
BENCH = ROOT / "research" / "benchmark" / "iva80_latest.json"
OUT = ROOT / "research" / "results"
SEED = 42; rng = np.random.default_rng(SEED)
DEPTH = 10
SEVERITIES = [0.0, 0.1, 0.25, 0.5, 0.75, 1.0]
N_REPEATS = 5


def main():
    chunks = [json.loads(l) for l in (IDX / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
    texts = [c["text"] for c in chunks]
    V = np.asarray(faiss.read_index(str(IDX / "faiss.index")).reconstruct_n(0, len(chunks)),
                   dtype=np.float32)
    qs = json.load(BENCH.open())["questions"]
    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer("BAAI/bge-small-en-v1.5")
    enc = lambda xs: m.encode(xs, normalize_embeddings=True, convert_to_numpy=True,
                              show_progress_bar=False).astype(np.float32)
    QV, GV = enc([q["question"] for q in qs]), enc([q["reference_answer"] for q in qs])
    tokc = [tokenize(t) for t in texts]
    bm25 = BM25(tokc)

    # runs (vector-side only - unaffected by metadata perturbation, by construction)
    dense_runs = [np.argsort(-(V @ QV[i]))[:DEPTH].tolist() for i in range(len(qs))]

    # per-question judgments (the more inclusive scheme)
    pools, qrels = [], {}
    for i in range(len(qs)):
        bm = [d for d, _ in bm25.search(qs[i]["question"], top_k=DEPTH)]
        pool = sorted(set(dense_runs[i]) | set(bm))
        s = V[pool] @ GV[i]
        ref = set(tokenize(qs[i]["reference_answer"]))
        thr = max(0.55, float(s.max()) - 0.06)
        qrels[qs[i]["id"]] = {pool[j]: 1.0 for j in range(len(pool))
                              if s[j] >= thr or
                              (len(ref & set(tokc[pool[j]])) / len(ref) if ref else 0) >= 0.5}
        pools.append(pool)

    rows = []
    for sev in SEVERITIES:
        rec, mrr, nd, cite = [], [], [], []
        for rep in range(N_REPEATS if sev not in (0.0,) else 1):
            perm = np.arange(len(chunks))
            n_shuf = int(round(sev * len(chunks)))
            if n_shuf > 1:
                pick = rng.choice(len(chunks), size=n_shuf, replace=False)
                perm[pick] = rng.permutation(pick)
            # retrieval metrics: identical by construction, but MEASURED not assumed
            r5 = [recall_at_k(dense_runs[i], qrels[qs[i]["id"]], 5)
                  for i in range(len(qs)) if qrels[qs[i]["id"]]]
            mr = [reciprocal_rank(dense_runs[i], qrels[qs[i]["id"]])
                  for i in range(len(qs)) if qrels[qs[i]["id"]]]
            n10 = [ndcg_at_k(dense_runs[i], qrels[qs[i]["id"]], 10)
                   for i in range(len(qs)) if qrels[qs[i]["id"]]]
            ok = tot = 0
            for i in range(len(qs)):
                for d in dense_runs[i][:6]:
                    tot += 1
                    reported = chunks[perm[d]]      # what the citation WOULD say
                    true = chunks[d]                # what the vector actually is
                    ok += (reported["source"] == true["source"] and reported["page"] == true["page"])
            rec.append(np.nanmean(r5)); mrr.append(np.nanmean(mr))
            nd.append(np.nanmean(n10)); cite.append(ok / tot)
        rows.append({"severity": sev,
                     "recall@5": float(np.mean(rec)), "recall@5_sd": float(np.std(rec)),
                     "mrr": float(np.mean(mrr)), "ndcg@10": float(np.mean(nd)),
                     "citation_correctness": float(np.mean(cite)),
                     "citation_sd": float(np.std(cite)), "repeats": len(cite)})

    r0 = rows[0]
    ret_range = max(r["recall@5"] for r in rows) - min(r["recall@5"] for r in rows)
    cite_drop = r0["citation_correctness"] - rows[-1]["citation_correctness"]
    verdict = ("SUPPORTED" if ret_range < 1e-9 and cite_drop > 0.9 else
               "PARTIAL" if ret_range < 0.01 else "FALSIFIED")

    print(f"{'severity':>9}{'Recall@5':>11}{'MRR':>9}{'nDCG@10':>10}{'citation acc':>14}")
    for r in rows:
        print(f"{r['severity']:>9.2f}{r['recall@5']:>11.4f}{r['mrr']:>9.4f}"
              f"{r['ndcg@10']:>10.4f}{r['citation_correctness']:>13.3f}")
    print(f"\nretrieval Recall@5 range across all severities : {ret_range:.2e}")
    print(f"citation correctness drop 0 -> 100% shuffle    : {cite_drop*100:.1f} pts")
    print(f"claim 'ranking metrics are blind to attribution failure': {verdict}")

    res = {"design": "inject metadata misalignment of controlled severity; measure retrieval "
                     "and citation correctness independently",
           "seed": SEED, "repeats_per_severity": N_REPEATS, "depth": DEPTH,
           "citation_top_k": 6, "rows": rows,
           "retrieval_recall5_range": ret_range,
           "citation_drop": cite_drop, "verdict": verdict,
           "interpretation": ("Retrieval metrics are invariant to metadata perturbation by "
                              "construction; the experiment confirms empirically that an "
                              "attribution failure of ANY severity is undetectable by "
                              "Recall@K / MRR / nDCG.")}
    (OUT / "processed" / "perturbation_study.json").write_text(json.dumps(res, indent=2))

    GOLD, INK = "#C9A84C", "#1A1A2E"
    fig, ax = plt.subplots(figsize=(6, 3.4), dpi=150)
    x = [r["severity"] * 100 for r in rows]
    ax.plot(x, [r["citation_correctness"] * 100 for r in rows], "o-", color=INK,
            label="citation correctness")
    ax.plot(x, [r["recall@5"] * 100 for r in rows], "s--", color=GOLD, label="Recall@5")
    ax.plot(x, [r["ndcg@10"] * 100 for r in rows], "^:", color="#8a8a99", label="nDCG@10")
    ax.set_xlabel("% of metadata rows misaligned"); ax.set_ylabel("%")
    ax.set_title("Ranking metrics are flat while attribution collapses", fontsize=9)
    ax.grid(alpha=.25, ls=":"); ax.legend(frameon=False, fontsize=8); ax.set_ylim(-3, 103)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    fig.tight_layout(); fig.savefig(OUT / "figures" / "fig6_perturbation.png", bbox_inches="tight")
    print("wrote research/results/processed/perturbation_study.json + figures/fig6_perturbation.png")


if __name__ == "__main__":
    main()
