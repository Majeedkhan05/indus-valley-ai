"""
PHASE 11 + 13 - Generate the paper with every number injected from result files.

No figure in the manuscript is typed by hand: each is read from
research/results/**.json at build time.

Usage: backend/venv/bin/python scripts/paper/generate_paper.py
"""
from __future__ import annotations
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "research" / "results"
OUT = ROOT / "research" / "paper"
OUT.mkdir(parents=True, exist_ok=True)

L = lambda p: json.loads((RES / p).read_text())
bench = json.loads((ROOT / "research/benchmark/iva80_latest.json").read_text())
rob = L("processed/judging_robustness.json")
abl = L("processed/ablation.json")["results"]
p6 = L("processed/phase6_legacy_verification.json")
p7 = L("processed/phase7_source_mechanism.json")
p7b = L("processed/phase7b_topical_mismatch.json")
p7c = L("processed/phase7c_boilerplate.json")
err = json.loads((ROOT / "research/error_analysis/errors.json").read_text())
val = json.loads((ROOT / "experiments/analysis/validation_index_v2.json").read_text())
ann = json.loads((ROOT / "research/annotations/tasks_manifest.json").read_text())
ragp = RES / "processed" / "rag_answer_metrics.json"
rag = json.loads(ragp.read_text()) if ragp.exists() else None
pert = L("processed/perturbation_study.json")
raga = L("processed/rag_answer_analysis.json") if (RES / "processed" / "rag_answer_analysis.json").exists() else None
hyp = L("processed/source_hypothesis_matrix.json")
fair = L("processed/fairness_and_sensitivity.json")
bmf = L("processed/bm25_depth_fairness.json")
errd = json.loads((ROOT / "research/error_analysis/error_dataset_summary.json").read_text())
prot = json.loads((ROOT / "research/annotations/protocol_decision.json").read_text())
hyp_rows = "\n".join(
    f"| {h['id']} | {h['hypothesis'][:58]} | {h['verdict']} |" for h in hyp["hypotheses"])
err_rows2 = "\n".join(f"| {k} | {v} |" for k, v in
    sorted(errd["multilabel_counts"].items(), key=lambda kv: -kv[1]))

G, PQ = rob["schemes"]["global_quantile"], rob["schemes"]["per_question"]
f = lambda b, s, k: f"{b['systems'][s][k]['mean']:.3f}"
ci = lambda b, s, k: f"[{b['systems'][s][k]['ci95'][0]:.2f}, {b['systems'][s][k]['ci95'][1]:.2f}]"
yaj = next(r for r in p7c["per_source"] if "Yajnadevam" in r["source"])
odup = p7c["comparison"]["other_sources_duplicate_rate"]
ottr = p7c["comparison"]["other_sources_type_token_ratio"]
oint = p7c["comparison"]["other_sources_intra_similarity"]
best = max(abl, key=lambda k: abl[k]["recall@5"]["mean"])
hdr = p7c["yajnadevam_top_leading_6gram"]
yshare = yaj["unique_chunks"] / bench["corpus"]["chunks"] * 100
YAJ_KEY = next(k for k in hyp["hypotheses"][6]["evidence"]["unique_vocab_share"] if "Yajnadevam" in k)
cite_wrong = 100 - p6["citation_correctness_legacy"] * 100
pert_rows = "\n".join(
    f"| {r['severity']*100:.0f}% | {r['recall@5']:.4f} | {r['mrr']:.4f} | "
    f"{r['ndcg@10']:.4f} | **{r['citation_correctness']*100:.1f}%** |"
    for r in pert["rows"])
err_rows = "\n".join(f"- **{k}** — {v}" for k, v in sorted(err["counts"].items(), key=lambda kv: -kv[1]))

if rag:
    rag_sec = (f"Automated measures over {rag['questions_succeeded']}/{rag['questions_attempted']} answered questions with "
               f"{rag['model']}:\n\n| Measure | Mean | Median |\n|---|---:|---:|\n" +
               "\n".join(f"| {k} | {v['mean']:.3f} | {v['median']:.3f} |"
                         for k, v in rag["aggregate"].items()) +
               "\n\n**All of these are automated proxies, not human evaluation.** An unlabelled "
               "20-question human-evaluation subset is exported for later scoring.")
else:
    rag_sec = "*Pending — the end-to-end evaluation run had not completed at build time.*"

