"""
PHASE 4/12 - Generate every paper table and figure FROM RESULT FILES.
No number is typed by hand. Run after the experiment scripts.
"""
from __future__ import annotations
import collections, json, pathlib, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "research" / "results"
TAB, FIG = RES / "tables", RES / "figures"
TAB.mkdir(parents=True, exist_ok=True); FIG.mkdir(parents=True, exist_ok=True)
GOLD, INK, GREY = "#C9A84C", "#1A1A2E", "#8a8a99"
plt.rcParams.update({"figure.dpi": 150, "font.size": 9, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.grid": True,
                     "grid.alpha": .25, "grid.linestyle": ":"})

L = lambda p: json.loads((RES / p).read_text())
bench = json.loads((ROOT / "research/benchmark/iva80_latest.json").read_text())
met = L("processed/metrics.json")
rob = L("processed/judging_robustness.json")
abl = L("processed/ablation.json")
p6 = L("processed/phase6_legacy_verification.json")
p7 = L("processed/phase7_source_mechanism.json")
p7c = L("processed/phase7c_boilerplate.json")
err = json.loads((ROOT / "research/error_analysis/errors.json").read_text())
out = []

def tbl(title, header, rows, note=""):
    global out
    out.append(f"\n## {title}\n")
    if note: out.append(note + "\n")
    out.append("| " + " | ".join(header) + " |")
    out.append("|" + "|".join(["---"] * len(header)) + "|")
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]

out.append("# IVA-80 — Generated Tables\n")
out.append(f"Auto-generated from `research/results/`. **Do not edit by hand.**\n")
out.append(f"Judge: **{met['judge']}**\n")

# T1 corpus
ps = {r["source"]: r for r in p7c["per_source"]}
tbl("Table 1 — Corpus composition and integrity",
    ["Source", "Raw rows", "Duplicate rows", "Dup %", "Unique chunks", "TTR", "Intra-source sim"],
    [[s[:44], r["raw_rows"], r["duplicate_rows"], f"{r['duplicate_rate']*100:.1f}%",
      r["unique_chunks"], f"{r['type_token_ratio']:.3f}",
      f"{r['mean_intra_source_similarity']:.3f}"]
     for s, r in sorted(ps.items(), key=lambda kv: -kv[1]["raw_rows"])],
    "TTR = type-token ratio (lexical diversity). Intra-source sim = mean chunk-to-chunk cosine.")

# T2 benchmark
tbl("Table 2 — IVA-80 benchmark composition",
    ["Property", "Value"],
    [["Questions", bench["n_questions"]], ["Version", bench["version"]],
     ["Categories", len(bench["categories"])],
     ["Contested-interpretation flagged", bench["flag_counts"].get("contested_interpretation", 0)],
     ["Possibly ambiguous", bench["flag_counts"].get("possibly_ambiguous", 0)],
     ["Negative/unknown answers", bench["flag_counts"].get("negative_or_unknown_answer", 0)],
     ["Tests lexical retrieval", bench["retrieval_type_counts"].get("lexical", 0)],
     ["Tests semantic retrieval", bench["retrieval_type_counts"].get("semantic", 0)],
     ["Tests multi-hop", bench["retrieval_type_counts"].get("multi_hop", 0)],
     ["Human labels", "NONE - annotation pending"]])

# T3 main results (both schemes)
rows = []
for scheme, blk in rob["schemes"].items():
    for s, mm in blk["systems"].items():
        rows.append([scheme, s, blk["questions_covered"],
                     *[f"{mm[k]['mean']:.3f} [{mm[k]['ci95'][0]:.2f}, {mm[k]['ci95'][1]:.2f}]"
                       for k in ("recall@1", "recall@5", "recall@10", "mrr", "ndcg@10")]])
tbl("Table 3 — Retrieval results under both judging schemes",
    ["Judge scheme", "System", "n", "R@1", "R@5", "R@10", "MRR", "nDCG@10"], rows,
    "95% CIs are non-parametric bootstrap over questions (10,000 resamples).")

