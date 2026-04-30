"""
PDF + CSV ingestion with semantic chunking.
============================================
- Reads PDF page-by-page (preserves page numbers for citation).
- Cleans text (drops headers/footers/page numbers).
- Splits into ~500-token chunks with ~80-token overlap.
- Computes embeddings and adds them to the FAISS index.
- Stores chunk-level metadata: {source, page, chunk_id, text}.
"""
from __future__ import annotations

import csv
import json
import re
import logging
from pathlib import Path
from typing import List, Dict

import pypdf

log = logging.getLogger("ivai.ingest")

CHUNK_SIZE_WORDS    = 380   # ≈ 500 tokens
CHUNK_OVERLAP_WORDS = 60    # ≈ 80 tokens
MIN_CHUNK_WORDS     = 30    # skip tiny fragments


# ─── text cleaning ──────────────────────────────────────────────────────────
def clean_pdf_text(text: str) -> str:
    """Remove ligatures, soft-hyphens, page-number headers, multiple blank lines."""
    text = text.replace("\xad", "")           # soft hyphen
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl")
    text = re.sub(r"-\n", "", text)            # join hyphenated line-breaks
    text = re.sub(r"\n{3,}", "\n\n", text)     # collapse blank lines
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)  # bare page-numbers
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


# ─── chunking ───────────────────────────────────────────────────────────────
def chunk_words(text: str, size: int = CHUNK_SIZE_WORDS, overlap: int = CHUNK_OVERLAP_WORDS) -> List[str]:
    words = text.split()
    if len(words) < MIN_CHUNK_WORDS:
        return []
    chunks, i = [], 0
    while i < len(words):
        seg = " ".join(words[i:i + size]).strip()
        if seg:
            chunks.append(seg)
        if i + size >= len(words):
            break
        i += (size - overlap)
    return chunks


# ─── PDF ingestion ──────────────────────────────────────────────────────────
def ingest_pdf(pdf_path: Path, embedder, vectordb, index_dir: Path) -> int:
    """Extract → clean → chunk → embed → store. Returns number of chunks added."""
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)

    log.info(f"Opening {pdf_path.name}")
    reader = pypdf.PdfReader(str(pdf_path))
    n_pages = len(reader.pages)
    log.info(f"  {n_pages} pages")

    new_chunks: List[Dict] = []
    for page_idx, page in enumerate(reader.pages, start=1):
        try:
            raw = page.extract_text() or ""
        except Exception as e:
            log.warning(f"  page {page_idx}: extract failed ({e})")
            continue
        text = clean_pdf_text(raw)
        if not text:
            continue
        for chunk_text in chunk_words(text):
            new_chunks.append({
                "source": pdf_path.name,
                "page":   page_idx,
                "text":   chunk_text,
            })
    log.info(f"  produced {len(new_chunks)} chunks")
    if not new_chunks:
        return 0

    # embed in batches
    texts  = [c["text"] for c in new_chunks]
    vectors = embedder.encode(texts)

    # add to vector db
    start_id = vectordb.count()
    for i, c in enumerate(new_chunks):
        c["chunk_id"] = start_id + i
    vectordb.add(vectors, new_chunks)
    vectordb.save()

    # write metadata index update
    meta_path = index_dir / "chunks.jsonl"
    with meta_path.open("a", encoding="utf-8") as f:
        for c in new_chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    log.info(f"  added {len(new_chunks)} chunks  →  total now {vectordb.count()}")
    return len(new_chunks)


# ─── CSV ingestion (for sign-corpus tables, sheets) ─────────────────────────
def ingest_csv(csv_path: Path, embedder, vectordb, index_dir: Path) -> int:
    """Each non-empty CSV row is treated as one chunk."""
    rows: List[Dict] = []
    with csv_path.open(encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        header = next(reader, [])
        for ri, row in enumerate(reader, start=2):
            text = " | ".join(f"{h}: {v}" for h, v in zip(header, row) if v)
            if len(text.split()) >= 4:
                rows.append({
                    "source": csv_path.name,
                    "page":   ri,           # row number used as "page"
                    "text":   text,
                })

    if not rows:
        return 0
    vectors = embedder.encode([r["text"] for r in rows])
    start_id = vectordb.count()
    for i, r in enumerate(rows):
        r["chunk_id"] = start_id + i
    vectordb.add(vectors, rows)
    vectordb.save()
    meta_path = index_dir / "chunks.jsonl"
    with meta_path.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return len(rows)


# ─── inventory ──────────────────────────────────────────────────────────────
def list_indexed_documents(index_dir: Path) -> List[Dict]:
    """Inventory of unique source documents currently in the index."""
    meta_path = index_dir / "chunks.jsonl"
    if not meta_path.exists():
        return []
    counter: Dict[str, int] = {}
    pages:   Dict[str, set] = {}
    with meta_path.open(encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
            except Exception:
                continue
            counter[obj["source"]] = counter.get(obj["source"], 0) + 1
            pages.setdefault(obj["source"], set()).add(obj.get("page", 0))
    return sorted(
        [{"source": s, "chunks": c, "pages": len(pages[s])} for s, c in counter.items()],
        key=lambda d: -d["chunks"],
    )
