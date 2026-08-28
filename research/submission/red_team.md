# Adversarial review — 16 hostile questions

Every criticism is answered with **an experiment, a strengthened analysis, a
narrowed claim, or an explicit limitation** — never a rebuttal alone. Where a
criticism landed, the work changed. Four criticisms produced new experiments;
two produced retractions.

---

### 1. "Is this actually novel?"

**Conceded, then generalised.** A single incident is an anecdote. So we ran a
controlled perturbation study: metadata misalignment injected at 0/10/25/50/75/100%,
5 repeats, seed 42. Recall@5, MRR and nDCG@10 are **exactly invariant** (range
**0.0e+00**) while citation correctness falls 100% → 0.6%.

The claim is not "we found a bug". It is: *ranking metrics cannot detect
attribution failure at any severity, because they never read the metadata the
citation is built from.* → **new experiment** (§5.1, Fig 6).

### 2. "Is this merely standard RAG applied to archaeology?"

**Yes, deliberately.** bge-small + FAISS IndexFlatIP + BM25 + RRF. If the stack
were exotic, the failure would be dismissed as idiosyncratic. The contribution is
diagnostic, not architectural — the abstract says "Not a better retriever". No
component exists solely to look novel.

### 3. "Is the benchmark reliable?"

**No, and we say so in the abstract.** κ ≈ 0.28–0.33. Under global-quantile
judging **41/80 questions get no relevant chunk**, and `EVALUATION_ERROR` is the
single largest error category (123 records). 22/80 questions are contested, 7
ambiguous — all flagged, none deleted. → **limitation, prominently placed**

### 4. "Is 80 questions enough?"

**No.** n = 39–77 depending on judging scheme, and every CI is wide (e.g. hybrid
Recall@5 = 0.466, CI [0.35, 0.59]). 80 questions cannot resolve differences of
the size observed (~0.05–0.08). We make **no ranking claim**. The results that do
survive are direct counts, not estimates. → **limitation**

### 5. "Are human labels reliable?"

**There are none.** Zero human labels exist. Everything retrieval-related rests
on two automatic judges. We ship the protocol, a blind randomised task set, CLI
and web tools, and agreement/adjudication code that **refuses to emit qrels**
until two annotators plus adjudication exist. We did not fabricate a single label.

### 6. "Are confidence intervals appropriate?"

Non-parametric bootstrap over *questions* (10,000 resamples) — appropriate
because questions are the sampling unit and metrics are non-normal and bounded.
Comparisons use a **paired** bootstrap, correct for the same questions scored by
different systems. We report the CI of the *difference*, not just overlapping
marginal CIs. `citation_correctness` gets no CI because it is a **census, not a
sample**.

### 7. "Are the comparisons fair?"

**Audited, and one violation found and reported.** Identical corpus
(sha `81292fcefd537433`), identical queries, identical depth parameter, one pooled
qrels file for all systems.

**Violation:** BM25 returns fewer than 10 candidates on **9/80 queries** (shortest: 1),
because it only scores documents sharing a query term. This can only *lower* its
Recall@10 — a bias **against** the system that outranks our deployed retriever.
On the 33 queries where BM25 returns a full list the ordering is unchanged, but
BM25's Recall@10 (0.693) then **exceeds** hybrid's (0.671). We report BM25
Recall@10 as a **lower bound** rather than padding it with invented ordering.
→ **new experiment**

### 8. "Are the embedding models identical across systems?"

**Verified programmatically.** Dense and hybrid use the *same vectors* — hybrid
fuses the dense run itself, so it cannot use a different model. BM25 uses no
embeddings. All three are scored over the identical chunk list.

### 9. "Is the corpus biased?"

**Yes, and it is one of our findings.** One source is 25.3% of the corpus and is
retrieved at 0.26× its share. We tested **ten** explanations (§6); only
near-duplicate collapse survives. We also **retract our own earlier claim** that
this source was 80% of the corpus — that was a duplication artifact, and the raw
figure was 57.4%, not 80%.

### 10. "Does source composition explain the results?"

**Tested directly: no.** Removing the entire 25.3% source changes hybrid Recall@5
by **+0.001** and leaves the ordering unchanged. → **ablation**