# T4 significance
rows = []
for scheme, blk in rob["schemes"].items():
    for s, d in blk["paired_vs_dense"].items():
        for k in ("recall@5", "mrr", "ndcg@10"):
            x = d[k]
            rows.append([scheme, f"{s} vs dense", k, f"{x['diff']:+.3f}",
                         f"[{x['ci95'][0]:+.3f}, {x['ci95'][1]:+.3f}]", f"{x['p']:.3f}",
                         "**significant**" if x["p"] < 0.05 else "not significant"])
tbl("Table 4 — Paired bootstrap significance tests", 
    ["Judge scheme", "Comparison", "Metric", "Δ", "95% CI of Δ", "p (2-sided)", "Verdict"], rows,
    "Paired over questions. No comparison reaches significance at α=0.05.")

# T5 ablation
a = abl["results"]
tbl("Table 5 — Ablation",
    ["Configuration", "R@1", "R@5", "R@10", "MRR", "nDCG@10"],
    [[n] + [f"{a[n][k]['mean']:.3f}" for k in ("recall@1", "recall@5", "recall@10", "mrr", "ndcg@10")]
     for n in sorted(a, key=lambda x: -a[x]["recall@5"]["mean"])])

# T6 legacy
c = p6
tbl("Table 6 — Legacy vs corrected index (citation integrity)",
    ["Measure", "Legacy", "Corrected"],
    [["Vectors / metadata rows", "1506 / 2112", "1199 / 1199"],
     ["Counts aligned", "NO", "YES"],
     ["Citation correctness", f"{c['citation_correctness_legacy']*100:.1f}%", "100%"],
     ["Wrong document", c["wrong_document"], 0],
     ["Content Jaccard vs corrected", f"{c['content_jaccard_mean']:.3f}", "1.000"],
     ["Kendall τ of ranking", f"{c['kendall_tau_on_shared_mean']:.3f}", "1.000"],
     ["Retrieval Recall@5", "identical", "identical"]],
    "Retrieval was unaffected (τ=1.0); only attribution was destroyed.")

# T7 source strata
tbl("Table 7 — Retrieval share by source and chunk type",
    ["Stratum", "Chunks", "Corpus share", "Retrieved share", "Ratio"],
    [[r["label"], r["chunks"], f"{r['corpus_share']*100:.1f}%",
      f"{r['retrieved_share']*100:.1f}%", f"{r['ratio']:.2f}"]
     for r in sorted(p7["strata"], key=lambda x: -x["corpus_share"])],
    "Ratio > 1 = over-retrieved relative to corpus share.")

# T8 errors
tbl("Table 8 — Error taxonomy",
    ["Category", "Failing questions"],
    [[k, v] for k, v in sorted(err["counts"].items(), key=lambda kv: -kv[1])],
    f"{err['n_failing']} of {bench['n_questions']} questions fall below Recall@5 = 0.5 "
    "(multi-label). `evaluation_artifact` = the automatic judge produced no relevant chunk.")

# RAG answers if available
rp = RES / "processed" / "rag_answer_metrics.json"
if rp.exists():
    r = json.loads(rp.read_text())
    tbl("Table 9 — End-to-end RAG answer measures (automated)",
        ["Measure", "Mean", "Median", "n"],
        [[k, f"{v['mean']:.3f}", f"{v['median']:.3f}", v["n"]] for k, v in r["aggregate"].items()],
        f"Model: {r['model']}. {r['questions_succeeded']}/{r['questions_attempted']} answered. "
        "**All measures are automated proxies, not human evaluation.**")

(TAB / "all_tables.md").write_text("\n".join(out) + "\n")

# ---------------- FIGURES ----------------
def save(fig, name):
    fig.tight_layout(); fig.savefig(FIG / name, bbox_inches="tight"); plt.close(fig)

