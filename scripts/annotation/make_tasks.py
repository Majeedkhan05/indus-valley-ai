"""
PHASE 3 - Build the human annotation task set.

Pool = union of top-K from every system under comparison (TREC-style pooling),
so the labels produced are valid for BM25, dense and hybrid alike.

Output: research/annotations/tasks.jsonl  (one (question, chunk) pair per line)
NO LABELS ARE GENERATED HERE. Grades are supplied only by human annotators.
"""
from __future__ import annotations
import json, os, pathlib, sys
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np, faiss

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from retrieval.lexical.bm25 import BM25, tokenize

IDX = ROOT / "backend" / "data" / "index_v2"
BENCH = ROOT / "research" / "benchmark" / "iva80_latest.json"
OUT = ROOT / "research" / "annotations"
POOL_K = int(os.environ.get("IVAI_POOL_K", "10"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    chunks = [json.loads(l) for l in (IDX / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
    texts = [c["text"] for c in chunks]
    V = np.asarray(faiss.read_index(str(IDX / "faiss.index")).reconstruct_n(0, len(chunks)),
                   dtype=np.float32)
    bench = json.load(BENCH.open())
    qs = bench["questions"]

    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer("BAAI/bge-small-en-v1.5")
    QV = m.encode([q["question"] for q in qs], normalize_embeddings=True,
                  convert_to_numpy=True, show_progress_bar=False).astype(np.float32)
    bm25 = BM25([tokenize(t) for t in texts])

    def rrf(ls, k=60):
        s = {}
        for l in ls:
            for r, d in enumerate(l, 1): s[d] = s.get(d, 0.0) + 1.0 / (k + r)
        return [d for d, _ in sorted(s.items(), key=lambda kv: -kv[1])]

    rows, per_q = [], []
    rng = np.random.default_rng(42)
    for i, q in enumerate(qs):
        dense = np.argsort(-(V @ QV[i]))[:POOL_K].tolist()
        lex = [d for d, _ in bm25.search(q["question"], top_k=POOL_K)]
        hyb = rrf([lex, dense])[:POOL_K]
        pool = sorted(set(dense) | set(lex) | set(hyb))
        order = rng.permutation(len(pool))          # blind: hide system identity & rank
        per_q.append(len(pool))
        for pos in order:
            d = pool[pos]
            rows.append({
                "task_id": f"q{q['id']}_c{d}",
                "qid": q["id"], "question": q["question"], "category": q["category"],
                "reference_answer": q["reference_answer"],
                "chunk_id": int(d), "source": chunks[d]["source"], "page": chunks[d]["page"],
                "chunk_text": texts[d],
                # deliberately NOT exposed to the annotator:
                "_hidden_systems": sorted(
                    ([("dense", dense.index(d) + 1)] if d in dense else []) +
                    ([("bm25", lex.index(d) + 1)] if d in lex else []) +
                    ([("hybrid", hyb.index(d) + 1)] if d in hyb else [])),
            })

    with (OUT / "tasks.jsonl").open("w", encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    meta = {"pool_depth_per_system": POOL_K, "questions": len(qs), "tasks": len(rows),
            "mean_pool_per_question": float(np.mean(per_q)),
            "min_pool": int(min(per_q)), "max_pool": int(max(per_q)),
            "presentation": "randomised per question, seed 42; system identity hidden",
            "labels_present": False,
            "estimated_person_hours_per_annotator": round(len(rows) * 15 / 3600, 1)}
    (OUT / "tasks_manifest.json").write_text(json.dumps(meta, indent=2))
    print(json.dumps(meta, indent=2))
    print(f"\nwrote {(OUT/'tasks.jsonl').relative_to(ROOT)}  ({len(rows)} tasks, NO labels)")


if __name__ == "__main__":
    main()
