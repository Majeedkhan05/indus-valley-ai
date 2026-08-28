"""
PHASE 7b - Follow-up after the tabular hypothesis was FALSIFIED.

Yajnadevam is under-retrieved in BOTH the prose and tabular strata, so chunk type
does not explain it. Next falsifiable hypothesis:

  H2: Yajnadevam is under-retrieved because its CONTENT IS ABOUT A DIFFERENT TOPIC
      than the benchmark asks about. The book argues a Sanskrit decipherment; the
      benchmark asks about sites, seals, trade and archaeology. If so, low
      retrieval is CORRECT selectivity, not a retrieval defect.

  Prediction if H2 holds: on questions whose subject matter IS the script/
  decipherment, Yajnadevam should be retrieved at or above its corpus share.
  H2 is falsified if Yajnadevam stays suppressed even on script questions.

This distinguishes "the retriever is biased" from "the retriever is right".
"""
from __future__ import annotations
import collections, json, os, pathlib, sys
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np, faiss

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from retrieval.lexical.bm25 import BM25, tokenize

IDX = ROOT / "backend" / "data" / "index_v2"
BENCH = ROOT / "research" / "benchmark" / "iva80_latest.json"
OUT = ROOT / "research" / "results" / "processed"
YAJ = "Indus Inscriptions by Yajnadevam.pdf"
DEPTH = 10


def main():
    chunks = [json.loads(l) for l in (IDX / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
    texts = [c["text"] for c in chunks]
    srcs = np.array([c["source"] for c in chunks])
    V = np.asarray(faiss.read_index(str(IDX / "faiss.index")).reconstruct_n(0, len(chunks)),
                   dtype=np.float32)
    qs = json.load(BENCH.open())["questions"]
    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer("BAAI/bge-small-en-v1.5")
    QV = m.encode([q["question"] for q in qs], normalize_embeddings=True,
                  convert_to_numpy=True, show_progress_bar=False).astype(np.float32)
    bm25 = BM25([tokenize(t) for t in texts])

    yaj_share = float((srcs == YAJ).mean())
    per_cat = collections.defaultdict(lambda: {"n": 0, "yaj_hits": 0, "hits": 0})
    for i, q in enumerate(qs):
        dn = np.argsort(-(V @ QV[i]))[:DEPTH].tolist()
        bm = [d for d, _ in bm25.search(q["question"], top_k=DEPTH)]
        got = list(set(dn) | set(bm))
        c = per_cat[q["category"]]
        c["n"] += 1; c["hits"] += len(got)
        c["yaj_hits"] += sum(1 for d in got if srcs[d] == YAJ)

    rows = []
    for cat, d in sorted(per_cat.items(), key=lambda kv: -kv[1]["n"]):
        share = d["yaj_hits"] / d["hits"] if d["hits"] else 0.0
        rows.append({"category": cat, "questions": d["n"], "retrieved": d["hits"],
                     "yajnadevam_hits": d["yaj_hits"], "yajnadevam_share": share,
                     "ratio_vs_corpus": share / yaj_share if yaj_share else float("nan")})

    print(f"Yajnadevam corpus share: {yaj_share*100:.1f}%\n")
    print(f"{'category':<18}{'Qs':>4}{'yaj hits':>10}{'yaj share':>11}{'ratio':>8}")
    for r in rows:
        print(f"{r['category']:<18}{r['questions']:>4}{r['yajnadevam_hits']:>10}"
              f"{r['yajnadevam_share']*100:>10.1f}%{r['ratio_vs_corpus']:>8.2f}")

    script_like = {"script", "seals"}
    sr = [r for r in rows if r["category"] in script_like]
    other = [r for r in rows if r["category"] not in script_like]
    s_ratio = float(np.mean([r["ratio_vs_corpus"] for r in sr])) if sr else float("nan")
    o_ratio = float(np.mean([r["ratio_vs_corpus"] for r in other])) if other else float("nan")

    if s_ratio >= 0.9:
        verdict, why = "SUPPORTED", (
            f"On script/seal questions Yajnadevam is retrieved at {s_ratio:.2f}x its corpus share "
            f"versus {o_ratio:.2f}x elsewhere. Low overall retrieval reflects CORRECT topical "
            f"selectivity, not a retrieval defect.")
    elif s_ratio > 2 * o_ratio and s_ratio > 0.5:
        verdict, why = "PARTIALLY SUPPORTED", (
            f"Yajnadevam is retrieved {s_ratio/max(o_ratio,1e-9):.1f}x more on script/seal questions "
            f"({s_ratio:.2f}x vs {o_ratio:.2f}x corpus share), so topic clearly matters, but it "
            f"remains below parity even on its own subject matter.")
    else:
        verdict, why = "FALSIFIED", (
            f"Yajnadevam stays suppressed even on script/seal questions ({s_ratio:.2f}x vs "
            f"{o_ratio:.2f}x). Topical mismatch does NOT explain it. Cause remains UNKNOWN.")

    print(f"\nH2: topical mismatch explains under-retrieval -> {verdict}")
    print(f"  {why}")
    res = {"hypothesis": "Yajnadevam under-retrieval reflects topical mismatch with the benchmark, "
                         "i.e. correct selectivity rather than bias",
           "yajnadevam_corpus_share": yaj_share, "depth": DEPTH, "by_category": rows,
           "script_like_categories": sorted(script_like),
           "mean_ratio_script_like": s_ratio, "mean_ratio_other": o_ratio,
           "verdict": verdict, "reasoning": why}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "phase7b_topical_mismatch.json").write_text(json.dumps(res, indent=2))
    print(f"\nwrote {(OUT/'phase7b_topical_mismatch.json').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