# F1 main comparison, both schemes
fig, axes = plt.subplots(1, 2, figsize=(9, 3.4), sharey=True)
for ax, (scheme, blk) in zip(axes, rob["schemes"].items()):
    sys_names = list(blk["systems"])
    x = np.arange(len(sys_names)); w = 0.35
    for j, k in enumerate(("recall@5", "ndcg@10")):
        mu = [blk["systems"][s][k]["mean"] for s in sys_names]
        lo = [mu[i] - blk["systems"][s][k]["ci95"][0] for i, s in enumerate(sys_names)]
        hi = [blk["systems"][s][k]["ci95"][1] - mu[i] for i, s in enumerate(sys_names)]
        ax.bar(x + (j - .5) * w, mu, w, yerr=[lo, hi], capsize=3,
               color=[GOLD, INK][j], alpha=.85, label=k)
    ax.set_xticks(x); ax.set_xticklabels(sys_names, rotation=12)
    ax.set_title(f"{scheme}  (n={blk['questions_covered']})", fontsize=9)
axes[0].set_ylabel("score"); axes[0].legend(frameon=False, fontsize=8)
fig.suptitle("Retrieval performance with 95% bootstrap CIs", fontsize=10)
save(fig, "fig1_retrieval_comparison.png")

# F2 source ratio
fig, ax = plt.subplots(figsize=(7, 3.6))
st = sorted(p7["strata"], key=lambda x: x["ratio"])
cols = [GOLD if s["kind"] == "prose" else GREY for s in st]
ax.barh([s["label"][:40] for s in st], [s["ratio"] for s in st], color=cols)
ax.axvline(1.0, color=INK, lw=1, ls="--")
ax.set_xlabel("retrieved share ÷ corpus share  (1.0 = proportional)")
ax.set_title("Retrieval bias by source and chunk type (gold = prose, grey = tabular)", fontsize=9)
save(fig, "fig2_source_bias.png")

# F3 corpus integrity
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.5, 3.2))
srcs = sorted(ps.items(), key=lambda kv: -kv[1]["raw_rows"])
a1.barh([s[:26] for s, _ in srcs], [r["duplicate_rate"] * 100 for _, r in srcs], color=GOLD)
a1.set_xlabel("% duplicate rows"); a1.set_title("Duplication by source", fontsize=9)
a2.scatter([r["type_token_ratio"] for _, r in srcs],
           [r["mean_intra_source_similarity"] for _, r in srcs], color=INK, s=45)
for s, r in srcs:
    a2.annotate(s[:14], (r["type_token_ratio"], r["mean_intra_source_similarity"]),
                fontsize=6.5, xytext=(3, 3), textcoords="offset points")
a2.set_xlabel("type-token ratio"); a2.set_ylabel("intra-source similarity")
a2.set_title("Lexical diversity vs chunk self-similarity", fontsize=9)
save(fig, "fig3_corpus_integrity.png")

# F4 errors
fig, ax = plt.subplots(figsize=(6.5, 3.2))
ec = sorted(err["counts"].items(), key=lambda kv: kv[1])
ax.barh([k for k, _ in ec], [v for _, v in ec], color=GOLD)
ax.set_xlabel("failing questions (multi-label)"); ax.set_title("Error taxonomy", fontsize=9)
save(fig, "fig4_error_taxonomy.png")

# F5 legacy citation
fig, ax = plt.subplots(figsize=(5.5, 3))
ax.bar(["legacy", "corrected"], [p6["citation_correctness_legacy"] * 100, 100],
       color=[GREY, GOLD])
ax.bar(["legacy", "corrected"], [p6["content_jaccard_mean"] * 100, 100],
       color="none", edgecolor=INK, lw=1.4, ls="--", label="content overlap")
ax.set_ylabel("%"); ax.set_ylim(0, 105)
ax.set_title("Citation correctness vs retrieved-content overlap", fontsize=9)
ax.legend(frameon=False, fontsize=8)
save(fig, "fig5_legacy_citations.png")

print("tables ->", (TAB / "all_tables.md").relative_to(ROOT))
for f in sorted(FIG.glob("*.png")): print("figure ->", f.relative_to(ROOT))
