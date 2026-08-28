# Research Questions

Only questions that are **experimentally feasible on current hardware before ~24 Sep 2026**
are marked ACTIVE. The rest are honestly deferred.

## ACTIVE

**RQ1 — Does structured metadata + spatial grounding improve retrieval over text-only RAG
on Indus Valley archaeological questions?**
- Arms: BM25 · vector RAG (current system) · vector + metadata · vector + metadata + spatial
- Metrics: Recall@K, MRR, nDCG@10 (retrieval-only — **no LLM needed, so CPU-cheap**)
- Data: existing 1,506-chunk corpus, existing 80-question benchmark
- Feasible: **yes**

**RQ2 — Does grounding reduce unsupported claims and improve citation accuracy?**
- Metrics: citation accuracy (does cited page contain the claim?), unsupported-claim rate,
  evidence coverage
- Requires: LLM generation on 80 questions × arms at 21–54 s/question → budget carefully;
  consider 2 arms only
- Feasible: **yes, if arms are limited to 2**

**RQ3 — REFRAMED after measurement.** *Original motivation ("80% of the corpus is one
book") was falsified — that was a duplication artifact; the corpus is balanced.*

**RQ3' — Why does retrieval systematically under-select the largest source?**
- Measured: the dense retriever returns Yajnadevam material at **0.14×** its corpus
  share, while over-returning CISI 1 at **1.75–2.10×** (E001, Table 5)
- Candidate explanations to test: chunk length, OCR quality, tabular/glyph-list
  formatting, embedding-model domain mismatch
- Feasible: **yes** — retrieval-only, cheap
- Status of cause: **UNKNOWN / NOT INVESTIGATED**

**RQ0 — NEW, and answered: does index/metadata integrity hold?**
- **No.** 1,506 vectors vs 2,112 metadata rows; 6/10 alignment probes fail.
- Consequence: citations are wrong for most retrieved chunks.
- This supersedes every other question — a grounded-QA system whose citations are
  misaligned cannot be evaluated on grounding until it is fixed.

## DEFERRED — blocked by missing data, not by time

**RQ4 — Damaged/rare sign recognition.**
BLOCKED: the 103 seal images have **no labels**. No labels → no training set, no test set,
no accuracy. Would require an annotation effort that does not exist yet.

**RQ5 — Knowledge-graph grounded QA.**
BLOCKED: no entity/relation data exists. `data.js` contains **no `site:` fields and no
coordinates**. A KG cannot be built from nothing, and edges must not be invented.

**RQ6 — Geographic distribution analysis.**
BLOCKED: no site coordinates in the repository. Coordinates must not be fabricated.

**RQ7 — Expert-verified benchmark release.**
BLOCKED: no expert verification process exists. Per the master instruction, the dataset
**may not be called "expert-verified" or "benchmark"** until tasks, splits, provenance,
protocol and baselines all exist.
