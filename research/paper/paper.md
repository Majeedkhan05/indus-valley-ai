# Corpus-Integrity Failures Are Invisible to Standard RAG Evaluation

*Anonymous submission · 1199-chunk archaeological corpus · IVA-80 benchmark*

## Claim classification

Every substantive claim below is tagged:

`[DIRECT RESULT]` measured, traceable to a result file ·
`[SUPPORTED BY LITERATURE]` standard, needs a citation ·
`[INTERPRETATION]` our reading of a result ·
`[HYPOTHESIS]` proposed, not established ·
`[LIMITATION]` a known weakness

## Candidate titles

1. **Corpus-Integrity Failures Are Invisible to Standard RAG Evaluation**
2. When Retrieval Is Right and Citations Are Wrong: Silent Attribution Failure in RAG
3. Retrieval Metrics Do Not Measure Evidence Attribution
4. Diagnosing Corpus Integrity in Retrieval-Augmented Generation over Historical Archives
5. The 25% Source That Cannot Be Retrieved: Near-Duplicate Collapse in Domain Corpora

---

## Abstract

Retrieval-augmented generation is evaluated almost entirely with ranking metrics —
Recall@K, MRR, nDCG. We show, on a deployed archaeological QA system over a
1199-chunk corpus of the *Corpus of Indus Seals and Inscriptions*, that these
metrics are **blind to two distinct corpus-integrity failures that materially
degrade the user-facing product**.

First, a vector/metadata misalignment in the deployed index left retrieval
**exactly unchanged** (Kendall tau = 1.000, content Jaccard = 0.965) while
destroying **96.1%** of citations: 769 of 800 citations named the wrong
document. Every retrieval metric was identical before and after repair.

Second, a source occupying **75% duplicate rows** and **25.3%** of the de-duplicated
corpus is effectively **unretrievable** — recovered at 0.27x its corpus share.
We falsify two explanations (tabular content; topical mismatch) and support a
third: **near-duplicate collapse**, in which 302/303 chunks share one table header,
lexical diversity halves (0.121 vs 0.214) and intra-source similarity rises
to 0.894 (vs 0.662), so the source's chunks compete with each other rather
than with the query.

We further show the retrieval comparison itself is **not robust**: across lexical,
dense and hybrid retrieval **no pairwise difference is statistically significant**,
and the system ordering **flips with the relevance-judging scheme**. We release
corpus statistics, an 80-question benchmark with flags and retrieval-type labels,
an annotation protocol over 1382 pooled pairs, integrity regression tests, and a
reproducible pipeline.

**Contribution.** Not a better retriever — a demonstration that the standard
evaluation protocol cannot see failures that break the deliverable, plus
diagnostics that can.

---

## 1. Introduction

RAG systems are judged on whether they retrieve the right passages. The product,
however, promises something stronger: an answer *plus a verifiable citation*. We
report a deployed system in which those two came apart completely.

Historical and archaeological corpora make this acute. Sources are scanned and
OCR'd, formats are heterogeneous (prose, catalogues, glyph tables), and the
scholarship is contested — 22 of our 80 questions concern actively disputed
interpretations. In that setting the provenance of a claim is not a nicety; it is
the product.

**Contributions.**

1. **A silent attribution failure.** A vector/metadata misalignment left every
   ranking metric unchanged while making 96.1% of citations wrong (Section 5).
2. **A retrievability failure invisible to corpus statistics.** A source that is
   25.3% of the corpus by chunk count contributes almost nothing to retrieval; we
   falsify two hypotheses and support a third (Section 6).
3. **A robustness result.** No retriever difference is significant, and the
   ordering depends on the judging scheme (Section 4).
4. **Artifacts.** Benchmark, annotation protocol and tooling, integrity tests,
   diagnostics, and a one-command reproduction (Section 8).

## 2. Related work

Positioned against: dense retrieval (DPR, ANCE); lexical baselines (BM25) and the
repeated finding that BM25 remains competitive in specialised domains; hybrid
fusion (reciprocal rank fusion); RAG and attribution/faithfulness evaluation;
pooled evaluation from the TREC tradition and its known pool-depth bias; and
digital-humanities retrieval over OCR'd archives.

*The reference list is deliberately not fabricated. Citations must be inserted
from verified sources before submission; the claims above are standard and
uncontroversial, but this manuscript ships with an* **empty verified bibliography**
*rather than invented keys.* See Section 10.

