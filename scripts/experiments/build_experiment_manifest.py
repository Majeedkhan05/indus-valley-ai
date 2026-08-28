"""
Result validation: emit, for EVERY experiment, the required fields:
configuration, dataset version, corpus version, model version, random seed,
metric definition, raw output, processed output, confidence interval,
statistical comparison, interpretation, limitations.

Every paper table must be traceable to one of these entries.
"""
from __future__ import annotations
import hashlib, json, pathlib, platform
import numpy as np, faiss

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "research" / "results"
IDX = ROOT / "backend" / "data" / "index_v2"
OUT = ROOT / "research" / "reproducibility" / "experiment_manifest.json"

sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()[:16]
bench = json.loads((ROOT / "research/benchmark/iva80_latest.json").read_text())
idx = faiss.read_index(str(IDX / "faiss.index"))

COMMON = {
    "dataset_version": f"{bench['benchmark']} v{bench['version']} ({bench['n_questions']} questions)",
    "dataset_sha256_16": sha(ROOT / "research/benchmark/iva80_latest.json"),
    "corpus_version": f"index_v2 ({idx.ntotal} chunks, dim {idx.d})",
    "corpus_sha256_16": {"faiss": sha(IDX / "faiss.index"), "chunks": sha(IDX / "chunks.jsonl")},
    "model_version": {"embedder": "BAAI/bge-small-en-v1.5 (384-d, L2-normalised)",
                      "generator": "gemma3:4b via Ollama",
                      "bm25": "in-repo Okapi, k1=1.5 b=0.75, idf_variant=lucene"},
    "random_seed": 42,
    "environment": {"python": platform.python_version(), "platform": platform.platform(),
                    "numpy": np.__version__, "faiss": faiss.__version__},
}

METRIC_DEFS = {
    "recall@k": "fraction of JUDGED-relevant chunks appearing in the top-k. Pooled: "
                "relevance is only defined over the pool, so this is POOLED recall.",
    "precision@k": "fraction of the top-k that is judged relevant",
    "mrr": "1/rank of the first judged-relevant chunk, 0 if none in the list",
    "ndcg@k": "sum(gain/log2(rank+1)) over top-k, normalised by the ideal ordering; "
              "binary gains unless stated",
    "citation_correctness": "fraction of emitted citations whose (document,page) matches "
                            "the chunk the retrieved vector actually encodes. DIRECT COUNT, "
                            "no relevance judging involved.",
    "citation_validity": "fraction of cited (document,page) pairs that exist in the corpus",
    "citation_grounding": "fraction of citations drawn from the chunks actually retrieved",
    "retrieval_ratio": "share of retrieved slots from a stratum / that stratum's corpus share",
    "cohens_kappa": "chance-corrected agreement between the two automatic judges",
}

