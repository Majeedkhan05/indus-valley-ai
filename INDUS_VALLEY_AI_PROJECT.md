# Indus Valley AI — Full Project Documentation

> **What it is:** A local, private, scholarship-grade AI assistant for the Indus Valley Civilization. Built entirely without cloud AI — it runs completely on your laptop.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [What Problem It Solves](#2-what-problem-it-solves)
3. [Architecture at a Glance](#3-architecture-at-a-glance)
4. [Tech Stack](#4-tech-stack)
5. [File-by-File Walkthrough](#5-file-by-file-walkthrough)
6. [The Knowledge Base Pipeline](#6-the-knowledge-base-pipeline)
7. [The RAG Backend (Python)](#7-the-rag-backend-python)
8. [The Vision Module (CLIP)](#8-the-vision-module-clip)
9. [Gemini Nano (On-Device LLM)](#9-gemini-nano-on-device-llm)
10. [3D Scene System](#10-3d-scene-system)
11. [Design System](#11-design-system)
12. [Training Data & Fine-Tuning](#12-training-data--fine-tuning)
13. [Benchmark & Evaluation](#13-benchmark--evaluation)
14. [Corpus — The Four CISI Volumes](#14-corpus--the-four-cisi-volumes)
15. [What Was Built, End to End](#15-what-was-built-end-to-end)
16. [How to Run Locally](#16-how-to-run-locally)
17. [Deployment](#17-deployment)

---

## 1. Project Overview

**Indus Valley AI** is a full-stack, locally-hosted research assistant that lets anyone ask questions about the Indus Valley Civilization (IVC) and get grounded, cited answers — sourced directly from academic PDF corpora, not from a generic internet-crawled model.

The interface is an immersive website with:
- A **chat window** powered by a local LLM (via Ollama) and a FAISS vector database
- A **vision module** that lets you upload a photo of an IVC artifact and identifies it using CLIP
- **3D animated scenes** of Mohenjo-daro and Dholavira rendered in WebGL (Three.js)
- **Gemini Nano** running in-browser (Chrome's on-device model) as a lightweight inference fallback
- An **academic paper** documenting the system, with a formal evaluation benchmark

**Key design principle:** Everything runs locally. No data is sent to OpenAI, Anthropic, or any cloud service. The model, the vector store, and the embedder all live on your machine.

---

## 2. What Problem It Solves

Most people who want to learn about the Indus Valley Civilization hit two walls:

1. **Generic AI** (ChatGPT, Gemini) gives plausible-sounding but often wrong or uncited answers about IVC — a topic where the scholarship is very specialized and contested.
2. **Academic papers** are locked behind jargon and hard to search.

This project bridges the gap: it indexes the actual academic source books (the 4-volume *Corpus of Indus Seals and Inscriptions*) and lets you ask natural-language questions. Every answer comes with page-number citations from the source documents.

---

## 3. Architecture at a Glance

```
User browser
    │
    ├─ index.html / app.js          ← Single-page frontend
    ├─ three-scene.js               ← 3D WebGL scenes (Three.js)
    ├─ gemini-nano.js               ← In-browser LLM (Chrome Nano API)
    ├─ vision.js                    ← Image upload UI
    └─ rag-client.js                ← Talks to backend over HTTP
              │
              ▼
    backend/main.py (FastAPI, port 8000)
         │
         ├─ rag/embed.py            ← BAAI/bge-small-en-v1.5 (384-dim)
         ├─ rag/vectordb.py         ← FAISS flat-IP index
         ├─ rag/ingest.py           ← PDF → chunks pipeline
         ├─ rag/retrieve.py         ← Cosine retrieval (top-k = 6)
         ├─ rag/generate.py         ← Ollama LLM client + prompt builder
         ├─ rag/guardrails.py       ← Domain filter (IVC-only)
         └─ vision/clip_match.py   ← CLIP image encoder + motif search
              │
              ▼
         Ollama (local, port 11434)
         Model: gemma3:4b  (switchable via env var IVAI_OLLAMA_MODEL)
```

---

## 4. Tech Stack

| Layer | Technology | Why |
|---|---|---|
| **Frontend** | Vanilla HTML/CSS/JS | Zero build step, fast load, works on GitHub Pages |
| **3D** | Three.js (CDN) | WebGL scenes without a React overhead |
| **In-browser LLM** | Chrome Gemini Nano (`window.ai`) | Offline fallback, no server needed |
| **Backend** | FastAPI (Python 3.13) | Async, typed, auto-docs at `/docs` |
| **Embedder** | `BAAI/bge-small-en-v1.5` via `sentence-transformers` | 384-dim, fast on CPU, strong retrieval |
| **Vector DB** | FAISS (`faiss-cpu`) | In-memory flat index, no external DB needed |
| **LLM** | Ollama (local) — `gemma3:4b` default | Private, offline, swappable |
| **Vision** | OpenAI CLIP (`openai/clip-vit-base-patch32`) via HuggingFace | Image → text embedding space matching |
| **PDF OCR** | `ocrmypdf` + Tesseract | Makes scanned academic PDFs machine-readable |
| **PDF parsing** | `pypdf` | Page-level text extraction with page number tracking |
| **Paper** | LaTeX | Academic-grade typesetting |
| **Fine-tuning** | Unsloth + LoRA (Colab notebook) | Optional fine-tune of Phi-3 Mini on IVC Q&A |

---

## 5. File-by-File Walkthrough

### Frontend (root of project)

#### `index.html`
The single HTML file for the entire site. Loads Three.js, imports all JS modules, and defines the DOM structure: nav bar, hero section, 3D canvas, chat UI, vision upload panel, and the scroll-animated site sections.

#### `styles.css`
Design system implementation. Uses CSS custom properties (`--gold`, `--charcoal`, `--terracotta`) for the ancient-meets-futuristic color palette. Handles: 
- Glassmorphism cards
- Animated glowing borders on the chat window
- Responsive layout for mobile/desktop
- Dark parchment texture overlays

#### `app.js`
Main orchestrator. Handles:
- Tab/section routing
- Chat send/receive flow (calls `rag-client.js`, falls back to `gemini-nano.js` if backend is down)
- Rendering citations in the chat UI
- Connecting the vision upload result back into the chat

#### `rag-client.js`
Thin HTTP client. Sends `POST /query` to `http://127.0.0.1:8000` with `{question, top_k}`. Returns `{answer, citations, confidence, in_domain}`. Handles timeout gracefully.

#### `knowledge-base.js`
Static fallback knowledge base (JavaScript object with ~40 hard-coded Q&A pairs about IVC). Used when both the backend and Gemini Nano are unavailable (purely offline mode).

#### `gemini-nano.js`
Wrapper around Chrome's experimental `window.ai.languageModel` API (Gemini Nano, built into Chrome Canary). Creates a session with an IVC-specific system prompt and streams responses back to the chat UI. Gracefully no-ops if the API is not available.

#### `vision.js`
Handles image file drop/select UI. Sends the image as `multipart/form-data` to `POST /vision/match` on the backend. Renders the top-3 matching motifs with similarity scores and descriptions back into the chat.

#### `three-scene.js`
WebGL scene manager. Creates:
- A procedural Mohenjo-daro reconstruction (brick geometry, Great Bath, city grid)
- A Dholavira scene (signboard replica, water reservoirs)
- Orbital camera controls
- Ambient particle effects (dust motes, fireflies)

#### `three-routes.js`
Router for the 3D scenes. Listens to nav events and swaps which Three.js scene is active. Handles canvas resize on window events.

#### `data.js`
Static data file. Contains the catalog of ~60 known IVC seal motifs (unicorn, tiger, elephant, Pashupati, etc.) with descriptions, site provenance, and image paths. Used by both the vision module and the knowledge base.

#### `script-analysis.js`
Experimental module. Takes a sign sequence (IVC script glyphs entered as Unicode points) and runs frequency/bigram analysis. Does **not** attempt decipherment — just statistical patterns.

#### `gen_report.py`
Python script that reads the benchmark `results.jsonl` and generates a formatted PDF report using ReportLab. Used for the academic paper's appendix.

---

### Backend (`backend/`)

#### `backend/main.py` (280 lines)
The FastAPI application. Defines all HTTP endpoints:

| Endpoint | Method | What it does |
|---|---|---|
| `/health` | GET | Returns embedder info, vector count, document inventory |
| `/query` | POST | Full RAG pipeline: embed → retrieve → guard → generate |
| `/query/stream` | POST | Same as above but streams tokens via SSE |
| `/ingest/pdf` | POST | Upload a new PDF and add it to the index |
| `/ingest/csv` | POST | Upload a CSV of Q&A pairs |
| `/vision/match` | POST | Upload an image, get top-3 CLIP matches |
| `/documents` | GET | List all indexed documents |
| `/documents/{name}` | DELETE | Remove a document from the index |

Uses lazy singleton pattern — the embedder, FAISS index, and Ollama client are initialized once on first use, not at startup, so the server starts in ~1 second.

#### `backend/rag/embed.py` (43 lines)
Wraps `sentence_transformers.SentenceTransformer`. Default model: `BAAI/bge-small-en-v1.5` (384 dimensions). Normalizes embeddings so cosine similarity = inner product — compatible with FAISS `IndexFlatIP`. Overridable via `IVAI_EMBED_MODEL` env var.

#### `backend/rag/vectordb.py` (83 lines)
FAISS wrapper. Maintains:
- `faiss.IndexFlatIP` for vectors
- A parallel `chunks.jsonl` file that stores `{text, source, page}` metadata
- Atomic save/load so the index survives restarts

#### `backend/rag/ingest.py` (157 lines)
PDF ingestion pipeline:
1. Opens PDF with `pypdf`
2. Extracts text page by page
3. Splits into chunks of ~400 tokens with 50-token overlap
4. Embeds each chunk
5. Adds to FAISS index + appends to `chunks.jsonl`
6. Logs running totals

Handles scanned PDFs (via OCR-preprocessed copies), encoding errors, and pages with no extractable text.

#### `backend/rag/retrieve.py` (32 lines)
Takes a question, embeds it, queries FAISS for `top_k=6` nearest chunks. Returns `RetrievedChunk` dataclasses with `{text, source, page, score}`. Applies a `MIN_RELEVANCE = 0.30` cosine threshold.

#### `backend/rag/generate.py` (174 lines)
Ollama HTTP client + prompt builder:
- **System prompt** (80 lines): Mandates a 5-section answer structure (Direct Answer → Evidence → Interpretation → Alternative View → Limitation), confidence hedging vocabulary, and citation format.
- `build_prompt()`: Assembles the context block from retrieved chunks, adds conversation history (last 3 turns), injects the question.
- `OllamaClient.generate()`: Non-streaming call with 60s timeout.
- `OllamaClient.stream()`: Server-sent events streaming, yields tokens as they arrive.
- Default model: `gemma3:4b` (overridable via `IVAI_OLLAMA_MODEL`).

#### `backend/rag/guardrails.py` (56 lines)
Domain classifier. Checks whether a question is about the Indus Valley Civilization. Uses a keyword blocklist + allowlist approach. Returns `(is_in_domain: bool, reason: str)`. If out-of-domain, the API returns a polite refusal instead of hallucinating.

#### `backend/ingest_corpus.py` (63 lines)
One-shot script to bulk-ingest all PDFs in `data/pdfs/`. Skips already-indexed documents (checks by filename). Run once after adding new PDFs. Logs a full inventory at the end.

#### `backend/vision/clip_match.py`
CLIP-based image matcher:
1. Loads `openai/clip-vit-base-patch32` from HuggingFace
2. Pre-encodes all reference motif images from `data.js` at startup
3. On `/vision/match`: encodes the uploaded image, computes cosine similarity against all reference embeddings, returns top-3

---

### Paper (`paper/`)

#### `paper/main.tex`
LaTeX source for the academic paper *"IVA: A Locally-Hosted RAG System for Indus Valley Civilization Scholarship"*. Sections: Abstract, Introduction, Related Work, System Design, Corpus, Evaluation, Results, Limitations, Conclusion.

#### `paper/eval/benchmark_questions.json`
The IVA-Q benchmark: a set of questions about IVC with expected answer keywords and citation expectations. Covers: urban planning, seals & script, trade networks, water systems, decline theories, notable sites.

#### `paper/eval/run_benchmark.py` (55 lines)
Automated benchmark runner. Sends each question to the live backend, records the answer + citations + latency + confidence, writes to `results.jsonl`. Human rating step (0/1/2) is manual.

#### `paper/eval/results.jsonl`
Output of the benchmark run. Each line is a JSON object: `{id, q, expected_keywords, answer, citations, confidence, latency_s, system}`.

---

### Training (`training/`)

#### `training/training_data.jsonl`
~200 IVC-specific Q&A pairs in instruction-tuning format (`{instruction, input, output}`). Curated from the CISI volumes and secondary literature.

#### `training/finetune_colab.ipynb`
Google Colab notebook. Uses Unsloth + LoRA to fine-tune `Phi-3-mini-4k-instruct` on the training data. Runs on a free T4 GPU in ~25 minutes. Exports a GGUF file suitable for Ollama.

#### `training/extract_data.py`
Script that reads the indexed `chunks.jsonl` and auto-generates candidate Q&A pairs using a local LLM. Output is manually reviewed and merged into `training_data.jsonl`.

---

## 6. The Knowledge Base Pipeline

```
PDF (scanned)
    │
    ▼ ocrmypdf --skip-text --language eng
OCR-enhanced PDF  (adds invisible text layer over scans)
    │
    ▼ pypdf page extraction
Raw text per page
    │
    ▼ chunk(size=400, overlap=50)
Text chunks  [{text, source, page}]
    │
    ▼ BAAI/bge-small-en-v1.5
Float32 vectors  [N × 384]
    │
    ├─► FAISS IndexFlatIP  (faiss.index)
    └─► JSONL metadata     (chunks.jsonl)
```

**OCR step matters:** The CISI volumes are high-quality scans of printed books — the text layer is images, not real text. `ocrmypdf` runs Tesseract over each page and bakes in a hidden text layer. This is what makes the PDFs machine-readable. Processing all 4 volumes takes ~2 hours and produces ~950 MB of OCR-enhanced PDFs.

**Final corpus size:** 1,506 chunks across 5 documents, 384-dimensional embeddings, stored in ~2 MB of FAISS index data.

---

## 7. The RAG Backend (Python)

The core query flow (every question):

```
Question: "What material were most Indus seals made from?"
    │
    ▼ guardrails.py — is this about IVC? YES
    │
    ▼ embed.py — encode question → [384-dim float32 vector]
    │
    ▼ vectordb.py — FAISS top-6 search (cosine similarity)
    │   Returns chunks from CISI_3.1, CISI_1, Yajnadevam — all with score > 0.30
    │
    ▼ generate.py — build_prompt()
    │   Assembles: [SYSTEM PROMPT] + [6 context chunks with citations] + [question]
    │
    ▼ Ollama HTTP call → gemma3:4b
    │   Generates: structured 5-section answer with inline [source, p.N] citations
    │
    ▼ API response: {answer, citations:[{source,page,score}], confidence, in_domain}
```

**Confidence score:** Computed as the mean cosine similarity of the top-3 retrieved chunks. Below 0.30 → answer is replaced with "I couldn't find enough relevant information in the indexed corpus."

**Citation format:** `[CISI_3.1_Mohenjodaro_and_Harappa.pdf, p.47]` — so the reader can go verify.

---

## 8. The Vision Module (CLIP)

CLIP (Contrastive Language–Image Pre-training) maps both images and text into the same 512-dimensional embedding space. This means "a unicorn seal from the Indus Valley" as text and a photo of an actual unicorn seal will have similar embeddings.

**How it works here:**
1. At server startup, CLIP encodes all ~60 reference motif descriptions (text) from `data.js`
2. When a user uploads a photo of an IVC artifact, CLIP encodes the image
3. Cosine similarity between the image vector and all text vectors → top-3 matches
4. Returns: motif name, description, known sites, similarity score

**Limitation:** CLIP was not fine-tuned on IVC imagery. It works surprisingly well for iconic motifs (unicorn, elephant, tiger) but struggles with abstract geometric patterns common in IVC seals.

---

## 9. Gemini Nano (On-Device LLM)

Chrome Canary ships with Gemini Nano built in, accessible via `window.ai.languageModel`. This project uses it as a **fallback** when the Python backend isn't running — useful for demos without a terminal.

```javascript
// gemini-nano.js
const session = await window.ai.languageModel.create({
  systemPrompt: IVC_SYSTEM_PROMPT,
  temperature: 0.4,
  topK: 40
});
const stream = session.promptStreaming(question);
for await (const chunk of stream) {
  appendToChat(chunk);
}
```

**Tradeoff:** Gemini Nano has no access to the CISI corpus — it answers from its training data only. Answers are less grounded and uncited. But it works with zero setup, which is good for quick demos.

---

## 10. 3D Scene System

Built with Three.js loaded from CDN (no build step). Two scenes:

**Mohenjo-daro Scene** (`three-scene.js`):
- Procedurally generated brick grid (instanced meshes for performance)
- The Great Bath — a rectangular depression with a blue reflective plane
- Granary building with a ridged roof
- Street grid aligned to cardinal directions (IVC cities were famously grid-planned)
- Point lights simulating oil lamps at dusk

**Dholavira Scene** (`three-scene.js`):
- The signboard — the only known IVC inscription displayed publicly (10 large signs)
- Stepped water reservoirs (Dholavira had the most sophisticated water management of any IVC city)
- Rocky Gujarat terrain

**Camera:** `OrbitControls` — user can click-drag to rotate, scroll to zoom. Auto-rotates slowly if idle.

---

## 11. Design System

**Color palette** (CSS custom properties):
```css
--gold:        #C9A84C;   /* Indus seal bronze */
--charcoal:    #1A1A2E;   /* deep night */
--terracotta:  #8B4513;   /* fired clay */
--parchment:   #F5E6C8;   /* aged paper */
--accent-cyan: #00D4FF;   /* futuristic glow */
```

**Typography:** Cinzel Decorative (headings, feels ancient/Roman), Inter (body, readable).

**Key UI patterns:**
- Glassmorphism chat window: `backdrop-filter: blur(10px)` over the 3D scene
- Gold animated border on the active chat input
- Scroll-triggered fade-in for content sections
- Citation chips: small gold-bordered tags showing `[source, p.N]` inline in chat responses

---

## 12. Training Data & Fine-Tuning

The training pipeline is optional — the system works without fine-tuning. But it's there for anyone who wants a model specifically tuned on IVC.

**Data:** ~200 Q&A pairs in `training/training_data.jsonl`. Format:
```json
{"instruction": "What is the significance of the unicorn motif in IVC seals?",
 "input": "",
 "output": "The unicorn appears on more IVC seals than any other motif..."}
```

**Fine-tuning:** Unsloth + LoRA on Phi-3-mini-4k (3.8B params). LoRA rank 16, alpha 32, targeting `q_proj` and `v_proj`. ~25 minutes on Colab T4.

**Output:** A GGUF file you can `ollama create ivai-phi3 -f Modelfile` to use as a drop-in replacement for gemma3:4b.

---

## 13. Benchmark & Evaluation

**The IVA-Q benchmark** (`paper/eval/benchmark_questions.json`) tests:
- Factual recall (seal counts, site names, dates)
- Reasoning (why did IVC cities decline?)
- Uncertainty handling (does the model admit it doesn't know?)
- Citation quality (are page numbers real and relevant?)

**How to run:**
```bash
cd paper/eval
python run_benchmark.py          # runs all questions, writes results.jsonl
python run_benchmark.py --limit 10  # quick smoke test
```

**Manual rating step:** Each answer is rated 0/1/2 (wrong / partial / correct) by a human reviewer. `gen_report.py` then computes aggregate metrics and generates the paper appendix table.

---

## 14. Corpus — The Four CISI Volumes

The *Corpus of Indus Seals and Inscriptions* (CISI) is the definitive academic catalog of IVC artifacts. Edited by Asko Parpola and colleagues. All four volumes were OCR-processed and indexed:

| File | Content | Pages | Chunks |
|---|---|---|---|
| `CISI_1_Collections_in_India.pdf` | Indian museum collections | 81 pages | 132 chunks |
| `CISI_2_Collections_in_Pakistan.pdf` | Pakistani museum collections | 112 pages | 186 chunks |
| `CISI_3.1_Mohenjodaro_and_Harappa.pdf` | Major site excavations | 171 pages | 298 chunks |
| `CISI_3.2_Recent_Findings_from_India___Pakistan.pdf` | Recent excavations | 161 pages | 276 chunks |
| `Indus Inscriptions by Yajnadevam.pdf` | Script analysis | 303 pages | 1,212 chunks |
| `Authority Structure and the Evolution of Early Writing Systems 2.pdf` | Comparative epigraphy | 4 pages | 8 chunks |

**Total:** 1,506 chunks, 832 pages of academic content

---

## 15. What Was Built, End to End

Here is the full timeline of what was created in this project session:

1. **Frontend website** — `index.html`, `styles.css`, `app.js`, `data.js` — a complete themed SPA
2. **3D scenes** — Two WebGL reconstructions of IVC cities using Three.js
3. **Gemini Nano integration** — In-browser LLM fallback with IVC system prompt
4. **CLIP vision module** — Image → motif matching with `backend/vision/clip_match.py`
5. **RAG backend** — Full FastAPI server with embedding, FAISS indexing, retrieval, Ollama generation, domain guardrails, streaming, and citation support
6. **OCR pipeline** — Ran `ocrmypdf` over 4 CISI volumes (~2 hours, ~950 MB output)
7. **Corpus ingestion** — Indexed 1,506 chunks from 5 academic PDFs into FAISS
8. **Training data** — `training_data.jsonl` + Colab fine-tuning notebook
9. **Academic paper** — LaTeX paper (`paper/main.tex`) documenting the system
10. **Benchmark** — `paper/eval/` with questions, runner, and results schema
11. **Project report PDF** — Publication-grade PDF generated with ReportLab (`gen_report.py`)

---

## 16. How to Run Locally

### Prerequisites
- Python 3.11+
- [Ollama](https://ollama.com/download) installed
- A modern browser (Chrome Canary for Gemini Nano, Chrome/Firefox for everything else)

### Steps

```bash
# 1. Pull a model
ollama pull gemma3:4b

# 2. Set up the backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Add your PDFs to backend/data/pdfs/ (or symlink them)
# If PDFs are scanned, OCR them first:
#   ocrmypdf "input.pdf" "output.pdf" --skip-text --language eng

# 4. Ingest the corpus
python ingest_corpus.py

# 5. Start the backend
uvicorn main:app --host 127.0.0.1 --port 8000

# 6. Open the frontend
open index.html   # or serve with: python -m http.server 3000
```

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `IVAI_OLLAMA_MODEL` | `llama3.1:8b` | Which Ollama model to use |
| `IVAI_OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `IVAI_EMBED_MODEL` | `BAAI/bge-small-en-v1.5` | Sentence-transformers model |

To use gemma3:4b (faster, smaller):
```bash
IVAI_OLLAMA_MODEL=gemma3:4b uvicorn main:app --host 127.0.0.1 --port 8000
```

---

## 17. Deployment

The project ships as two separate deployable units:

**Frontend:** Static files only (`index.html`, `*.js`, `styles.css`, `assets/`). Deploy to:
- GitHub Pages (free, already configured in `.gitattributes`)
- Hugging Face Spaces (see `DEPLOY_HF.md`)
- Any static CDN

**Backend:** Python + Ollama. Requires a machine with:
- ~4 GB RAM for gemma3:4b
- ~8 GB RAM for llama3.1:8b
- No GPU required (runs on CPU, ~5–15s per answer)

For remote deployment, update the backend URL in `rag-client.js`:
```javascript
const BACKEND_URL = "https://your-server.com";  // default: http://127.0.0.1:8000
```

---

## Summary

| What | Details |
|---|---|
| **Purpose** | Private, grounded AI research assistant for Indus Valley scholarship |
| **Corpus** | 1,506 chunks, 832 pages, 5 academic PDFs including all 4 CISI volumes |
| **LLM** | Ollama (local) — gemma3:4b / llama3.1:8b |
| **Embedder** | BAAI/bge-small-en-v1.5 (384-dim, CPU-fast) |
| **Vector DB** | FAISS flat-IP index (~2 MB on disk) |
| **Vision** | CLIP (openai/clip-vit-base-patch32) |
| **In-browser LLM** | Chrome Gemini Nano (fallback) |
| **3D** | Three.js WebGL scenes of Mohenjo-daro & Dholavira |
| **Paper** | LaTeX, with formal IVA-Q benchmark evaluation |
| **Deployment** | Frontend → GitHub Pages; Backend → local or any Linux server |
| **Privacy** | 100% local — no data sent to any cloud service |
