"""
Indus Valley AI — Training Data Extractor
============================================
Converts the website's knowledge-base.js into instruction-tuning JSONL
format suitable for fine-tuning LLaMA/Mistral via QLoRA.

Output: training_data.jsonl
Format: one JSON object per line:
    {"instruction": "...", "input": "", "output": "..."}

Run: python3 extract_data.py
"""

import json
import re
import os
import html
from pathlib import Path

HERE = Path(__file__).parent
KB_PATH = HERE.parent / "knowledge-base.js"
OUT_PATH = HERE / "training_data.jsonl"
QA_PER_TOPIC = 6  # number of synthetic question-answer pairs per topic


def strip_html(text: str) -> str:
    """Remove HTML tags but keep the words inside <em>, <strong>, <code> etc."""
    text = re.sub(r"<ul>", "\n", text)
    text = re.sub(r"</ul>", "\n", text)
    text = re.sub(r"<li>", "  - ", text)
    text = re.sub(r"</li>", "\n", text)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def extract_topics_from_kb(kb_path: Path):
    """
    Parse knowledge-base.js — a JavaScript file — to extract topic objects.
    We don't run JS; we use a regex-based scan that matches the file's structure.
    """
    src = kb_path.read_text(encoding="utf-8")

    # Crop to the topics array
    topics_block = src.split("topics: [", 1)[1]
    topics_block = topics_block.split("domainFallback", 1)[0]

    # Grab each {...} object
    topics = []
    depth, start, in_str, str_ch, escape = 0, None, False, None, False
    for i, ch in enumerate(topics_block):
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if in_str:
            if ch == str_ch:
                in_str = False
            continue
        if ch in ("'", '"', "`"):
            in_str, str_ch = True, ch
            continue
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                topics.append(topics_block[start:i + 1])
                start = None

    # Parse each topic object loosely
    parsed = []
    for raw in topics:
        title_m = re.search(r"title:\s*['\"`]([^'\"`]+)['\"`]", raw)
        sources_m = re.search(r"sources:\s*['\"`]([^'\"`]*)['\"`]", raw)
        if not title_m:
            continue

        # keys array
        keys = []
        keys_block = re.search(r"keys:\s*\[(.*?)\]", raw, flags=re.DOTALL)
        if keys_block:
            for k in re.findall(r"['\"`]([^'\"`]+)['\"`]", keys_block.group(1)):
                keys.append(k.strip())

        # body array — take everything between body: [ and the closing ]
        body_block = re.search(r"body:\s*\[(.*?)\]\s*\}\s*$", raw, flags=re.DOTALL)
        if not body_block:
            body_block = re.search(r"body:\s*\[(.*?)\]", raw, flags=re.DOTALL)
        body_paragraphs = []
        if body_block:
            for p in re.findall(r"['\"`](.*?)['\"`]\s*(?:,|$)", body_block.group(1), flags=re.DOTALL):
                clean = strip_html(p).replace("\\'", "'").replace('\\"', '"')
                if clean and len(clean) > 20:
                    body_paragraphs.append(clean)

        parsed.append({
            "title": title_m.group(1),
            "sources": sources_m.group(1) if sources_m else "",
            "keys": keys,
            "body": body_paragraphs,
        })
    return parsed


def make_qa_pairs(topic: dict) -> list:
    """
    Generate multiple question/answer training pairs per topic, so the model
    learns to recognise the same topic from many phrasings.
    """
    title = topic["title"]
    sources = topic["sources"]
    body_text = "\n\n".join(topic["body"])
    if sources:
        body_with_cite = f"{body_text}\n\n[Source: {sources}]"
    else:
        body_with_cite = body_text

    # Question templates — varied phrasings for the SAME answer
    templates = [
        f"What is {title}?",
        f"Tell me about {title}.",
        f"Explain {title}.",
        f"Describe {title} in detail.",
        f"Can you explain what {title} refers to?",
        f"Give me a scholarly overview of {title}.",
    ]

    # Add keyword-based questions for variety
    for key in topic["keys"][:6]:
        if len(key) >= 4 and not key.startswith("what"):
            templates.append(f"What can you tell me about {key}?")
        if len(key) >= 4:
            templates.append(f"{key.capitalize()}?")

    pairs = []
    for q in templates[:QA_PER_TOPIC]:
        pairs.append({
            "instruction": q,
            "input": "",
            "output": body_with_cite,
        })
    return pairs


def main():
    print(f"Reading: {KB_PATH}")
    topics = extract_topics_from_kb(KB_PATH)
    print(f"Parsed {len(topics)} topics")

    examples = []
    for topic in topics:
        if not topic["body"]:
            continue
        examples.extend(make_qa_pairs(topic))

    # Add system-prompt examples to enforce domain locking and style
    SYSTEM_GUIDANCE = (
        "You are Indus Valley AI, a domain-restricted scholarly assistant on "
        "the Indus / Harappan civilization (c. 3300–1300 BCE). You answer ONLY "
        "questions about Indus archaeology, sites, seals, script, motifs, "
        "trade, decline, and related topics. Decline politely if a question "
        "is out of scope."
    )

    # Out-of-domain refusal examples
    refusals = [
        ("What is bitcoin?", "I'm Indus Valley AI — I only answer questions about the Indus / Harappan civilization. For bitcoin, please use a general-purpose AI."),
        ("Tell me about the iPhone.", "Out of scope. I'm a domain-restricted assistant for the Indus Valley Civilization only. Try asking me about Mohenjo-daro, the Indus script, or Harappan trade instead."),
        ("Who is the current president?", "I only handle Indus / Harappan civilization questions. Please use a general-purpose AI for current affairs."),
        ("What's the recipe for biryani?", "I'm scoped to the Indus Valley Civilization. I can talk about Harappan agriculture, foodways from carbonised remains, or storage practices — but not modern cuisine."),
        ("Solve x^2 + 5x + 6 = 0", "Out of scope. I only handle Indus archaeology and history questions."),
    ]
    for q, a in refusals:
        examples.append({"instruction": q, "input": "", "output": a})

    # Shuffle to mix topics
    import random
    random.seed(42)
    random.shuffle(examples)

    # Write JSONL
    with OUT_PATH.open("w", encoding="utf-8") as f:
        for ex in examples:
            ex["system"] = SYSTEM_GUIDANCE
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    print(f"Wrote {len(examples):,} training examples to: {OUT_PATH}")
    print(f"Approx size: {OUT_PATH.stat().st_size / 1024:.1f} KB")
    print()
    print("Next step: open training/finetune_colab.ipynb in Google Colab,")
    print("upload training_data.jsonl, and run the notebook.")


if __name__ == "__main__":
    main()