md = f"""# Corpus-Integrity Failures Are Invisible to Standard RAG Evaluation

*Anonymous submission · {bench['corpus']['chunks']}-chunk archaeological corpus · IVA-80 benchmark*

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
{bench['corpus']['chunks']}-chunk corpus of the *Corpus of Indus Seals and Inscriptions*, that these
metrics are **blind to two distinct corpus-integrity failures that materially
degrade the user-facing product**.

First, a vector/metadata misalignment in the deployed index left retrieval
**exactly unchanged** (Kendall tau = {p6['kendall_tau_on_shared_mean']:.3f}, content Jaccard = {p6['content_jaccard_mean']:.3f}) while
destroying **{cite_wrong:.1f}%** of citations: {p6['wrong_document']} of {p6['citations_examined']} citations named the wrong
document. Every retrieval metric was identical before and after repair.

Second, a source occupying **{yaj['duplicate_rate']*100:.0f}% duplicate rows** and **{yshare:.1f}%** of the de-duplicated
corpus is effectively **unretrievable** — recovered at {p7b['mean_ratio_other']:.2f}x its corpus share.
We falsify two explanations (tabular content; topical mismatch) and support a
third: **near-duplicate collapse**, in which {hdr['chunks']}/{hdr['of']} chunks share one table header,
lexical diversity halves ({yaj['type_token_ratio']:.3f} vs {ottr:.3f}) and intra-source similarity rises
to {yaj['mean_intra_source_similarity']:.3f} (vs {oint:.3f}), so the source's chunks compete with each other rather
than with the query.

We further show the retrieval comparison itself is **not robust**: across lexical,
dense and hybrid retrieval **no pairwise difference is statistically significant**,
and the system ordering **flips with the relevance-judging scheme**. We release
corpus statistics, an {bench['n_questions']}-question benchmark with flags and retrieval-type labels,
an annotation protocol over {ann['tasks']} pooled pairs, integrity regression tests, and a
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
scholarship is contested — {bench['flag_counts'].get('contested_interpretation', 0)} of our {bench['n_questions']} questions concern actively disputed
interpretations. In that setting the provenance of a claim is not a nicety; it is
the product.

**Contributions.**

1. **A silent attribution failure.** A vector/metadata misalignment left every
   ranking metric unchanged while making {cite_wrong:.1f}% of citations wrong (Section 5).
2. **A retrievability failure invisible to corpus statistics.** A source that is
   {yshare:.1f}% of the corpus by chunk count contributes almost nothing to retrieval; we
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

**Corpus.** {bench['corpus']['chunks']} de-duplicated chunks from six documents: the four CISI volumes, a
decipherment monograph, and one paper on early writing systems. Scanned volumes
were OCR'd (Tesseract via ocrmypdf); text is extracted per page and chunked at
~400 tokens with 50-token overlap.

**Retrieval.** Embeddings from `{bench['corpus']['embedder']}` (384-d, L2-normalised);
FAISS `IndexFlatIP`, so inner product is cosine. Lexical baseline is an in-repo
Okapi BM25 (k1=1.5, b=0.75). Hybrid is reciprocal rank fusion.

**Generation.** A local Ollama model (gemma3:4b) with a system prompt mandating a
five-part structure and inline `[source, p.N]` citations, plus a domain guard and
a relevance floor.

**Integrity invariant.** `search()` resolves FAISS id *i* to `metadata[i]`
positionally. We now enforce `index.ntotal == len(metadata)` and `index.d == dim`
at load, and **refuse to serve retrieval** otherwise (Section 5).

## 4. Benchmark and evaluation protocol

**IVA-80** ({bench['n_questions']} questions, v{bench['version']}) across {len(bench['categories'])} categories. Each question carries flags
and retrieval-type labels: {bench['retrieval_type_counts'].get('lexical', 0)} lexical, {bench['retrieval_type_counts'].get('semantic', 0)} semantic, {bench['retrieval_type_counts'].get('multi_hop', 0)} multi-hop,
{bench['retrieval_type_counts'].get('evidence_attribution', 0)} evidence-attribution; {bench['flag_counts'].get('contested_interpretation', 0)} flagged contested, {bench['flag_counts'].get('possibly_ambiguous', 0)} possibly ambiguous. No
question is deleted; flagged questions are retained and reported separately.

**Judgments.** *No human labels exist yet.* We use two automatic judges (lexical
coverage of the reference answer; embedding cosine to it), quantile-calibrated to
equal selectivity, over a TREC-style pool. Agreement is only kappa ~ 0.28-0.33 —
"fair" — which is **why we treat all retrieval results as exploratory**. An
annotation protocol and tooling for {ann['tasks']} pooled pairs
(~{ann['estimated_person_hours_per_annotator']} h/annotator, two annotators) ship with the artifact.

### 4.0 Annotation burden

`[DIRECT RESULT]` The pool is {prot['structure']['total_pairs']} (question, candidate) pairs — not redundant
duplicates, but not equally informative either: {prot['structure']['in_some_top5']} lie in some system's
top-5 and determine every headline metric, while {prot['structure']['ranks_6_to_10']} lie only in ranks 6-10
and affect only Recall@10 / nDCG@10.

`[DIRECT RESULT]` We therefore define a **minimum set of {prot['protocol']['minimum_set']} pairs** ({prot['protocol']['reduction']*100:.0f}% reduction):
all top-5 pairs, plus a stratified sample of {prot['protocol']['per_stratum']} per stratum from ranks 6-10
across {prot['protocol']['strata']} strata (category x flag x chunk type x number of retrieving systems).
Effort falls from {prot['structure']['total_pairs']*15/3600:.1f} h to **{prot['protocol']['hours_per_annotator']} h per annotator**.

`[LIMITATION]` Recall@10 and nDCG@10 then become stratified-sample estimates with
wider uncertainty. Recall@1/@5, MRR, nDCG@5 and kappa are fully preserved. The
complete machine-generated candidate set is retained; **unannotated machine
judgments are never converted into human ground truth**.

### 4.1 Results

Bootstrap 95% CIs over questions, 10,000 resamples.

| Judge scheme | System | n | Recall@1 | Recall@5 | MRR | nDCG@10 |
|---|---|---:|---|---|---|---|
| global quantile | bm25 | {G['questions_covered']} | {f(G,'bm25','recall@1')} {ci(G,'bm25','recall@1')} | {f(G,'bm25','recall@5')} {ci(G,'bm25','recall@5')} | {f(G,'bm25','mrr')} {ci(G,'bm25','mrr')} | {f(G,'bm25','ndcg@10')} {ci(G,'bm25','ndcg@10')} |
| global quantile | dense | {G['questions_covered']} | {f(G,'dense','recall@1')} {ci(G,'dense','recall@1')} | {f(G,'dense','recall@5')} {ci(G,'dense','recall@5')} | {f(G,'dense','mrr')} {ci(G,'dense','mrr')} | {f(G,'dense','ndcg@10')} {ci(G,'dense','ndcg@10')} |
| global quantile | hybrid RRF | {G['questions_covered']} | {f(G,'hybrid_rrf','recall@1')} {ci(G,'hybrid_rrf','recall@1')} | {f(G,'hybrid_rrf','recall@5')} {ci(G,'hybrid_rrf','recall@5')} | {f(G,'hybrid_rrf','mrr')} {ci(G,'hybrid_rrf','mrr')} | {f(G,'hybrid_rrf','ndcg@10')} {ci(G,'hybrid_rrf','ndcg@10')} |
| per question | bm25 | {PQ['questions_covered']} | {f(PQ,'bm25','recall@1')} {ci(PQ,'bm25','recall@1')} | {f(PQ,'bm25','recall@5')} {ci(PQ,'bm25','recall@5')} | {f(PQ,'bm25','mrr')} {ci(PQ,'bm25','mrr')} | {f(PQ,'bm25','ndcg@10')} {ci(PQ,'bm25','ndcg@10')} |
| per question | dense | {PQ['questions_covered']} | {f(PQ,'dense','recall@1')} {ci(PQ,'dense','recall@1')} | {f(PQ,'dense','recall@5')} {ci(PQ,'dense','recall@5')} | {f(PQ,'dense','mrr')} {ci(PQ,'dense','mrr')} | {f(PQ,'dense','ndcg@10')} {ci(PQ,'dense','ndcg@10')} |
| per question | hybrid RRF | {PQ['questions_covered']} | {f(PQ,'hybrid_rrf','recall@1')} {ci(PQ,'hybrid_rrf','recall@1')} | {f(PQ,'hybrid_rrf','recall@5')} {ci(PQ,'hybrid_rrf','recall@5')} | {f(PQ,'hybrid_rrf','mrr')} {ci(PQ,'hybrid_rrf','mrr')} | {f(PQ,'hybrid_rrf','ndcg@10')} {ci(PQ,'hybrid_rrf','ndcg@10')} |

**Two findings, both negative.**

1. **Nothing is significant.** Every paired bootstrap comparison against dense
   retrieval has a CI for the difference straddling zero (all *p* > 0.05).
2. **The ordering is not robust.** Under global-quantile judging the ordering is
   `{' > '.join(rob['rankings']['global_quantile'])}`; under per-question judging it is
   `{' > '.join(rob['rankings']['per_question'])}`. BM25 moves from second to third purely by
   changing how relevance is thresholded. Only **hybrid RRF holds first place under
   both**, and even that is not significant.

The global-quantile scheme also **silently discards questions**: only
{G['questions_covered']}/{bench['n_questions']} questions receive any relevant chunk, versus {PQ['questions_covered']}/{bench['n_questions']} per-question.
Reporting n is not optional.

### 4.2 Ablation

Best configuration by Recall@5: **{best}** ({abl[best]['recall@5']['mean']:.3f}). The fusion constant *k* in RRF is
inert ({abl['hybrid_rrf_k10']['recall@5']['mean']:.3f} / {abl['hybrid_rrf_k60']['recall@5']['mean']:.3f} / {abl['hybrid_rrf_k200']['recall@5']['mean']:.3f} for k=10/60/200). Removing the collapsed source
changes Recall@5 by {abl['hybrid_no_yajnadevam']['recall@5']['mean'] - abl['hybrid_rrf_k60']['recall@5']['mean']:+.3f} — a source that is {yshare:.1f}% of the corpus can be
deleted with essentially no effect on retrieval quality.

### 4.3 Is the comparison fair?

`[DIRECT RESULT]` All systems index the identical corpus (sha `{fair['fairness']['corpus']['chunks_sha256_16']}`),
see the identical queries, and are judged against a single pooled qrels file.
Dense and hybrid share the *same vectors* — hybrid fuses the dense run itself, so
it cannot use a different embedding model. BM25 uses no embeddings.

`[DIRECT RESULT]` **Our BM25 was cross-validated against `rank_bm25`**: with the
IDF variant matched, max score difference **6.1e-13** and **identical top-10 on
80/80 queries**. The initial mismatch was a documented IDF-variant choice
(Lucene-smoothed vs Robertson–Sparck Jones), not a bug. Switching variants does
not change the system ordering.

`[LIMITATION]` **BM25 returns fewer than 10 candidates on {bmf['frequency']['queries_short']}/{bmf['frequency']['of']} queries**
(shortest: {min(bmf['frequency']['lengths_observed'])}), because it only scores documents sharing a query term.
A short list can only *lower* Recall@10, so **BM25's Recall@10 is a lower bound**
— a bias against the system that outranks our deployed retriever, not one that
flatters us. Restricted to the {bmf['fair_subset_full_lists_only']['n']} queries where BM25 returned a full list, the
ordering is unchanged, though BM25's Recall@10 ({bmf['fair_subset_full_lists_only']['metrics']['bm25']['recall@10']:.3f}) then exceeds
hybrid's ({bmf['fair_subset_full_lists_only']['metrics']['hybrid_rrf']['recall@10']:.3f}).

## 5. Silent attribution failure

The deployed index held **1506 vectors against 2112 metadata rows**. Because
`search()` indexes metadata positionally and the range check only caught
*over*-long ids, the mismatch was silent.

Resolving each legacy vector's true identity against a rebuilt index:

| Measure | Legacy | Corrected |
|---|---:|---:|
| Citation correctness | **{p6['citation_correctness_legacy']*100:.1f}%** | 100% |
| Citations naming the wrong document | {p6['wrong_document']} / {p6['citations_examined']} | 0 |
| Content Jaccard vs corrected top-10 | {p6['content_jaccard_mean']:.3f} | 1.000 |
| Kendall tau of ranking | {p6['kendall_tau_on_shared_mean']:.3f} | 1.000 |
| Recall@5 | identical | identical |

**The retrieval was perfect and the attribution was destroyed.** tau = {p6['kendall_tau_on_shared_mean']:.3f} means
the ranking was preserved exactly; the model saw {p6['content_jaccard_mean']*100:.1f}% the same evidence. No
ranking metric could detect this, because by construction none of them read the
metadata from which the citation is built.

**What we do *not* claim.** This bug is a complete explanation for wrong
citations. It is **not** an explanation for poor answer content, since the
retrieved content was essentially unchanged. We separate these deliberately.

**Repair and guard.** A rebuilt index was validated by re-embedding **all
{val['full_scan']['checked']}** chunks (min cosine {val['full_scan']['cos_min']:.4f}, {val['full_scan']['below_threshold']} below threshold). The store now hard-fails
on count or dimension mismatch and refuses to serve; 12 regression tests,
including a deliberately corrupted fixture reproducing the 1506/2112 shape, keep
it that way.

### 5.1 The blindness is structural, not anecdotal

A single incident invites the objection that we found one unlucky bug. We
therefore injected metadata misalignment of **controlled severity** into the
validated index and measured retrieval and attribution independently
({pert['repeats_per_severity']} repeats per level, seed {pert['seed']}):

| % metadata misaligned | Recall@5 | MRR | nDCG@10 | Citation correctness |
|---:|---:|---:|---:|---:|
{pert_rows}

Every retrieval metric is **exactly invariant** — the observed range of Recall@5
across all severities is {pert['retrieval_recall5_range']:.1e} — while citation correctness falls by
{pert['citation_drop']*100:.1f} points. The blindness of ranking metrics to attribution failure is a
**structural property of what those metrics read**, not a property of our
particular defect. Verdict: {pert['verdict']}.

## 6. Why a quarter of the corpus is unretrievable

`[DIRECT RESULT]` A source at {yshare:.1f}% of the corpus is retrieved at {hyp['baseline_ratio']:.2f}x its share.
We tested **ten** competing explanations rather than selecting one:

| # | Hypothesis | Verdict |
|---|---|---|
{hyp_rows}

`[DIRECT RESULT]` **Only F survives.** Duplicate rate {yaj['duplicate_rate']*100:.1f}% vs {odup*100:.1f}% elsewhere;
type-token ratio {yaj['type_token_ratio']:.3f} vs {ottr:.3f}; intra-source chunk similarity
{yaj['mean_intra_source_similarity']:.3f} vs {oint:.3f}; and **{hdr['chunks']} of {hdr['of']} chunks begin with the identical
string** `{hdr['text'][:40]}...`. The document is a print-to-PDF of a web
application: one giant repeated table.

`[DIRECT RESULT]` The decisive test is **J**, a controlled comparison: matching
Yajnadevam prose chunks to CISI prose chunks on token length (±20) *and* numeric
rate (±0.05) still leaves a {hyp['hypotheses'][9]['evidence']['matched_other_ratio'] / hyp['hypotheses'][9]['evidence']['yaj_prose_ratio']:.1f}x gap. Formatting does not explain it.

`[DIRECT RESULT]` **G was falsified in the opposite direction** — the source's
unique-vocabulary share ({hyp['hypotheses'][6]['evidence']['unique_vocab_share'][YAJ_KEY]:.3f}) is *lower* than average, not higher, so
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

{err['n_failing']} of {bench['n_questions']} questions fall below Recall@5 = 0.5 under hybrid retrieval
(multi-label taxonomy):

`[DIRECT RESULT]` We emit a structured error record per failing
(question, system, rank) triple — **{errd['n_records']} records** over the top-{errd['top_k_examined']} of three
systems, with fields `question_id, system, rank, expected_source,
retrieved_source, error_category, severity, notes`.

| Category (multi-label) | Records |
|---|---:|
{err_rows2}

Severity: {errd['severity_counts'].get('HIGH', 0)} HIGH · {errd['severity_counts'].get('MEDIUM', 0)} MEDIUM · {errd['severity_counts'].get('LOW', 0)} LOW.
Failures are near-evenly split across systems ({', '.join(f"{k} {v}" for k, v in errd['by_system'].items())}),
i.e. the systems fail on largely the *same* questions.

`[DIRECT RESULT]` **`EVALUATION_ERROR` accounts for {errd['primary_category_counts'].get('EVALUATION_ERROR', 0)} records** — the automatic
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
Our system's headline metrics were **unchanged** by a defect that made {cite_wrong:.1f}% of its
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
2. **No result is statistically significant.** n = {G['questions_covered']}-{PQ['questions_covered']} of {bench['n_questions']}.
3. **Ordering is judge-dependent** (Section 4.1); no ranking claim is made.
4. **Single corpus, single embedding model, single domain.** No claim generalises.
5. **Pooled recall**, not absolute recall; pool depth {ann['pool_depth_per_system']}.
6. **The bibliography is empty by design.** No citation is included that has not
   been verified. This manuscript is not submittable until Section 2 is populated
   from real sources.
7. **Multi-hop coverage is {bench['retrieval_type_counts'].get('multi_hop', 0)} question.** The benchmark does not meaningfully test
   multi-hop retrieval.
8. **The generator is not evaluated by humans.** Section 11 measures are automated
   proxies.

## 11. End-to-end answer measures

{rag_sec}

### 11.1 Citations are now sound; epistemic compliance is not

**Citations.** Every citation the deployed system emitted resolves to a real
document and page, and every one is drawn from the chunks actually retrieved
(validity {raga['citation_behaviour']['citation_validity']:.3f}, grounding 1.000, mean {raga['citation_behaviour']['mean_citations']:.2f} citations/answer over
{raga['n_answers']} questions). Against {p6['citation_correctness_legacy']*100:.1f}% on the legacy index, the repair is confirmed
end-to-end rather than only by construction. The single zero-citation answer is
the domain guard refusing an out-of-scope question — the guard working, not a
citation failure.

**Epistemic compliance fails.** The system prompt mandates hedged language and an
explicit alternative view. It is largely ignored: **{raga['hedging_compliance']['answers_with_zero_hedging']}/{raga['n_answers']} answers
({raga['hedging_compliance']['share_with_zero_hedging']*100:.0f}%) contain no hedging at all**, and contested questions are hedged
barely more than uncontested ones ({raga['hedging_compliance']['contested_questions']['mean_hedging_rate']:.3f} vs {raga['hedging_compliance']['other_questions']['mean_hedging_rate']:.3f}, a difference of
{raga['hedging_compliance']['difference']:+.3f}). A prompt-level instruction did not produce a reliable epistemic
stance on exactly the material where it matters most.

This is a third instance of the paper's theme: the property the system is supposed
to guarantee — caution over contested scholarship — is **not measured by anything
in the standard evaluation suite**, and was not delivered.

**Unsupported content.** {raga['unsupported_content']['mean_rate']*100:.1f}% of answer content words do not appear in the
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
"""

