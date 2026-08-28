"""
PHASE 8 - Ablation matrix.   PHASE 9 - Error taxonomy and analysis.

ABLATION (only components that actually exist - no artificial knobs):
  retriever      : bm25 | dense | hybrid_rrf
  depth K        : 1,3,5,10
  RRF k constant : 10, 60, 200
  fusion         : rrf vs score-normalised linear blend
  corpus variant : full | drop near-duplicate-collapsed source (Yajnadevam)
                   (motivated by the Phase-7c finding, not invented)

ERROR ANALYSIS: categorises every failing question against a fixed taxonomy and
extracts representative examples.
"""
from __future__ import annotations
import collections, json, os, pathlib, sys, time
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np, faiss

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from retrieval.lexical.bm25 import BM25, tokenize
from evaluation.metrics.ir_metrics import recall_at_k, reciprocal_rank, ndcg_at_k

IDX = ROOT / "backend" / "data" / "index_v2"
BENCH = ROOT / "research" / "benchmark" / "iva80_latest.json"
RES = ROOT / "research" / "results"
ERR = ROOT / "research" / "error_analysis"
SEED = 42; rng = np.random.default_rng(SEED)
SEL = 0.05; DEPTH = 10; YAJ = "Indus Inscriptions by Yajnadevam.pdf"


def rrf(lists, k=60):
    s = {}
    for l in lists:
        for r, d in enumerate(l, 1): s[d] = s.get(d, 0.0) + 1.0 / (k + r)
    return [d for d, _ in sorted(s.items(), key=lambda kv: -kv[1])]


def linear_blend(bm_scores, dn_scores, alpha=0.5):
    def nz(x):
        x = np.asarray(x, float)
        return (x - x.min()) / (x.max() - x.min()) if x.max() > x.min() else np.zeros_like(x)
    s = alpha * nz(dn_scores) + (1 - alpha) * nz(bm_scores)
    return np.argsort(-s).tolist()


