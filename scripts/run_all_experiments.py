"""
PHASE 15 - One-command reproduction of every number in the paper.

    backend/venv/bin/python scripts/run_all_experiments.py [--skip-rag] [--skip-rebuild]

Stages run in dependency order. Each stage is skipped if its outputs are current
unless --force. Records environment, versions, seeds and runtime.
"""
from __future__ import annotations
import argparse, json, os, pathlib, platform, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parents[1]
PY = str(ROOT / "backend" / "venv" / "bin" / "python")
REPRO = ROOT / "research" / "reproducibility"
REPRO.mkdir(parents=True, exist_ok=True)

STAGES = [
    ("rebuild_index",   "scripts/data_ingestion/rebuild_index.py",   ["backend/data/index_v2/faiss.index"]),
    ("validate_index",  "scripts/data_ingestion/validate_index.py",  ["experiments/analysis/validation_index_v2.json"]),
    ("integrity_tests", "tests/data/test_index_integrity.py",        []),
    ("benchmark_v2",    "scripts/benchmark/build_benchmark_v2.py",   ["research/benchmark/iva80_latest.json"]),
    ("annotation_tasks","scripts/annotation/make_tasks.py",          ["research/annotations/tasks.jsonl"]),
    ("retrieval_eval",  "scripts/experiments/run_retrieval_eval.py", ["research/results/processed/metrics.json"]),
    ("judging_robust",  "scripts/experiments/judging_robustness.py", ["research/results/processed/judging_robustness.json"]),
    ("legacy_source",   "scripts/experiments/verify_legacy_and_source_bias.py",
                        ["research/results/processed/phase6_legacy_verification.json"]),
    ("topical_test",    "scripts/experiments/phase7b_topical_mismatch.py",
                        ["research/results/processed/phase7b_topical_mismatch.json"]),
    ("boilerplate_test","scripts/experiments/phase7c_boilerplate.py",
                        ["research/results/processed/phase7c_boilerplate.json"]),
    ("ablation_errors", "scripts/experiments/run_ablation_and_errors.py",
                        ["research/results/processed/ablation.json"]),
    ("rag_answers",     "scripts/experiments/run_rag_answer_eval.py",
                        ["research/results/processed/rag_answer_metrics.json"]),
    ("hypothesis_matrix","scripts/experiments/source_hypothesis_matrix.py",
                        ["research/results/processed/source_hypothesis_matrix.json"]),
    ("fairness",        "scripts/experiments/fairness_and_sensitivity.py",
                        ["research/results/processed/fairness_and_sensitivity.json"]),
    ("bm25_depth",      "scripts/experiments/bm25_depth_fairness.py",
                        ["research/results/processed/bm25_depth_fairness.json"]),
    ("perturbation",    "scripts/experiments/perturbation_study.py",
                        ["research/results/processed/perturbation_study.json"]),
    ("error_dataset",   "scripts/experiments/build_error_dataset.py",
                        ["research/error_analysis/error_dataset.jsonl"]),
    ("annotation_opt",  "scripts/annotation/optimize_protocol.py",
                        ["research/annotations/protocol_decision.json"]),
    ("rag_analysis",    "scripts/experiments/analyze_rag_answers.py",
                        ["research/results/processed/rag_answer_analysis.json"]),
    ("exp_manifest",    "scripts/experiments/build_experiment_manifest.py",
                        ["research/reproducibility/experiment_manifest.json"]),
    ("tables_figures",  "scripts/experiments/generate_tables_figures.py",
                        ["research/results/tables/all_tables.md"]),
    ("paper",           "scripts/paper/generate_paper.py",           ["research/paper/paper.md"]),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-rag", action="store_true", help="skip the slow LLM stage")
    ap.add_argument("--skip-rebuild", action="store_true", help="skip index rebuild (~3 min)")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    env = dict(os.environ, HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", PYTHONUNBUFFERED="1")
    log, t_all = [], time.time()
    for name, script, outputs in STAGES:
        if a.skip_rag and name == "rag_answers":
            log.append({"stage": name, "status": "SKIPPED (--skip-rag)"}); print(f"SKIP  {name}"); continue
        if a.skip_rebuild and name == "rebuild_index":
            log.append({"stage": name, "status": "SKIPPED (--skip-rebuild)"}); print(f"SKIP  {name}"); continue
        if not a.force and outputs and all((ROOT / o).exists() for o in outputs):
            log.append({"stage": name, "status": "CURRENT (outputs exist)"}); print(f"OK    {name} (cached)"); continue
        t0 = time.time()
        print(f"RUN   {name} ...", flush=True)
        r = subprocess.run([PY, str(ROOT / script)], cwd=ROOT, env=env,
                           capture_output=True, text=True)
        dt = round(time.time() - t0, 1)
        ok = r.returncode == 0
        log.append({"stage": name, "script": script, "status": "OK" if ok else "FAILED",
                    "seconds": dt, "returncode": r.returncode,
                    "stderr_tail": r.stderr.strip().splitlines()[-3:] if not ok else []})
        print(f"{'DONE ' if ok else 'FAIL '} {name}  ({dt}s)")
        if not ok:
            print(r.stderr[-1500:]); break

    manifest = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "total_seconds": round(time.time() - t_all, 1),
        "seed": 42,
        "environment": {
            "python": platform.python_version(), "platform": platform.platform(),
            "processor": platform.processor(), "cpu_count": os.cpu_count(),
        },
        "versions": {},
        "models": {"embedder": "BAAI/bge-small-en-v1.5 (384-d)",
                   "generator": "gemma3:4b via Ollama"},
        "retrieval_parameters": {"bm25_k1": 1.5, "bm25_b": 0.75, "rrf_k": 60,
                                 "pool_depth": 10, "top_k_default": 6},
        "chunking": {"target_tokens": 400, "overlap_tokens": 50},
        "stages": log,
    }
    for mod in ("numpy", "faiss", "scipy", "matplotlib", "sentence_transformers", "torch"):
        try:
            m = __import__(mod)
            manifest["versions"][mod] = getattr(m, "__version__", "unknown")
        except Exception:
            manifest["versions"][mod] = "not installed"
    idx = ROOT / "backend" / "data" / "index_v2" / "manifest.json"
    if idx.exists(): manifest["index_manifest"] = json.loads(idx.read_text())
    (REPRO / "run_manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"\ntotal {manifest['total_seconds']}s  ->  research/reproducibility/run_manifest.json")
    failed = [s for s in log if s["status"] == "FAILED"]
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
