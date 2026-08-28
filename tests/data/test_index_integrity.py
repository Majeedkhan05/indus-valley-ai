"""
Permanent regression suite for the citation-integrity invariant.

Guards docs/bug-index-metadata-misalignment.md from recurring.

Run:
  backend/venv/bin/python -m pytest tests/data/test_index_integrity.py -v
  backend/venv/bin/python tests/data/test_index_integrity.py        # no pytest needed
"""
from __future__ import annotations
import json, os, pathlib, sys, tempfile

# The embedding model is already cached locally; avoid any network round-trip so
# the suite runs deterministically offline.
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

import numpy as np
import faiss

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from rag.vectordb import VectorDB, IndexIntegrityError   # noqa: E402

LIVE      = ROOT / "backend" / "data" / "index"
CORRECTED = ROOT / "backend" / "data" / "index_v2"
DIM       = 384
EMBED_MODEL = "BAAI/bge-small-en-v1.5"

_model = None
def embedder():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


# ── fixtures ────────────────────────────────────────────────────────────────
def make_store(tmp: pathlib.Path, n_vec: int, n_meta: int, dim: int = DIM):
    """Build a store with a deliberately chosen vector/metadata count."""
    tmp.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(42)
    v = rng.normal(size=(n_vec, dim)).astype(np.float32)
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    idx = faiss.IndexFlatIP(dim)
    idx.add(v)
    faiss.write_index(idx, str(tmp / "faiss.index"))
    with (tmp / "chunks.jsonl").open("w", encoding="utf-8") as f:
        for i in range(n_meta):
            f.write(json.dumps({"text": f"chunk {i}", "source": "fixture.pdf", "page": i}) + "\n")
    return tmp


# ── 1. count equality ───────────────────────────────────────────────────────
def test_counts_match_corrected_index():
    db = VectorDB(CORRECTED, dim=DIM)
    db.load_or_init()
    assert db.index.ntotal == len(db.metadata)
    assert db.integrity_ok


def test_live_legacy_index_is_rejected():
    """The legacy index MUST hard-fail. This is the incident being guarded."""
    db = VectorDB(LIVE, dim=DIM)
    try:
        db.load_or_init()
    except IndexIntegrityError as e:
        assert "CITATION INTEGRITY FAILURE" in str(e)
        assert not db.integrity_ok
        return
    raise AssertionError("legacy index loaded without error - guard is not working")


# ── 2. embedding dimension ──────────────────────────────────────────────────
def test_dimension_mismatch_hard_fails():
    with tempfile.TemporaryDirectory() as td:
        d = make_store(pathlib.Path(td) / "s", 10, 10, dim=128)
        db = VectorDB(d, dim=384)                 # embedder says 384, index is 128
        try:
            db.load_or_init()
        except IndexIntegrityError as e:
            assert "DIMENSION MISMATCH" in str(e)
            return
        raise AssertionError("dimension mismatch was not caught")


# ── 3/4. metadata schema and validity ───────────────────────────────────────
def test_metadata_missing_required_fields_hard_fails():
    with tempfile.TemporaryDirectory() as td:
        d = pathlib.Path(td) / "s"; make_store(d, 3, 3)
        with (d / "chunks.jsonl").open("w", encoding="utf-8") as f:
            f.write(json.dumps({"text": "a", "source": "x.pdf", "page": 1}) + "\n")
            f.write(json.dumps({"text": "b", "page": 2}) + "\n")          # no source
            f.write(json.dumps({"text": "c", "source": "x.pdf", "page": 3}) + "\n")
        db = VectorDB(d, dim=DIM)
        try:
            db.load_or_init()
        except IndexIntegrityError as e:
            assert "METADATA SCHEMA FAILURE" in str(e)
            return
        raise AssertionError("missing metadata field was not caught")


