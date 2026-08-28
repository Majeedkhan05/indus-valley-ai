"""
Regression test for docs/bug-index-metadata-misalignment.md

Guards the invariant vectordb.search() relies on:
    faiss_vector[i]  <->  chunks.jsonl line i+1

Run:  backend/venv/bin/python -m pytest tests/data/test_index_alignment.py -v
      (or execute directly: backend/venv/bin/python tests/data/test_index_alignment.py)
"""
from __future__ import annotations
import json, pathlib, sys
import numpy as np, faiss

ROOT = pathlib.Path(__file__).resolve().parents[2]
PROBES = [0, 1, 50, 300, 700, 899, 900, 901, 1200, 1505]
COS_MIN = 0.99


def _load(index_dir: pathlib.Path):
    rows = [json.loads(l) for l in (index_dir / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
    idx = faiss.read_index(str(index_dir / "faiss.index"))
    return rows, idx


def check_counts(index_dir: pathlib.Path) -> tuple[bool, str]:
    rows, idx = _load(index_dir)
    ok = idx.ntotal == len(rows)
    return ok, f"vectors={idx.ntotal} metadata_rows={len(rows)}"


def check_alignment(index_dir: pathlib.Path) -> tuple[bool, list[str]]:
    from sentence_transformers import SentenceTransformer
    rows, idx = _load(index_dir)
    V = np.asarray(idx.reconstruct_n(0, idx.ntotal), dtype=np.float32)
    probes = [p for p in PROBES if p < min(len(rows), idx.ntotal)]
    m = SentenceTransformer("BAAI/bge-small-en-v1.5")
    E = m.encode([rows[p]["text"] for p in probes], normalize_embeddings=True,
                 convert_to_numpy=True, show_progress_bar=False)
    msgs, ok = [], True
    for j, p in enumerate(probes):
        c = float(E[j] @ V[p])
        good = c >= COS_MIN
        ok &= good
        msgs.append(f"id={p:5d} cos={c:.3f} {'OK' if good else 'MISALIGNED'}")
    return ok, msgs


def test_live_index_counts_match():
    ok, detail = check_counts(ROOT / "backend" / "data" / "index")
    assert ok, f"live index metadata mismatch: {detail}"


def test_rebuilt_index_counts_match():
    d = ROOT / "backend" / "data" / "index_v2"
    if not (d / "faiss.index").exists():
        return
    ok, detail = check_counts(d)
    assert ok, f"index_v2 metadata mismatch: {detail}"


if __name__ == "__main__":
    for name in ("index", "index_v2"):
        d = ROOT / "backend" / "data" / name
        if not (d / "faiss.index").exists():
            print(f"[{name}] absent, skipped"); continue
        ok, detail = check_counts(d)
        print(f"[{name}] counts: {'PASS' if ok else 'FAIL'}  {detail}")
        aok, msgs = check_alignment(d)
        print(f"[{name}] alignment: {'PASS' if aok else 'FAIL'}")
        for m in msgs:
            print("   ", m)
