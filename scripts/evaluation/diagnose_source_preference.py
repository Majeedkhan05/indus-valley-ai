"""
E004 - (a) Corpus accounting  (b) Diagnostics for retrieval source preference.

(a) Recomputes corpus composition PROGRAMMATICALLY at every stage:
    raw rows -> duplicate rows -> deduplicated rows -> unique corpus.
    No proportion is hard-coded.

(b) Yajnadevam is retrieved far below its corpus share and CISI_1 far above it.
    CAUSE IS UNKNOWN. This script measures candidate explanatory factors only.
    It does NOT assert a cause.

Usage: backend/venv/bin/python scripts/evaluation/diagnose_source_preference.py
"""
from __future__ import annotations
import collections, hashlib, json, os, pathlib, re, sys, time
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np, faiss

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from retrieval.lexical.bm25 import tokenize

LEG = ROOT / "backend" / "data" / "index" / "chunks.jsonl"
COR = ROOT / "backend" / "data" / "index_v2"
BENCH = ROOT / "paper" / "eval" / "benchmark_questions.json"
OUT = ROOT / "experiments" / "results" / "E004_corpus_and_source_preference"
WORD = re.compile(r"^[a-z]{2,}$")

# ---------- (a) corpus accounting -------------------------------------------
raw = [json.loads(l) for l in LEG.open(encoding="utf-8") if l.strip()]
h = [hashlib.md5(r["text"].encode()).hexdigest() for r in raw]
cnt = collections.Counter(h)
dup_rows = sum(v - 1 for v in cnt.values() if v > 1)
dedup = [json.loads(l) for l in (COR / "chunks.jsonl").open(encoding="utf-8") if l.strip()]

def shares(rows):
    c = collections.Counter(r["source"] for r in rows); t = sum(c.values())
    return {k: {"chunks": v, "share": v / t} for k, v in c.most_common()}, t

raw_sh, raw_t = shares(raw)
ded_sh, ded_t = shares(dedup)
accounting = {
    "raw_rows": raw_t, "unique_texts": len(cnt), "duplicate_rows": dup_rows,
    "deduplicated_rows": ded_t,
    "arithmetic_check": raw_t - dup_rows == ded_t,
    "by_source_raw": raw_sh, "by_source_deduplicated": ded_sh,
}
cisi = sum(v["share"] for k, v in ded_sh.items() if k.startswith("CISI"))
yaj = next((v["share"] for k, v in ded_sh.items() if "Yajnadevam" in k), 0.0)
accounting["recomputed"] = {"yajnadevam_share": yaj, "cisi_share": cisi}

print("=== (a) CORPUS ACCOUNTING (recomputed, nothing hard-coded) ===")
print(f"  raw rows            : {raw_t}")
print(f"  unique texts        : {len(cnt)}")
print(f"  duplicate rows      : {dup_rows}")
print(f"  deduplicated corpus : {ded_t}   (check {raw_t}-{dup_rows}=={ded_t}: {accounting['arithmetic_check']})")
print(f"  Yajnadevam share    : {yaj*100:.1f}%   (raw was {raw_sh['Indus Inscriptions by Yajnadevam.pdf']['share']*100:.1f}%)")
print(f"  CISI combined share : {cisi*100:.1f}%")

# ---------- (b) diagnostics --------------------------------------------------
idx = faiss.read_index(str(COR / "faiss.index"))
V = np.asarray(idx.reconstruct_n(0, idx.ntotal), dtype=np.float32)
questions = json.load(BENCH.open())["questions"]
from sentence_transformers import SentenceTransformer
m = SentenceTransformer("BAAI/bge-small-en-v1.5")
QV = m.encode([q["q"] for q in questions], normalize_embeddings=True,
              convert_to_numpy=True, show_progress_bar=False).astype(np.float32)

by_src = collections.defaultdict(list)
for i, r in enumerate(dedup):
    by_src[r["source"]].append(i)

centroid = V.mean(axis=0); centroid /= np.linalg.norm(centroid)
qcent = QV.mean(axis=0); qcent /= np.linalg.norm(qcent)
qvocab = set()
for q in questions:
    qvocab |= set(tokenize(q["q"])) | set(tokenize(q["ground_truth"]))

diag = {}
for src, ids in by_src.items():
    txts = [dedup[i]["text"] for i in ids]
    toks = [tokenize(t) for t in txts]
    lens = np.array([len(t) for t in toks])
    allw = [w for tk in toks for w in tk]
    dictish = sum(1 for w in allw if WORD.match(w)) / max(len(allw), 1)   # OCR-quality proxy
    digitish = sum(1 for w in allw if any(ch.isdigit() for ch in w)) / max(len(allw), 1)
    vocab = set(allw)
    ov = len(vocab & qvocab) / max(len(qvocab), 1)
    sub = V[ids]
    sim_q = float((sub @ QV.T).mean())          # mean similarity to all queries
    diag[src] = {
        "chunks": len(ids),
        "corpus_share": len(ids) / len(dedup),
        "mean_tokens_per_chunk": float(lens.mean()),
        "median_tokens_per_chunk": float(np.median(lens)),
        "dictionary_word_rate": dictish,
        "numeric_token_rate": digitish,
        "vocab_size": len(vocab),
        "query_vocab_coverage": ov,
        "mean_cos_to_all_queries": sim_q,
        "mean_cos_to_corpus_centroid": float((sub @ centroid).mean()),
        "mean_cos_to_query_centroid": float((sub @ qcent).mean()),
    }

print("\n=== (b) SOURCE DIAGNOSTICS (measurements only - no causal claim) ===")
hdr = f"{'source':<44}{'share':>7}{'tok/chunk':>10}{'dictwd':>8}{'num':>7}{'qvocab':>8}{'cos→q':>8}"
print(hdr)
for s, d in sorted(diag.items(), key=lambda kv: -kv[1]["corpus_share"]):
    print(f"{s[:43]:<44}{d['corpus_share']*100:6.1f}%{d['mean_tokens_per_chunk']:10.0f}"
          f"{d['dictionary_word_rate']:8.2f}{d['numeric_token_rate']:7.2f}"
          f"{d['query_vocab_coverage']:8.3f}{d['mean_cos_to_all_queries']:8.3f}")

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "corpus_accounting.json").write_text(json.dumps(accounting, indent=2))
(OUT / "source_diagnostics.json").write_text(json.dumps(diag, indent=2))
print(f"\nwrote {OUT.relative_to(ROOT)}")
print("\nCAUSE OF SOURCE PREFERENCE: still UNKNOWN. "
      "These are correlates, not a demonstrated mechanism.")
