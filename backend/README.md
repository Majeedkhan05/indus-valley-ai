# Indus Valley AI — RAG Backend

Production-grade local RAG system. Turns the existing static site into a
ChatGPT-style domain-specific assistant grounded in your own corpus
(CISI volumes, Marshall, Mahadevan, Yajnadevam, etc.).

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────┐
│  Your PDFs  │───▶│  Chunk +     │───▶│  FAISS      │───▶│  Top-k   │
│  (CISI etc) │    │  Embed       │    │  Vector DB  │    │  Retrieve│
└─────────────┘    └──────────────┘    └─────────────┘    └────┬─────┘
                                                                │
┌─────────────┐    ┌──────────────┐    ┌─────────────┐         │
│  Browser    │◀───│  Streamed    │◀───│  Ollama     │◀────────┘
│  ChatGPT-UI │    │  with cites  │    │  (LLaMA 3)  │  +context
└─────────────┘    └──────────────┘    └─────────────┘
```

All local. All private. **Cost: $0.**

---

## One-time setup (~15 minutes)

### 1. Install Ollama
```bash
# macOS
curl -fsSL https://ollama.com/download/Ollama-darwin.zip -o /tmp/ollama.zip
# Or download manually: https://ollama.com/download

ollama serve            # leave this running in its own terminal
ollama pull llama3.1:8b # ~5 GB download
# Alternatives: ollama pull mistral, ollama pull qwen2.5:7b
```

### 2. Drop your PDFs
Copy your CISI volumes / Marshall / Mahadevan / Yajnadevam PDFs into:
```
backend/data/pdfs/
```
For example:
```bash
cp ~/Downloads/CISI*.pdf backend/data/pdfs/
cp "~/Downloads/Indus Valley Project/Indus Inscriptions by Yajnadevam.pdf" backend/data/pdfs/
cp "~/Downloads/Indus Valley Project/Authority Structure and the Evolution of Early Writing Systems 2.pdf" backend/data/pdfs/
cp "~/Downloads/Indus Valley Project/im_417_150.csv" backend/data/pdfs/
```

### 3. Bulk-ingest (one-time, ~10–30 min depending on PDFs)
```bash
cd backend
./run.sh           # creates venv + installs deps + starts server
# In another terminal:
source venv/bin/activate
python ingest_corpus.py
```

You'll see progress like:
```
Found 5 PDFs and 1 CSV
Loading embedding model: BAAI/bge-small-en-v1.5
  dim = 384
Opening CISI 1 Collections in India.pdf
  482 pages
  produced 1837 chunks
  added 1837 chunks  →  total now 1837
...
Total vectors: 14,592
```

### 4. Run
```bash
./run.sh
```

The server is now at:
- **API:**           http://localhost:8000
- **Swagger docs:**  http://localhost:8000/docs
- **Health check:**  http://localhost:8000/health

### 5. Open the website
Open `../index.html` in your browser. The chat will automatically detect
the backend and route through the RAG pipeline. The status badge will
change to `RAG · llama3.1:8b · 14592 chunks`.

---

## API endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/`                | GET  | Service info |
| `/health`          | GET  | Embedder + vector count + Ollama status |
| `/documents`       | GET  | Inventory of indexed sources |
| `/upload_pdf`      | POST | Upload one PDF (form-data, field `file`) |
| `/upload_csv`      | POST | Upload one CSV/TSV |
| `/query`           | POST | `{question, top_k, history}` → grounded answer |
| `/query_stream`    | POST | Server-Sent-Events streaming version |
| `/analyze_image`   | POST | CLIP motif match + RAG explanation |

Full Swagger UI at http://localhost:8000/docs.

---

## Tunables (env vars)

| Variable | Default | Effect |
|---|---|---|
| `IVAI_OLLAMA_HOST`   | `http://localhost:11434`     | Ollama URL |
| `IVAI_OLLAMA_MODEL`  | `llama3.1:8b`                | Which model to use |
| `IVAI_EMBED_MODEL`   | `BAAI/bge-small-en-v1.5`     | Sentence embedder |
| `IVAI_CLIP_MODEL`    | `openai/clip-vit-base-patch32` | CLIP model |

```bash
IVAI_OLLAMA_MODEL=mistral ./run.sh
```

---

## Guardrails

1. **Domain gate** (`rag/guardrails.py`) — out-of-scope queries are refused before the LLM is even called.
2. **Relevance threshold** (`rag/retrieve.py`) — if top-1 cosine < 0.30, the system says "not in corpus" instead of hallucinating.
3. **Strict system prompt** (`rag/generate.py`) — the LLM is instructed to answer ONLY from context, with inline citations.
4. **Citations always shown** — every grounded answer is accompanied by source + page numbers.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| "Ollama is not running" | `ollama serve` in another terminal |
| Model not found         | `ollama pull llama3.1:8b` |
| FAISS install fails on Mac | `pip install faiss-cpu --no-binary :all:` |
| Out of RAM during embedding | Use `IVAI_EMBED_MODEL=BAAI/bge-small-en-v1.5` (already default) |
| PDF text extraction empty | The PDF is scanned. Run OCR first: `ocrmypdf in.pdf out.pdf` |
| Slow on first query | First-time CLIP/embedder load takes ~10s. Cached after. |

---

## Reverting

The original v1 site files are in `../backup-v1-original/`. The new
`backend/` folder and `rag-client.js` are additive — the website works
exactly as before with the backend off. To roll back fully, follow
`../REVERT.md`.

---

## Legal posture

The CISI volumes (Parpola et al.), Marshall, Mackay, and Vats works are
under various copyright statuses:

- **Marshall 1931, Mackay 1937–38, Vats 1940**: public domain in India
- **CISI volumes (1987–2024)**: under copyright, used here under
  fair-dealing for academic research (Indian Copyright Act §52)
- **Yajnadevam decipherment paper**: distributed by author publicly

This setup processes them on YOUR machine for YOUR research. The model
generates paraphrased grounded answers with citations — never reproduces
substantial verbatim passages. Do **NOT** redistribute the raw indexed
text or host the corpus publicly. Keep `backend/data/index/` local.
