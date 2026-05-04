"""
Ollama LLM client — local LLaMA 3 / Mistral.
=============================================
Configure model with env var IVAI_OLLAMA_MODEL (default: 'llama3.1:8b').
Install Ollama:    https://ollama.com/download
Pull a model:      ollama pull llama3.1:8b   (or mistral, qwen2.5, etc.)
"""
from __future__ import annotations

import os
import json
import logging
from typing import Iterator, List

import requests

log = logging.getLogger("ivai.gen")

OLLAMA_HOST  = os.environ.get("IVAI_OLLAMA_HOST",  "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("IVAI_OLLAMA_MODEL", "llama3.1:8b")


SYSTEM_PROMPT = """You are a domain-specific research assistant for the Indus Valley Civilization.
Follow these rules STRICTLY.

═══════════════════════════════════════════════════════════════
ANSWER STRUCTURE — MANDATORY (every reply must follow this)
═══════════════════════════════════════════════════════════════
1. DIRECT ANSWER     — 1–2 lines that answer the actual question.
2. EVIDENCE          — From archaeology, PDFs, specific sites (e.g. Dholavira, Harappa, Mohenjo-daro, Lothal). Cite inline [source, p.<page>].
3. INTERPRETATION    — Explain implications: "what does this mean?"
4. ALTERNATIVE VIEW  — At least ONE competing or minority explanation.
5. LIMITATION        — Cautious language acknowledging gaps or uncertainty.

═══════════════════════════════════════════════════════════════
CONFIDENCE CONTROL
═══════════════════════════════════════════════════════════════
AVOID  ❌ universally · definitive · proves · unique · always · never · "no civilization"
USE    ✅ widely believed · suggests · likely indicates · the evidence is consistent with ·
          scholars debate · remains contested · cannot be confirmed · may indicate

═══════════════════════════════════════════════════════════════
REDUNDANCY CONTROL
═══════════════════════════════════════════════════════════════
- Do NOT repeat information already given in the same answer.
- If a point was made above, refer back to it instead of restating.
- No filler: every sentence must add new substance.

═══════════════════════════════════════════════════════════════
PDF / FILE HANDLING
═══════════════════════════════════════════════════════════════
- Treat the supplied CONTEXT (retrieved from uploaded PDFs) as the PRIMARY source.
- Prioritise uploaded PDF content over general knowledge.
- If the CONTEXT does not directly address the question, say so explicitly:
    "The indexed corpus does not directly address this. Based on related material in [source]..."
- Avoid generic responses when specific PDF data exists — quote / cite it.

═══════════════════════════════════════════════════════════════
DISABLED CAPABILITIES
═══════════════════════════════════════════════════════════════
- No video, animation, image, or multimedia generation.
- No phonetic readings of the (still-undeciphered) Indus script.
- No out-of-domain answers — politely refuse and redirect.

═══════════════════════════════════════════════════════════════
TONE
═══════════════════════════════════════════════════════════════
Cautious academic researcher. PDF-grounded. Structured. Non-overconfident.
Concise — under 220 words. Short paragraphs. Bullets only for real enumerations.
"""


def build_prompt(question: str, retrieved, history: List[dict]) -> str:
    """Compose the final prompt with grounded context + brief history."""
    ctx_parts = []
    for i, r in enumerate(retrieved, start=1):
        ctx_parts.append(
            f"[{i}] (source: {r.source}, p.{r.page}, relevance: {r.score:.2f})\n{r.text}"
        )
    context_block = "\n\n".join(ctx_parts) if ctx_parts else "(no context retrieved)"

    history_block = ""
    if history:
        for h in history[-4:]:           # last 2 turns
            role = h.get("role", "user")
            content = h.get("content", "")
            history_block += f"{role.upper()}: {content}\n"

    prompt = f"""SYSTEM:
{SYSTEM_PROMPT}

CONTEXT:
{context_block}

{history_block}USER QUESTION:
{question}

GROUNDED ANSWER (with inline citations):"""
    return prompt


# ─── Ollama HTTP client ─────────────────────────────────────────────────────
class OllamaClient:
    def __init__(self, host: str = OLLAMA_HOST, model: str = OLLAMA_MODEL):
        self.host = host.rstrip("/")
        self.model_name = model

    def ping(self) -> bool:
        try:
            r = requests.get(f"{self.host}/api/tags", timeout=3)
            return r.status_code == 200
        except Exception:
            return False

    def generate(self, prompt: str, temperature: float = 0.2, max_tokens: int = 220) -> str:
        try:
            r = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model":  self.model_name,
                    "prompt": prompt,
                    "keep_alive": "30m",      # keep model loaded between queries
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                        "top_k": 30,
                        "top_p": 0.9,
                        "num_ctx": 2048,       # smaller ctx → faster prompt eval
                    },
                    "stream": False,
                },
                timeout=600,
            )
            if r.status_code != 200:
                return f"[ollama error {r.status_code}: {r.text[:200]}]"
            return (r.json().get("response") or "").strip()
        except requests.exceptions.ConnectionError:
            return ("[Ollama is not running. Start it with `ollama serve` and pull a model "
                    "with `ollama pull llama3.1:8b`.]")
        except Exception as e:
            return f"[ollama exception: {e}]"

    def stream(self, prompt: str, temperature: float = 0.2, max_tokens: int = 512) -> Iterator[str]:
        try:
            r = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model":  self.model_name,
                    "prompt": prompt,
                    "keep_alive": "30m",      # keep model loaded between queries
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                        "num_ctx": 2048,
                    },
                    "stream": True,
                },
                stream=True,
                timeout=600,
            )
            for line in r.iter_lines():
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                tok = obj.get("response", "")
                if tok:
                    yield tok
                if obj.get("done"):
                    return
        except Exception as e:
            yield f"[stream error: {e}]"
