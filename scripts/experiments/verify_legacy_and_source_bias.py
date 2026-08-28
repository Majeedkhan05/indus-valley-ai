"""
PHASE 6 - INDEPENDENT re-verification of the legacy-vs-corrected finding.
PHASE 7 - TARGETED mechanism test for the source-retrieval imbalance.

Phase 6 uses a different code path from E002: it compares the two systems by
RANK CORRELATION and set overlap rather than by identity resolution, so agreement
between the two methods is genuine corroboration rather than a repeated bug.

Phase 7 tests a falsifiable mechanism rather than listing correlates:
    H: Yajnadevam is under-retrieved because most of its chunks are TABULAR
       (glyph/ID listings), not because the source is disfavoured as such.
    Prediction: if H holds, Yajnadevam PROSE chunks should be retrieved at a rate
    comparable to CISI prose, while its TABULAR chunks are near-absent.
    H is falsified if prose Yajnadevam chunks are also strongly under-retrieved.
"""
from __future__ import annotations
import collections, json, os, pathlib, sys, time
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np, faiss
from scipy import stats

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from retrieval.lexical.bm25 import BM25, tokenize

COR = ROOT / "backend" / "data" / "index_v2"
LEG = ROOT / "backend" / "data" / "index"
BENCH = ROOT / "research" / "benchmark" / "iva80_latest.json"
OUT = ROOT / "research" / "results"
DEPTH = 10
YAJ = "Indus Inscriptions by Yajnadevam.pdf"


