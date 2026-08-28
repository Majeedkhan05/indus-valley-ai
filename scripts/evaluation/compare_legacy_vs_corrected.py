"""
E002 - Direct measurement of the citation-integrity bug's effect.

DESIGN
------
For the legacy index we can determine the TRUE identity of every vector: the
corrected index contains a re-embedding of every unique chunk text, so
legacy_vector[i] can be matched against the corrected index. A cosine of ~1.0
identifies which chunk legacy vector i actually encodes.

That gives, per retrieved hit:
    reported citation = legacy_metadata[i]          (what the user was shown)
    true citation     = corrected_metadata[argmax]  (what the vector really is)

Citation correctness = fraction of hits where reported == true (source AND page).

Also compares retrieval quality legacy-vs-corrected on the same benchmark.

Usage: backend/venv/bin/python scripts/evaluation/compare_legacy_vs_corrected.py
"""
from __future__ import annotations
import json, os, pathlib, sys, time
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np, faiss

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
LEG = ROOT / "backend" / "data" / "index"
COR = ROOT / "backend" / "data" / "index_v2"
BENCH = ROOT / "paper" / "eval" / "benchmark_questions.json"
OUT = ROOT / "experiments" / "results" / "E002_legacy_vs_corrected"
TOP_K = 6           # the production default
MATCH_COS = 0.99


