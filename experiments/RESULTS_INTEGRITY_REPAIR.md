# Integrity Repair — Results (E002, E003, E004)

Generated from `experiments/results/`. Every number traces to a JSON file.

---

## §3 Validation of the corrected index

Full scan — **every** vector re-embedded with the production configuration and
compared to the stored vector. Not sampled.

| Check | Result |
|---|---|
| count equality (`ntotal == len(metadata)`) | **PASS** — 1199 == 1199 |
| vectors L2-normalised | **PASS** |
| embedder dim == index.d | **PASS** (384) |
| full re-embedding alignment | **PASS** — 0/1199 below cos 0.99 |
| cosine min / mean | 1.000000 / 1.000000 |

Required id classes (first, early, boundary ~311, random, late, final) all returned
cosine 1.000 — see `experiments/analysis/validation_index_v2.json`.

**Verdict: PASS.**

---

## §6 + §8 The bug's actual effect — measured, not assumed

Legacy vectors were resolved to their true identity by matching against the
corrected index (1506/1506 resolved at cos ≥ 0.99), giving an exact
answer to "what did the citation *claim* vs what was the chunk *really*".

**Metadata integrity of the legacy index**

Legacy `metadata[i]` correctly described `vector[i]` for only
**307/1506 ids (20.4%)**.

**Citation correctness over the 80 benchmark queries, top-6**

| Measure | Legacy | Corrected |
|---|---:|---:|
| hits examined | 480 | 480 |
| citations correct | **11 (2.3%)** | **100%** (validated) |
| wrong document | **469** | 0 |
| right document, wrong page | 0 | 0 |
| queries with ≥1 wrong citation | **80/80** | 0/80 |
| queries with ALL citations wrong | **72/80** | 0/80 |

### The decisive nuance

Mean top-6 **content** overlap between what legacy actually retrieved and what the
corrected system retrieves: **0.979**.

So the bug did **not** meaningfully change *which text* was retrieved. It changed
*what that text was labelled as*. The language model received essentially correct
evidence; the user was shown almost entirely wrong attributions.

### Does this explain the presentation failure?

**Partially, and only partially — the evidence does not support a stronger claim.**

- It **fully explains** citations that did not match the answer, and the same
  sources appearing for unrelated questions. 97.7% of shown citations were wrong.
- It **does not explain** poor answer *content*, because the retrieved content was
  97.9% identical to the corrected system's. Content quality problems must
  have another cause (model size, prompt, or retrieval quality itself).

Stated precisely: **the bug is a demonstrated, complete explanation for the
citation failures, and is not an explanation for content failures.**

---

## §7 Retrieval evaluation, all systems

Selectivity 0.05, κ = 0.277, n = 45 questions with ≥1 judged-relevant chunk.
95% CIs are non-parametric bootstrap over questions (10,000 resamples).

| System | Recall@1 | Recall@5 | Recall@10 | MRR | nDCG@10 |
|---|---|---|---|---|---|
| legacy_vector | 0.102 [0.04, 0.18] | 0.304 [0.21, 0.40] | 0.482 [0.37, 0.59] | 0.458 [0.35, 0.58] | 0.384 [0.30, 0.47] |
| corrected_vector | 0.102 [0.04, 0.18] | 0.304 [0.21, 0.41] | 0.482 [0.37, 0.59] | 0.458 [0.35, 0.57] | 0.384 [0.30, 0.47] |
| bm25 | 0.098 [0.05, 0.16] | 0.260 [0.17, 0.35] | 0.434 [0.33, 0.54] | 0.488 [0.36, 0.61] | 0.374 [0.29, 0.47] |
| hybrid_rrf | 0.098 [0.05, 0.16] | 0.348 [0.25, 0.45] | 0.502 [0.40, 0.60] | 0.566 [0.45, 0.68] | 0.424 [0.34, 0.51] |

Per-system files: `experiments/results/E003_{legacy_vector,corrected_vector,bm25,hybrid_rrf}/`.

### What this shows

1. **`legacy_vector` and `corrected_vector` are identical on every metric.**
   Expected: the vectors are the same, only the labels differed. **The repair did
   not improve retrieval quality, and it was never supposed to.** Reported as-is.
