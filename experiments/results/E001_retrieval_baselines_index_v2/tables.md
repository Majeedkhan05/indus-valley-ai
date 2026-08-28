# Generated Tables — E001 Retrieval Baselines

Auto-generated from `experiments/results/E001_retrieval_baselines_index_v2`. Do not edit by hand.

- Index: `index_v2` — 1199 chunks
- Questions: 80
- Judgments: **AUTOMATIC PROXY - quantile-calibrated dual judge. NOT human, NOT expert.**
- Built: 2026-08-23T10:51:51.538925+00:00


## Table 1 — Corpus composition (after de-duplication)

| Source | Chunks | Share |
|---|---:|---:|
| Indus Inscriptions by Yajnadevam.pdf | 303 | 25.3% |
| CISI_3.1_Mohenjodaro_and_Harappa.pdf | 298 | 24.9% |
| CISI_3.2_Recent_Findings_from_India___Pakistan.pdf | 276 | 23.0% |
| CISI_2_Collections_in_Pakistan.pdf | 186 | 15.5% |
| CISI_1_Collections_in_India.pdf | 132 | 11.0% |
| Authority Structure and the Evolution of Early Writing Systems 2.pdf | 4 | 0.3% |
| **Total** | **1199** | 100% |

## Table 2 — IVA-80 benchmark by category

| Category | Questions |
|---|---:|
| sites | 10 |
| seals | 10 |
| script | 10 |
| trade | 10 |
| controversies | 8 |
| scholars | 8 |
| religion | 7 |
| methodology | 7 |
| decline | 6 |
| iconography | 4 |
| **Total** | **80** |

## Table 3 — Retrieval baselines (proxy judgments, selectivity=0.05, lenient)

Questions with ≥1 judged-relevant chunk: **45/80** · judge agreement κ = **0.270**

| System | R@1 | R@5 | R@10 | P@5 | MRR | nDCG@10 |
|---|---:|---:|---:|---:|---:|---:|
| BM25 | 0.093 | 0.246 | 0.392 | 0.236 | 0.479 | 0.354 |
| VECTOR | 0.097 | 0.271 | 0.444 | 0.213 | 0.439 | 0.360 |
| VECTOR+PREFIX | 0.094 | 0.263 | 0.429 | 0.222 | 0.433 | 0.359 |
| HYBRID_RRF | 0.088 | 0.311 | 0.456 | 0.271 | 0.529 | 0.390 |

## Table 4 — Sensitivity of the ranking to the judging operating point

Recall@5 (lenient) at each judge selectivity. Tests whether conclusions survive a change of threshold.

| Selectivity | κ | n questions | BM25 | VECTOR | VECTOR+PREFIX | HYBRID_RRF | Best |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.03 | 0.131 | 33 | 0.366 | 0.216 | 0.223 | 0.379 | HYBRID_RRF |
| 0.05 | 0.270 | 45 | 0.246 | 0.271 | 0.263 | 0.311 | HYBRID_RRF |
| 0.10 | 0.277 | 58 | 0.304 | 0.238 | 0.261 | 0.323 | HYBRID_RRF |
| 0.20 | 0.360 | 74 | 0.233 | 0.193 | 0.215 | 0.228 | BM25 |

**Ranking stable across all operating points: `False`**

- selectivity 0.03: HYBRID_RRF > BM25 > VECTOR+PREFIX > VECTOR
- selectivity 0.05: HYBRID_RRF > VECTOR > VECTOR+PREFIX > BM25
- selectivity 0.10: HYBRID_RRF > BM25 > VECTOR+PREFIX > VECTOR
- selectivity 0.20: BM25 > HYBRID_RRF > VECTOR+PREFIX > VECTOR

## Table 5 — Source-bias analysis

Share of top-10 retrieved chunks drawn from each source, versus that source's share of the corpus. Ratio > 1 = over-retrieved.

| Source | Corpus share | BM25 (ratio) | VECTOR (ratio) | VECTOR+PREFIX (ratio) | HYBRID_RRF (ratio) |
|---|---:|---:|---:|---:|---:|
| Indus Inscriptions by Yajnadevam.pdf | 25.3% | 8.2% (0.32) | 3.6% (0.14) | 5.6% (0.22) | 5.8% (0.23) |
| CISI_3.1_Mohenjodaro_and_Harappa.pdf | 24.9% | 30.1% (1.21) | 30.6% (1.23) | 30.9% (1.24) | 28.9% (1.16) |
| CISI_3.2_Recent_Findings_from_India___Pakistan.pdf | 23.0% | 17.1% (0.74) | 23.6% (1.03) | 19.6% (0.85) | 20.9% (0.91) |
| CISI_2_Collections_in_Pakistan.pdf | 15.5% | 20.3% (1.31) | 21.5% (1.39) | 23.1% (1.49) | 21.2% (1.37) |
| CISI_1_Collections_in_India.pdf | 11.0% | 23.2% (2.10) | 19.2% (1.75) | 19.8% (1.79) | 22.1% (2.01) |
| Authority Structure and the Evolution of Early Writing Systems 2.pdf | 0.3% | 1.1% (3.21) | 1.4% (4.12) | 1.0% (3.00) | 1.1% (3.37) |
