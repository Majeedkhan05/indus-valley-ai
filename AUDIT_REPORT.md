# AUDIT_REPORT.md — Indus Valley AI

**Date:** 2026-08-23  ·  **Phase:** 0 (PRESERVE) → 1 (EXECUTE)  ·  **Existing code modified: NONE**

> ### ⚠ CORRECTIONS — two claims in this audit were later falsified by measurement
> 1. **"Corpus is 80% one book" — WRONG.** That was an artifact of 913 duplicate
>    metadata rows. After de-duplication the corpus is balanced (Yajnadevam 25.3%,
>    CISI volumes 74.4%). See `experiments/RESULTS.md` Finding 2.
> 2. **"1,506 vectors" understates a defect.** The index holds 1,506 vectors but
>    2,112 metadata rows — a misalignment that **invalidates most citations**.
>    See `docs/bug-index-metadata-misalignment.md`. This is now the project's
>    most important finding.
>
> Sections below are the original audit text, left intact for the record.

This is an inspection-only audit. No files were deleted, moved, reset, or overwritten.
No git commands other than read-only inspection (`status`, `branch`, `remote`, `log`) were run.

---

## 1. Existing project structure

```
indus-valley/                      ← repo root, git repo, branch `main`
├── index.html  (800)              ← static SPA, no build step
├── app.js (849)  styles.css (1465)
├── knowledge-base.js (1232)       ← 71-topic curated fallback KB
├── data.js (348)                  ← cities / motifs / seals catalog
├── three-scene.js (313)  three-routes.js (231)
├── vision.js (203)  gemini-nano.js (126)  rag-client.js (92)
├── script-analysis.js (158)
├── assets/seals/                  ← 103 seal images (Git LFS)
├── backup-v1-original/            ← full v1 snapshot, 9 files
├── backend/                       ← SEPARATE git repo (nested)
│   ├── main.py (280)
│   ├── rag/ {embed, vectordb, ingest, retrieve, generate, guardrails}
│   ├── vision/clip_match.py
│   ├── ingest_corpus.py (63)
│   └── data/{pdfs, ocr, index}
├── paper/eval/                    ← benchmark (UNTRACKED in git)
├── training/                      ← LoRA finetune notebook + 200 Q&A pairs
└── docs (root .md files)          ← README, HOW_IT_WORKS, SETUP_RAG, DEPLOY_HF, REVERT
```

Total frontend: **5,817 lines** JS/HTML/CSS. Backend: **546 lines** Python.

## 2. Existing 3D website — **KEEP, DO NOT REPLACE**

Vanilla Three.js (CDN importmap, no bundler). Two scenes: hero seal (`three-scene.js`)
and trade-routes globe (`three-routes.js`). Plus custom cursor, spotlight, scroll spine,
magnetic buttons. **Status: working.** This is the project's strongest visible asset.

## 3. Existing RAG — **KEEP + IMPROVE (this is the research baseline)**

| Stage | Implementation | Verdict |
|---|---|---|
| Ingestion | `pypdf`, page-level, 400-tok chunks / 50 overlap | KEEP |
| Embeddings | `BAAI/bge-small-en-v1.5`, 384-d, normalized | KEEP |
| Vector DB | FAISS `IndexFlatIP` + parallel `chunks.jsonl` | **BROKEN — index/metadata misaligned, see corrections above** |
| Retrieval | cosine top-k=6, `MIN_RELEVANCE = 0.30` | **IMPROVE** — no reranker, threshold likely too low |
| Prompting | 80-line structured system prompt, 5 mandatory sections | KEEP — genuinely good |
| Citations | inline `[source, p.N]` + citation array in response | KEEP |
| Guardrails | keyword allow/block domain filter | **IMPROVE** — not evaluated, no measured FP/FN |
| Evaluation | IVA-Q benchmark exists but **incomplete** | **BUILD OUT** |

**This is a solid, honest text-only RAG baseline.** For the research framing it is exactly
what a paper needs as the "conventional RAG" comparison arm. Do not discard it.

## 4. Existing models

- **LLM:** Ollama `gemma3:4b`, local (env `IVAI_OLLAMA_MODEL`). No fine-tuned model deployed.
- **Embedder:** `BAAI/bge-small-en-v1.5` (off-the-shelf).
- **Vision:** `openai/clip-vit-base-patch32`, zero-shot, **not fine-tuned on Indus imagery**.
- `backend/models/` — **empty**. No checkpoints exist.
- `training/finetune_colab.ipynb` — Phi-3-mini + LoRA pipeline, **never executed**.

