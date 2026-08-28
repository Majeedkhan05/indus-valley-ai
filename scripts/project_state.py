"""PHASE 1 - machine-readable project state report."""
from __future__ import annotations
import hashlib, json, os, pathlib, platform, subprocess, sys, time, urllib.request
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np, faiss

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "research" / "reproducibility" / "project_state.json"

def sh(*a, cwd=ROOT):
    try: return subprocess.run(a, cwd=cwd, capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception as e: return f"(error: {e})"

def http(url, timeout=15):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"error": str(e)}

def sha(p, n=1 << 20):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while (b := f.read(n)): h.update(b)
    return h.hexdigest()[:16]

def index_state(name):
    d = ROOT / "backend" / "data" / name
    if not (d / "faiss.index").exists(): return {"present": False}
    rows = sum(1 for l in (d / "chunks.jsonl").open(encoding="utf-8") if l.strip())
    idx = faiss.read_index(str(d / "faiss.index"))
    return {"present": True, "vectors": int(idx.ntotal), "metadata_rows": rows,
            "dim": int(idx.d), "aligned_counts": int(idx.ntotal) == rows,
            "faiss_sha256_16": sha(d / "faiss.index"),
            "chunks_sha256_16": sha(d / "chunks.jsonl")}

tests = {}
for t in ["tests/data/test_index_integrity.py"]:
    r = subprocess.run([str(ROOT / "backend/venv/bin/python"), str(ROOT / t)],
                       capture_output=True, text=True, cwd=ROOT, timeout=900)
    last = [l for l in r.stdout.strip().splitlines() if "passed" in l]
    tests[t] = {"exit_code": r.returncode, "summary": last[-1].strip() if last else "(none)",
                "passed": r.returncode == 0}

health = http("http://127.0.0.1:8000/health")
try:
    req = urllib.request.Request("http://127.0.0.1:8000/query",
        data=json.dumps({"question": "Where is Mohenjo-daro located?", "top_k": 3}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r: q = json.loads(r.read().decode())
    live = {"ok": True, "in_domain": q.get("in_domain"), "confidence": q.get("confidence"),
            "n_citations": len(q.get("citations") or []),
            "citations": [{"document": c["document"], "page": c["page"], "score": c["score"]}
                          for c in (q.get("citations") or [])[:3]],
            "answer_nonempty": bool((q.get("answer") or "").strip()),
            "answer_is_error": "[ollama error" in (q.get("answer") or "")}
except Exception as e:
    live = {"ok": False, "error": str(e)}

fe = {}
try:
    with urllib.request.urlopen("http://127.0.0.1:5500/index.html", timeout=15) as r:
        html = r.read().decode("utf-8", "replace")
    fe = {"http": 200, "bytes": len(html), "has_three_importmap": "three" in html,
          "n_sections": html.count("<section")}
except Exception as e:
    fe = {"error": str(e)}

state = {
  "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
  "phase": "1 - freeze and protect",
  "environment": {"python": platform.python_version(), "platform": platform.platform(),
                  "numpy": np.__version__, "faiss": faiss.__version__,
                  "cpu_count": os.cpu_count()},
  "git": {"parent_branch": sh("git", "branch", "--show-current"),
          "parent_head": sh("git", "rev-parse", "--short", "HEAD"),
          "parent_remotes": sh("git", "remote", "-v"),
          "parent_modified": [l for l in sh("git", "status", "--short").splitlines()
                              if l and not l.startswith("??")],
          "nested_backend_repo": {"head": sh("git", "rev-parse", "--short", "HEAD",
                                             cwd=ROOT / "backend"),
                                  "remote": sh("git", "remote", "-v", cwd=ROOT / "backend"),
                                  "preserved": True}},
  "indexes": {"legacy_index": {**index_state("index"),
                               "status": "LEGACY - KNOWN CITATION INTEGRITY FAILURE",
                               "retained": True},
              "index_v2": {**index_state("index_v2"), "status": "CANONICAL"}},
  "tests": tests,
  "backend": {"health": health, "live_query": live},
  "frontend": fe,
  "protected_invariants": [
      "do not rewrite the Three.js frontend",
      "do not migrate to Next.js",
      "do not delete backend/data/index (legacy)",
      "do not delete backend/.git",
      "do not rewrite git history or push",
  ],
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(state, indent=2))
print(json.dumps({
  "tests_passed": all(t["passed"] for t in tests.values()),
  "index_v2": state["indexes"]["index_v2"],
  "legacy": {k: state["indexes"]["legacy_index"][k] for k in ("vectors","metadata_rows","aligned_counts")},
  "backend_vectors": health.get("vector_count"),
  "live_query_ok": live.get("ok"), "citations": live.get("n_citations"),
  "answer_is_error": live.get("answer_is_error"),
  "frontend": fe.get("http"),
}, indent=2))
print(f"\nwrote {OUT.relative_to(ROOT)}")
