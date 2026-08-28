# ICLR submission package — readiness checklist

**Status: NOT READY TO SUBMIT.** Two blockers, both listed first. This checklist
records actual state, not intent.

## Blockers

| # | Blocker | Detail |
|---|---|---|
| B1 | **Empty bibliography** | §2 has no verified citation keys. Must be populated from real sources. No key may be invented. |
| B2 | **No human relevance judgments** | κ ≈ 0.28–0.33 automatic judges only. ~5.8 h × 2 annotators outstanding. All retrieval claims stay exploratory until done. |

## Formatting

| Item | State |
|---|---|
| Template | **TODO** — manuscript is Markdown; must be ported to the official LaTeX style |
| Page limit | Not yet checked against the official limit — content is ~2,300 words + 6 figures, well under a 9-page main body |
| Figures | 6 generated PNGs at 150 dpi from result files |
| Tables | 9 generated from JSON |
| Appendix | Error taxonomy, per-question results, annotation protocol available |

## Anonymity — verified

- Manuscript contains **no author name, institution, funder, or acknowledgement**.
- No GitHub URL, Hugging Face Space ID, or personal identifier in `paper.md`.
- Repository paths in the artifact are relative.
- **Action required before upload:** the public artifact repo is deanonymising if
  linked directly; use an anonymised mirror.

Automated check: `scripts/submission/check_anonymity.py`.

## Reproducibility statement

- One command: `scripts/run_all_experiments.py` (14 stages).
- Seeds fixed (42); versions, platform and runtimes recorded in `run_manifest.json`.
- Index ships with a manifest and SHA-256 prefixes.
- **Data availability:** derived index, chunk metadata, benchmark and all results
  are included. **Source PDFs are copyrighted and are not redistributed** — OCR
  cannot be re-run by a third party without obtaining the volumes independently.

## Ethics

- Corpus is published archaeological scholarship. No personal data.
- The domain is contested; 22/80 benchmark questions concern disputed
  interpretations. The system prompt mandates hedging and alternative views, and
  the paper makes no claim about the Indus script's linguistic content.
- No human subjects. When annotation is performed, annotators are project members
  performing relevance judgment, not subjects.

## AI-use disclosure

This artifact was developed with substantial AI coding-assistant involvement:
implementation, experiment scripts, analysis and manuscript drafting. All
experiments were executed and their outputs are machine-generated and inspectable
in `research/results/`. **This must be disclosed in the submission form** per
current ICLR policy.

## Conflicts of interest

To be completed by the author at submission time — not inferable from the artifact.

## Deadline

Reported deadline for the Brazil-hosted ICLR cycle is **unverified**. Do not plan
around any date in this repository; check the official site.
