"""
Structured error dataset - one record PER FAILING (question, system, rank).

Schema (as specified):
  question_id, system, rank, expected_source, retrieved_source,
  error_category, severity, notes

Categories: LEXICAL_MISMATCH SEMANTIC_MISMATCH SOURCE_ATTRIBUTION PAGE_ATTRIBUTION
INSUFFICIENT_EVIDENCE AMBIGUITY CONTESTED_INTERPRETATION CHUNKING OCR MULTI_HOP
CORPUS_BIAS EVALUATION_ERROR OTHER

Severity: HIGH (relevant evidence missed entirely at this rank)
          MEDIUM (wrong source but topically adjacent)
          LOW (right source, wrong page/chunk)
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
RAW = ROOT / "research" / "results" / "raw"
ERR = ROOT / "research" / "error_analysis"
YAJ = "Indus Inscriptions by Yajnadevam.pdf"
TOPK = 5

chunks = [json.loads(l) for l in (IDX / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
texts = [c["text"] for c in chunks]
V = np.asarray(faiss.read_index(str(IDX / "faiss.index")).reconstruct_n(0, len(chunks)),
               dtype=np.float32)
bench = {q["id"]: q for q in json.load(BENCH.open())["questions"]}
qrels = json.loads((RAW / "qrels_used.json").read_text())["qrels"]
runs = {s: json.loads((RAW / f"{s}_run.json").read_text())
        for s in ("bm25", "dense", "hybrid_rrf")}
tokc = [tokenize(t) for t in texts]
bm25 = BM25(tokc)
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("BAAI/bge-small-en-v1.5")
qids = sorted(bench)
QV = model.encode([bench[i]["question"] for i in qids], normalize_embeddings=True,
                  convert_to_numpy=True, show_progress_bar=False).astype(np.float32)
QVi = {q: QV[k] for k, q in enumerate(qids)}

numrate = np.array([sum(1 for w in t if any(c.isdigit() for c in w)) / max(len(t), 1) for t in tokc])
dictrate = np.array([sum(1 for w in t if w.isalpha() and len(w) > 2) / max(len(t), 1) for t in tokc])

records = []
for qid in qids:
    q = bench[qid]
    rel = {int(c) for c in qrels.get(str(qid), {})}
    for sysname, run in runs.items():
        ranked = run.get(str(qid), [])
        if not rel:
            records.append({
                "question_id": qid, "system": sysname, "rank": None,
                "expected_source": None,
                "retrieved_source": chunks[ranked[0]]["source"] if ranked else None,
                "error_category": "EVALUATION_ERROR", "severity": "HIGH",
                "notes": "automatic judge produced no relevant chunk for this question; "
                         "failure of the evaluation, not of the system"})
            continue
        for rank, cid in enumerate(ranked[:TOPK], 1):
            if cid in rel:
                continue                       # this hit is fine
            exp = sorted(rel)[0]
            exp_src, got_src = chunks[exp]["source"], chunks[cid]["source"]
            cats, notes = [], []
            qtok = set(tokenize(q["question"]))
            hits = sum(1 for t in qtok if bm25.inv.get(t))
            if qtok and hits < 0.5 * len(qtok):
                cats.append("LEXICAL_MISMATCH"); notes.append(f"{hits}/{len(qtok)} query terms in corpus")
            best = float(np.max(V[sorted(rel)] @ QVi[qid]))
            if best < 0.60:
                cats.append("SEMANTIC_MISMATCH"); notes.append(f"best relevant cos={best:.2f}")
            if exp_src != got_src:
                cats.append("SOURCE_ATTRIBUTION"); notes.append(f"expected {exp_src[:26]}")
            elif chunks[exp]["page"] != chunks[cid]["page"]:
                cats.append("PAGE_ATTRIBUTION")
                notes.append(f"right source, expected p.{chunks[exp]['page']} got p.{chunks[cid]['page']}")
            if q["evidence_ceiling_cos"] < 0.62:
                cats.append("INSUFFICIENT_EVIDENCE"); notes.append(f"ceiling {q['evidence_ceiling_cos']:.2f}")
            if "possibly_ambiguous" in q["flags"]: cats.append("AMBIGUITY")
            if "contested_interpretation" in q["flags"]: cats.append("CONTESTED_INTERPRETATION")
            if len(tokc[cid]) < 90:
                cats.append("CHUNKING"); notes.append(f"retrieved chunk only {len(tokc[cid])} tokens")
            if dictrate[cid] < 0.45:
                cats.append("OCR"); notes.append(f"dictionary-word rate {dictrate[cid]:.2f}")
            if "multi_hop" in q["retrieval_types"]: cats.append("MULTI_HOP")
            if got_src == YAJ or exp_src == YAJ: cats.append("CORPUS_BIAS")
            if not cats: cats.append("OTHER")

            sev = ("LOW" if "PAGE_ATTRIBUTION" in cats else
                   "MEDIUM" if "SOURCE_ATTRIBUTION" in cats and rank > 2 else "HIGH")
            records.append({
                "question_id": qid, "system": sysname, "rank": rank,
                "expected_source": f"{exp_src} p.{chunks[exp]['page']}",
                "retrieved_source": f"{got_src} p.{chunks[cid]['page']}",
                "error_category": cats[0], "all_categories": cats, "severity": sev,
                "notes": "; ".join(notes) or "no diagnostic signal matched"})

with (ERR / "error_dataset.jsonl").open("w", encoding="utf-8") as f:
    for r in records: f.write(json.dumps(r, ensure_ascii=False) + "\n")

cat = collections.Counter(r["error_category"] for r in records)
sev = collections.Counter(r["severity"] for r in records)
bysys = collections.Counter(r["system"] for r in records)
multi = collections.Counter(c for r in records for c in r.get("all_categories", []))

print(f"error records (failing question x system x rank, top-{TOPK}): {len(records)}")
print("\nprimary category:")
for k, v in cat.most_common(): print(f"  {v:5d}  {k}")
print("\nall categories (multi-label):")
for k, v in multi.most_common(): print(f"  {v:5d}  {k}")
print("\nseverity:", dict(sev))
print("by system:", dict(bysys))

summary = {"schema": ["question_id", "system", "rank", "expected_source",
                      "retrieved_source", "error_category", "severity", "notes"],
           "top_k_examined": TOPK, "n_records": len(records),
           "primary_category_counts": dict(cat), "multilabel_counts": dict(multi),
           "severity_counts": dict(sev), "by_system": dict(bysys)}
(ERR / "error_dataset_summary.json").write_text(json.dumps(summary, indent=2))

print("\n=== representative examples (manually inspectable) ===")
for c in ("SOURCE_ATTRIBUTION", "LEXICAL_MISMATCH", "EVALUATION_ERROR", "OCR"):
    ex = [r for r in records if r["error_category"] == c][:1]
    for r in ex:
        print(f"\n[{c}] Q{r['question_id']} {bench[r['question_id']]['question'][:56]}")
        print(f"   system={r['system']} rank={r['rank']} severity={r['severity']}")
        print(f"   expected : {r['expected_source']}")
        print(f"   retrieved: {r['retrieved_source']}")
        print(f"   notes    : {r['notes'][:96]}")
print(f"\nwrote {(ERR/'error_dataset.jsonl').relative_to(ROOT)}")
