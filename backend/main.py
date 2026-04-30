"""
Indus Valley AI — RAG Backend
==============================
Production FastAPI server with:
  • PDF ingestion & semantic chunking
  • sentence-transformers embeddings
  • FAISS vector store
  • Ollama LLM (LLaMA 3 / Mistral)
  • CLIP image → motif matching
  • Domain guardrails + confidence filtering
  • Source citations with page numbers
  • Streaming responses

Run:
  pip install -r requirements.txt
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field

from rag.ingest    import ingest_pdf, list_indexed_documents, ingest_csv
from rag.embed     import EmbeddingModel
from rag.vectordb  import VectorDB
from rag.retrieve  import retrieve, MIN_RELEVANCE
from rag.generate  import OllamaClient, build_prompt
from rag.guardrails import is_in_domain, OUT_OF_DOMAIN_RESPONSE
from vision.clip_match import CLIPMatcher

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("ivai")

# ─── paths ──────────────────────────────────────────────────────────────────
HERE      = Path(__file__).parent
PDF_DIR   = HERE / "data" / "pdfs"
INDEX_DIR = HERE / "data" / "index"
PDF_DIR.mkdir(parents=True, exist_ok=True)
INDEX_DIR.mkdir(parents=True, exist_ok=True)

# ─── lazy singletons ────────────────────────────────────────────────────────
_embedder: Optional[EmbeddingModel] = None
_vectordb: Optional[VectorDB]       = None
_ollama:   Optional[OllamaClient]   = None
_clip:     Optional[CLIPMatcher]    = None


def embedder() -> EmbeddingModel:
    global _embedder
    if _embedder is None:
        _embedder = EmbeddingModel()
    return _embedder


def vectordb() -> VectorDB:
    global _vectordb
    if _vectordb is None:
        _vectordb = VectorDB(INDEX_DIR, dim=embedder().dim)
        _vectordb.load_or_init()
    return _vectordb


def ollama() -> OllamaClient:
    global _ollama
    if _ollama is None:
        _ollama = OllamaClient()
    return _ollama


def clip() -> CLIPMatcher:
    global _clip
    if _clip is None:
        _clip = CLIPMatcher()
    return _clip


# ─── FastAPI app ────────────────────────────────────────────────────────────
app = FastAPI(
    title="Indus Valley AI — RAG Backend",
    version="2.0.0",
    description="Local, private, grounded AI for Indus Valley scholarship.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # static site + dev — tighten in production
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── schemas ────────────────────────────────────────────────────────────────
class QueryRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=2000)
    top_k: int = 3
    stream: bool = False
    history: List[dict] = []


class Citation(BaseModel):
    document: str
    page: Optional[int]
    score: float
    snippet: str


class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
    confidence: float
    in_domain: bool
    used_ollama: bool


# ─── endpoints ──────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "service": "Indus Valley AI — RAG backend",
        "status": "ok",
        "endpoints": ["/health", "/upload_pdf", "/upload_csv", "/query", "/analyze_image", "/documents"],
    }


@app.get("/health")
def health():
    return {
        "embedder":      embedder().model_name,
        "embedding_dim": embedder().dim,
        "vector_count":  vectordb().count(),
        "documents":     list_indexed_documents(INDEX_DIR),
        "ollama_model":  ollama().model_name,
        "ollama_ready":  ollama().ping(),
    }


@app.get("/documents")
def documents():
    return {"documents": list_indexed_documents(INDEX_DIR)}


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only .pdf files are accepted.")
    dest = PDF_DIR / file.filename
    with dest.open("wb") as f:
        f.write(await file.read())
    log.info(f"Saved {dest.name} ({dest.stat().st_size / 1e6:.1f} MB) — ingesting…")

    chunks_added = ingest_pdf(dest, embedder(), vectordb(), INDEX_DIR)
    return {"file": file.filename, "chunks_added": chunks_added, "total": vectordb().count()}


@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".csv", ".tsv")):
        raise HTTPException(400, "Only .csv/.tsv files are accepted.")
    dest = PDF_DIR / file.filename
    with dest.open("wb") as f:
        f.write(await file.read())
    chunks_added = ingest_csv(dest, embedder(), vectordb(), INDEX_DIR)
    return {"file": file.filename, "chunks_added": chunks_added, "total": vectordb().count()}


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    # 1. domain gate — refuse out-of-domain BEFORE we waste compute
    if not is_in_domain(req.question):
        return QueryResponse(
            answer=OUT_OF_DOMAIN_RESPONSE,
            citations=[], confidence=0.0,
            in_domain=False, used_ollama=False,
        )

    # 2. retrieve
    retrieved = retrieve(req.question, embedder(), vectordb(), top_k=req.top_k)
    if not retrieved or retrieved[0].score < MIN_RELEVANCE:
        return QueryResponse(
            answer=("I couldn't find a confident match in the indexed corpus. "
                    "If you have the relevant CISI volume / paper, upload it via /upload_pdf "
                    "and I'll be able to answer."),
            citations=[], confidence=0.0,
            in_domain=True, used_ollama=False,
        )

    # 3. build grounded prompt
    prompt = build_prompt(req.question, retrieved, req.history)

    # 4. generate (non-streaming)
    answer = ollama().generate(prompt)

    # 5. confidence = top retrieval score (0..1)
    confidence = float(retrieved[0].score)

    citations = [
        Citation(document=r.source, page=r.page, score=round(r.score, 3),
                 snippet=r.text[:240] + ("…" if len(r.text) > 240 else ""))
        for r in retrieved
    ]
    return QueryResponse(
        answer=answer,
        citations=citations,
        confidence=round(confidence, 3),
        in_domain=True,
        used_ollama=True,
    )


@app.post("/query_stream")
def query_stream(req: QueryRequest):
    """Server-Sent-Events streaming endpoint for ChatGPT-style typing effect."""
    if not is_in_domain(req.question):
        return StreamingResponse(
            iter([f"data: {json.dumps({'token': OUT_OF_DOMAIN_RESPONSE, 'done': True})}\n\n"]),
            media_type="text/event-stream",
        )

    retrieved = retrieve(req.question, embedder(), vectordb(), top_k=req.top_k)
    if not retrieved or retrieved[0].score < MIN_RELEVANCE:
        msg = "I couldn't find a confident match in the indexed corpus."
        return StreamingResponse(
            iter([f"data: {json.dumps({'token': msg, 'done': True})}\n\n"]),
            media_type="text/event-stream",
        )

    prompt = build_prompt(req.question, retrieved, req.history)

    def stream():
        for token in ollama().stream(prompt):
            yield f"data: {json.dumps({'token': token, 'done': False})}\n\n"
        # send citations at the end
        cites = [{"document": r.source, "page": r.page, "score": round(r.score, 3)} for r in retrieved]
        yield f"data: {json.dumps({'citations': cites, 'done': True})}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")


@app.post("/analyze_image")
async def analyze_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Image required.")
    raw = await file.read()
    matches = clip().match_motif(raw, top_k=5)

    # Compose an answer from top match + RAG retrieval on its label
    top_label = matches[0]["motif"] if matches else "Indus seal"
    rag_question = f"Tell me about the {top_label} in Indus Valley iconography."
    retrieved = retrieve(rag_question, embedder(), vectordb(), top_k=4)

    if retrieved and retrieved[0].score >= MIN_RELEVANCE:
        prompt = build_prompt(rag_question, retrieved, [])
        explanation = ollama().generate(prompt)
        cites = [
            {"document": r.source, "page": r.page, "score": round(r.score, 3)}
            for r in retrieved
        ]
    else:
        explanation = (f"This image most closely matches the '{top_label}' motif "
                       f"({matches[0]['similarity']:.1%} similarity). "
                       "Upload a CISI volume to get a full grounded explanation.")
        cites = []

    return {
        "matches": matches,
        "explanation": explanation,
        "citations": cites,
    }


# ─── module entrypoint ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
