"""
PHASE 2 - Turn IVA-80 into a versioned research benchmark.

Produces research/benchmark/iva80_v2.json with, per question:
  id, question, category, reference_answer,
  candidate_evidence (CANDIDATES - machine generated, NOT ground truth),
  retrieval_types, flags, annotation scaffold.

Audits for duplicates/near-duplicates, ambiguity, insufficient corpus evidence,
contested interpretations, and classifies the retrieval skill each question tests.

Nothing is deleted. Problematic questions are FLAGGED and retained.
"""
from __future__ import annotations
import collections, json, os, pathlib, re, sys
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np, faiss

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from retrieval.lexical.bm25 import BM25, tokenize

IDX = ROOT / "backend" / "data" / "index_v2"
SRC = ROOT / "paper" / "eval" / "benchmark_questions.json"
OUT = ROOT / "research" / "benchmark"
VERSION = "2.0.0"

CONTESTED = re.compile(r"\b(debat|contest|disput|controvers|decipher|claim|theor|"
                       r"hypothes|believ|argu|interpret|whether|really|actually)\w*", re.I)
COMPARATIVE = re.compile(r"\b(compare|versus|vs\.?|difference|differ|both|"
                         r"relationship between|similar)\w*", re.I)
PROPER = re.compile(r"\b[A-Z][a-z]{3,}(?:[- ][A-Z]?[a-z]+)*\b")
VAGUE = re.compile(r"\b(what about|anything|stuff|things|etc)\b", re.I)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    chunks = [json.loads(l) for l in (IDX / "chunks.jsonl").open(encoding="utf-8") if l.strip()]
    texts = [c["text"] for c in chunks]
    idx = faiss.read_index(str(IDX / "faiss.index"))
    V = np.asarray(idx.reconstruct_n(0, idx.ntotal), dtype=np.float32)
    qs = json.load(SRC.open())["questions"]

    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer("BAAI/bge-small-en-v1.5")
    enc = lambda xs: m.encode(xs, normalize_embeddings=True, convert_to_numpy=True,
                              show_progress_bar=False).astype(np.float32)
    QV, GV = enc([q["q"] for q in qs]), enc([q["ground_truth"] for q in qs])
    bm25 = BM25([tokenize(t) for t in texts])

    qsim = QV @ QV.T
    np.fill_diagonal(qsim, 0.0)
    near = collections.defaultdict(list)
    for i in range(len(qs)):
        for j in range(i + 1, len(qs)):
            if qsim[i, j] >= 0.93:
                near[qs[i]["id"]].append({"id": qs[j]["id"], "cos": round(float(qsim[i, j]), 4)})
                near[qs[j]["id"]].append({"id": qs[i]["id"], "cos": round(float(qsim[i, j]), 4)})
    exact = collections.Counter(q["q"].strip().lower() for q in qs)

    records, stats = [], collections.Counter()
    for i, q in enumerate(qs):
        qt, gt = q["q"], q["ground_truth"]
        dense = np.argsort(-(V @ QV[i]))[:5].tolist()
        lex = [d for d, _ in bm25.search(qt, top_k=5)]
        gtsim = V @ GV[i]
        gtop = np.argsort(-gtsim)[:5].tolist()
        cand = list(dict.fromkeys(dense + lex + gtop))[:12]
        evidence = [{"chunk_id": int(d), "source": chunks[d]["source"], "page": chunks[d]["page"],
                     "cos_to_question": round(float(V[d] @ QV[i]), 4),
                     "cos_to_reference_answer": round(float(gtsim[d]), 4),
                     "snippet": texts[d][:180].replace("\n", " "),
                     "retrieved_by": ("dense " if d in dense else "") +
                                     ("lexical " if d in lex else "") +
                                     ("answer-sim" if d in gtop else "")}
                    for d in cand]

        types = []
        q_toks = set(tokenize(qt)); ref_toks = set(tokenize(gt))
        hits = sum(1 for t in q_toks if bm25.inv.get(t))
        if q_toks and hits >= max(2, 0.6 * len(q_toks)): types.append("lexical")
        if float(gtsim.max()) >= 0.65: types.append("semantic")
        if COMPARATIVE.search(qt) or len(PROPER.findall(qt)) >= 2: types.append("multi_hop")
        if len({chunks[d]["source"] for d in cand[:6]}) == 1: types.append("source_specific")
        if q["category"] in ("scholars", "methodology"): types.append("evidence_attribution")
        if not types: types.append("unclassified")

        flags = []
        best = float(gtsim.max())
        if best < 0.55: flags.append("insufficient_corpus_evidence")
        if CONTESTED.search(qt) or CONTESTED.search(gt) or q["category"] == "controversies":
            flags.append("contested_interpretation")
        # Ambiguity: few content tokens AND no anchoring proper noun. A short question
        # naming a specific site/scholar (e.g. "Where is Mohenjo-daro located?") is
        # specific, not ambiguous - an earlier length-only rule flagged 48/80 and was
        # not discriminative.
        anchored = len(PROPER.findall(qt[1:])) >= 1     # skip sentence-initial capital
        if VAGUE.search(qt) or (len(q_toks) <= 3 and not anchored):
            flags.append("possibly_ambiguous")
        if len(ref_toks) <= 3: flags.append("very_short_reference_answer")
        if exact[qt.strip().lower()] > 1: flags.append("exact_duplicate_question")
        if near.get(q["id"]): flags.append("near_duplicate_question")
        if gt.strip().lower().startswith(("no ", "not ", "none", "unknown", "undeciphered")):
            flags.append("negative_or_unknown_answer")
        for f in flags: stats[f] += 1
        for t in types: stats["type:" + t] += 1

        records.append({
            "id": q["id"], "question": qt, "category": q["category"],
            "reference_answer": gt, "retrieval_types": types, "flags": flags,
            "near_duplicates": near.get(q["id"], []),
            "evidence_ceiling_cos": round(best, 4),
            "candidate_evidence": evidence,
            "relevance_criteria":
                "RELEVANT (2): chunk contains information sufficient to answer the question or "
                "directly supports the reference answer. PARTIAL (1): related context or part of "
                "the answer. NOT RELEVANT (0): otherwise. Judge the chunk against the QUESTION, "
                "not the wording of the reference answer.",
            "annotation": {"status": "PENDING", "annotators": [], "disagreements": [],
                           "final_labels": {}, "adjudicator": None},
        })

    usable = [r for r in records if "insufficient_corpus_evidence" not in r["flags"]]
    doc = {
        "benchmark": "IVA-80", "version": VERSION,
        "created_from": str(SRC.relative_to(ROOT)),
        "corpus": {"index": "index_v2", "chunks": len(chunks),
                   "embedder": "BAAI/bge-small-en-v1.5"},
        "n_questions": len(records), "n_without_blocking_flags": len(usable),
        "categories": dict(collections.Counter(r["category"] for r in records)),
        "flag_counts": {k: v for k, v in stats.items() if not k.startswith("type:")},
        "retrieval_type_counts": {k[5:]: v for k, v in stats.items() if k.startswith("type:")},
        "policy": "No question is deleted. Problematic questions are flagged and retained; "
                  "analyses report with and without flagged subsets.",
        "annotation_state": "PENDING - no human labels exist. candidate_evidence is machine "
                            "generated and is NOT ground truth.",
        "questions": records,
    }
    (OUT / f"iva80_v{VERSION}.json").write_text(json.dumps(doc, indent=2))
    (OUT / "iva80_latest.json").write_text(json.dumps(doc, indent=2))

    print(f"IVA-80 v{VERSION}: {len(records)} questions, {len(usable)} without blocking flags")
    print("\nflags:")
    for k, v in sorted(doc["flag_counts"].items(), key=lambda kv: -kv[1]): print(f"  {v:3d}  {k}")
    print("\nretrieval types (multi-label):")
    for k, v in sorted(doc["retrieval_type_counts"].items(), key=lambda kv: -kv[1]): print(f"  {v:3d}  {k}")
    ec = [r["evidence_ceiling_cos"] for r in records]
    print(f"\nevidence ceiling cos: min={min(ec):.3f} median={np.median(ec):.3f} max={max(ec):.3f}")
    print(f"wrote {(OUT / f'iva80_v{VERSION}.json').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
