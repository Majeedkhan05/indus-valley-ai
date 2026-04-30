"""
Bulk-ingest the entire Indus corpus before starting the server.
================================================================
Run once after dropping all your CISI / Marshall / Mahadevan PDFs into
backend/data/pdfs/.

Usage:
    cd backend
    python ingest_corpus.py
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

from rag.embed    import EmbeddingModel
from rag.vectordb import VectorDB
from rag.ingest   import ingest_pdf, ingest_csv, list_indexed_documents

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("ivai.bulk")


def main() -> int:
    here    = Path(__file__).parent
    pdf_dir = here / "data" / "pdfs"
    idx_dir = here / "data" / "index"
    pdf_dir.mkdir(parents=True, exist_ok=True)
    idx_dir.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(pdf_dir.glob("*.pdf"))
    csvs = sorted(pdf_dir.glob("*.csv")) + sorted(pdf_dir.glob("*.tsv"))
    if not pdfs and not csvs:
        log.error(f"No PDFs or CSVs found in {pdf_dir}")
        log.error("Drop your CISI / Marshall / Mahadevan files there and re-run.")
        return 1

    log.info(f"Found {len(pdfs)} PDFs and {len(csvs)} CSVs")
    embedder = EmbeddingModel()
    vdb      = VectorDB(idx_dir, dim=embedder.dim)
    vdb.load_or_init()

    for p in pdfs:
        try:
            ingest_pdf(p, embedder, vdb, idx_dir)
        except Exception as e:
            log.error(f"Failed to ingest {p.name}: {e}")
    for c in csvs:
        try:
            ingest_csv(c, embedder, vdb, idx_dir)
        except Exception as e:
            log.error(f"Failed to ingest {c.name}: {e}")

    log.info("Done. Inventory:")
    for d in list_indexed_documents(idx_dir):
        log.info(f"  • {d['source']}  →  {d['chunks']} chunks across {d['pages']} pages")
    log.info(f"Total vectors: {vdb.count()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
