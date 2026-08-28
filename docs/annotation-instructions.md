# IVA-80 Annotation Instructions

**No labels exist yet.** Everything reported from automatic judges is exploratory.
These instructions produce the human ground truth that replaces them.

## Scope
- **1,382** `(question, chunk)` pairs across 80 questions (mean 17.3 chunks/question).
- **≈5.8 hours per annotator** at 15 s/judgment. **Two annotators required.**
- Pool = union of top-10 from BM25, dense and hybrid, so labels are valid for all
  three systems. Presentation order is randomised (seed 42) and system identity
  is hidden, so you cannot tell which retriever proposed a chunk.

## Two ways to annotate

**Web UI (recommended)**
```bash
open research/annotations/annotate.html
```
Enter your name, load `research/annotations/tasks.jsonl`, judge with keys
`2` / `1` / `0` / `s`. Progress is saved in the browser. Click *Export* to get
`labels_<you>.jsonl`, and place it in `research/annotations/`.

**CLI**
```bash
backend/venv/bin/python scripts/annotation/annotate_cli.py --annotator alice --limit 50
```
Append-only and resumable; re-run to continue where you stopped.

## The scale

| Grade | Meaning |
|---:|---|
| **2** | Chunk contains information **sufficient to answer** the question, or directly supports the reference answer. |
| **1** | **Partial** — related context, or part of the answer, but not enough alone. |
| **0** | **Not relevant.** |
| **s** | Unsure — resolved at adjudication. Prefer this over guessing. |

Binary metrics treat grade ≥ 1 as relevant. nDCG uses the grade as gain.

## Rules
1. Judge the chunk against the **question**, not against the reference answer's wording.
   A chunk that answers correctly in different words is relevant.
2. The reference answer is a **hint, not a key**. It is short and may be incomplete.
3. OCR garbage or a bare image caption with no substance → **0**.
4. A chunk about the same site but answering a *different* question → **0 or 1**, never 2.
5. Merely containing the right proper noun is not enough for 2.
6. Grade what the chunk **says**, not whether you agree with it. A chunk stating a
   contested view is still relevant to a question about that view.
   **22 of the 80 questions are flagged `contested_interpretation`** — expect this.
7. Do not look up outside sources. Judge only the chunk in front of you.

## After annotation
```bash
backend/venv/bin/python scripts/annotation/compute_agreement.py
```
Reports pairwise Cohen's κ and writes `disagreements.jsonl`.

- **Target κ ≥ 0.6.** If κ < 0.6, revise these instructions and re-annotate.
  Do not proceed on weak agreement — that is the mistake the automatic judges made
  (κ = 0.277).
- Adjudicate every disagreement and every `unsure` into
  `research/annotations/adjudicated.jsonl` as `{"task_id": ..., "grade": 0|1|2}`.
- Re-run `compute_agreement.py`; it writes `qrels_human.json` **only** when nothing
  is unresolved.

## Prohibited
- Fabricating labels, or copying the automatic judge's output into a labels file.
- Calling anything "expert-verified" unless a domain expert performed it.
- Reporting κ from a single annotator (undefined).