## 3. System and corpus

**Corpus.** 1199 de-duplicated chunks from six documents: the four CISI volumes, a
decipherment monograph, and one paper on early writing systems. Scanned volumes
were OCR'd (Tesseract via ocrmypdf); text is extracted per page and chunked at
~400 tokens with 50-token overlap.

**Retrieval.** Embeddings from `BAAI/bge-small-en-v1.5` (384-d, L2-normalised);
FAISS `IndexFlatIP`, so inner product is cosine. Lexical baseline is an in-repo
Okapi BM25 (k1=1.5, b=0.75). Hybrid is reciprocal rank fusion.

**Generation.** A local Ollama model (gemma3:4b) with a system prompt mandating a
five-part structure and inline `[source, p.N]` citations, plus a domain guard and
a relevance floor.

**Integrity invariant.** `search()` resolves FAISS id *i* to `metadata[i]`
positionally. We now enforce `index.ntotal == len(metadata)` and `index.d == dim`
at load, and **refuse to serve retrieval** otherwise (Section 5).

## 4. Benchmark and evaluation protocol

**IVA-80** (80 questions, v2.0.0) across 10 categories. Each question carries flags
and retrieval-type labels: 72 lexical, 63 semantic, 1 multi-hop,
15 evidence-attribution; 22 flagged contested, 7 possibly ambiguous. No
question is deleted; flagged questions are retained and reported separately.

**Judgments.** *No human labels exist yet.* We use two automatic judges (lexical
coverage of the reference answer; embedding cosine to it), quantile-calibrated to
equal selectivity, over a TREC-style pool. Agreement is only kappa ~ 0.28-0.33 —
"fair" — which is **why we treat all retrieval results as exploratory**. An
annotation protocol and tooling for 1382 pooled pairs
(~5.8 h/annotator, two annotators) ship with the artifact.

### 4.0 Annotation burden

`[DIRECT RESULT]` The pool is 1382 (question, candidate) pairs — not redundant
duplicates, but not equally informative either: 741 lie in some system's
top-5 and determine every headline metric, while 641 lie only in ranks 6-10
and affect only Recall@10 / nDCG@10.

`[DIRECT RESULT]` We therefore define a **minimum set of 855 pairs** (38% reduction):
all top-5 pairs, plus a stratified sample of 2 per stratum from ranks 6-10
across 63 strata (category x flag x chunk type x number of retrieving systems).
Effort falls from 5.8 h to **3.6 h per annotator**.

`[LIMITATION]` Recall@10 and nDCG@10 then become stratified-sample estimates with
wider uncertainty. Recall@1/@5, MRR, nDCG@5 and kappa are fully preserved. The
complete machine-generated candidate set is retained; **unannotated machine
judgments are never converted into human ground truth**.

### 4.1 Results

Bootstrap 95% CIs over questions, 10,000 resamples.

| Judge scheme | System | n | Recall@1 | Recall@5 | MRR | nDCG@10 |
|---|---|---:|---|---|---|---|
| global quantile | bm25 | 39 | 0.162 [0.09, 0.25] | 0.431 [0.31, 0.55] | 0.545 [0.41, 0.68] | 0.503 [0.40, 0.61] |
| global quantile | dense | 39 | 0.099 [0.04, 0.17] | 0.383 [0.28, 0.49] | 0.467 [0.35, 0.59] | 0.437 [0.35, 0.53] |
| global quantile | hybrid RRF | 39 | 0.140 [0.07, 0.23] | 0.466 [0.35, 0.59] | 0.560 [0.44, 0.68] | 0.517 [0.43, 0.61] |
| per question | bm25 | 77 | 0.099 [0.07, 0.14] | 0.332 [0.28, 0.39] | 0.663 [0.58, 0.74] | 0.526 [0.46, 0.59] |
| per question | dense | 77 | 0.090 [0.06, 0.13] | 0.365 [0.31, 0.42] | 0.667 [0.58, 0.75] | 0.591 [0.53, 0.65] |
| per question | hybrid RRF | 77 | 0.117 [0.09, 0.15] | 0.392 [0.35, 0.44] | 0.744 [0.67, 0.82] | 0.599 [0.55, 0.65] |

**Two findings, both negative.**

