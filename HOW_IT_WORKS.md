# Indus Valley AI — How It Works
**A complete project explanation for board members & professors**

> A concise, honest, technical-yet-readable walkthrough of what was built, how, and why.

---

## 1.  The 30-second pitch

**Indus Valley AI** is a **domain-restricted research assistant** for the Indus / Harappan
Civilization (c. 3300–1300 BCE), **built end-to-end from scratch** by AI Hub at Mahindra
University. It runs entirely in the browser, **uses zero external paid APIs**, and no
data ever leaves the user's device.

Every answer is **grounded** — drawn from a hand-curated scholarly knowledge base we wrote
from primary sources, or directly from uploaded scholarly PDFs — and **structured** in five
parts: *Direct Answer → Evidence → Interpretation → Alternative View → Limitation*.

Cost to operate: **₹0**.  Privacy: **100 %**.  Hostable on any static web server
(GitHub Pages, Hugging Face Spaces, Netlify, etc.).

### What "from scratch" honestly means here

| Built from scratch by us | Open-source models we use (no API calls) |
|---|---|
| ✅ The 71-topic knowledge base — every word | ⚙️ LLaMA 3.2 (Meta, open weights) |
| ✅ All ~7,000 lines of HTML / CSS / JS | ⚙️ Sentence-transformers BGE (open weights) |
| ✅ Two procedural 3D WebGL scenes | ⚙️ OpenAI CLIP (Apache 2.0, open weights) |
| ✅ Custom canvas image-vision algorithm | ⚙️ Gemini Nano (built into Chrome) |
| ✅ FastAPI RAG backend (953 lines) | ⚙️ FAISS, FastAPI, Three.js (libraries) |
| ✅ Computational analysis dashboard | |
| ✅ Domain gate, guardrails, citation system | |
| ✅ Design system + visual identity | |

**We did NOT train an LLM from scratch** — that costs ₹10 crore+ and 6 months of GPU time.
We did engineer the **entire system around** existing open-source pre-trained models, which
is what every modern AI startup does (including OpenAI, Anthropic, and Google when they
fine-tune on top of base models).

---

## 2.  Is it an LLM or an SLM?

Both, depending on which mode is active. Honest breakdown:

| Mode | Model | Where it runs | Use |
|---|---|---|---|
| **Curated KB** (default) | Not an LLM — pure keyword matching over 71 hand-written scholarly topics | Browser | Fast, instant, deterministic, demo-grade |
| **Gemini Nano** (optional) | Small Language Model (~1.8 B params, on-device) | User's Chrome browser | Adds an extra paragraph of contextual reasoning |
| **RAG Backend** (optional) | LLaMA 3.2 (Small Language Model, 1–3 B params) running through Ollama, grounded in retrieved PDF chunks | User's local machine | Full ChatGPT-style answers from your own scholarly corpus |

So strictly, the system uses **two SLMs (Gemini Nano + LLaMA 3.2)** plus the curated KB.
We did **NOT train an LLM from scratch** — that would cost ₹8 crore+ and 6 months of GPU
time. We did **engineer a system around existing open-source SLMs** that produces answers
specialised to one domain.

---

## 3.  Project timeline — what we built, in order

### Phase 1 — Foundation (the static site)
1. Designed a 13-section single-page application: hero → ticker → about → AI chat →
   pillars → seal gallery → cities → trade routes → timeline → motifs → script →
   computational analysis → research → CTA.
2. Built two real-time **3D WebGL scenes** with Three.js — the hero seal (procedurally
   generated unicorn motif) and the trade-routes globe (9 cities, 8 arc routes, particle
   dust ambience).
3. Designed a custom visual system: Cormorant Garamond × Inter × JetBrains Mono;
   charcoal/gold palette modelled on fired Harappan steatite.
4. Implemented custom cursor, magnetic-hover buttons, scroll-spine navigation,
   IntersectionObserver-based reveal animations.

