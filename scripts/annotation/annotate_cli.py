"""
PHASE 3 - CLI annotation tool.

Usage:
  backend/venv/bin/python scripts/annotation/annotate_cli.py --annotator alice
  ... --limit 50            annotate only the next 50 unlabelled tasks
  ... --qid 14              annotate one question

Writes research/annotations/labels_<annotator>.jsonl (append-only, resumable).
Never writes a grade the annotator did not enter.
"""
from __future__ import annotations
import argparse, json, pathlib, sys, time

ROOT = pathlib.Path(__file__).resolve().parents[2]
ANN = ROOT / "research" / "annotations"
GRADES = {"2": 2, "1": 1, "0": 0}
HELP = """
  2 = RELEVANT      chunk is sufficient to answer the question
  1 = PARTIAL       related context, or part of the answer
  0 = NOT RELEVANT
  s = skip (records UNSURE, resolved at adjudication)
  q = save and quit
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--annotator", required=True)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--qid", type=int, default=None)
    a = ap.parse_args()

    tasks = [json.loads(l) for l in (ANN / "tasks.jsonl").open(encoding="utf-8") if l.strip()]
    out = ANN / f"labels_{a.annotator}.jsonl"
    done = set()
    if out.exists():
        done = {json.loads(l)["task_id"] for l in out.open(encoding="utf-8") if l.strip()}
    todo = [t for t in tasks if t["task_id"] not in done
            and (a.qid is None or t["qid"] == a.qid)]
    if a.limit: todo = todo[: a.limit]
    if not todo:
        print("nothing to annotate"); return

    print(f"annotator={a.annotator}  todo={len(todo)}  already done={len(done)}")
    print(HELP)
    n = 0
    with out.open("a", encoding="utf-8") as f:
        for t in todo:
            print("=" * 78)
            print(f"[{n+1}/{len(todo)}]  Q{t['qid']} ({t['category']})")
            print(f"QUESTION : {t['question']}")
            print(f"REFERENCE: {t['reference_answer']}")
            print("-" * 78)
            print(f"CANDIDATE EVIDENCE  ({t['source']}, p.{t['page']})")
            print(t["chunk_text"][:1100])
            print("-" * 78)
            g = input("relevance [2/1/0/s/q]: ").strip().lower()
            if g == "q": break
            rec = {"task_id": t["task_id"], "qid": t["qid"], "chunk_id": t["chunk_id"],
                   "annotator": a.annotator, "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
            if g == "s":
                rec["grade"] = None; rec["unsure"] = True
            elif g in GRADES:
                rec["grade"] = GRADES[g]; rec["unsure"] = False
                rec["source_ok"] = input("  correct source? [y/n/?]: ").strip().lower() or "?"
                rec["page_ok"] = input("  correct page?   [y/n/?]: ").strip().lower() or "?"
                rec["evidence_sufficient"] = input("  evidence sufficient? [y/n/?]: ").strip().lower() or "?"
                rec["notes"] = input("  notes (optional): ").strip()
            else:
                print("  unrecognised input - recorded as UNSURE")
                rec["grade"] = None; rec["unsure"] = True
            f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
            n += 1
    print(f"\nsaved {n} judgments -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
