"""
PHASE 7c - Third hypothesis after H(tabular) and H(topic) were both FALSIFIED.

Clue: de-duplication removed 913 rows, and 909 of them were Yajnadevam. A source
whose text is 75% duplicated is not a normal document.

  H3: The Yajnadevam PDF is a print-to-PDF of a web application. Its chunks carry
      repeated interface boilerplate and low lexical diversity, which dilutes the
      embedding of every chunk and flattens its similarity to any query.

  Predictions if H3 holds:
    (a) Yajnadevam has a far higher duplicate rate than any other source;
    (b) its chunks share a common boilerplate prefix/vocabulary;
    (c) its intra-source chunk-to-chunk similarity is unusually HIGH
        (chunks look like each other, not like queries);
    (d) its chunks sit closer to each other than to the corpus centroid.
  H3 is falsified if Yajnadevam looks lexically normal on these measures.
"""
from __future__ import annotations
import collections, hashlib, json, os, pathlib, sys
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np, faiss

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from retrieval.lexical.bm25 import tokenize

IDX = ROOT / "backend" / "data" / "index_v2"
RAW = ROOT / "backend" / "data" / "index" / "chunks.jsonl"
OUT = ROOT / "research" / "results" / "processed"
YAJ = "Indus Inscriptions by Yajnadevam.pdf"


def main():
    raw = [json.loads(l) for l in RAW.open(encoding="utf-8") if l.strip()]
    dup_by_src = collections.Counter()
    seen = set()
    tot_by_src = collections.Counter()
    for r in raw:
        tot_by_src[r["source"]] += 1
        h = hashlib.md5(r["text"].encode()).hexdigest()
        if h in seen: dup_by_src[r["source"]] += 1
        seen.add(h)

    chunks = [json.loads(l) for l in (IDX / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
    texts = [c["text"] for c in chunks]
    srcs = np.array([c["source"] for c in chunks])
    V = np.asarray(faiss.read_index(str(IDX / "faiss.index")).reconstruct_n(0, len(chunks)),
                   dtype=np.float32)
    centroid = V.mean(0); centroid /= np.linalg.norm(centroid)

    print(f"{'source':<44}{'raw':>6}{'dups':>6}{'dup%':>7}{'TTR':>7}{'intra':>7}{'cent':>7}")
    rows = []
    for s in sorted(set(srcs)):
        ids = np.where(srcs == s)[0]
        toks = [tokenize(texts[i]) for i in ids]
        allw = [w for t in toks for w in t]
        ttr = len(set(allw)) / max(len(allw), 1)          # type-token ratio (lexical diversity)
        sub = V[ids]
        sim = sub @ sub.T
        np.fill_diagonal(sim, np.nan)
        intra = float(np.nanmean(sim))                     # chunk-to-chunk similarity
        cent = float((sub @ centroid).mean())
        d = dup_by_src[s]; t = tot_by_src[s]
        rows.append({"source": s, "raw_rows": t, "duplicate_rows": d,
                     "duplicate_rate": d / t if t else 0.0, "type_token_ratio": ttr,
                     "mean_intra_source_similarity": intra, "mean_cos_to_corpus_centroid": cent,
                     "unique_chunks": int(len(ids))})
        print(f"{s[:43]:<44}{t:>6}{d:>6}{100*d/max(t,1):>6.1f}%{ttr:>7.3f}{intra:>7.3f}{cent:>7.3f}")

    y = next(r for r in rows if r["source"] == YAJ)
    others = [r for r in rows if r["source"] != YAJ and r["unique_chunks"] >= 50]
    o_dup = float(np.mean([r["duplicate_rate"] for r in others]))
    o_ttr = float(np.mean([r["type_token_ratio"] for r in others]))
    o_intra = float(np.mean([r["mean_intra_source_similarity"] for r in others]))

    # boilerplate probe: most common leading 6-gram
    ytexts = [texts[i] for i in np.where(srcs == YAJ)[0]]
    heads = collections.Counter(" ".join(t.split()[:6]) for t in ytexts)
    top_head, top_head_n = heads.most_common(1)[0]

    checks = {
        "a_duplicate_rate_much_higher": y["duplicate_rate"] > 2 * o_dup,
        "b_shared_boilerplate_prefix": top_head_n / len(ytexts) > 0.10,
        "c_intra_similarity_higher": y["mean_intra_source_similarity"] > o_intra,
        "d_lexical_diversity_lower": y["type_token_ratio"] < o_ttr,
    }
    n_pass = sum(checks.values())
    verdict = ("SUPPORTED" if n_pass >= 3 else
               "PARTIALLY SUPPORTED" if n_pass == 2 else "FALSIFIED")

    print(f"\nYajnadevam duplicate rate {y['duplicate_rate']*100:.1f}%  vs others {o_dup*100:.1f}%")
    print(f"type-token ratio          {y['type_token_ratio']:.3f}   vs others {o_ttr:.3f}")
    print(f"intra-source similarity   {y['mean_intra_source_similarity']:.3f}   vs others {o_intra:.3f}")
    print(f"most common leading 6-gram: {top_head_n}/{len(ytexts)} chunks -> {top_head!r}")
    print("\nchecks:")
    for k, v in checks.items(): print(f"  {'PASS' if v else 'FAIL'}  {k}")
    print(f"\nH3 verdict: {verdict} ({n_pass}/4 predictions met)")

    res = {"hypothesis": "Yajnadevam is a print-to-PDF of a web app; boilerplate and low lexical "
                         "diversity dilute its embeddings",
           "per_source": rows, "checks": checks, "n_predictions_met": n_pass,
           "verdict": verdict,
           "yajnadevam_top_leading_6gram": {"text": top_head, "chunks": top_head_n,
                                            "of": len(ytexts)},
           "comparison": {"other_sources_duplicate_rate": o_dup,
                          "other_sources_type_token_ratio": o_ttr,
                          "other_sources_intra_similarity": o_intra},
           "note": "Even if supported, this explains a MECHANISM of dilution; it does not by "
                   "itself prove the retrieval outcome is wrong."}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "phase7c_boilerplate.json").write_text(json.dumps(res, indent=2))
    print(f"wrote {(OUT/'phase7c_boilerplate.json').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