### 11. "Is hybrid actually better?"

**Not demonstrably.** It has the highest point estimates and holds first place
under both judging schemes, but every paired comparison against dense is
non-significant (Recall@5 Δ = +0.083, CI [−0.06, +0.22], p = 0.243). On the
BM25-full-list subset, BM25 beats hybrid on Recall@10. **We do not claim hybrid
is superior.**

### 12. "Are improvements statistically meaningful?"

**No.** Every CI of every difference straddles zero. Table 4 lists all of them
marked "not significant". This is reported as a finding, not buried.

### 13. "Could another implementation reproduce this?"

**Cross-validated our BM25 against `rank_bm25`**: with the IDF variant matched,
max score difference **6.1e-13** and **identical top-10 on 80/80 queries**. The
initial mismatch was a documented IDF-variant choice (Lucene-smoothed vs
Robertson–Sparck Jones), not a bug; switching variants does not change the
ordering. IR metrics are separately unit-tested against hand-computed values.
→ **new experiment**

`run_all_experiments.py` runs 14 stages and records versions, seeds, platform and
index SHA-256. **Gap:** source PDFs are copyrighted and not redistributed, so OCR
cannot be re-run by a third party.

### 14. "Are the citations genuinely correct?"

Verified three ways: (i) full re-embedding of all 1,199 chunks, min cosine
0.9999996; (ii) 12 integrity regression tests including a corrupted fixture
reproducing the original 1506/2112 shape; (iii) live end-to-end run — citation
validity **1.000**, grounding **1.000** over 80/80 answers, versus 3.9% on the
legacy index.

### 15. "Does the paper overclaim?"

We audited our own claims and **withdrew two**:

- *"The dense retriever is worst at every operating point."* Withdrawn — with CIs
  and a second judging scheme, nothing is significant and the ordering flips.
- *"One source is 80% of the corpus."* Wrong twice; recomputed to 57.4% raw /
  25.3% deduplicated.

We also **found and fixed a bug in our own favour**: mapping legacy ids to
corrected chunks collapsed duplicates, truncating 17/80 legacy lists below depth
and biasing legacy Recall@10 *low* — i.e. making the repair look more beneficial
than it was. After the fix, legacy is **exactly identical** to dense (Δ = 0.000,
CI [0, 0], p = 1.000). The corrected result is *stronger and cleaner*, but it was
found by auditing against our own interest.

Every claim in the paper is tagged `[DIRECT RESULT]`, `[SUPPORTED BY LITERATURE]`,
`[INTERPRETATION]`, `[HYPOTHESIS]` or `[LIMITATION]`.

### 16. "What happens if the main hypothesis is false?"

Claims ranked by fragility:

| Claim | Basis | Survives? |
|---|---|---|
| 769/800 legacy citations named the wrong document | census | **Yes** |
| Ranking metrics invariant under misalignment | controlled, range 0.0e+00 | **Yes** |
| Near-duplicate collapse (F); 302/303 shared header | corpus census | **Yes** |
| Citation validity 1.000 after repair | 80/80 live answers | **Yes** |
| Any retriever beats another | proxy judges, n ≤ 77 | **No — withdrawn** |
| Hedging non-compliance (36/80) | census over answers | **Yes** |

The paper's thesis rests on the first three, all of which are counts or
controlled invariances rather than estimates. If the retrieval comparison
evaporates entirely — as we already concede it may — **the contribution is
unaffected**.

---

## Criticisms we cannot answer

1. **No human labels.** ~3.6 h × 2 annotators of work that has not been done.
2. **Empty bibliography.** §2 ships no citation keys. The paper is **not
   submittable** in this state. Fabricating references would be worse.
3. **One corpus, one embedding model, one domain.** No generalisation claim.
4. **Multi-hop is 1/80 questions.** The benchmark does not test it.
5. **No intervention experiment** for §6: we have not de-duplicated the collapsed
   source and re-indexed, so the mechanism is *consistent with* all controlled
   comparisons but is not a proven causal chain.
6. **Generator quality unevaluated by humans.** §11 is automated proxies only.