1. **Nothing is significant.** Every paired bootstrap comparison against dense
   retrieval has a CI for the difference straddling zero (all *p* > 0.05).
2. **The ordering is not robust.** Under global-quantile judging the ordering is
   `hybrid_rrf > bm25 > dense`; under per-question judging it is
   `hybrid_rrf > dense > bm25`. BM25 moves from second to third purely by
   changing how relevance is thresholded. Only **hybrid RRF holds first place under
   both**, and even that is not significant.

The global-quantile scheme also **silently discards questions**: only
39/80 questions receive any relevant chunk, versus 77/80 per-question.
Reporting n is not optional.

### 4.2 Ablation

Best configuration by Recall@5: **hybrid_no_yajnadevam** (0.459). The fusion constant *k* in RRF is
inert (0.458 / 0.458 / 0.458 for k=10/60/200). Removing the collapsed source
changes Recall@5 by +0.001 — a source that is 25.3% of the corpus can be
deleted with essentially no effect on retrieval quality.

### 4.3 Is the comparison fair?

`[DIRECT RESULT]` All systems index the identical corpus (sha `81292fcefd537433`),
see the identical queries, and are judged against a single pooled qrels file.
Dense and hybrid share the *same vectors* — hybrid fuses the dense run itself, so
it cannot use a different embedding model. BM25 uses no embeddings.

`[DIRECT RESULT]` **Our BM25 was cross-validated against `rank_bm25`**: with the
IDF variant matched, max score difference **6.1e-13** and **identical top-10 on
80/80 queries**. The initial mismatch was a documented IDF-variant choice
(Lucene-smoothed vs Robertson–Sparck Jones), not a bug. Switching variants does
not change the system ordering.

`[LIMITATION]` **BM25 returns fewer than 10 candidates on 9/80 queries**
(shortest: 1), because it only scores documents sharing a query term.
A short list can only *lower* Recall@10, so **BM25's Recall@10 is a lower bound**
— a bias against the system that outranks our deployed retriever, not one that
flatters us. Restricted to the 33 queries where BM25 returned a full list, the
ordering is unchanged, though BM25's Recall@10 (0.693) then exceeds
hybrid's (0.671).

## 5. Silent attribution failure

The deployed index held **1506 vectors against 2112 metadata rows**. Because
`search()` indexes metadata positionally and the range check only caught
*over*-long ids, the mismatch was silent.

Resolving each legacy vector's true identity against a rebuilt index:

| Measure | Legacy | Corrected |
|---|---:|---:|
| Citation correctness | **3.9%** | 100% |
| Citations naming the wrong document | 769 / 800 | 0 |
| Content Jaccard vs corrected top-10 | 0.965 | 1.000 |
| Kendall tau of ranking | 1.000 | 1.000 |
| Recall@5 | identical | identical |

**The retrieval was perfect and the attribution was destroyed.** tau = 1.000 means
the ranking was preserved exactly; the model saw 96.5% the same evidence. No
ranking metric could detect this, because by construction none of them read the
metadata from which the citation is built.

**What we do *not* claim.** This bug is a complete explanation for wrong
citations. It is **not** an explanation for poor answer content, since the
retrieved content was essentially unchanged. We separate these deliberately.

**Repair and guard.** A rebuilt index was validated by re-embedding **all
1199** chunks (min cosine 1.0000, 0 below threshold). The store now hard-fails
on count or dimension mismatch and refuses to serve; 12 regression tests,
including a deliberately corrupted fixture reproducing the 1506/2112 shape, keep
it that way.

### 5.1 The blindness is structural, not anecdotal

A single incident invites the objection that we found one unlucky bug. We
therefore injected metadata misalignment of **controlled severity** into the
validated index and measured retrieval and attribution independently
(5 repeats per level, seed 42):

| % metadata misaligned | Recall@5 | MRR | nDCG@10 | Citation correctness |
|---:|---:|---:|---:|---:|
| 0% | 0.3650 | 0.6670 | 0.5914 | **100.0%** |
| 10% | 0.3650 | 0.6670 | 0.5914 | **90.4%** |
| 25% | 0.3650 | 0.6670 | 0.5914 | **73.2%** |
| 50% | 0.3650 | 0.6670 | 0.5914 | **48.3%** |
| 75% | 0.3650 | 0.6670 | 0.5914 | **25.9%** |
| 100% | 0.3650 | 0.6670 | 0.5914 | **0.6%** |