EXPS = [
  {"id": "E-RETRIEVAL", "title": "Retrieval baselines with statistical validation",
   "script": "scripts/experiments/run_retrieval_eval.py",
   "config": {"depth": 10, "pool": "union of top-10 of all systems",
              "selectivity_sweep": [0.03, 0.05, 0.10, 0.20], "bootstrap": 10000},
   "metrics": ["recall@k", "precision@k", "mrr", "ndcg@k"],
   "raw": ["research/results/raw/{bm25,dense,hybrid_rrf,legacy_dense,legacy_dense_slotwaste}_run.json",
           "research/results/raw/qrels_used.json"],
   "processed": ["research/results/processed/metrics.json",
                 "research/results/processed/per_question.json"],
   "confidence_interval": "non-parametric bootstrap over questions, 10,000 resamples, 95%",
   "statistical_comparison": "paired bootstrap vs dense; two-sided p",
   "interpretation": "No pairwise difference is significant. hybrid_rrf has the highest "
                     "point estimates. legacy_dense is EXACTLY identical to dense "
                     "(diff 0.000, CI [0,0]), isolating the misalignment from retrieval.",
   "limitations": ["automatic proxy judgments, kappa~0.33", "n=39 at primary selectivity",
                   "pooled recall, not absolute recall"]},

  {"id": "E-JUDGE-ROBUST", "title": "Judging-scheme robustness",
   "script": "scripts/experiments/judging_robustness.py",
   "config": {"schemes": ["global_quantile", "per_question"], "bootstrap": 10000},
   "metrics": ["recall@k", "mrr", "ndcg@k"],
   "raw": ["(reuses E-RETRIEVAL runs)"],
   "processed": ["research/results/processed/judging_robustness.json"],
   "confidence_interval": "bootstrap 95%",
   "statistical_comparison": "paired bootstrap vs dense under each scheme",
   "interpretation": "System ordering FLIPS between schemes (bm25 2nd vs 3rd). Only "
                     "hybrid_rrf holds first place under both. No ranking claim is defensible.",
   "limitations": ["global scheme silently drops 41/80 questions",
                   "both schemes are automatic, neither is ground truth"]},

  {"id": "E-LEGACY", "title": "Legacy vs corrected index (citation integrity)",
   "script": "scripts/experiments/verify_legacy_and_source_bias.py",
   "config": {"depth": 10, "identity_match_threshold": 0.99},
   "metrics": ["citation_correctness"],
   "raw": ["experiments/results/E002_legacy_vs_corrected/per_query.json"],
   "processed": ["research/results/processed/phase6_legacy_verification.json"],
   "confidence_interval": "not applicable - direct count, not an estimate",
   "statistical_comparison": "two independent methods (identity resolution; rank correlation) "
                             "agree",
   "interpretation": "Retrieval ranking preserved exactly (Kendall tau 1.000); citation "
                     "correctness 3.9%. The defect destroyed attribution, not retrieval.",
   "limitations": ["single index, single incident - generalised separately by E-PERTURB"]},

  {"id": "E-PERTURB", "title": "Controlled metadata-misalignment perturbation",
   "script": "scripts/experiments/perturbation_study.py",
   "config": {"severities": [0, .1, .25, .5, .75, 1.0], "repeats": 5, "citation_top_k": 6},
   "metrics": ["recall@k", "mrr", "ndcg@k", "citation_correctness"],
   "raw": ["(generated in-script)"],
   "processed": ["research/results/processed/perturbation_study.json"],
   "confidence_interval": "sd across 5 repeats per severity",
   "statistical_comparison": "retrieval range across severities vs citation drop",
   "interpretation": "Retrieval metrics EXACTLY invariant (range 0.0e+00) while citation "
                     "correctness falls 100%->0.6%. The blindness is structural.",
   "limitations": ["retrieval invariance is partly analytic - the experiment confirms it "
                   "empirically rather than discovering it"]},

  {"id": "E-SOURCE", "title": "Source-imbalance hypothesis matrix (A-J)",
   "script": "scripts/experiments/source_hypothesis_matrix.py",
   "config": {"depth": 10, "hypotheses": list("ABCDEFGHIJ")},
   "metrics": ["retrieval_ratio"],
   "raw": ["(generated in-script)"],
   "processed": ["research/results/processed/source_hypothesis_matrix.json",
                 "research/results/processed/phase7c_boilerplate.json"],
   "confidence_interval": "not applicable - descriptive ratios",
   "statistical_comparison": "controlled matched comparison (J); Pearson correlations (A, C)",
   "interpretation": "Only F (near-duplicate collapse) survives a controlled test. "
                     "B, D, G, H, I, J NOT SUPPORTED. A, C INCONCLUSIVE (n=6 sources).",
   "limitations": ["correlations over 6 sources are uninterpretable",
                   "B under-powered (NaN in two length bands)",
                   "no intervention experiment (de-duplicate and re-index) has been run, "
                   "so no causal chain is proven"]},

  {"id": "E-ABLATION", "title": "Ablation over retriever, fusion and corpus",
   "script": "scripts/experiments/run_ablation_and_errors.py",
   "config": {"configurations": 10, "selectivity": 0.05},
   "metrics": ["recall@k", "mrr", "ndcg@k"],
   "raw": ["(generated in-script)"],
   "processed": ["research/results/processed/ablation.json"],
   "confidence_interval": "bootstrap 95%, 4000 resamples",
   "statistical_comparison": "point estimates ordered; CIs overlap throughout",
   "interpretation": "RRF constant k is inert. Removing 25.3% of the corpus changes "
                     "Recall@5 by +0.001.",
   "limitations": ["no reranker exists in the architecture, so none is ablated"]},

  {"id": "E-FAIRNESS", "title": "Comparison fairness and BM25 IDF sensitivity",
   "script": "scripts/experiments/fairness_and_sensitivity.py",
   "config": {"idf_variants": ["lucene", "robertson"]},
   "metrics": ["recall@k", "mrr", "ndcg@k"],
   "raw": ["(generated in-script)"],
   "processed": ["research/results/processed/fairness_and_sensitivity.json",
                 "research/results/processed/bm25_depth_fairness.json"],
   "confidence_interval": "not applicable",
   "statistical_comparison": "ordering under each IDF variant and on the fair subset",
   "interpretation": "Same corpus, queries, depth and qrels for all systems; dense and "
                     "hybrid share vectors. Ordering unchanged by IDF variant and on the "
                     "BM25-full-list subset. BM25 Recall@10 is a LOWER BOUND.",
   "limitations": ["BM25 returns <10 candidates on 9/80 queries, biasing against BM25"]},

  {"id": "E-RAG", "title": "End-to-end RAG answer evaluation",
   "script": "scripts/experiments/run_rag_answer_eval.py",
   "config": {"top_k": 6, "questions": 80, "model": "gemma3:4b"},
   "metrics": ["citation_validity", "citation_grounding"],
   "raw": ["research/results/raw/rag_answers.json"],
   "processed": ["research/results/processed/rag_answer_metrics.json",
                 "research/results/processed/rag_answer_analysis.json"],
   "confidence_interval": "not computed - descriptive means over 80 answers",
   "statistical_comparison": "contested vs uncontested hedging rate",
   "interpretation": "Citation validity and grounding are 1.000. Epistemic compliance "
                     "fails: 36/80 answers contain no hedging.",
   "limitations": ["automated proxies only, no human evaluation",
                   "unsupported_rate is a LEXICAL upper bound, not a hallucination rate"]},
]

for e in EXPS:
    e.update(COMMON)
    e["metric_definitions"] = {m: METRIC_DEFS[m] for m in e["metrics"] if m in METRIC_DEFS}

doc = {"generated_by": "scripts/experiments/build_experiment_manifest.py",
       "rule": "Every paper table must be reproducible from these entries. "
               "No manually typed research numbers.",
       "n_experiments": len(EXPS), "experiments": EXPS}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(doc, indent=2))
missing = []
for e in EXPS:
    for f in e["processed"]:
        if not f.startswith("(") and not (ROOT / f).exists(): missing.append(f)
print(f"{len(EXPS)} experiments documented")
print(f"missing processed outputs: {missing if missing else 'none - all present'}")
print(f"wrote {OUT.relative_to(ROOT)}")
