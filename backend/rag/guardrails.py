"""
Domain guardrails.
==================
- Whitelist of in-domain keywords (Indus / Harappan / archaeology / specific sites).
- Hard out-of-scope blocklist (crypto, sports, modern tech, current events).
- Returns True/False for is_in_domain(question).
"""
from __future__ import annotations

import re

IN_DOMAIN_KEYWORDS = {
    "indus","harappa","harappan","mohenjo","daro","dholavira","lothal","rakhigarhi",
    "kalibangan","banawali","surkotada","chanhu","mehrgarh","meluhha","dilmun","magan",
    "sarasvati","saraswati","ghaggar","hakra","seal","seals","script","sign","unicorn",
    "zebu","pashupati","priest-king","priest king","dancing girl","great bath","granary",
    "carnelian","steatite","ivory","adna","aryan","bronze age","south asia","sindh",
    "punjab","gujarat","haryana","rajasthan","balochistan","kutch","citadel","drainage",
    "marshall","mackay","vats","wheeler","kenoyer","possehl","parpola","mahadevan",
    "yajnadevam","cisi","corpus of indus","fish sign","jar sign","brahmi","tablet",
    "amulet","sealings","faience","shortugai","mound","cemetery","fire altar","ploughed",
    "harappan period","mature harappan","early harappan","late harappan","jhukar","cemetery h",
    "ravi phase","kot diji","sothi","hakra ware","civilization","civilisation","indo-aryan",
    "rigveda","vedic","decipherment","logographic","logo-syllabic","ideograph"
}

OUT_OF_SCOPE_PATTERNS = re.compile(
    r"\b(bitcoin|crypto|stock\s*price|recipe|football|cricket|ipl|nba|"
    r"chatgpt|gpt-?4|openai|anthropic|claude|gemini\s+pro|"
    r"netflix|whatsapp|iphone|android|"
    r"javascript|python\s+code|react\s+component|"
    r"current\s+president|prime\s+minister|election|"
    r"weather|temperature\s+(today|tomorrow))\b",
    re.IGNORECASE,
)

OUT_OF_DOMAIN_RESPONSE = (
    "I'm Indus Valley AI — a domain-restricted assistant for the Indus / Harappan civilization. "
    "Out-of-scope question. Try asking about Mohenjo-daro, the Indus script, seals, trade with Mesopotamia, "
    "or the Pashupati seal."
)


def is_in_domain(question: str) -> bool:
    q = question.lower()
    if OUT_OF_SCOPE_PATTERNS.search(q):
        return False
    # any keyword present → in domain
    for kw in IN_DOMAIN_KEYWORDS:
        if kw in q:
            return True
    # default: shorter than 6 words and uses only generic terms → out
    if len(q.split()) < 4:
        return False
    # otherwise — let it through; retrieval threshold will catch noise
    return True