### Phase 2 — The curated knowledge base
5. Hand-wrote **71 scholarly topics** drawn from primary public-domain sources:
   Marshall 1931, Mackay 1937–38, Vats 1940, ASI Annual Reports, Wheeler 1947,
   Mahadevan 1977, B.B. Lal, S.R. Rao, Jarrige (Mehrgarh), and the recent Yajnadevam +
   Authority Structure papers.
6. Each topic carries: *trigger keywords*, *title*, *4–8 paragraph body*,
   *source citation* (e.g. "Marshall 1931; Wheeler 1947").
7. Implemented a **two-layer domain gate**: an in-domain keyword whitelist + an
   out-of-scope blocklist (bitcoin, iPhone, IPL, etc.) — so the system politely
   refuses out-of-domain questions instead of making things up.

### Phase 3 — The seal corpus
8. Ingested **92 real Harappan seal photographs** from the Indus-Seal-Dataset
   (originally up to 135 numbered folders) into `assets/seals/`.
9. Built a clickable **seal gallery** with a modal viewer.
10. Wrote **client-side computer vision** in `vision.js` — pure HTML-canvas pixel
    statistics: brightness, sepia warmth, edge density (Sobel-light), aspect ratio,
    dominant hue. Heuristically classifies uploaded images into seal / script /
    artifact / map / illustration / site-photo categories. **Zero API calls.**

### Phase 4 — Computational analysis section
11. Compiled **published Mahadevan 1977 + Parpola 1994 statistics** into a structured
    JS module (`script-analysis.js`):
    *frequency analysis* (top 20 signs), *positional analysis* (initial / medial /
    final preferences), *bigram analysis* (most frequent sign pairs), *Z-score
    significance* (statistical confidence), *length distribution*, and *collocation
    clusters*.
12. Built six animated dashboard cards rendering this data live in the browser.

### Phase 5 — On-device LLM (Gemini Nano)
13. Wired up `window.LanguageModel` (Chrome 127+ built-in API) so that when the user
    is on a recent Chrome with Gemini Nano enabled, **a Small Language Model running on
    the user's own GPU adds an enrichment paragraph after the curated answer**.
14. Hard-coded a domain-locked system prompt enforcing the 5-part answer structure,
    confidence controls, and redundancy rules.

### Phase 6 — Full RAG pipeline (production backend)
15. Wrote a **FastAPI backend** in Python (~950 lines): `/upload_pdf`, `/upload_csv`,
    `/query`, `/query_stream` (streaming SSE), `/analyze_image`, `/health`,
    `/documents`.
16. PDF ingestion (`rag/ingest.py`): page-by-page text extraction with `pypdf`,
    cleaning (ligatures, soft-hyphens, page-numbers), semantic chunking (~380 words
    with 60-word overlap, page-tagged for citation).
17. Embeddings (`rag/embed.py`): `BAAI/bge-small-en-v1.5` (sentence-transformers) —
    384-dim, normalized, fast on CPU.
18. Vector store (`rag/vectordb.py`): FAISS IndexFlatIP with persistence to disk —
    inner product on normalized vectors == cosine similarity.
19. Retrieval (`rag/retrieve.py`): top-k semantic search with a 0.30 cosine threshold
    — below threshold the system says "not in indexed corpus" instead of hallucinating.
20. LLM generation (`rag/generate.py`): integration with **Ollama** running
    LLaMA 3.2 (1B–3B). The system prompt enforces the 5-part structure
    (Direct Answer → Evidence → Interpretation → Alternative View → Limitation).
21. Image understanding (`vision/clip_match.py`): OpenAI CLIP (ViT-Base-Patch32)
    matching uploaded images against a 19-motif text catalogue.

### Phase 7 — The full corpus
22. **OCR pipeline** for the four CISI volumes (Parpola et al.'s *Corpus of Indus
    Seals and Inscriptions*, ~900 MB total). They are scanned image PDFs — `pypdf`
    extracts zero text, so we run `ocrmypdf` (Tesseract) to add a searchable text
    layer, then re-ingest them into FAISS for citation-grade retrieval.