def load(d):
    rows = [json.loads(l) for l in (d / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
    idx = faiss.read_index(str(d / "faiss.index"))
    return rows, np.asarray(idx.reconstruct_n(0, idx.ntotal), dtype=np.float32)


def main():
    t0 = time.time()
    cor, CV = load(COR); leg, LV = load(LEG)
    texts = [c["text"] for c in cor]
    qs = json.load(BENCH.open())["questions"]
    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer("BAAI/bge-small-en-v1.5")
    QV = m.encode([q["question"] for q in qs], normalize_embeddings=True,
                  convert_to_numpy=True, show_progress_bar=False).astype(np.float32)
    leg2cor = np.argmax(LV @ CV.T, axis=1)

    # ================= PHASE 6 ==========================================
    taus, jacc, cite_ok, cite_tot, doc_wrong, page_wrong = [], [], 0, 0, 0, 0
    for i in range(len(qs)):
        lscore, cscore = LV @ QV[i], CV @ QV[i]
        ltop = np.argsort(-lscore)[:DEPTH]
        ctop = np.argsort(-cscore)[:DEPTH].tolist()
        ltrue = [int(leg2cor[j]) for j in ltop]
        # rank correlation on the shared items
        shared = [d for d in ltrue if d in ctop]
        if len(shared) >= 3:
            taus.append(stats.kendalltau([ltrue.index(d) for d in shared],
                                         [ctop.index(d) for d in shared]).statistic)
        jacc.append(len(set(ltrue) & set(ctop)) / len(set(ltrue) | set(ctop)))
        for j in ltop:
            j = int(j); cite_tot += 1
            rep = leg[j] if j < len(leg) else None
            true = cor[int(leg2cor[j])]
            if rep and rep["source"] == true["source"] and rep["page"] == true["page"]:
                cite_ok += 1
            elif rep and rep["source"] != true["source"]:
                doc_wrong += 1
            elif rep:
                page_wrong += 1

    phase6 = {
        "method": "independent - rank correlation + set overlap (E002 used identity resolution)",
        "depth": DEPTH,
        "content_jaccard_mean": float(np.mean(jacc)),
        "kendall_tau_on_shared_mean": float(np.nanmean(taus)) if taus else float("nan"),
        "citation_correctness_legacy": cite_ok / cite_tot,
        "citations_examined": cite_tot,
        "wrong_document": doc_wrong, "wrong_page_only": page_wrong,
        "corroborates_E002": None,
    }
    e2p = ROOT / "experiments/results/E002_legacy_vs_corrected/metrics.json"
    if e2p.exists():
        e2 = json.loads(e2p.read_text())
        phase6["E002_citation_accuracy_topk6"] = e2["citation_correctness_legacy"]["accuracy"]
        phase6["E002_content_overlap"] = e2["content_overlap_topk"]
        phase6["corroborates_E002"] = bool(
            abs(phase6["citation_correctness_legacy"] - e2["citation_correctness_legacy"]["accuracy"]) < 0.05)

    print("=== PHASE 6 - independent verification ===")
    print(f"  content Jaccard (legacy TRUE vs corrected, top-{DEPTH}): {phase6['content_jaccard_mean']:.3f}")
    print(f"  Kendall tau on shared items                          : {phase6['kendall_tau_on_shared_mean']:.3f}")
    print(f"  legacy citation correctness                          : {phase6['citation_correctness_legacy']*100:.1f}%")
    print(f"  wrong document / wrong page only                     : {doc_wrong} / {page_wrong}")
    print(f"  corroborates E002                                    : {phase6['corroborates_E002']}")

    # ================= PHASE 7 ==========================================
    # classify chunks: TABULAR vs PROSE by numeric-token rate (pre-registered cut)
    def numrate(t):
        tk = tokenize(t)
        return (sum(1 for w in tk if any(ch.isdigit() for ch in w)) / len(tk)) if tk else 0.0
    rates = np.array([numrate(t) for t in texts])
    CUT = 0.30
    tabular = rates >= CUT
    bm25 = BM25([tokenize(t) for t in texts])

    retrieved = collections.Counter()
    for i in range(len(qs)):
        dn = np.argsort(-(CV @ QV[i]))[:DEPTH].tolist()
        bm = [d for d, _ in bm25.search(qs[i]["question"], top_k=DEPTH)]
        for d in set(dn) | set(bm): retrieved[d] += 1

    def stratum(mask, label):
        ids = np.where(mask)[0]
        if len(ids) == 0: return None
        share_corpus = len(ids) / len(texts)
        got = sum(retrieved[int(d)] for d in ids)
        total = sum(retrieved.values())
        share_ret = got / total if total else 0.0
        return {"label": label, "chunks": int(len(ids)), "corpus_share": share_corpus,
                "retrieved_share": share_ret,
                "ratio": (share_ret / share_corpus) if share_corpus else float("nan"),
                "mean_numeric_rate": float(rates[ids].mean())}

    srcs = np.array([c["source"] for c in cor])
    strata = []
    for s in sorted(set(srcs)):
        for lab, msk in (("prose", (srcs == s) & ~tabular), ("tabular", (srcs == s) & tabular)):
            r = stratum(msk, f"{s[:34]} [{lab}]")
            if r: r["source"] = s; r["kind"] = lab; strata.append(r)

    print(f"\n=== PHASE 7 - mechanism test (tabular cut: numeric-token rate >= {CUT}) ===")
    print(f"{'stratum':<50}{'chunks':>7}{'corpus':>9}{'retr':>8}{'ratio':>8}")
    for r in sorted(strata, key=lambda x: -x["corpus_share"]):
        print(f"{r['label']:<50}{r['chunks']:>7}{r['corpus_share']*100:>8.1f}%"
              f"{r['retrieved_share']*100:>7.1f}%{r['ratio']:>8.2f}")

    yp = next((r for r in strata if r["source"] == YAJ and r["kind"] == "prose"), None)
    yt = next((r for r in strata if r["source"] == YAJ and r["kind"] == "tabular"), None)
    cisi_prose = [r for r in strata if r["source"].startswith("CISI") and r["kind"] == "prose"]
    cp = float(np.mean([r["ratio"] for r in cisi_prose])) if cisi_prose else float("nan")

    verdict, reasoning = "UNRESOLVED", ""
    if yp and yt:
        if yp["ratio"] >= 0.6 * cp and yt["ratio"] < 0.4 * cp:
            verdict = "SUPPORTED"
            reasoning = ("Yajnadevam PROSE is retrieved at a rate comparable to CISI prose while "
                         "its TABULAR chunks are near-absent: the deficit is explained by chunk "
                         "TYPE, not by the source itself.")
        elif yp["ratio"] < 0.6 * cp:
            verdict = "FALSIFIED"
            reasoning = ("Yajnadevam PROSE chunks are ALSO strongly under-retrieved "
                         f"(ratio {yp['ratio']:.2f} vs CISI prose {cp:.2f}), so the tabular-content "
                         "hypothesis does NOT explain the deficit. Cause remains UNKNOWN.")
        else:
            reasoning = "Result is intermediate; the hypothesis is neither clearly supported nor refuted."
    phase7 = {"hypothesis": "Yajnadevam under-retrieval is caused by tabular (glyph/ID listing) "
                            "content rather than by the source itself",
              "tabular_cut_numeric_rate": CUT, "strata": strata,
              "yajnadevam_prose_ratio": yp["ratio"] if yp else None,
              "yajnadevam_tabular_ratio": yt["ratio"] if yt else None,
              "cisi_prose_mean_ratio": cp,
              "verdict": verdict, "reasoning": reasoning}
    print(f"\n  H: tabular content explains the deficit  ->  {verdict}")
    print(f"  {reasoning}")

    (OUT / "processed").mkdir(parents=True, exist_ok=True)
    (OUT / "processed" / "phase6_legacy_verification.json").write_text(json.dumps(phase6, indent=2))
    (OUT / "processed" / "phase7_source_mechanism.json").write_text(json.dumps(phase7, indent=2))
    print(f"\nwrote research/results/processed/  ({time.time()-t0:.1f}s)")


if __name__ == "__main__":
    main()