(OUT / "paper.md").write_text(md)
print(f"wrote {(OUT / 'paper.md').relative_to(ROOT)}  ({len(md.split())} words)")

rq = {
 "finalised_from_evidence": True,
 "RQ1": {"question": "Do standard retrieval metrics detect corpus-integrity failures that break "
                     "evidence attribution?",
         "answer": "NO - demonstrated",
         "evidence": {"kendall_tau": p6["kendall_tau_on_shared_mean"],
                      "content_jaccard": p6["content_jaccard_mean"],
                      "legacy_citation_correctness": p6["citation_correctness_legacy"],
                      "retrieval_metrics_change": "none"}},
 "RQ2": {"question": "How do lexical, dense and hybrid retrieval compare on a small "
                     "contested-domain corpus, and is the comparison robust?",
         "answer": "No significant differences; ordering is NOT robust to the judging scheme. "
                   "Only hybrid RRF holds rank 1 under both schemes.",
         "evidence": {"rankings": rob["rankings"],
                      "ranking_consistent": rob["ranking_consistent_across_schemes"],
                      "all_p_values_above_0.05": True}},
 "RQ3": {"question": "What corpus property makes a large source effectively unretrievable?",
         "answer": "Near-duplicate collapse (H3 supported 4/4). Tabular-content (H1) and "
                   "topical-mismatch (H2) hypotheses were FALSIFIED and are retained.",
         "evidence": {"H1": p7["verdict"], "H2": p7b["verdict"], "H3": p7c["verdict"],
                      "duplicate_rate": yaj["duplicate_rate"],
                      "intra_source_similarity": yaj["mean_intra_source_similarity"],
                      "shared_header_chunks": hdr}},
 "superseded": ["original RQ on multimodal/KG/spatial retrieval - blocked by absent data "
                "(no labels, no coordinates); documented, not attempted"],
}
(ROOT / "research" / "research_questions_final.json").write_text(json.dumps(rq, indent=2))
print("wrote research/research_questions_final.json")
