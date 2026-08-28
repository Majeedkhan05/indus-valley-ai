# CRITICAL BUG — vector/metadata misalignment invalidates citations

**Found:** 2026-08-23, during construction of the retrieval baseline harness.
**Severity:** Critical — the system's central claim (grounded, cited answers) is
compromised for the majority of retrieved chunks.
**Status:** Diagnosed and reproduced. Clean index built separately. **Live index
left untouched.**

## Symptom
`scripts/evaluation/run_retrieval_experiments.py` asserted index/metadata parity
and failed immediately:

```
AssertionError: index 1506 != meta 2112
```

## Root cause

`backend/rag/vectordb.py` keeps two parallel stores and assumes positional identity:

```python
# vectordb.py:75-82
scores, idx = self.index.search(query_vec, min(top_k, self.index.ntotal))
for s, i in zip(scores[0], idx[0]):
    if i < 0 or i >= len(self.metadata):
        continue
    m = dict(self.metadata[i])     # <-- assumes vector i  <->  metadata row i
```

That invariant is broken on disk:

| Store | Count |
|---|---|
| `faiss.index` vectors | **1,506** |
| `chunks.jsonl` rows | **2,112** |
| unique chunk texts | 1,199 |
| exact-duplicate rows | 913 |

The guard `i >= len(self.metadata)` only catches out-of-range ids. Because
metadata is *longer* than the index, every id is in range — so the bug is silent.

## Empirical confirmation

Test: does `faiss_vector[i]` equal `embed(chunks.jsonl[i].text)`? Cosine ≈ 1.0
means aligned. Same model, same normalization as the live system.

| FAISS id | cosine | verdict | metadata claims |
|---|---|---|---|
| 0 | 1.000 | OK | Authority Structure p.1 |
| 1 | 1.000 | OK | Authority Structure p.2 |
| 50 | 1.000 | OK | Yajnadevam p.47 |
| 300 | 1.000 | OK | Yajnadevam p.297 |
| 700 | **0.726** | **MISALIGNED** | CISI 1 p.129 |
| 899 | **0.599** | **MISALIGNED** | CISI 2 p.213 |
| 900 | **0.670** | **MISALIGNED** | CISI 2 p.214 |
| 901 | **0.626** | **MISALIGNED** | CISI 2 p.215 |
| 1200 | **0.650** | **MISALIGNED** | CISI 3.1 p.243 |
| 1505 | **0.596** | **MISALIGNED** | CISI 3.2 p.217 |

**6/10 probes misaligned.** Alignment holds only for roughly the first ~311 ids
(Authority Structure 8 + Yajnadevam 303) — precisely the chunk count of the
*first* ingest run. Everything ingested afterwards is misaligned.

## Why it happened
`VectorDB.add()` appends to `self.metadata` and rewrites `chunks.jsonl` in full,
while `faiss.index` was rebuilt/replaced on a later run. The two files went out
of sync across ingest runs, and nothing validated the invariant. The duplicate
rows (913) indicate at least one document was ingested more than once.

## Consequences

1. **Citations are wrong for most answers.** A retrieved vector from CISI 3.2 can
   be reported as "CISI 1, p.129". The quoted page will not contain the claim.
2. **All previously recorded benchmark output is invalid.** `paper/eval/results.jsonl`
   (27 rows) carries citations produced under this bug. It cannot be used as
   evidence and must be regenerated.
3. **This plausibly explains the reported behaviour** — answers that did not match
   their citations, and repeated/irrelevant sources during the live demo. It was
   a data-integrity fault, not a weak language model.
4. Duplicate chunks additionally distort retrieval: a duplicated passage can
   occupy several of the top-k slots, crowding out other evidence.

## Fix (non-destructive)

`scripts/data_ingestion/rebuild_index.py`:
- reads `chunks.jsonl` as the authoritative text,
- drops exact-duplicate texts,
- re-embeds every surviving chunk with the same model,
- writes a **new** index to `backend/data/index_v2/` with a manifest,
- **never writes to `backend/data/index/`.**

Rollback: delete `backend/data/index_v2/`.

## Follow-up required (not done in this pass)
- `tests/data/test_index_alignment.py` now fails against the live index by design.
- `VectorDB.load_or_init()` should hard-fail when `ntotal != len(metadata)` instead
  of continuing silently. **Not yet changed** — it touches live serving code and
  needs your approval.
- Switching the backend to `index_v2` is a **separate, explicit decision**.
