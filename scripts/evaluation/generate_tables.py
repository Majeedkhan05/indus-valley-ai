"""
Generate paper-ready tables from experiment output files.

Rule (directive S24/S49): tables are GENERATED from experiments/results/*.json.
No number is ever typed by hand into a paper.

Usage: backend/venv/bin/python scripts/evaluation/generate_tables.py
Writes: experiments/results/<exp>/tables.md  and  experiments/analysis/source_bias.json
"""
from __future__ import annotations
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
EXP  = ROOT / "experiments" / "results" / "E001_retrieval_baselines_index_v2"
IDX  = ROOT / "backend" / "data" / "index_v2"
ANA  = ROOT / "experiments" / "analysis"; ANA.mkdir(parents=True, exist_ok=True)

cfg = json.loads((EXP / "config.json").read_text())
met = json.loads((EXP / "metrics.json").read_text())
pred = json.loads((EXP / "predictions.json").read_text())
chunks = [json.loads(l) for l in (IDX / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
bench = json.loads((ROOT / "paper" / "eval" / "benchmark_questions.json").read_text())["questions"]

SYS = cfg["systems"]
sel = f'{met["primary_selectivity"]:.2f}'
prim = met["sweep"][sel]

L = []
L.append("# Generated Tables — E001 Retrieval Baselines\n")
L.append(f"Auto-generated from `{EXP.relative_to(ROOT)}`. Do not edit by hand.\n")
L.append(f"- Index: `{cfg['index_dir']}` — {cfg['corpus_chunks']} chunks\n"
         f"- Questions: {cfg['questions']}\n"
         f"- Judgments: **{cfg['judgments']}**\n"
         f"- Built: {cfg['timestamp']}\n")

# ---- Table 1: dataset statistics -------------------------------------------
src = collections.Counter(c["source"] for c in chunks)
tot = sum(src.values())
L.append("\n## Table 1 — Corpus composition (after de-duplication)\n")
L.append("| Source | Chunks | Share |\n|---|---:|---:|")
for k, v in src.most_common():
    L.append(f"| {k} | {v} | {100*v/tot:.1f}% |")
L.append(f"| **Total** | **{tot}** | 100% |")

cat = collections.Counter(q["category"] for q in bench)
L.append("\n## Table 2 — IVA-80 benchmark by category\n")
L.append("| Category | Questions |\n|---|---:|")
for k, v in cat.most_common():
    L.append(f"| {k} | {v} |")
L.append(f"| **Total** | **{sum(cat.values())}** |")

# ---- Table 3: retrieval baselines ------------------------------------------
L.append(f"\n## Table 3 — Retrieval baselines (proxy judgments, selectivity={sel}, lenient)\n")
L.append(f"Questions with ≥1 judged-relevant chunk: "
         f"**{prim['questions_with_relevant']['lenient']}/{cfg['questions']}** · "
         f"judge agreement κ = **{prim['cohens_kappa']:.3f}**\n")
L.append("| System | R@1 | R@5 | R@10 | P@5 | MRR | nDCG@10 |\n|---|---:|---:|---:|---:|---:|---:|")
for s in SYS:
    m = prim["lenient"][s]
    L.append(f"| {s} | {m['recall@1']:.3f} | {m['recall@5']:.3f} | {m['recall@10']:.3f} "
             f"| {m['precision@5']:.3f} | {m['mrr']:.3f} | {m['ndcg@10']:.3f} |")

# ---- Table 4: sensitivity sweep --------------------------------------------
L.append("\n## Table 4 — Sensitivity of the ranking to the judging operating point\n")
L.append("Recall@5 (lenient) at each judge selectivity. Tests whether conclusions "
         "survive a change of threshold.\n")
L.append("| Selectivity | κ | n questions | " + " | ".join(SYS) + " | Best |")
L.append("|---:|---:|---:|" + "---:|" * (len(SYS) + 1))
for k, v in met["sweep"].items():
    row = [f"{v['lenient'][s]['recall@5']:.3f}" for s in SYS]
    best = max(SYS, key=lambda s: v["lenient"][s]["recall@5"])
    L.append(f"| {k} | {v['cohens_kappa']:.3f} | "
             f"{v['lenient'][SYS[0]]['n_questions_evaluated']} | " + " | ".join(row) + f" | {best} |")
L.append(f"\n**Ranking stable across all operating points: "
         f"`{met['ranking_stable_across_sweep']}`**\n")
for k, order in met["rankings"].items():
    L.append(f"- selectivity {k}: {' > '.join(order)}")

# ---- Table 5: source bias in retrieval -------------------------------------
L.append("\n## Table 5 — Source-bias analysis\n")
L.append("Share of top-10 retrieved chunks drawn from each source, versus that "
         "source's share of the corpus. Ratio > 1 = over-retrieved.\n")
bias = {}
header = "| Source | Corpus share | " + " | ".join(f"{s} (ratio)" for s in SYS) + " |"
L.append(header); L.append("|---|---:|" + "---:|" * len(SYS))
for name, cnt in src.most_common():
    corpus_share = cnt / tot
    cells, row = [], {"corpus_share": corpus_share}
    for s in SYS:
        got = [d for ids in pred[s].values() for d in ids[:10]]
        share = sum(1 for d in got if chunks[d]["source"] == name) / len(got)
        ratio = share / corpus_share if corpus_share else float("nan")
        row[s] = {"retrieved_share": share, "ratio": ratio}
        cells.append(f"{share*100:.1f}% ({ratio:.2f})")
    bias[name] = row
    L.append(f"| {name} | {corpus_share*100:.1f}% | " + " | ".join(cells) + " |")

(EXP / "tables.md").write_text("\n".join(L) + "\n")
(ANA / "source_bias.json").write_text(json.dumps(bias, indent=2))
print(f"wrote {(EXP/'tables.md').relative_to(ROOT)}")
print(f"wrote {(ANA/'source_bias.json').relative_to(ROOT)}")