Every retrieval metric is **exactly invariant** — the observed range of Recall@5
across all severities is 0.0e+00 — while citation correctness falls by
99.4 points. The blindness of ranking metrics to attribution failure is a
**structural property of what those metrics read**, not a property of our
particular defect. Verdict: SUPPORTED.

## 6. Why a quarter of the corpus is unretrievable

`[DIRECT RESULT]` A source at 25.3% of the corpus is retrieved at 0.26x its share.
We tested **ten** competing explanations rather than selecting one:

| # | Hypothesis | Verdict |
|---|---|---|
| A | Vocabulary mismatch with the benchmark explains under-retr | INCONCLUSIVE |
| B | Chunk length explains under-retrieval | NOT SUPPORTED |
| C | Token-distribution divergence from queries explains under- | INCONCLUSIVE |
| D | Numeric/glyph-heavy content explains under-retrieval | NOT SUPPORTED |
| E | Anomalous embedding behaviour (norm/anisotropy) explains u | PARTIALLY SUPPORTED |
| F | Duplicate / near-duplicate collapse explains under-retriev | SUPPORTED |
| G | Source-specific terminology (jargon islands) explains unde | NOT SUPPORTED |
| H | Overall corpus composition (source shares) explains the re | NOT SUPPORTED |
| I | Query category composition (benchmark asks about other top | NOT SUPPORTED |
| J | Chunking strategy / formatting alone explains it (source i | NOT SUPPORTED |

`[DIRECT RESULT]` **Only F survives.** Duplicate rate 75.0% vs 0.0% elsewhere;
type-token ratio 0.121 vs 0.214; intra-source chunk similarity
0.894 vs 0.662; and **302 of 303 chunks begin with the identical
string** `Seal ID CISI ID Len Inscription(R...`. The document is a print-to-PDF of a web
application: one giant repeated table.

`[DIRECT RESULT]` The decisive test is **J**, a controlled comparison: matching
Yajnadevam prose chunks to CISI prose chunks on token length (±20) *and* numeric
rate (±0.05) still leaves a 3.4x gap. Formatting does not explain it.

`[DIRECT RESULT]` **G was falsified in the opposite direction** — the source's
unique-vocabulary share (0.382) is *lower* than average, not higher, so
the "jargon island" account is wrong.

`[INTERPRETATION]` Chunks that are near-copies of each other occupy the same
region of embedding space and compete with each other rather than with the query.

`[LIMITATION]` A and C are **INCONCLUSIVE**: correlations over six sources are not
interpretable. B is under-powered (two of three length bands are empty for this
source). **No intervention experiment** — de-duplicating the source and
re-indexing — has been run, so no causal chain is proven.

`[INTERPRETATION]` Every standard corpus statistic reports this source as a
quarter of the corpus. Only duplication rate, lexical diversity and intra-source
similarity reveal that it is inert. We recommend reporting all three.

## 7. Error analysis

60 of 80 questions fall below Recall@5 = 0.5 under hybrid retrieval
(multi-label taxonomy):

`[DIRECT RESULT]` We emit a structured error record per failing
(question, system, rank) triple — **553 records** over the top-5 of three
systems, with fields `question_id, system, rank, expected_source,
retrieved_source, error_category, severity, notes`.

| Category (multi-label) | Records |
|---|---:|
| SOURCE_ATTRIBUTION | 311 |
| SEMANTIC_MISMATCH | 190 |
| CONTESTED_INTERPRETATION | 110 |
| PAGE_ATTRIBUTION | 107 |
| OCR | 89 |
| CHUNKING | 54 |
| AMBIGUITY | 41 |
| INSUFFICIENT_EVIDENCE | 37 |
| CORPUS_BIAS | 21 |
| MULTI_HOP | 15 |
| OTHER | 4 |

Severity: 237 HIGH · 209 MEDIUM · 107 LOW.
Failures are near-evenly split across systems (bm25 182, dense 190, hybrid_rrf 181),
i.e. the systems fail on largely the *same* questions.

`[DIRECT RESULT]` **`EVALUATION_ERROR` accounts for 123 records** — the automatic
judge produced no relevant chunk at all. That is a failure of *our evaluation*,
not of the system, and it is the strongest argument for completing human
annotation before any ranking claim is made.

## 8. Reproducibility

One command rebuilds every number: corpus statistics, benchmark, all retrieval
runs, ablations, diagnostics, tables and figures. Seeds are fixed (42); model,
FAISS and platform versions are recorded per experiment; the index ships with a
manifest and SHA-256 prefixes. Tables and figures are generated from the JSON
result files, never typed.

## 9. Discussion

The community optimises retrieval metrics because they are cheap and comparable.
Our system's headline metrics were **unchanged** by a defect that made 96.1% of its
user-facing citations wrong, and were **barely moved** by deleting a quarter of the
corpus. Both failures are properties of the *corpus and its bookkeeping*, not of
the ranking function — which is precisely where the metrics do not look.

We therefore argue for reporting, alongside Recall@K: an index-integrity check,
per-source duplication and lexical-diversity statistics, and citation correctness
measured independently of retrieval correctness.

## 10. Limitations

1. **No human relevance judgments exist.** All retrieval numbers rest on automatic
   judges with kappa ~ 0.28-0.33. They are exploratory. The protocol and tooling
   are released; the labels are not, because they have not been produced.
2. **No result is statistically significant.** n = 39-77 of 80.
3. **Ordering is judge-dependent** (Section 4.1); no ranking claim is made.
4. **Single corpus, single embedding model, single domain.** No claim generalises.
5. **Pooled recall**, not absolute recall; pool depth 10.
6. **The bibliography is empty by design.** No citation is included that has not
   been verified. This manuscript is not submittable until Section 2 is populated
   from real sources.
7. **Multi-hop coverage is 1 question.** The benchmark does not meaningfully test
   multi-hop retrieval.
8. **The generator is not evaluated by humans.** Section 11 measures are automated
   proxies.

## 11. End-to-end answer measures

Automated measures over 80/80 answered questions with gemma3:4b via Ollama:

| Measure | Mean | Median |
|---|---:|---:|
| citation_count | 5.925 | 6.000 |
| citation_validity | 1.000 | 1.000 |
| citation_grounding | 1.000 | 1.000 |
| answer_relevance_cos | 0.790 | 0.802 |
| answer_evidence_cos | 0.729 | 0.748 |
| reference_overlap | 0.132 | 0.111 |
| unsupported_rate | 0.334 | 0.270 |
| hedging_rate | 0.224 | 0.183 |
| latency_s | 33.418 | 15.780 |
| confidence | 0.665 | 0.690 |
| answer_words | 93.338 | 95.500 |

**All of these are automated proxies, not human evaluation.** An unlabelled 20-question human-evaluation subset is exported for later scoring.

### 11.1 Citations are now sound; epistemic compliance is not

**Citations.** Every citation the deployed system emitted resolves to a real
document and page, and every one is drawn from the chunks actually retrieved
(validity 1.000, grounding 1.000, mean 5.92 citations/answer over
80 questions). Against 3.9% on the legacy index, the repair is confirmed
end-to-end rather than only by construction. The single zero-citation answer is
the domain guard refusing an out-of-scope question — the guard working, not a
citation failure.

**Epistemic compliance fails.** The system prompt mandates hedged language and an
explicit alternative view. It is largely ignored: **36/80 answers
(45%) contain no hedging at all**, and contested questions are hedged
barely more than uncontested ones (0.242 vs 0.217, a difference of
+0.026). A prompt-level instruction did not produce a reliable epistemic
stance on exactly the material where it matters most.

This is a third instance of the paper's theme: the property the system is supposed
to guarantee — caution over contested scholarship — is **not measured by anything
in the standard evaluation suite**, and was not delivered.

**Unsupported content.** 33.4% of answer content words do not appear in the
retrieved evidence. This is a **lexical upper bound, not a hallucination rate**:
correct paraphrase is counted as unsupported. It is reported as a ceiling.

## 12. Conclusion

We do not present a better retriever. We present a deployed RAG system in which
standard evaluation was **fully satisfied** while the product was broken in two
independent ways, and a set of cheap diagnostics that expose both. On a corpus of
contested historical scholarship — where the citation *is* the deliverable — that
distinction is the whole point.

---

*Generated from result files by `scripts/paper/generate_paper.py`. Every numeric
value above is read at build time from `research/results/`.*
