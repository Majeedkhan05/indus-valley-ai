# IVA-80 — Generated Tables

Auto-generated from `research/results/`. **Do not edit by hand.**

Judge: **AUTOMATIC PROXY (no human labels exist)**


## Table 1 — Corpus composition and integrity

TTR = type-token ratio (lexical diversity). Intra-source sim = mean chunk-to-chunk cosine.

| Source | Raw rows | Duplicate rows | Dup % | Unique chunks | TTR | Intra-source sim |
|---|---|---|---|---|---|---|
| Indus Inscriptions by Yajnadevam.pdf | 1212 | 909 | 75.0% | 303 | 0.121 | 0.894 |
| CISI_3.1_Mohenjodaro_and_Harappa.pdf | 298 | 0 | 0.0% | 298 | 0.159 | 0.672 |
| CISI_3.2_Recent_Findings_from_India___Pakist | 276 | 0 | 0.0% | 276 | 0.216 | 0.644 |
| CISI_2_Collections_in_Pakistan.pdf | 186 | 0 | 0.0% | 186 | 0.220 | 0.667 |
| CISI_1_Collections_in_India.pdf | 132 | 0 | 0.0% | 132 | 0.260 | 0.665 |
| Authority Structure and the Evolution of Ear | 8 | 4 | 50.0% | 4 | 0.521 | 0.919 |

## Table 2 — IVA-80 benchmark composition

| Property | Value |
|---|---|
| Questions | 80 |
| Version | 2.0.0 |
| Categories | 10 |
| Contested-interpretation flagged | 22 |
| Possibly ambiguous | 7 |
| Negative/unknown answers | 6 |
| Tests lexical retrieval | 72 |
| Tests semantic retrieval | 63 |
| Tests multi-hop | 1 |
| Human labels | NONE - annotation pending |

## Table 3 — Retrieval results under both judging schemes

95% CIs are non-parametric bootstrap over questions (10,000 resamples).

| Judge scheme | System | n | R@1 | R@5 | R@10 | MRR | nDCG@10 |
|---|---|---|---|---|---|---|---|
| global_quantile | bm25 | 39 | 0.162 [0.09, 0.25] | 0.431 [0.31, 0.55] | 0.647 [0.52, 0.76] | 0.545 [0.41, 0.68] | 0.503 [0.40, 0.61] |
| global_quantile | dense | 39 | 0.099 [0.04, 0.17] | 0.383 [0.28, 0.49] | 0.629 [0.51, 0.74] | 0.467 [0.35, 0.59] | 0.437 [0.35, 0.53] |
| global_quantile | hybrid_rrf | 39 | 0.140 [0.07, 0.23] | 0.466 [0.35, 0.59] | 0.690 [0.58, 0.79] | 0.560 [0.44, 0.68] | 0.517 [0.43, 0.61] |
| per_question | bm25 | 77 | 0.099 [0.07, 0.14] | 0.332 [0.28, 0.39] | 0.551 [0.48, 0.62] | 0.663 [0.58, 0.74] | 0.526 [0.46, 0.59] |
| per_question | dense | 77 | 0.090 [0.06, 0.13] | 0.365 [0.31, 0.42] | 0.634 [0.57, 0.70] | 0.667 [0.58, 0.75] | 0.591 [0.53, 0.65] |
| per_question | hybrid_rrf | 77 | 0.117 [0.09, 0.15] | 0.392 [0.35, 0.44] | 0.618 [0.57, 0.67] | 0.744 [0.67, 0.82] | 0.599 [0.55, 0.65] |

## Table 4 — Paired bootstrap significance tests

Paired over questions. No comparison reaches significance at α=0.05.

| Judge scheme | Comparison | Metric | Δ | 95% CI of Δ | p (2-sided) | Verdict |
|---|---|---|---|---|---|---|
| global_quantile | bm25 vs dense | recall@5 | +0.048 | [-0.115, +0.212] | 0.567 | not significant |
| global_quantile | bm25 vs dense | mrr | +0.078 | [-0.101, +0.252] | 0.385 | not significant |
| global_quantile | bm25 vs dense | ndcg@10 | +0.066 | [-0.087, +0.217] | 0.404 | not significant |
| global_quantile | hybrid_rrf vs dense | recall@5 | +0.083 | [-0.055, +0.221] | 0.242 | not significant |
| global_quantile | hybrid_rrf vs dense | mrr | +0.094 | [-0.038, +0.227] | 0.164 | not significant |
| global_quantile | hybrid_rrf vs dense | ndcg@10 | +0.081 | [-0.028, +0.195] | 0.149 | not significant |
| per_question | bm25 vs dense | recall@5 | -0.033 | [-0.122, +0.052] | 0.460 | not significant |
| per_question | bm25 vs dense | mrr | -0.004 | [-0.118, +0.109] | 0.917 | not significant |
| per_question | bm25 vs dense | ndcg@10 | -0.065 | [-0.170, +0.040] | 0.224 | not significant |
| per_question | hybrid_rrf vs dense | recall@5 | +0.027 | [-0.031, +0.087] | 0.360 | not significant |
| per_question | hybrid_rrf vs dense | mrr | +0.077 | [-0.003, +0.159] | 0.058 | not significant |
| per_question | hybrid_rrf vs dense | ndcg@10 | +0.007 | [-0.054, +0.073] | 0.830 | not significant |

