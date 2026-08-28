# Hypotheses

Each is falsifiable. None is written to guarantee a positive result. A null result is a
publishable finding and must be reported as such.

**H1.** Metadata-filtered retrieval yields higher Recall@10 than unfiltered vector
retrieval on site-specific questions.
*Falsified if:* Recall@10 is equal or lower.
*Plausible null:* the corpus may not carry enough site-level structure for filtering to help.

**H2.** Spatial constraints improve retrieval **only** for geographically-scoped questions,
and do not help (or slightly hurt) on general questions.
*Falsified if:* no interaction between question type and spatial benefit is observed.

**H3.** Grounding increases citation accuracy relative to the current system.
*Falsified if:* citation accuracy does not improve.
*Note:* the current system's citation accuracy is **not yet measured** — H3 cannot be
tested until the baseline number exists.

**H4.** Retrieval is biased by corpus composition: chunks from the over-represented source
(80% of the index) are retrieved disproportionately even for questions it does not address.
*Falsified if:* retrieval distribution matches question-topic distribution.

**H5.** Raising `MIN_RELEVANCE` above 0.30 reduces unsupported claims at the cost of
answer coverage (more "I don't know" responses).
*Falsified if:* no such tradeoff appears.

## Not hypotheses
The following must **not** be asserted anywhere without evidence:
- that this approach is novel (requires a literature review — **not yet done**)
- that no prior work exists
- that the system is state-of-the-art
- any claim about what the Indus script *means*
