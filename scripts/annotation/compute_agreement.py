"""
PHASE 3 - Agreement, disagreement detection and adjudication scaffolding.

Reads research/annotations/labels_*.jsonl (one file per annotator) and produces:
  research/annotations/agreement.json      Cohen's kappa (pairwise), raw agreement
  research/annotations/disagreements.jsonl tasks needing adjudication
  research/annotations/qrels_human.json    FINAL labels - only when adjudicated

If fewer than two annotators have submitted labels, the script reports that and
writes NO qrels. It never invents a label.
"""
from __future__ import annotations
import collections, itertools, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
ANN = ROOT / "research" / "annotations"


def kappa(a, b):
    n = len(a)
    if n == 0: return float("nan")
    cats = sorted(set(a) | set(b))
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    return (po - pe) / (1 - pe) if pe != 1 else float("nan")


def main():
    files = sorted(ANN.glob("labels_*.jsonl"))
    labels = {}
    for f in files:
        who = f.stem.replace("labels_", "")
        labels[who] = {r["task_id"]: r for r in
                       (json.loads(l) for l in f.open(encoding="utf-8") if l.strip())}
    tasks = {json.loads(l)["task_id"]: json.loads(l)
             for l in (ANN / "tasks.jsonl").open(encoding="utf-8") if l.strip()}

    report = {"annotators": {k: len(v) for k, v in labels.items()},
              "total_tasks": len(tasks),
              "n_annotators": len(labels), "pairwise_kappa": {}, "raw_agreement": {},
              "status": "INSUFFICIENT_ANNOTATION"}

    if len(labels) < 2:
        report["message"] = (
            "Fewer than two annotators have submitted labels. Cohen's kappa requires two. "
            "No qrels_human.json written - human ground truth does NOT exist yet.")
        (ANN / "agreement.json").write_text(json.dumps(report, indent=2))
        print(json.dumps(report, indent=2)); return

    disagree = []
    for x, y in itertools.combinations(sorted(labels), 2):
        common = [t for t in labels[x] if t in labels[y]
                  and labels[x][t].get("grade") is not None
                  and labels[y][t].get("grade") is not None]
        ga = [labels[x][t]["grade"] for t in common]
        gb = [labels[y][t]["grade"] for t in common]
        report["pairwise_kappa"][f"{x}|{y}"] = kappa(ga, gb)
        report["raw_agreement"][f"{x}|{y}"] = (
            sum(u == v for u, v in zip(ga, gb)) / len(common) if common else float("nan"))
        for t in common:
            if labels[x][t]["grade"] != labels[y][t]["grade"]:
                disagree.append({"task_id": t, "qid": tasks[t]["qid"],
                                 "chunk_id": tasks[t]["chunk_id"],
                                 "grades": {x: labels[x][t]["grade"], y: labels[y][t]["grade"]}})
    unsure = [t for who in labels for t, r in labels[who].items() if r.get("grade") is None]
    need = {d["task_id"] for d in disagree} | set(unsure)
    with (ANN / "disagreements.jsonl").open("w", encoding="utf-8") as f:
        for d in disagree: f.write(json.dumps(d) + "\n")

    adj_path = ANN / "adjudicated.jsonl"
    adjudicated = ({json.loads(l)["task_id"]: json.loads(l)["grade"]
                    for l in adj_path.open(encoding="utf-8") if l.strip()}
                   if adj_path.exists() else {})
    unresolved = need - set(adjudicated)
    report.update({"disagreements": len(disagree), "unsure": len(unsure),
                   "needing_adjudication": len(need),
                   "adjudicated": len(adjudicated), "unresolved": len(unresolved)})

    if unresolved:
        report["status"] = "AWAITING_ADJUDICATION"
        report["message"] = (f"{len(unresolved)} tasks still need adjudication "
                             f"(see disagreements.jsonl). No qrels written.")
    else:
        qrels = collections.defaultdict(dict)
        for t, task in tasks.items():
            gs = [labels[w][t]["grade"] for w in labels
                  if t in labels[w] and labels[w][t].get("grade") is not None]
            g = adjudicated.get(t, gs[0] if gs and len(set(gs)) == 1 else None)
            if g is not None:
                qrels[str(task["qid"])][str(task["chunk_id"])] = g
        (ANN / "qrels_human.json").write_text(json.dumps(qrels, indent=2))
        report["status"] = "COMPLETE"
        report["qrels_questions"] = len(qrels)
    (ANN / "agreement.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