## Table 5 — Ablation

| Configuration | R@1 | R@5 | R@10 | MRR | nDCG@10 |
|---|---|---|---|---|---|
| hybrid_no_yajnadevam | 0.138 | 0.459 | 0.666 | 0.560 | 0.511 |
| hybrid_rrf_k10 | 0.138 | 0.458 | 0.660 | 0.556 | 0.503 |
| hybrid_rrf_k60 | 0.138 | 0.458 | 0.660 | 0.560 | 0.506 |
| hybrid_rrf_k200 | 0.138 | 0.458 | 0.660 | 0.560 | 0.506 |
| hybrid_linear_a0.3 | 0.146 | 0.457 | 0.690 | 0.549 | 0.521 |
| hybrid_linear_a0.5 | 0.140 | 0.451 | 0.665 | 0.522 | 0.504 |
| hybrid_linear_a0.7 | 0.130 | 0.409 | 0.617 | 0.528 | 0.477 |
| bm25 | 0.159 | 0.409 | 0.610 | 0.545 | 0.488 |
| dense | 0.097 | 0.375 | 0.609 | 0.467 | 0.428 |
| dense_no_yajnadevam | 0.097 | 0.375 | 0.619 | 0.467 | 0.434 |

## Table 6 — Legacy vs corrected index (citation integrity)

Retrieval was unaffected (τ=1.0); only attribution was destroyed.

| Measure | Legacy | Corrected |
|---|---|---|
| Vectors / metadata rows | 1506 / 2112 | 1199 / 1199 |
| Counts aligned | NO | YES |
| Citation correctness | 3.9% | 100% |
| Wrong document | 769 | 0 |
| Content Jaccard vs corrected | 0.965 | 1.000 |
| Kendall τ of ranking | 1.000 | 1.000 |
| Retrieval Recall@5 | identical | identical |

## Table 7 — Retrieval share by source and chunk type

Ratio > 1 = over-retrieved relative to corpus share.

| Stratum | Chunks | Corpus share | Retrieved share | Ratio |
|---|---|---|---|---|
| Indus Inscriptions by Yajnadevam.p [tabular] | 248 | 20.7% | 5.1% | 0.25 |
| CISI_3.1_Mohenjodaro_and_Harappa.p [tabular] | 189 | 15.8% | 6.9% | 0.44 |
| CISI_3.2_Recent_Findings_from_Indi [tabular] | 156 | 13.0% | 5.7% | 0.44 |
| CISI_3.2_Recent_Findings_from_Indi [prose] | 120 | 10.0% | 15.0% | 1.50 |
| CISI_3.1_Mohenjodaro_and_Harappa.p [prose] | 109 | 9.1% | 23.9% | 2.63 |
| CISI_2_Collections_in_Pakistan.pdf [tabular] | 101 | 8.4% | 2.7% | 0.32 |
| CISI_2_Collections_in_Pakistan.pdf [prose] | 85 | 7.1% | 17.8% | 2.51 |
| CISI_1_Collections_in_India.pdf [tabular] | 68 | 5.7% | 3.0% | 0.54 |
| CISI_1_Collections_in_India.pdf [prose] | 64 | 5.3% | 17.1% | 3.21 |
| Indus Inscriptions by Yajnadevam.p [prose] | 55 | 4.6% | 1.4% | 0.30 |
| Authority Structure and the Evolut [prose] | 4 | 0.3% | 1.4% | 4.12 |

## Table 8 — Error taxonomy

60 of 80 questions fall below Recall@5 = 0.5 (multi-label). `evaluation_artifact` = the automatic judge produced no relevant chunk.

| Category | Failing questions |
|---|---|
| evaluation_artifact | 41 |
| source_imbalance | 11 |
| semantic_mismatch | 7 |
| contested_interpretation | 5 |
| ocr_artifact | 3 |
| ambiguous_question | 3 |
| retrieval_failure | 3 |
| insufficient_evidence | 1 |
| near_duplicate_collapse | 1 |

## Table 9 — End-to-end RAG answer measures (automated)

Model: gemma3:4b via Ollama. 80/80 answered. **All measures are automated proxies, not human evaluation.**

| Measure | Mean | Median | n |
|---|---|---|---|
| citation_count | 5.925 | 6.000 | 80 |
| citation_validity | 1.000 | 1.000 | 79 |
| citation_grounding | 1.000 | 1.000 | 79 |
| answer_relevance_cos | 0.790 | 0.802 | 80 |
| answer_evidence_cos | 0.729 | 0.748 | 80 |
| reference_overlap | 0.132 | 0.111 | 80 |
| unsupported_rate | 0.334 | 0.270 | 80 |
| hedging_rate | 0.224 | 0.183 | 80 |
| latency_s | 33.418 | 15.780 | 80 |
| confidence | 0.665 | 0.690 | 80 |
| answer_words | 93.338 | 95.500 | 80 |
