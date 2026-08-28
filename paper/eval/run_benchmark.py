"""
Run the IVA-80 benchmark against the local backend.
Outputs results.jsonl with one row per question.

Usage:
    cd paper/eval
    python run_benchmark.py --system iva   # local RAG backend
    python run_benchmark.py --system kb    # KB-only fallback
"""
import argparse, json, time, requests, sys
from pathlib import Path

HERE = Path(__file__).parent
QUESTIONS = json.load((HERE / "benchmark_questions.json").open())["questions"]
RESULTS = HERE / "results.jsonl"

def query_iva(q: str) -> dict:
    t0 = time.time()
    try:
        r = requests.post(
            "http://127.0.0.1:8000/query",
            json={"question": q, "top_k": 6},
            timeout=180,
        )
        dt = time.time() - t0
        d = r.json()
        return {
            "answer":      d.get("answer", ""),
            "citations":   d.get("citations", []),
            "confidence":  d.get("confidence", 0),
            "in_domain":   d.get("in_domain", False),
            "latency_s":   round(dt, 2),
        }
    except Exception as e:
        return {"answer": f"[error: {e}]", "citations": [], "latency_s": round(time.time() - t0, 2)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--system", default="iva", choices=["iva"])
    ap.add_argument("--limit", type=int, default=None, help="Run first N only")
    args = ap.parse_args()

    qs = QUESTIONS[: args.limit] if args.limit else QUESTIONS
    print(f"Running {len(qs)} questions through {args.system}...")
    with RESULTS.open("w") as f:
        for q in qs:
            res = query_iva(q["q"])
            row = {**q, "system": args.system, **res}
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(f"  [{q['id']:>2}] ({res['latency_s']:>5.2f}s) {q['q'][:60]}")
    print(f"\nDone. Wrote {len(qs)} rows to {RESULTS}")
    print("Next: open results.jsonl and rate each answer (0/1/2) for accuracy + citation correctness.")

if __name__ == "__main__":
    main()
