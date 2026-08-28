# Indus Valley AI — Research Artifact

A reproducible study of **corpus-integrity failures in retrieval-augmented
generation**, built on a deployed archaeological QA system.

> **Headline:** a defect that made **96.1% of the system's citations name the
> wrong document** left **every retrieval metric exactly unchanged**. We show under
> controlled perturbation that this blindness is structural, not anecdotal.

## Reproduce everything

```bash
backend/venv/bin/python scripts/run_all_experiments.py
```

14 stages, dependency-ordered, cached. Add `--skip-rag` to omit the slow LLM stage
(~1 h) or `--force` to rebuild all. Writes
`research/reproducibility/run_manifest.json` with versions, seeds and runtimes.

## Layout

```
research/
├── benchmark/          IVA-80 v2.0.0 — 80 questions, flags, retrieval-type labels
├── annotations/        1,382 pooled pairs, annotation UI + CLI, agreement tooling
├── corpus_statistics/  (see results/processed/phase7c_boilerplate.json)
├── results/
│   ├── raw/            per-system ranked lists, qrels actually used
│   ├── processed/      metrics, CIs, significance, diagnostics, perturbation
│   ├── tables/         all_tables.md — generated, never hand-typed
│   └── figures/        6 PNGs — generated from result files
├── error_analysis/     taxonomy + per-question failures
├── paper/              paper.md — every number injected at build time
├── submission/         red_team.md, iclr_checklist.md
└── reproducibility/    project_state.json, run_manifest.json
```

## Key results

| Finding | Evidence |
|---|---|
| Ranking metrics cannot detect attribution failure | Recall@5 range **0.0e+00** across 0→100% metadata misalignment; citations 100%→0.6% |
| Legacy index citation correctness | **3.9%** (769/800 wrong document); Kendall τ = 1.000, content Jaccard = 0.965 |
| A 25.3% source is effectively unretrievable | retrieved at **0.27×** share; deleting it changes Recall@5 by **+0.001** |
| Cause: near-duplicate collapse | 75% duplicate rows, 302/303 chunks share one header, intra-source sim 0.894 vs 0.662 |
| Retriever comparison | **No difference significant**; ordering flips with judging scheme |

## Status and limits

- **No human relevance judgments exist.** Automatic judges only, κ ≈ 0.28–0.33.
  All retrieval results are **exploratory**. Protocol and tooling ship ready to run.
- **The bibliography is empty by design** — no unverified citation is included.
- Two of our own hypotheses were falsified and are retained (see `paper.md` §6).
- Source PDFs are copyrighted and not redistributed; the derived index is included.

## Integrity guarantees

```bash
backend/venv/bin/python tests/data/test_index_integrity.py   # 12 tests
```

The vector store hard-fails on count/dimension mismatch and refuses to serve.
A corrupted fixture reproducing the original 1506/2112 shape is part of the suite.
