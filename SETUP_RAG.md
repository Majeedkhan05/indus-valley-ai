# Setup — RAG-powered Indus Valley AI

A 3-step path from the current static site to a full ChatGPT-style
domain-specific AI grounded in your CISI / Marshall / Mahadevan corpus.

## Step 1 — Install Ollama (5 min)

```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Then in a separate terminal, leave running:
ollama serve

# Pull the LLM (one-time ~5 GB download):
ollama pull llama3.1:8b
```

## Step 2 — Drop your PDFs

```bash
cd indus-valley/backend
mkdir -p data/pdfs

# Copy your existing PDFs:
cp ~/Downloads/CISI*.pdf                                              data/pdfs/
cp "~/Downloads/Indus Valley Project/Indus Inscriptions by Yajnadevam.pdf"  data/pdfs/
cp "~/Downloads/Indus Valley Project/Authority Structure"*.pdf        data/pdfs/
cp "~/Downloads/Indus Valley Project/im_417_150.csv"                  data/pdfs/
```

## Step 3 — Run

```bash
cd indus-valley/backend
./run.sh                    # creates venv, installs deps, starts FastAPI

# In a second terminal — one-time bulk ingest:
source venv/bin/activate
python ingest_corpus.py
```

Then refresh `index.html` in your browser. The chat status badge will
flip to **`RAG · llama3.1:8b · N chunks`** when it detects the backend.

## What changes when the backend is on

| Mode | Off | On |
|---|---|---|
| Answer source | 71 KB topics (keyword) | Your full corpus (semantic) |
| Generation | Pre-written paragraphs | Real LLM (Ollama) |
| Citations | Generic ("Marshall 1931") | Specific (`CISI 1, p. 247`) |
| Style | Static | ChatGPT-style streaming |
| Out-of-domain | KB rejection | Stronger gate + threshold |
| Hallucinations | None (only KB) | Blocked by grounding + citations |
| Image upload | Heuristic vision.js | Heuristic + CLIP semantic match |

The static site **always works** even if the backend is off — it falls
back to the keyword KB.

---

## Architecture

```
indus-valley/
├── index.html / app.js / styles.css       ← unchanged static site
├── knowledge-base.js                      ← 71 KB topics (fallback)
├── rag-client.js                          ← bridge to backend (NEW)
├── script-analysis.js                     ← analytics module (NEW)
├── backend/                               ← RAG service (NEW)
│   ├── main.py                              FastAPI server
│   ├── ingest_corpus.py                     bulk-ingest PDFs
│   ├── run.sh                               launcher
│   ├── requirements.txt
│   ├── README.md
│   ├── rag/
│   │   ├── ingest.py                        PDF/CSV chunking
│   │   ├── embed.py                         sentence-transformers
│   │   ├── vectordb.py                      FAISS persistence
│   │   ├── retrieve.py                      top-k + threshold
│   │   ├── generate.py                      Ollama integration
│   │   └── guardrails.py                    domain gate
│   ├── vision/
│   │   └── clip_match.py                    CLIP motif matching
│   └── data/
│       ├── pdfs/                            ← drop CISI/Marshall here
│       └── index/                             FAISS + chunk metadata
├── training/                              ← LLaMA fine-tune pipeline (optional)
└── backup-v1-original/                    ← rollback safe copy
```

## What's automatic vs what you do

✅ **Already done by Claude:**
- Backend code (FastAPI, RAG, CLIP, embeddings, guardrails)
- Frontend connector (`rag-client.js`)
- Streaming UI with citations
- Bulk-ingest script
- Setup scripts and docs

⚙️ **You need to:**
1. Install Ollama (`ollama pull llama3.1:8b`)
2. Drop PDFs in `backend/data/pdfs/`
3. Run `./run.sh` then `python ingest_corpus.py`
4. Refresh the browser

That's it. No fine-tuning required — RAG over your own corpus is more
accurate and current than fine-tuning anyway.
