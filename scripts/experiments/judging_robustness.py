"""
PHASE 5b - Judging-scheme robustness.

Phase 9 exposed a flaw in the automatic judge: with a GLOBAL quantile threshold,
41/80 questions receive zero relevant chunks and are silently dropped, leaving
n=39. That is an evaluation artifact, not a system failure.

This script evaluates under TWO judging schemes and asks whether the ranking of
systems is an artifact of the scheme:

  A. global_quantile   - one threshold across all pooled pairs (Phase 4 default)
  B. per_question      - relevance relative to each question's OWN best score:
                         relevant if score >= max(floor, best - margin).
                         Every question with any usable evidence is retained.

If the two schemes agree on the ordering, the ordering is robust to the judge.
If they disagree, no ordering claim can be made without human labels.
"""
from __future__ import annotations
import collections, json, os, pathlib, sys
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np, faiss

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from retrieval.lexical.bm25 import BM25, tokenize
from evaluation.metrics.ir_metrics import recall_at_k, reciprocal_rank, ndcg_at_k

IDX = ROOT / "backend" / "data" / "index_v2"
BENCH = ROOT / "research" / "benchmark" / "iva80_latest.json"
OUT = ROOT / "research" / "results" / "processed"
SEED = 42; rng = np.random.default_rng(SEED)
DEPTH = 10; N_BOOT = 10000


def rrf(ls, k=60):
    s = {}
    for l in ls:
        for r, d in enumerate(l, 1): s[d] = s.get(d, 0.0) + 1.0 / (k + r)
    return [d for d, _ in sorted(s.items(), key=lambda kv: -kv[1])]


def boot(v):
    v = np.asarray([x for x in v if not np.isnan(x)], float)
    if len(v) < 2: return [float("nan")] * 2
    i = rng.integers(0, len(v), size=(N_BOOT, len(v)))
    mu = v[i].mean(1)
    return [float(np.percentile(mu, 2.5)), float(np.percentile(mu, 97.5))]


def paired(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = ~(np.isnan(a) | np.isnan(b)); a, b = a[ok], b[ok]
    if len(a) < 2: return {"diff": float("nan"), "p": float("nan")}
    i = rng.integers(0, len(a), size=(N_BOOT, len(a)))
    d = (a[i] - b[i]).mean(1)
    return {"diff": float(a.mean() - b.mean()),
            "ci95": [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))],
            "p": float(min(2 * min((d <= 0).mean(), (d >= 0).mean()), 1.0))}


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

    runs = {"bm25": [], "dense": [], "hybrid_rrf": []}
    for i, q in enumerate(qs):
        bm = [d for d, _ in bm25.search(q["question"], top_k=DEPTH)]
        dn = np.argsort(-(V @ QV[i]))[:DEPTH].tolist()
        runs["bm25"].append(bm); runs["dense"].append(dn)
        runs["hybrid_rrf"].append(rrf([bm, dn])[:DEPTH])

    pools = [sorted(set().union(*[set(runs[s][i]) for s in runs])) for i in range(len(qs))]
    lexs, sems = [], []
    for i, pool in enumerate(pools):
        ref = set(tokenize(qs[i]["reference_answer"]))
        cos = V[pool] @ GV[i]
        lexs.append(np.array([len(ref & set(tokc[d])) / len(ref) if ref else 0.0 for d in pool]))
        sems.append(np.array([float(c) for c in cos]))

    def qrels_global(sel=0.05):
        al, as_ = np.concatenate(lexs), np.concatenate(sems)
        lt, st = np.quantile(al, 1 - sel), np.quantile(as_, 1 - sel)
        return {qs[i]["id"]: {pools[i][j]: 1.0 for j in range(len(pools[i]))
                              if lexs[i][j] >= lt or sems[i][j] >= st}
                for i in range(len(qs))}

    def qrels_per_question(margin=0.06, floor=0.55):
        qr = {}
        for i in range(len(qs)):
            s = sems[i]
            if len(s) == 0: qr[qs[i]["id"]] = {}; continue
            thr = max(floor, float(s.max()) - margin)
            sel = {pools[i][j]: 1.0 for j in range(len(s))
                   if s[j] >= thr or lexs[i][j] >= 0.5}
            qr[qs[i]["id"]] = sel
        return qr

    schemes = {"global_quantile": qrels_global(), "per_question": qrels_per_question()}
    report = {"schemes": {}, "rankings": {}}
    for name, qr in schemes.items():
        cov = sum(1 for v in qr.values() if v)
        per = {s: collections.defaultdict(list) for s in runs}
        for i, q in enumerate(qs):
            rel = qr.get(q["id"], {})
            if not rel: continue
            for s in runs:
                for k in (1, 5, 10):
                    per[s][f"recall@{k}"].append(recall_at_k(runs[s][i], rel, k))
                per[s]["mrr"].append(reciprocal_rank(runs[s][i], rel))
                per[s]["ndcg@10"].append(ndcg_at_k(runs[s][i], rel, 10))
        block = {"questions_covered": cov, "coverage": cov / len(qs),
                 "mean_relevant_per_question": float(np.mean([len(v) for v in qr.values() if v])),
                 "systems": {s: {k: {"mean": float(np.nanmean(v)), "ci95": boot(v), "n": len(v)}
                                 for k, v in per[s].items()} for s in runs},
                 "paired_vs_dense": {s: {k: paired(per[s][k], per["dense"][k])
                                         for k in ("recall@5", "mrr", "ndcg@10")}
                                     for s in runs if s != "dense"}}
        report["schemes"][name] = block
        report["rankings"][name] = sorted(runs, key=lambda s: -block["systems"][s]["recall@5"]["mean"])
        print(f"\n=== {name}  (coverage {cov}/{len(qs)} questions, "
              f"mean {block['mean_relevant_per_question']:.1f} relevant/question) ===")
        print(f"{'system':<13}{'R@1':>20}{'R@5':>20}{'MRR':>20}{'nDCG@10':>20}")
        for s in runs:
            cells = "".join(f"{block['systems'][s][k]['mean']:.3f} "
                            f"[{block['systems'][s][k]['ci95'][0]:.2f},{block['systems'][s][k]['ci95'][1]:.2f}]".rjust(20)
                            for k in ("recall@1", "recall@5", "mrr", "ndcg@10"))
            print(f"{s:<13}{cells}")
        for s, d in block["paired_vs_dense"].items():
            x = d["recall@5"]
            print(f"  {s} vs dense  R@5 diff={x['diff']:+.3f} "
                  f"CI[{x['ci95'][0]:+.3f},{x['ci95'][1]:+.3f}] p={x['p']:.3f} "
                  f"{'SIGNIFICANT' if x['p'] < 0.05 else 'ns'}")

    agree = report["rankings"]["global_quantile"] == report["rankings"]["per_question"]
    report["ranking_consistent_across_schemes"] = agree
    print(f"\nranking consistent across judging schemes: {agree}")
    for k, v in report["rankings"].items(): print(f"  {k}: {' > '.join(v)}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "judging_robustness.json").write_text(json.dumps(report, indent=2))
    print(f"\nwrote {(OUT/'judging_robustness.json').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
