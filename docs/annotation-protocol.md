# Annotation Protocol — IVA-80 relevance judgments

**Status: DEFINED, NOT YET EXECUTED.** No human annotation has taken place.
Until it does, all reported retrieval metrics rest on automatic proxy judgments
and must be labelled as such.

## Why this is needed
E001 evaluates retrieval using two automatic judges. Their agreement is only
κ = 0.13–0.36 ("slight" to "fair"). At that level the judgments are too noisy to
settle close comparisons — and indeed the system ranking is **not stable** across
judging thresholds. Human judgments are the only way to fix this.

## Unit of annotation
A `(question, chunk)` pair drawn from the **pool** — the union of the top-20
results of all four systems. Pool size: **2,930 pairs** over 80 questions
(mean 36.6 chunks/question). This is TREC-style pooling; chunks outside the pool
are unjudged, so recall is *pooled recall*, not absolute recall.

## Scale (graded, 0–2)

| Grade | Label | Criterion |
|---:|---|---|
| 0 | Not relevant | Chunk does not help answer the question. |
| 1 | Partially relevant | Chunk contains related context, or part of the answer, but not enough to answer on its own. |
| 2 | Relevant | Chunk contains information sufficient to answer the question, or directly supports the reference answer. |

Binary metrics (Recall, Precision, MRR) treat grade ≥ 1 as relevant.
nDCG uses the graded value as gain.

## Rules for annotators
1. Judge the **chunk against the question**, not against the reference answer's
   wording. A chunk that answers correctly in different words is relevant.
2. The reference answer is a *hint*, not a key. It is short and may be incomplete.
3. If the chunk is OCR garbage or an image caption with no substance → 0.
4. If the chunk answers a *different* question about the same site → 0 or 1, not 2.
5. Do not reward a chunk for merely mentioning the right proper noun.
6. Grade what the chunk says, not whether you believe it. A chunk stating a
   contested view is still relevant to a question about that view.
7. Mark `UNSURE` rather than guessing. Unsure pairs are resolved by adjudication.

## Process
1. **Two independent annotators** judge every pooled pair, blind to system identity
   and to each other. Presentation order randomized (seed 42).
2. Report **Cohen's κ** on the graded scale. Target κ ≥ 0.6 ("substantial").
   If κ < 0.6, revise the guidelines and re-annotate — do not proceed.
3. **Adjudicate** disagreements and all `UNSURE` pairs with a third judgment.
4. Freeze as `data/annotations/qrels_human_v1.jsonl`, one record per pair:
   `{"qid": int, "chunk_id": int, "grade": 0|1|2, "annotator": str, "adjudicated": bool}`
5. Re-run `scripts/evaluation/run_retrieval_experiments.py` against the frozen
   qrels and regenerate all tables.

## Effort estimate
2,930 pairs × 2 annotators ≈ 5,860 judgments. At ~15 s/judgment that is roughly
**24 person-hours**. Reducing pool depth from 20 to 10 roughly halves this at the
cost of shallower recall measurement.

## What may NOT be claimed before this is done
- "expert-verified"
- "ground truth" / "gold labels"
- "benchmark" in the formal sense (per directive §60)
- any statistically-argued superiority of one retriever over another