## 5. Existing datasets

| Asset | Size | Status |
|---|---|---|
| FAISS index | 1,506 vectors / 2.3 MB | ✅ built, current |
| `chunks.jsonl` | 3.0 MB | ✅ current |
| CISI vols 1, 2, 3.1, 3.2 (OCR'd) | 948 MB, 525 pages | ✅ ingested |
| Yajnadevam, Authority Structure | 307 pages | ✅ ingested |
| `assets/seals/` | 103 images | ⚠️ **images only — no labels, no metadata** |
| `training_data.jsonl` | ~200 Q&A pairs | ⚠️ unused |

Chunk distribution: Yajnadevam 1212 · CISI 3.1 298 · CISI 3.2 276 · CISI 2 186 · CISI 1 132 · Authority 8.

⚠️ **Corpus imbalance:** Yajnadevam is **80% of all chunks**. That book argues a specific
(contested) decipherment. Retrieval is therefore biased toward one interpretive position.
This is a real methodological finding and must be disclosed in any paper.

## 6. Existing Hugging Face resources — **PRESERVED, NOT TOUCHED**

- Space: `AIHub-Mu/indus-valley-ai` — git remote `hfspace`, branch `main`.
- Seal images tracked via **Git LFS** (commits `701cc59`, `813944f`, `f677d9e`).
- Static frontend only; the FastAPI backend does **not** run on the Space.
- Full detail: `docs/huggingface-assets.md`.

## 7. Existing research

- `paper/eval/benchmark_questions.json` — **80 questions**, with `category` + `ground_truth`.
- `paper/eval/results.jsonl` — **only 27 of 80 rows.** Run was interrupted.
- **No ratings applied.** No accuracy, citation-accuracy, or hallucination numbers exist yet.
- Latency observed: 21–54 s/question (CPU inference).
- No `main.tex` / LaTeX source present in the repo.

## 8. Existing APIs

`/health` · `/query` · `/query/stream` (SSE) · `/ingest/pdf` · `/ingest/csv` ·
`/vision/match` · `/documents` (GET) · `/documents/{name}` (DELETE). CORS `*`.

## 9–12. Frameworks

Frontend: **vanilla JS + Three.js CDN** (no React/Next/Vite/bundler).
Backend: **FastAPI + uvicorn**, lazy singletons.
Vector DB: **FAISS flat**. No relational DB, no graph DB, no spatial store.

## 13. What is working
Frontend, 3D scenes, KB fallback, Gemini Nano fallback, FastAPI backend, FAISS retrieval
(68–72% cosine on real queries), citations with page numbers, streaming, HF Space deploy.

## 14. What is broken / incomplete
1. **Benchmark 34% complete** (27/80), unrated → **zero quantitative results exist**.
2. **CPU-only inference**, 21–54 s/query — too slow to run 80 questions × N ablation arms.
3. **103 seal images have no labels/metadata** → no CV task, no KG, no spatial layer possible yet.
4. CLIP is zero-shot, never evaluated → no accuracy number.
5. Guardrails unmeasured.
6. Nested git repos (`backend/` has its own `.git` + separate GitHub remote) — a submodule/
   nesting hazard, but **not touched** in this audit.
7. Working tree has an uncommitted deletion: `Indus_Valley_AI_Project_Report.pdf` (status `D`).
   **Not restored and not committed** — flagged for your decision.
8. `paper/` is untracked.

## 15. Reusable as-is
3D website · RAG pipeline (as baseline arm) · citation mechanism · system prompt ·
OCR'd corpus · benchmark question set · 103 seal images (as raw CV data).

## 16. Needs improvement
Reranking · relevance threshold calibration · corpus rebalancing · guardrail evaluation ·
inference speed · benchmark completion.

## 17. Missing for a research paper
Structured artifact metadata · site coordinates · sign labels · knowledge graph ·
spatial layer · image retrieval eval · baselines (BM25/TF-IDF) · ablations ·
error analysis · statistical testing · reproducibility manifest · tests.

**Blunt assessment:** the system is a working *product*. It is **not yet a paper**, because
no experiment has produced a number. The gap is measurement, not features.

## 18. Conference candidates
Best-evidence candidate: **ICLR 2027 (Brazil), submission deadline ~24 Sep 2026.**
See `docs/conference-requirements.md` — including an honest assessment of fit.
Status: **NEEDS VERIFICATION against the official ICLR site.**

## 19. Recommended research direction

**Pursue ONE paper, not five.** With ~4 weeks and CPU-only hardware, five is not achievable.

**Recommended: Paper 3 (KG/spatial-grounded retrieval) — reduced scope.**

Why this one:
- It builds on what already exists and works (the RAG pipeline).
- It needs **no GPU** — retrieval ablations are CPU-cheap; only generation is slow, and
  retrieval-only metrics (Recall@K, nDCG, MRR) need no LLM at all.
- The 103 seal images cannot support Paper 2 (CV) without labels you do not have.
- Paper 5 (benchmark) cannot claim "expert-verified" — no expert verification exists.

Feasible contribution: *"Does adding site-level spatial and metadata grounding to a
citation-grounded archaeological RAG system improve retrieval and reduce unsupported
claims, relative to text-only RAG?"* — with BM25 and vector-RAG baselines, one ablation
axis, on the existing 1,506-chunk corpus and 80-question benchmark.

## 20. Proposed first implementation step

**Finish the measurement, before building anything new.**

1. Complete the benchmark run (53 remaining questions).
2. Rate all 80 answers (0/1/2 accuracy + citation correctness).
3. Add a **BM25 baseline** (`rank_bm25`, ~40 lines, no GPU) and score it on the same 80.

That produces the first two rows of Table 3 and is the smallest step that turns this
project into research. Nothing existing gets modified — new files only.

---

## Component mapping

| Component | Status | Action | Research role | Paper |
|---|---|---|---|---|
| 3D website | Working | **KEEP** | Research interface / demo | all |
| RAG pipeline | Working | **KEEP + IMPROVE** | Baseline arm | 3 |
| System prompt | Good | KEEP | Faithfulness control | 3 |
| FAISS index | Current | KEEP | Retrieval corpus | 3 |
| Benchmark | 27/80 | **COMPLETE** | Evaluation set | 3 |
| CLIP matcher | Untested | **EVALUATE** | Needs labels first | 2 (deferred) |
| 103 seals | Unlabeled | **ANNOTATE** | Blocks CV + KG | 2/5 (deferred) |
| KB fallback | Working | KEEP | Offline demo path | — |
| Gemini Nano | Working | KEEP | Offline demo path | — |
| `backup-v1-original/` | Archive | **PRESERVE** | Rollback | — |
| HF Space | Live | **DO NOT TOUCH** | Preserved legacy deploy | — |
| `training/` | Unused | KEEP | Optional future | — |

**No component is marked DELETE.**


---

# ADDENDUM — Execution phase (2026-08-23)

Audit → execution. New files only; no existing file was modified.

## Built
| Component | Path |
|---|---|
| BM25 (in-repo Okapi, no dependency) | `retrieval/lexical/bm25.py` |
| IR metrics (R@K, P@K, MRR, nDCG, Hit@K) | `evaluation/metrics/ir_metrics.py` |
| Proxy relevance judges + agreement | `evaluation/benchmarks/relevance.py` |
| E001 experiment runner | `scripts/evaluation/run_retrieval_experiments.py` |
| Table generator | `scripts/evaluation/generate_tables.py` |
| Clean index rebuild | `scripts/data_ingestion/rebuild_index.py` |
| Alignment regression test | `tests/data/test_index_alignment.py` |
| Corrected index (new, live index untouched) | `backend/data/index_v2/` |

## Results
See `experiments/RESULTS.md`. Headline: the deployed dense retriever is last or
second-to-last at every judging operating point; hybrid RRF leads at 3 of 4.
Judgments are automatic proxies (κ ≤ 0.36) — direction only, not proof.

## Blocking next step
Human relevance judgments (`docs/annotation-protocol.md`, ~24 person-hours).
Until then no retrieval claim is publishable.

## Decisions still required from the project owner
1. Switch the backend from `data/index/` to `data/index_v2/`? (fixes citations;
   changes live behaviour — **not done without approval**)
2. Make `VectorDB.load_or_init()` hard-fail on count mismatch? (touches serving code)
3. `Indus_Valley_AI_Project_Report.pdf` still shows as deleted (`D`) — restore or commit?
4. Nested git repo under `backend/` — leave, submodule, or separate?
