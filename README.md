# IVA: Indus Valley AI 🏛️

An end-to-end, locally-hosted, citation-grounded research assistant for the Corpus of Indus Seals and Inscriptions (CISI). Built 100% locally to provide auditable, page-level answers without relying on paid, closed cloud APIs.

## ⚡ The Quick Pitch
General-purpose LLMs hallucinate wild decipherment claims, fake dates, and non-existent sites because they lack dense pretraining data on the Indus Valley script. IVA solves this by using a local OCR-to-Retrieval pipeline that forces an open-weight model to only generate answers backed by verifiable page-level evidence.

---

##  Tech Stack & Architecture

### Core Engineering Environment
*   **Target Machine:** Optimized for local consumer hardware (Tested on Apple Silicon M2, 16GB Unified Memory).
*   **LLM Runtime:** Ollama via native Apple Metal GPU acceleration.
*   **LLM Backbone:** Gemma 3 4B (Selected for native multimodal support, permissive license, and low memory footprint).

### Data Pipeline & Retrieval Backend
*   **OCR Engine:** `OCRmyPDF` (with a Tesseract 5 backend) to generate a hidden searchable text layer over out-of-print, image-only PDFs.
*   **Chunking Strategy:** Custom sliding-window token splitter (~380 words per chunk, 60-word overlap) preserving source and page metadata.
*   **Vector Search Matrix:** `BAAI/bge-small-en-v1.5` dense embeddings (384-dimensions, L2-normalized) feeding a local **FAISS** `IndexFlatIP` database.

---

##  Repository Structure

*   `/backend/` — Main server logic, local pipeline setups, and OCR intake scripts.
*   `/training/` — Code tracking the experimental fine-tuning pipeline and data maps.
*   `/assets/` — Visual assets, project logs, and high-resolution seal data photographs.
*   `app.js` / `index.html` — The localized user deployment interface and configuration.
*   `rag-client.js` — Client connection interface handling live semantic search requests.
*   `three-routes.js` / `three-scene.js` — Core routing logic and interactive visual scenes.
*   `script-analysis.js` — Data analysis tools evaluating local index statistics and runtimes.

---

##  Anti-Hallucination Guardrails

To preserve academic integrity, this codebase implements three strict programmatic guardrails:
1.  **Mathematical Refusal Gate ($\tau = 0.30$):** If the top-1 cosine similarity score from the FAISS database drops below `0.30`, retrieval aborts and returns an explicit refusal message rather than invoking the language model.
2.  **Structural Output Prompt Constraints:** The system prompt restricts generation to a hard-coded 5-part layout (*Direct Answer*, *Evidence* with inline `[source, page]` tags, *Interpretation*, *Alternative View*, and a hedged academic *Limitation* clause).
3.  **Regex Domain Filter:** Validates incoming text against a domain keyword whitelist and active regex blocklist to drop off-topic requests (e.g., cryptocurrency, coding) at the gate.

---

##  Setting Up Locally

### Prerequisites
Make sure you have Ollama installed and running with Apple Metal support active:
```bash
ollama pull gemma3:4b