def main():
    t0 = time.time()
    ERR.mkdir(parents=True, exist_ok=True)
    chunks = [json.loads(l) for l in (IDX / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
    texts = [c["text"] for c in chunks]
    srcs = np.array([c["source"] for c in chunks])
    V = np.asarray(faiss.read_index(str(IDX / "faiss.index")).reconstruct_n(0, len(chunks)),
                   dtype=np.float32)
    qs = json.load(BENCH.open())["questions"]
    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer("BAAI/bge-small-en-v1.5")
    enc = lambda xs: m.encode(xs, normalize_embeddings=True, convert_to_numpy=True,
                              show_progress_bar=False).astype(np.float32)
    QV, GV = enc([q["question"] for q in qs]), enc([q["reference_answer"] for q in qs])
    tok_corpus = [tokenize(t) for t in texts]
    bm25 = BM25(tok_corpus)

    keep = np.where(srcs != YAJ)[0]
    bm25_noyaj = BM25([tok_corpus[i] for i in keep])

    # ---------- build every ablation run --------------------------------
    runs: dict[str, list[list[int]]] = collections.defaultdict(list)
    for i, q in enumerate(qs):
        bm_all = bm25.search(q["question"], top_k=len(texts))
        bm_rank = [d for d, _ in bm_all[:DEPTH]]
        bmvec = np.zeros(len(texts)); 
        for d, s in bm_all: bmvec[d] = s
        dnvec = V @ QV[i]
        dn_rank = np.argsort(-dnvec)[:DEPTH].tolist()
        runs["bm25"].append(bm_rank)
        runs["dense"].append(dn_rank)
        for kk in (10, 60, 200):
            runs[f"hybrid_rrf_k{kk}"].append(rrf([bm_rank, dn_rank], k=kk)[:DEPTH])
        for al in (0.3, 0.5, 0.7):
            runs[f"hybrid_linear_a{al}"].append(linear_blend(bmvec, dnvec, al)[:DEPTH])
        # corpus variant: Yajnadevam removed
        sub = V[keep]
        dn_ny = [int(keep[j]) for j in np.argsort(-(sub @ QV[i]))[:DEPTH]]
        bm_ny = [int(keep[d]) for d, _ in bm25_noyaj.search(q["question"], top_k=DEPTH)]
        runs["dense_no_yajnadevam"].append(dn_ny)
        runs["hybrid_no_yajnadevam"].append(rrf([bm_ny, dn_ny])[:DEPTH])

    # ---------- judgments (same protocol as Phase 4) ---------------------
    pools, lex, sem = [], [], []
    for i in range(len(qs)):
        pool = sorted(set().union(*[set(r[i]) for r in runs.values()]))
        ref = set(tokenize(qs[i]["reference_answer"]))
        cos = V[pool] @ GV[i]
        for j, d in enumerate(pool):
            lex.append(len(ref & set(tok_corpus[d])) / len(ref) if ref else 0.0)
            sem.append(float(cos[j]))
        pools.append(pool)
    lex, sem = np.array(lex), np.array(sem)
    flat = [(i, d) for i, p in enumerate(pools) for d in p]
    la = (lex >= np.quantile(lex, 1 - SEL)).astype(int)
    sa = (sem >= np.quantile(sem, 1 - SEL)).astype(int)
    qr = {}
    for n, (i, d) in enumerate(flat):
        qr.setdefault(qs[i]["id"], {})
        if la[n] or sa[n]: qr[qs[i]["id"]][d] = 1.0

    def boot(v):
        v = np.asarray([x for x in v if not np.isnan(x)], float)
        if len(v) < 2: return [float("nan")] * 2
        idx = rng.integers(0, len(v), size=(4000, len(v)))
        mu = v[idx].mean(1)
        return [float(np.percentile(mu, 2.5)), float(np.percentile(mu, 97.5))]

    abl = {}
    for name, rl in runs.items():
        per = collections.defaultdict(list)
        for i, q in enumerate(qs):
            rel = qr.get(q["id"], {})
            if not rel: continue
            for k in (1, 3, 5, 10): per[f"recall@{k}"].append(recall_at_k(rl[i], rel, k))
            per["mrr"].append(reciprocal_rank(rl[i], rel))
            per["ndcg@10"].append(ndcg_at_k(rl[i], rel, 10))
        abl[name] = {k: {"mean": float(np.nanmean(v)), "ci95": boot(v), "n": len(v)}
                     for k, v in per.items()}

    print("=== PHASE 8 ABLATION (Recall@5, MRR; automatic proxy judge) ===")
    print(f"{'configuration':<26}{'R@1':>8}{'R@5':>8}{'R@10':>8}{'MRR':>8}{'nDCG@10':>10}")
    for n in sorted(abl, key=lambda x: -abl[x]["recall@5"]["mean"]):
        a = abl[n]
        print(f"{n:<26}{a['recall@1']['mean']:>8.3f}{a['recall@5']['mean']:>8.3f}"
              f"{a['recall@10']['mean']:>8.3f}{a['mrr']['mean']:>8.3f}{a['ndcg@10']['mean']:>10.3f}")

    # ---------- PHASE 9 error taxonomy -----------------------------------
    TAX = ["lexical_mismatch", "semantic_mismatch", "ambiguous_question",
           "insufficient_evidence", "source_imbalance", "ocr_artifact",
           "chunking_problem", "near_duplicate_collapse", "contested_interpretation",
           "retrieval_failure", "evaluation_artifact"]
    errors, counts = [], collections.Counter()
    for i, q in enumerate(qs):
        rel = qr.get(q["id"], {})
        if not rel: 
            counts["evaluation_artifact"] += 1
            errors.append({"qid": q["id"], "question": q["question"],
                           "categories": ["evaluation_artifact"],
                           "why": "no chunk passed the judging threshold for this question"})
            continue
        r5 = recall_at_k(runs["hybrid_rrf_k60"][i], rel, 5)
        if r5 >= 0.5: continue                       # not a failure
        cats, why = [], []
        qtok = set(tokenize(q["question"]))
        hits = sum(1 for t in qtok if bm25.inv.get(t))
        top = runs["hybrid_rrf_k60"][i][:5]
        gold = list(rel)
        if hits < 0.5 * len(qtok):
            cats.append("lexical_mismatch"); why.append(f"only {hits}/{len(qtok)} query terms in corpus")
        gsim = float(np.max(V[gold] @ QV[i])) if gold else 0.0
        if gsim < 0.60:
            cats.append("semantic_mismatch"); why.append(f"best relevant chunk cos={gsim:.2f}")
        if "possibly_ambiguous" in q["flags"]: cats.append("ambiguous_question")
        if "contested_interpretation" in q["flags"]: cats.append("contested_interpretation")
        if q["evidence_ceiling_cos"] < 0.62:
            cats.append("insufficient_evidence"); why.append(f"evidence ceiling {q['evidence_ceiling_cos']:.2f}")
        gs = collections.Counter(srcs[d] for d in gold)
        ts = collections.Counter(srcs[d] for d in top)
        if gs and ts and gs.most_common(1)[0][0] != ts.most_common(1)[0][0]:
            cats.append("source_imbalance")
            why.append(f"relevant mostly {gs.most_common(1)[0][0][:24]}, retrieved mostly {ts.most_common(1)[0][0][:24]}")
        if any(srcs[d] == YAJ for d in gold): cats.append("near_duplicate_collapse")
        toks = [tok_corpus[d] for d in top]
        dic = np.mean([sum(1 for w in t if w.isalpha() and len(w) > 2) / max(len(t), 1) for t in toks]) if toks else 1
        if dic < 0.5: cats.append("ocr_artifact"); why.append(f"retrieved dictionary-word rate {dic:.2f}")
        if np.mean([len(tok_corpus[d]) for d in top]) < 90:
            cats.append("chunking_problem"); why.append("retrieved chunks very short")
        if not cats: cats.append("retrieval_failure")
        for c in cats: counts[c] += 1
        errors.append({"qid": q["id"], "question": q["question"], "category": q["category"],
                       "recall@5": r5, "categories": cats, "why": "; ".join(why),
                       "top_sources": [f"{srcs[d][:30]} p.{chunks[d]['page']}" for d in top[:3]]})

    print(f"\n=== PHASE 9 ERROR ANALYSIS ({len(errors)} failing questions of {len(qs)}) ===")
    for c, n in counts.most_common():
        print(f"  {n:3d}  {c}")
    print("\n  representative failures:")
    for e in errors[:5]:
        print(f"   Q{e['qid']:2d} R@5={e.get('recall@5', float('nan')):.2f} [{','.join(e['categories'])}]")
        print(f"        {e['question'][:70]}")
        if e.get("why"): print(f"        {e['why'][:100]}")

    (RES / "processed" / "ablation.json").write_text(json.dumps(
        {"selectivity": SEL, "depth": DEPTH, "seed": SEED, "results": abl}, indent=2))
    (ERR / "errors.json").write_text(json.dumps(
        {"taxonomy": TAX, "n_failing": len(errors), "counts": dict(counts),
         "failures": errors}, indent=2))
    print(f"\nwrote ablation.json + error_analysis/errors.json  ({time.time()-t0:.1f}s)")


if __name__ == "__main__":
    main()