2. `hybrid_rrf` has the highest point estimates, but **its CI overlaps
   `corrected_vector` on every metric** (e.g. R@5 0.348 [0.25, 0.45] vs
   0.304 [0.21, 0.41]). **No significant difference is demonstrated.**
3. The earlier E001 impression that the dense retriever was "worst at every
   operating point" **does not survive** the addition of confidence intervals.
   Treat it as withdrawn.

---

## §9 Corpus accounting (recomputed programmatically)

| Stage | Rows |
|---|---:|
| raw rows | 2112 |
| unique texts | 1199 |
| duplicate rows | 913 |
| deduplicated corpus | 1199 |
| arithmetic check (2112 − 913 = 1199) | **True** |

| Source | Raw chunks | Raw share | Dedup chunks | Dedup share |
|---|---:|---:|---:|---:|
| Indus Inscriptions by Yajnadevam.pdf | 1212 | 57.4% | 303 | 25.3% |
| CISI_3.1_Mohenjodaro_and_Harappa.pdf | 298 | 14.1% | 298 | 24.9% |
| CISI_3.2_Recent_Findings_from_India___Pakistan.pdf | 276 | 13.1% | 276 | 23.0% |
| CISI_2_Collections_in_Pakistan.pdf | 186 | 8.8% | 186 | 15.5% |
| CISI_1_Collections_in_India.pdf | 132 | 6.2% | 132 | 11.0% |
| Authority Structure and the Evolution of Early Writi | 8 | 0.4% | 4 | 0.3% |

Recomputed: Yajnadevam **25.3%**, CISI combined **74.4%**.

**Correction to the correction.** The audit first said Yajnadevam was ~80% of the
corpus. That figure divided 1,212 by the *vector* count (1,506) rather than the
*row* count (2,112). The true raw share was **57.4%**, and after de-duplication
**25.3%**. Both the original claim and its first correction were imprecise;
this is the recomputed figure.

---

## §10 Source-preference diagnostics — cause still UNKNOWN

Yajnadevam is retrieved at ≈0.14× its corpus share; CISI 1 at ≈2.1×. Candidate
factors measured (correlates only — **no causal claim is made**):

| Source | Share | Tokens/chunk | Dict-word rate | Numeric rate | Query-vocab coverage | Mean cos→queries |
|---|---:|---:|---:|---:|---:|---:|
| Indus Inscriptions by Yajnadevam.pdf | 25.3% | 163 | 0.48 | 0.37 | 0.214 | 0.506 |
| CISI_3.1_Mohenjodaro_and_Harappa.pdf | 24.9% | 208 | 0.48 | 0.38 | 0.663 | 0.508 |
| CISI_3.2_Recent_Findings_from_India___Pakist | 23.0% | 210 | 0.62 | 0.29 | 0.522 | 0.481 |
| CISI_2_Collections_in_Pakistan.pdf | 15.5% | 154 | 0.65 | 0.26 | 0.561 | 0.509 |
| CISI_1_Collections_in_India.pdf | 11.0% | 154 | 0.68 | 0.23 | 0.547 | 0.506 |
| Authority Structure and the Evolution of Ear | 0.3% | 173 | 0.97 | 0.03 | 0.103 | 0.535 |

**Strongest correlate:** Yajnadevam's vocabulary covers only
**0.214** of the benchmark's query/answer vocabulary, versus 0.52–0.66 for the
CISI volumes. It also has the lowest dictionary-word rate paired with the highest
numeric-token rate (0.37) — consistent with tabular glyph/ID listings rather
than prose.

**But** its mean cosine to queries (0.506) is indistinguishable from the CISI
volumes (0.481–0.509). So an "embeddings find it dissimilar on average"
explanation is **not** supported by the measurement.

**Cause: UNKNOWN.** A controlled experiment (e.g. re-chunking Yajnadevam as prose
and re-measuring) has not been run.

---

## Limitations

1. Relevance judgments remain **automatic proxies**, κ = 0.277. Not human, not
   expert, not ground truth. `docs/annotation-protocol.md` is the gate.
2. Retrieval-only. No answer-correctness, faithfulness, or hallucination metrics.
3. Pooled recall, not absolute recall.
4. n = 45/80 at the primary operating point.
5. No claim of significance survives the confidence intervals except the citation
   result, which is a direct count and not an estimate.
6. `paper/eval/results.jsonl` (27 rows) remains void — produced under the bug.
