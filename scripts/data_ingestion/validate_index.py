"""
Full validation of a vector store before it may be activated.

Re-embeds EVERY chunk with the exact production embedding configuration and
compares against the stored vector. Does not sample.

Usage: backend/venv/bin/python scripts/data_ingestion/validate_index.py index_v2
"""
from __future__ import annotations
import json, os, pathlib, sys, time
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np, faiss

ROOT = pathlib.Path(__file__).resolve().parents[2]
NAME = sys.argv[1] if len(sys.argv) > 1 else "index_v2"
D = ROOT / "backend" / "data" / NAME
MODEL = "BAAI/bge-small-en-v1.5"
COS_MIN = 0.99

rows = [json.loads(l) for l in (D / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
idx = faiss.read_index(str(D / "faiss.index"))
n = int(idx.ntotal)
print(f"index={NAME}  vectors={n}  metadata_rows={len(rows)}  dim={idx.d}")
counts_ok = (n == len(rows))
print(f"[1] count equality           : {'PASS' if counts_ok else 'FAIL'}")
if not counts_ok:
    sys.exit(1)

V = np.asarray(idx.reconstruct_n(0, n), dtype=np.float32)
norms = np.linalg.norm(V, axis=1)
norm_ok = bool(np.allclose(norms, 1.0, atol=1e-3))
print(f"[2] vectors L2-normalised    : {'PASS' if norm_ok else 'FAIL'} "
      f"(min={norms.min():.4f} max={norms.max():.4f})")

from sentence_transformers import SentenceTransformer
m = SentenceTransformer(MODEL)
dim_ok = int(m.get_sentence_embedding_dimension()) == int(idx.d)
print(f"[3] embedder dim == index.d  : {'PASS' if dim_ok else 'FAIL'}")

print(f"[4] re-embedding all {n} chunks and comparing (COS_MIN={COS_MIN}) ...", flush=True)
t0, B, cos = time.time(), 64, np.zeros(n, dtype=np.float32)
for i in range(0, n, B):
    E = m.encode([r["text"] for r in rows[i:i + B]], normalize_embeddings=True,
                 convert_to_numpy=True, show_progress_bar=False).astype(np.float32)
    cos[i:i + B] = np.einsum("ij,ij->i", E, V[i:i + B])
    if (i // B) % 5 == 0:
        print(f"    {min(i+B,n)}/{n}  ({time.time()-t0:.0f}s)", flush=True)

bad = np.where(cos < COS_MIN)[0]
print(f"\n    cosine: min={cos.min():.4f} mean={cos.mean():.4f} "
      f"p01={np.percentile(cos,1):.4f}")
print(f"[4] FULL alignment           : {'PASS' if len(bad)==0 else 'FAIL'} "
      f"({len(bad)}/{n} below threshold)")
for i in bad[:10]:
    print(f"      id={i} cos={cos[i]:.4f} {rows[i]['source'][:40]} p.{rows[i]['page']}")

# spot-report the required id classes
classes = {"first": [0, 1, 2],
           "early": [5, 10, 50, 100],
           "boundary(~311)": [305, 310, 311, 312, 320],
           "random": sorted(np.random.default_rng(42).choice(n, 6, replace=False).tolist()),
           "late": [n - 50, n - 10, n - 5],
           "final": [n - 1]}
print("\n    required id classes:")
for label, ids in classes.items():
    ids = [i for i in ids if 0 <= i < n]
    print(f"      {label:16s} " + " ".join(f"{i}:{cos[i]:.3f}" for i in ids))

report = {
    "index": NAME, "vectors": n, "metadata_rows": len(rows), "dim": int(idx.d),
    "count_equality": counts_ok, "vectors_normalised": norm_ok,
    "embedder_dim_matches": dim_ok, "model": MODEL, "cos_min_threshold": COS_MIN,
    "full_scan": {"checked": n, "below_threshold": int(len(bad)),
                  "cos_min": float(cos.min()), "cos_mean": float(cos.mean()),
                  "cos_p01": float(np.percentile(cos, 1))},
    "id_classes": {k: {str(i): float(cos[i]) for i in v if 0 <= i < n} for k, v in classes.items()},
    "verdict": "PASS" if (counts_ok and norm_ok and dim_ok and len(bad) == 0) else "FAIL",
    "seconds": round(time.time() - t0, 1),
}
out = ROOT / "experiments" / "analysis" / f"validation_{NAME}.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2))
print(f"\nVERDICT: {report['verdict']}   -> {out.relative_to(ROOT)}")
sys.exit(0 if report["verdict"] == "PASS" else 1)