def test_corrected_index_metadata_is_well_formed():
    rows = [json.loads(l) for l in (CORRECTED / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
    assert rows, "corrected index has no metadata"
    for i, m in enumerate(rows):
        assert isinstance(m.get("text"), str) and m["text"].strip(), f"row {i} empty text"
        assert isinstance(m.get("source"), str) and m["source"], f"row {i} bad source"
        assert isinstance(m.get("page"), int) and m["page"] >= 0, f"row {i} bad page"


def test_corrected_index_has_no_duplicate_texts():
    """De-duplication must have actually worked (dupes crowd out top-k slots)."""
    import hashlib
    rows = [json.loads(l) for l in (CORRECTED / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
    h = [hashlib.md5(r["text"].encode()).hexdigest() for r in rows]
    assert len(set(h)) == len(h), f"{len(h) - len(set(h))} duplicate chunk texts remain"


# ── 5. one-to-one vector <-> metadata mapping ───────────────────────────────
def test_every_vector_maps_to_exactly_one_metadata_record():
    db = VectorDB(CORRECTED, dim=DIM)
    db.load_or_init()
    n = int(db.index.ntotal)
    assert n == len(db.metadata)
    for i in (0, n // 2, n - 1):
        assert isinstance(db.metadata[i], dict)
    # reconstruct_n must yield exactly n vectors of the right width
    V = db.index.reconstruct_n(0, n)
    assert V.shape == (n, DIM)


# ── 6. retrieved result resolves to the intended chunk ──────────────────────
def test_retrieval_resolves_to_intended_source_chunk():
    """Query with the embedding of a known chunk; rank-1 must be that chunk."""
    db = VectorDB(CORRECTED, dim=DIM)
    db.load_or_init()
    m = embedder()
    for probe in (0, 5, 250, 600, 900, len(db.metadata) - 1):
        target = db.metadata[probe]
        q = m.encode([target["text"]], normalize_embeddings=True,
                     convert_to_numpy=True, show_progress_bar=False).astype(np.float32)
        hits = db.search(q, top_k=1)
        assert hits, f"probe {probe}: no hit"
        top = hits[0]
        assert top["source"] == target["source"] and top["page"] == target["page"], (
            f"probe {probe}: citation resolved to {top['source']} p.{top['page']} "
            f"but chunk is {target['source']} p.{target['page']}")
        assert top["score"] > 0.99, f"probe {probe}: self-similarity {top['score']:.3f}"


# ── 7. corrupted fixture refuses to start ───────────────────────────────────
def test_corrupted_fixture_more_metadata_than_vectors_refuses():
    """Exactly the live failure shape: metadata longer than the index."""
    with tempfile.TemporaryDirectory() as td:
        d = make_store(pathlib.Path(td) / "s", n_vec=1506, n_meta=2112)
        db = VectorDB(d, dim=DIM)
        try:
            db.load_or_init()
        except IndexIntegrityError as e:
            assert "1506 vectors but 2112 metadata rows" in str(e)
            assert not db.integrity_ok
            return
        raise AssertionError("corrupted fixture (meta > vectors) was accepted")


def test_corrupted_fixture_more_vectors_than_metadata_refuses():
    with tempfile.TemporaryDirectory() as td:
        d = make_store(pathlib.Path(td) / "s", n_vec=100, n_meta=40)
        db = VectorDB(d, dim=DIM)
        try:
            db.load_or_init()
        except IndexIntegrityError:
            return
        raise AssertionError("corrupted fixture (vectors > meta) was accepted")


def test_search_refused_before_verification():
    """search() must not run on an unverified store."""
    db = VectorDB(CORRECTED, dim=DIM)          # deliberately NOT calling load_or_init
    try:
        db.search(np.zeros((1, DIM), dtype=np.float32), top_k=1)
    except IndexIntegrityError as e:
        assert "integrity was never verified" in str(e)
        return
    raise AssertionError("search ran on an unverified store")


def test_add_rejects_mismatched_batch():
    with tempfile.TemporaryDirectory() as td:
        db = VectorDB(pathlib.Path(td) / "s", dim=DIM)
        db.load_or_init()
        try:
            db.add(np.zeros((3, DIM), dtype=np.float32), [{"text": "a", "source": "s", "page": 1}])
        except IndexIntegrityError:
            return
        raise AssertionError("add() accepted a mismatched batch")


if __name__ == "__main__":
    tests = [(n, o) for n, o in sorted(globals().items())
             if n.startswith("test_") and callable(o)]
    passed = failed = 0
    for name, fn in tests:
        try:
            fn(); print(f"  PASS  {name}"); passed += 1
        except Exception as e:
            print(f"  FAIL  {name}: {type(e).__name__}: {e}"); failed += 1
    print(f"\n{passed} passed, {failed} failed, {len(tests)} total")
    sys.exit(1 if failed else 0)
