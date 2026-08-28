"""
Rebuild a CONSISTENT vector index from chunks.jsonl.

WHY (see docs/bug-index-metadata-misalignment.md):
  The live index at backend/data/index/ has 1,506 vectors but 2,112 metadata
  rows. vectordb.search() returns FAISS id i and reads metadata[i], so for
  i >= ~311 the citation returned describes a DIFFERENT chunk than the vector
  that matched. Every citation past that boundary is wrong.

WHAT THIS DOES (non-destructive):
  - reads backend/data/index/chunks.jsonl        (source of truth for text)
  - drops exact-duplicate texts (keeps first occurrence)
  - re-embeds every surviving chunk with the SAME model the system uses
  - writes a NEW index to backend/data/index_v2/
  - NEVER touches backend/data/index/

ROLLBACK: delete backend/data/index_v2/. Nothing else changes.
"""
from __future__ import annotations
import hashlib, json, pathlib, sys, time
import numpy as np, faiss

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC  = ROOT / "backend" / "data" / "index"
DST  = ROOT / "backend" / "data" / "index_v2"
MODEL = "BAAI/bge-small-en-v1.5"

def main():
    DST.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(l) for l in (SRC / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
    print(f"read {len(rows)} metadata rows", flush=True)

    seen, uniq, dup = set(), [], 0
    for r in rows:
        h = hashlib.md5(r["text"].encode("utf-8")).hexdigest()
        if h in seen:
            dup += 1
            continue
        seen.add(h)
        uniq.append(r)
    print(f"deduped: kept {len(uniq)}, dropped {dup} exact duplicates", flush=True)

    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer(MODEL)
    dim = m.get_sentence_embedding_dimension()
    print(f"embedding {len(uniq)} chunks with {MODEL} (dim={dim}) ...", flush=True)

    t0, B, vecs = time.time(), 64, []
    for i in range(0, len(uniq), B):
        batch = [r["text"] for r in uniq[i:i + B]]
        vecs.append(m.encode(batch, normalize_embeddings=True, convert_to_numpy=True,
                             show_progress_bar=False).astype(np.float32))
        done = min(i + B, len(uniq))
        print(f"  {done}/{len(uniq)}  ({time.time()-t0:.0f}s)", flush=True)
    V = np.vstack(vecs)
    assert V.shape[0] == len(uniq), "vector/metadata count mismatch"

    idx = faiss.IndexFlatIP(dim)
    idx.add(V)
    faiss.write_index(idx, str(DST / "faiss.index"))
    with (DST / "chunks.jsonl").open("w", encoding="utf-8") as f:
        for r in uniq:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    manifest = {
        "built_from": str(SRC / "chunks.jsonl"),
        "model": MODEL, "dim": dim,
        "input_rows": len(rows), "duplicates_dropped": dup, "vectors": int(idx.ntotal),
        "alignment": "vector[i] corresponds exactly to chunks.jsonl line i+1",
        "build_seconds": round(time.time() - t0, 1),
    }
    (DST / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2), flush=True)
    print("DONE", flush=True)

if __name__ == "__main__":
    main()