23. Already indexed: Yajnadevam *Indus Inscriptions* (303 chunks), Authority
    Structure paper (4 chunks), indusscript_net (4 chunks).

### Phase 8 — Polish + scope tightening
24. Removed video-generation feature (not aligned with the scholarly-research scope).
25. Optimized cursor → translate3d, GPU compositing, instant dot, lerp-snappy ring,
    throttled spotlight.
26. Backed up the original v1 site to `backup-v1-original/` for safe rollback.
27. Generated a publication-grade PDF project report
    (`Indus_Valley_AI_Project_Report.pdf`).

---

## 4.  How a question flows through the system

```
   ┌────────────────────────────────────────────────────────────────┐
   │  USER TYPES A QUESTION INTO THE CHAT                            │
   └─────────────────────┬──────────────────────────────────────────┘
                         │
            ┌────────────▼────────────┐
            │  Domain gate            │   ✗ out of scope → polite refusal
            │  (keyword whitelist +   │
            │   out-of-scope regex)   │
            └────────────┬────────────┘
                         │ ✓ in domain
                         │
   ┌─────────────────────┴────────────────────────────────────────────┐
   │                                                                   │
   │   Is the RAG backend running?                                     │
   │                                                                   │
   │   YES ────────────►  ① embed query (sentence-transformers)        │
   │                      ② FAISS top-k retrieval                       │
   │                      ③ if top score < 0.30 → "not in corpus"      │
   │                      ④ build grounded prompt + chat history       │
   │                      ⑤ Ollama (LLaMA 3.2) generates with strict   │
   │                          5-part structure                          │
   │                      ⑥ stream tokens back to browser              │
   │                      ⑦ append source + page citations              │
   │                                                                   │
   │   NO ─────────────►  ① keyword scoring across 71 KB topics        │
   │                          (longer keys score higher → specificity)  │
   │                      ② return matching topic's title + body       │
   │                          + cited sources                           │
   │                      ③ Gemini Nano (if Chrome 127+) adds an       │
   │                          enrichment paragraph (also 5-part rules)  │
   │                                                                   │
   └───────────────────────────────────────────────────────────────────┘
```

---

## 5.  The data we use

| Source | License | Status | Used for |
|---|---|---|---|
| Marshall 1931 *Mohenjo-daro and the Indus Civilization* | Public domain (India) | Knowledge in KB | 19 KB topics |
| Mackay 1937–38 *Further Excavations at Mohenjo-daro* | Public domain | Knowledge in KB | DK area, wells, pottery topics |
| Vats 1940 *Excavations at Harappa* | Public domain | Knowledge in KB | Mound F, R-37 topics |
| Wheeler 1947 ASI reports | Public domain | Knowledge in KB | Stratigraphy, granary topics |
| Mahadevan 1977 *Indus Script Concordance* | Public domain (ASI) | Statistics in `script-analysis.js` | Frequency / positional / bigram data |
| Parpola 1994 *Deciphering the Indus Script* | Copyright | Cited only | Cross-references |
| **CISI 1–3.2** (Parpola et al.) | Copyright | Indexed via RAG (fair-dealing for academic research) | Full-text retrieval |
| Yajnadevam *Indus Inscriptions* | Author-distributed | RAG (303 chunks) | Decipherment hypothesis |
| Authority Structure paper | Author-distributed | RAG (4 chunks) | Administrative typology |
| Rakhigarhi aDNA study (Shinde et al. 2019, *Cell*) | Open access | Knowledge in KB | aDNA / Aryan-migration topic |
| harappa.com / Wikipedia | (not used — no scraping) | — | — |
| 92 real seal images | From Indus-Seal-Dataset | Visual gallery | `assets/seals/` |

The KB itself is **71 hand-written scholarly topics totalling ~99 KB** of curated text,
each with cited primary sources.

---

## 6.  Mandatory answer structure (enforced everywhere)

Every answer — KB, Gemini Nano, RAG — follows the same 5-part format:

```
1. DIRECT ANSWER       (1–2 sentences answering the question)
2. EVIDENCE            (sites, artefacts, scholarly findings, with citations)
3. INTERPRETATION      (what the evidence implies — "what does this mean?")
4. ALTERNATIVE VIEW    (at least one competing / minority interpretation)
5. LIMITATION          (gaps, debates, caveats — cautious language)
```

**Confidence controls** (also enforced everywhere):

| ❌ Avoid | ✅ Use instead |
|---|---|
| universally | widely believed |
| definitive | suggests |
| proves | likely indicates |
| unique | the evidence is consistent with |
| always / never | scholars debate / remains contested |
| no civilization | cannot be confirmed |

**Redundancy control**: do not repeat information already stated in the same answer.

---

## 7.  Why this matters — what makes it different

| | Indus Valley AI | Wikipedia | ChatGPT / general LLMs | Academic websites |
|---|---|---|---|---|
| Domain-locked | ✅ | ❌ | ❌ | ✅ |
| Cited sources per answer | ✅ | ✅ | ⚠️ often invented | ✅ |
| Real 3D / interactive | ✅ | ❌ | ❌ | ❌ |
| Image analysis | ✅ (canvas + CLIP) | ❌ | needs paid API | ❌ |
| Refuses out-of-domain | ✅ hard gate | ❌ | partial | ❌ |
| 5-part structured answers | ✅ | ❌ | ❌ | varies |
| Hosting cost | ₹0 | ₹0 | ₹400–₹8 000/month | ₹0 |
| Privacy | 100 % on-device | partial | sends data to cloud | 100 % |
| Works offline | ✅ after first load | ❌ | ❌ | ❌ |

---

## 8.  The technology stack — at a glance

| Layer | Technology | Why this choice |
|---|---|---|
| Markup | Semantic HTML5 | Zero framework lock-in |
| Styling | Vanilla CSS3 with custom properties | Will work in 10 years without updates |
| Interactions | Vanilla JavaScript (no React, no build step) | Zero dependency vulnerabilities |
| 3D graphics | Three.js 0.160 (CDN) | Industry standard; pure WebGL underneath |
| On-device LLM | Gemini Nano (`window.LanguageModel`) | Free, private, no API key |
| Backend (optional) | Python FastAPI | Modern async, OpenAPI docs auto-generated |
| Embeddings | `BAAI/bge-small-en-v1.5` (sentence-transformers) | 384-dim, fast on CPU, top retrieval benchmarks |
| Vector store | FAISS IndexFlatIP | Industry standard, persistent, scales to millions |
| RAG LLM | Ollama + LLaMA 3.2 (1B / 3B) | Open-source, runs locally, no API cost |
| Image AI | OpenAI CLIP (ViT-Base-Patch32) | Apache 2.0, open weights |
| OCR | OCRmyPDF + Tesseract | Open source, handles scanned scholarly PDFs |
| PDF report generation | Python ReportLab | Programmatic, deterministic, version-controlled |

---

## 9.  Scalability & extensibility

* **Add more PDFs** → drop into `backend/data/pdfs/` → `python ingest_corpus.py` → done.
* **Use a bigger LLM** → `ollama pull mistral` and set `IVAI_OLLAMA_MODEL=mistral`.
* **Switch embedder** → set `IVAI_EMBED_MODEL=BAAI/bge-base-en-v1.5` for better quality.
* **Public deployment** → upload to GitHub Pages or Netlify (static) — backend stays
  optional and local for now.

---

## 10.  Three-sentence summary you can say out loud

> Indus Valley AI is a domain-restricted research assistant for the Indus Civilization
> that runs entirely in the browser with zero cloud cost. It combines a curated
> 71-topic knowledge base, an on-device Small Language Model (Gemini Nano), and an
> optional local RAG pipeline (FastAPI + FAISS + LLaMA 3.2) that ingests scholarly
> PDFs like the *Corpus of Indus Seals and Inscriptions* and answers questions with
> full source citations and a strict five-part academic structure — direct answer,
> evidence, interpretation, alternative view, and limitation.

That's the project, end to end.