def load(d):
    rows = [json.loads(l) for l in (d / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
    idx = faiss.read_index(str(d / "faiss.index"))
    V = np.asarray(idx.reconstruct_n(0, idx.ntotal), dtype=np.float32)
    return rows, V


def main():
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    leg_meta, LV = load(LEG)
    cor_meta, CV = load(COR)
    print(f"legacy   : {LV.shape[0]} vectors, {len(leg_meta)} metadata rows  <- MISMATCHED")
    print(f"corrected: {CV.shape[0]} vectors, {len(cor_meta)} metadata rows")

    # --- resolve the TRUE identity of every legacy vector -------------------
    print("\nresolving true identity of each legacy vector against corrected index ...")
    sim = LV @ CV.T                       # 1506 x 1199
    best = np.argmax(sim, axis=1)
    bestcos = sim[np.arange(len(best)), best]
    resolved = bestcos >= MATCH_COS
    print(f"  resolved {int(resolved.sum())}/{len(best)} legacy vectors "
          f"(cos>={MATCH_COS}); unresolved treated as UNKNOWN")

    # how many legacy metadata rows actually describe their own vector?
    agree = np.zeros(len(best), dtype=bool)
    for i in range(len(best)):
        if not resolved[i] or i >= len(leg_meta):
            continue
        t, r = cor_meta[best[i]], leg_meta[i]
        agree[i] = (t["source"] == r["source"] and t["page"] == r["page"])
    print(f"  legacy metadata[i] correctly describes vector[i] for "
          f"{int(agree.sum())}/{len(best)} ids ({100*agree.mean():.1f}%)")

    # --- run the benchmark queries through both indexes ---------------------
    questions = json.load(BENCH.open())["questions"]
    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer("BAAI/bge-small-en-v1.5")
    QV = m.encode([q["q"] for q in questions], normalize_embeddings=True,
                  convert_to_numpy=True, show_progress_bar=False).astype(np.float32)

    per_q, n_hits, n_correct, n_unknown = [], 0, 0, 0
    src_wrong = page_wrong = 0
    for qi, q in enumerate(questions):
        lidx = np.argsort(-(LV @ QV[qi]))[:TOP_K]
        cidx = np.argsort(-(CV @ QV[qi]))[:TOP_K]
        hits = []
        for rank, i in enumerate(lidx, 1):
            i = int(i)
            rep = leg_meta[i] if i < len(leg_meta) else None
            if resolved[i]:
                true = cor_meta[int(best[i])]
                ok = bool(rep and true["source"] == rep["source"] and true["page"] == rep["page"])
                n_correct += ok
                if rep and not ok:
                    src_wrong += (true["source"] != rep["source"])
                    page_wrong += (true["source"] == rep["source"] and true["page"] != rep["page"])
                hits.append({
                    "rank": rank, "faiss_id": i,
                    "reported_source": rep["source"] if rep else None,
                    "reported_page": rep["page"] if rep else None,
                    "true_source": true["source"], "true_page": true["page"],
                    "citation_correct": ok,
                    "score": float((LV[i] @ QV[qi])),
                })
            else:
                n_unknown += 1
                hits.append({"rank": rank, "faiss_id": i,
                             "reported_source": rep["source"] if rep else None,
                             "reported_page": rep["page"] if rep else None,
                             "true_source": "UNRESOLVED", "true_page": None,
                             "citation_correct": False,
                             "score": float((LV[i] @ QV[qi]))})
            n_hits += 1
        per_q.append({
            "id": q["id"], "category": q["category"], "question": q["q"],
            "legacy_hits": hits,
            "corrected_hits": [
                {"rank": r, "faiss_id": int(j), "source": cor_meta[int(j)]["source"],
                 "page": cor_meta[int(j)]["page"], "score": float(CV[int(j)] @ QV[qi])}
                for r, j in enumerate(cidx, 1)],
        })

    acc = n_correct / n_hits if n_hits else float("nan")
    print(f"\n--- CITATION CORRECTNESS over {len(questions)} benchmark queries, top-{TOP_K} ---")
    print(f"  hits examined      : {n_hits}")
    print(f"  citation correct   : {n_correct}  ({100*acc:.1f}%)")
    print(f"  wrong DOCUMENT     : {src_wrong}")
    print(f"  right doc, wrong PAGE: {page_wrong}")
    print(f"  unresolvable vector: {n_unknown}")

    # per-question: how many queries had at least one wrong citation?
    q_any_wrong = sum(1 for p in per_q if any(not h["citation_correct"] for h in p["legacy_hits"]))
    q_all_wrong = sum(1 for p in per_q if all(not h["citation_correct"] for h in p["legacy_hits"]))
    print(f"  queries with >=1 wrong citation : {q_any_wrong}/{len(questions)}")
    print(f"  queries with ALL citations wrong: {q_all_wrong}/{len(questions)}")

    # --- does the retrieved TEXT differ between the two indexes? ------------
    same_text = 0
    for p in per_q:
        lt = {h["true_source"] + "|" + str(h["true_page"]) for h in p["legacy_hits"]}
        ct = {h["source"] + "|" + str(h["page"]) for h in p["corrected_hits"]}
        same_text += len(lt & ct) / max(len(ct), 1)
    overlap = same_text / len(per_q)
    print(f"\n  mean top-{TOP_K} content overlap (legacy TRUE vs corrected): {overlap:.3f}")

    summary = {
        "experiment_id": "E002_legacy_vs_corrected",
        "top_k": TOP_K, "questions": len(questions),
        "legacy": {"vectors": int(LV.shape[0]), "metadata_rows": len(leg_meta)},
        "corrected": {"vectors": int(CV.shape[0]), "metadata_rows": len(cor_meta)},
        "legacy_vector_identity": {
            "resolved": int(resolved.sum()), "total": int(len(best)),
            "metadata_describes_own_vector": int(agree.sum()),
            "metadata_correct_fraction": float(agree.mean()),
        },
        "citation_correctness_legacy": {
            "hits": n_hits, "correct": n_correct, "accuracy": acc,
            "wrong_document": src_wrong, "wrong_page_only": page_wrong,
            "unresolvable": n_unknown,
            "queries_with_any_wrong": q_any_wrong,
            "queries_with_all_wrong": q_all_wrong,
        },
        "citation_correctness_corrected": {
            "accuracy": 1.0,
            "basis": "index_v2 fully validated: 1199/1199 vectors re-embedded, cos>=0.99 "
                     "(experiments/analysis/validation_index_v2.json)",
        },
        "content_overlap_topk": overlap,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    (OUT / "metrics.json").write_text(json.dumps(summary, indent=2))
    (OUT / "per_query.json").write_text(json.dumps(per_q, indent=2))
    print(f"\nwrote {OUT.relative_to(ROOT)}  ({time.time()-t0:.1f}s)")


if __name__ == "__main__":
    main()
