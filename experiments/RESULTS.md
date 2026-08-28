# Experimental Results — first real measurements

Generated from `experiments/results/`. Every number here traces to a file.
**Nothing in this document is hand-typed from memory.**

| Paper table | Experiment | File |
|---|---|---|
| Tables 1–5 | E001 | `experiments/results/E001_retrieval_baselines_index_v2/tables.md` |
| raw metrics | E001 | `.../metrics.json` |
| runs | E001 | `.../predictions.json` |
| judgments | E001 | `.../qrels.json` |
| source bias | E001 | `experiments/analysis/source_bias.json` |

---

## Finding 1 — A data-integrity bug invalidated the system's citations

The live index (`backend/data/index/`) holds **1,506 vectors against 2,112
metadata rows**. `vectordb.search()` maps FAISS id → `metadata[i]` positionally,
so past id ≈ 311 every returned citation describes a different chunk than the one
that actually matched.

Probe test (cosine between `vector[i]` and `embed(metadata[i].text)`; 1.0 = aligned):

| id | 0 | 1 | 50 | 300 | 700 | 899 | 900 | 901 | 1200 | 1505 |
|---|---|---|---|---|---|---|---|---|---|---|
| cos | 1.000 | 1.000 | 1.000 | 1.000 | **0.726** | **0.599** | **0.670** | **0.626** | **0.650** | **0.596** |

**6/10 probes misaligned.** Full analysis: `docs/bug-index-metadata-misalignment.md`.

This is the most consequential result so far. It is a plausible cause of the
previously observed behaviour where answers did not match their citations. It
also means **`paper/eval/results.jsonl` (27 rows) is unusable as evidence.**

A corrected index was built into `backend/data/index_v2/` (1,199 chunks,
alignment verified). **The live index was not modified.**

## Finding 2 — The "80% single-source corpus" claim was wrong

The earlier audit reported that one book supplied 80% of the corpus. That was an
artifact of **913 duplicate rows**. After de-duplication:

| Source | Chunks | Share |
|---|---:|---:|
| Yajnadevam | 303 | 25.3% |
| CISI 3.1 Mohenjo-daro & Harappa | 298 | 24.9% |
| CISI 3.2 Recent Findings | 276 | 23.0% |
| CISI 2 Collections in Pakistan | 186 | 15.5% |
| CISI 1 Collections in India | 132 | 11.0% |
| Authority Structure | 4 | 0.3% |

The corpus is **reasonably balanced**. The planned source-imbalance study (RQ3)
loses its original motivation and has been reframed — see Finding 4.
*A prior claim of ours was falsified by measurement; it is corrected here rather
than quietly dropped.*

## Finding 3 — The deployed dense retriever is never the best system

Recall@5 under proxy judgments, swept across four judging operating points:

| Selectivity | κ | n | BM25 | VECTOR (deployed) | VECTOR+PREFIX | HYBRID_RRF |
|---:|---:|---:|---:|---:|---:|---:|
| 0.03 | 0.131 | 33 | 0.366 | 0.216 | 0.223 | **0.379** |
| 0.05 | 0.270 | 45 | 0.246 | 0.271 | 0.263 | **0.311** |
| 0.10 | 0.277 | 58 | 0.304 | 0.238 | 0.261 | **0.323** |
| 0.20 | 0.360 | 74 | **0.233** | 0.193 | 0.215 | 0.228 |

**Ranking is NOT stable across operating points** — reported as-is rather than
selecting the threshold that tells the nicest story.

What survives the instability:
- **HYBRID_RRF is best at 3 of 4 operating points**, and second at the fourth.
- **VECTOR — the currently deployed retriever — is last or second-to-last at every
  operating point.** This is the one consistent result.
- The BGE query-instruction prefix gives a small, inconsistent change; it is not
  a reliable win.

**This does not yet establish that hybrid retrieval is better.** κ ≤ 0.36 means
the judgments are too noisy, and no significance testing has been run. It
establishes a *direction* worth testing properly with human qrels.

## Finding 4 — Retrieval systematically under-selects the largest single source

Share of top-10 results per source vs. that source's corpus share (ratio > 1 = over-retrieved):

| Source | Corpus | BM25 | VECTOR | HYBRID_RRF |
|---|---:|---:|---:|---:|
| Yajnadevam | 25.3% | 0.32 | **0.14** | 0.23 |
| CISI 3.1 | 24.9% | 1.21 | 1.23 | 1.16 |
| CISI 3.2 | 23.0% | 0.74 | 1.03 | 0.91 |
| CISI 2 | 15.5% | 1.31 | 1.39 | 1.37 |
| CISI 1 | 11.0% | **2.10** | 1.75 | 2.01 |
| Authority Structure | 0.3% | 3.21 | 4.12 | 3.37 |

The dense retriever draws only **14%** of the Yajnadevam material its corpus share
would predict, while over-drawing CISI 1 by ~2×. The direction is the **opposite**
of the bias originally hypothesised. Cause is not yet established — plausible
candidates are chunk length, OCR quality, and the tabular/glyph-listing format of
much of the Yajnadevam text. **Not investigated. Marked UNKNOWN.**

---

## Limitations (binding on any write-up)

1. **Judgments are automatic, not human.** κ = 0.13–0.36. Not "ground truth",
   not "expert-verified". See `docs/annotation-protocol.md`.
2. **Pooled recall**, not absolute recall — only pooled chunks were judged.
3. **No significance testing.** Differences reported are not shown to be reliable.
4. **Retrieval only.** No LLM was run: no answer-correctness, citation-accuracy,
   faithfulness or hallucination numbers exist yet.
5. **n varies** with the operating point (33–74 of 80 questions).
6. **Single embedding model, single corpus.** No claim generalises beyond it.
7. **`paper/eval/results.jsonl` is void** — produced under the misalignment bug.

## Reproduce

```bash
backend/venv/bin/python scripts/data_ingestion/rebuild_index.py
backend/venv/bin/python tests/data/test_index_alignment.py
backend/venv/bin/python scripts/evaluation/run_retrieval_experiments.py
backend/venv/bin/python scripts/evaluation/generate_tables.py
```
Seed 42. Runtime ≈ 3 min (rebuild) + ≈ 25 s (evaluation) on CPU.
