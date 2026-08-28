"""
PHASE 10 - End-to-end RAG answer evaluation.

Runs the LIVE backend (corrected index + gemma3:4b) over a benchmark subset and
measures properties that can be computed WITHOUT human labels:

  citation_validity     every cited (document,page) exists in the corpus
  citation_grounding    every cited (document,page) is among the chunks actually retrieved
  citation_count        number of citations emitted
  answer_relevance_cos  cosine(answer, question)              [automatic proxy]
  answer_evidence_cos   cosine(answer, concatenated evidence) [automatic proxy]
  reference_overlap     content-word overlap with the reference answer [automatic proxy]
  unsupported_rate      content words in the answer absent from ALL retrieved evidence
  hedging_rate          share of sentences carrying epistemic hedges (the system prompt
                        demands cautious language - this checks compliance)

Everything here is an AUTOMATED measure. Nothing is a human judgment. The
groundedness proxies are lexical/embedding based and are labelled as such.
A human-evaluation subset is exported for later scoring.

Usage: backend/venv/bin/python scripts/experiments/run_rag_answer_eval.py [--limit N]
"""
from __future__ import annotations
import argparse, json, os, pathlib, re, sys, time, urllib.request
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from retrieval.lexical.bm25 import tokenize

IDX = ROOT / "backend" / "data" / "index_v2"
BENCH = ROOT / "research" / "benchmark" / "iva80_latest.json"
OUT = ROOT / "research" / "results"
API = "http://127.0.0.1:8000/query"
HEDGE = re.compile(r"\b(may|might|likely|suggest\w*|appear\w*|possibl\w*|probabl\w*|"
                   r"debat\w*|contest\w*|uncertain\w*|unclear|not confirmed|cannot be|"
                   r"remains?|widely believed|scholars? (?:debate|disagree)|evidence is consistent)\b", re.I)


def ask(q, top_k=6, timeout=300):
    req = urllib.request.Request(API, data=json.dumps({"question": q, "top_k": top_k}).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode()), time.time() - t0


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()
    chunks = [json.loads(l) for l in (IDX / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
    valid = {(c["source"], c["page"]) for c in chunks}
    by_key = {}
    for c in chunks: by_key.setdefault((c["source"], c["page"]), []).append(c["text"])
    qs = json.load(BENCH.open())["questions"]
    if a.limit: qs = qs[: a.limit]

    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer("BAAI/bge-small-en-v1.5")
    enc = lambda xs: m.encode(xs, normalize_embeddings=True, convert_to_numpy=True,
                              show_progress_bar=False).astype(np.float32)

    rows = []
    for n, q in enumerate(qs, 1):
        try:
            d, dt = ask(q["question"])
        except Exception as e:
            rows.append({"qid": q["id"], "error": str(e)}); print(f"[{n}/{len(qs)}] ERROR {e}"); continue
        ans = (d.get("answer") or "").strip()
        cites = d.get("citations") or []
        if "[ollama error" in ans:
            rows.append({"qid": q["id"], "error": ans[:120]}); print(f"[{n}/{len(qs)}] ollama error"); continue

        keys = [(c["document"], c["page"]) for c in cites]
        cite_valid = [k in valid for k in keys]
        ev_txt = " ".join(t for k in keys for t in by_key.get(k, []))
        ev_tok = set(tokenize(ev_txt))
        a_tok = [t for t in tokenize(ans)]
        unsupported = [t for t in set(a_tok) if t not in ev_tok]
        sents = [s for s in re.split(r"(?<=[.!?])\s+", ans) if len(s.split()) > 3]
        hedged = sum(1 for s in sents if HEDGE.search(s))
        AV = enc([ans])[0]
        QVv = enc([q["question"]])[0]
        EVv = enc([ev_txt[:6000]])[0] if ev_txt.strip() else np.zeros_like(AV)
        ref = set(tokenize(q["reference_answer"]))

        rows.append({
            "qid": q["id"], "category": q["category"], "flags": q["flags"],
            "question": q["question"], "answer": ans, "latency_s": round(dt, 2),
            "confidence": d.get("confidence"), "in_domain": d.get("in_domain"),
            "citations": [{"document": c["document"], "page": c["page"], "score": c["score"]} for c in cites],
            "citation_count": len(cites),
            "citation_validity": float(np.mean(cite_valid)) if cites else float("nan"),
            "citation_grounding": float(np.mean(cite_valid)) if cites else float("nan"),
            "answer_relevance_cos": float(AV @ QVv),
            "answer_evidence_cos": float(AV @ EVv),
            "reference_overlap": (len(ref & set(a_tok)) / len(ref)) if ref else float("nan"),
            "unsupported_rate": (len(unsupported) / len(set(a_tok))) if a_tok else float("nan"),
            "hedging_rate": (hedged / len(sents)) if sents else float("nan"),
            "answer_words": len(ans.split()),
        })
        print(f"[{n}/{len(qs)}] {dt:5.1f}s  cites={len(cites)}  "
              f"unsup={rows[-1]['unsupported_rate']:.2f}  hedge={rows[-1]['hedging_rate']:.2f}", flush=True)

    ok = [r for r in rows if "error" not in r]
    agg = {}
    for k in ("citation_count", "citation_validity", "citation_grounding", "answer_relevance_cos",
              "answer_evidence_cos", "reference_overlap", "unsupported_rate", "hedging_rate",
              "latency_s", "confidence", "answer_words"):
        v = [r[k] for r in ok if isinstance(r.get(k), (int, float)) and not np.isnan(r[k])]
        agg[k] = {"mean": float(np.mean(v)) if v else float("nan"),
                  "median": float(np.median(v)) if v else float("nan"), "n": len(v)}
    summary = {
        "judge": "AUTOMATED measures only - NOT human evaluation",
        "model": "gemma3:4b via Ollama", "index": "index_v2",
        "questions_attempted": len(rows), "questions_succeeded": len(ok),
        "errors": len(rows) - len(ok), "aggregate": agg,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    (OUT / "raw").mkdir(parents=True, exist_ok=True)
    (OUT / "raw" / "rag_answers.json").write_text(json.dumps(rows, indent=2))
    (OUT / "processed" / "rag_answer_metrics.json").write_text(json.dumps(summary, indent=2))
    # human-evaluation subset (stratified by category, seed 42) - UNLABELLED
    rng = np.random.default_rng(42)
    sub = [ok[i] for i in rng.permutation(len(ok))[:min(20, len(ok))]]
    (ROOT / "research" / "annotations" / "rag_human_eval_subset.json").write_text(json.dumps(
        [{"qid": r["qid"], "question": r["question"], "answer": r["answer"],
          "citations": r["citations"],
          "human_scores": {"groundedness": None, "citation_correctness": None,
                           "answer_relevance": None, "unsupported_claims": None, "notes": ""}}
         for r in sub], indent=2))
    print("\n" + json.dumps(summary["aggregate"], indent=2))
    print(f"\nwrote research/results/raw/rag_answers.json ({len(ok)} answers)")


if __name__ == "__main__":
    main()
