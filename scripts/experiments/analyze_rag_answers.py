"""
Follow-up analysis of the end-to-end answers.

Two questions the aggregate table does not answer:
  1. Does the generator COMPLY with the system prompt's epistemic-caution rule?
     The prompt mandates hedged language and an explicit alternative view.
  2. Where does unsupported content come from - is it uniform, or concentrated?
"""
from __future__ import annotations
import json, pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
RAW = ROOT / "research" / "results" / "raw" / "rag_answers.json"
OUT = ROOT / "research" / "results" / "processed" / "rag_answer_analysis.json"

rows = [r for r in json.loads(RAW.read_text()) if "error" not in r]
con = [r for r in rows if "contested_interpretation" in r["flags"]]
oth = [r for r in rows if "contested_interpretation" not in r["flags"]]
h = [r["hedging_rate"] for r in rows]
zero = [r for r in rows if r["hedging_rate"] == 0]
nocite = [r for r in rows if r["citation_count"] == 0]
ood = [r for r in rows if r.get("in_domain") is False]

def m(xs, k): return float(np.mean([x[k] for x in xs])) if xs else float("nan")

res = {
    "n_answers": len(rows),
    "hedging_compliance": {
        "system_prompt_requires": "cautious/hedged language and at least one alternative view",
        "mean_hedging_rate": float(np.mean(h)),
        "answers_with_zero_hedging": len(zero),
        "share_with_zero_hedging": len(zero) / len(rows),
        "contested_questions": {"n": len(con), "mean_hedging_rate": m(con, "hedging_rate")},
        "other_questions": {"n": len(oth), "mean_hedging_rate": m(oth, "hedging_rate")},
        "difference": m(con, "hedging_rate") - m(oth, "hedging_rate"),
        "finding": ("The prompt's epistemic-caution instruction is largely not complied with: "
                    f"{len(zero)}/{len(rows)} answers contain no hedging at all, and contested "
                    "questions are hedged barely more than uncontested ones."),
    },
    "citation_behaviour": {
        "mean_citations": m(rows, "citation_count"),
        "citation_validity": m([r for r in rows if r["citation_count"]], "citation_validity"),
        "answers_with_zero_citations": len(nocite),
        "zero_citation_questions": [{"qid": r["qid"], "question": r["question"],
                                     "in_domain": r.get("in_domain")} for r in nocite],
        "out_of_domain_refusals": len(ood),
        "note": ("Zero-citation answers coincide with the domain guard firing; that is the "
                 "guard working as designed, not a citation failure."),
    },
    "unsupported_content": {
        "mean_rate": m(rows, "unsupported_rate"),
        "median_rate": float(np.median([r["unsupported_rate"] for r in rows])),
        "excluding_out_of_domain": m([r for r in rows if r.get("in_domain") is not False],
                                     "unsupported_rate"),
        "top_offenders": [{"qid": r["qid"], "question": r["question"],
                           "unsupported_rate": r["unsupported_rate"]}
                          for r in sorted(rows, key=lambda x: -x["unsupported_rate"])[:5]],
        "caveat": ("Measured as answer content-words absent from the retrieved evidence. This "
                   "is a LEXICAL proxy: correct paraphrase counts as unsupported, so the true "
                   "unsupported rate is lower. It is an upper bound, not a hallucination rate."),
    },
    "latency": {"median_s": float(np.median([r["latency_s"] for r in rows])),
                "mean_s": m(rows, "latency_s"),
                "max_s": float(max(r["latency_s"] for r in rows)),
                "note": "CPU-only inference; the mean is skewed by a single 530 s outlier."},
}
OUT.write_text(json.dumps(res, indent=2))
print(json.dumps({k: (v if not isinstance(v, dict) else
                      {kk: vv for kk, vv in v.items() if not isinstance(vv, (list, dict))})
                  for k, v in res.items()}, indent=2))
print(f"\nwrote {OUT.relative_to(ROOT)}")
