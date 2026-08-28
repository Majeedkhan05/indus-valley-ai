"""Scan the manuscript for deanonymising strings before submission."""
from __future__ import annotations
import pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
TARGETS = [ROOT / "research" / "paper" / "paper.md"]
PATTERNS = {
    "personal name": r"(?i)\bmajeed\b|\bmohammed\s+majeed\b|\bkhan\b",
    "institution": r"(?i)mahindra university|ai\s*hub",
    "github identity": r"(?i)github\.com/[A-Za-z0-9_-]+",
    "huggingface space": r"(?i)huggingface\.co/spaces/[A-Za-z0-9_-]+",
    "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "absolute home path": r"/Users/[A-Za-z0-9_.-]+/",
    "acknowledgement": r"(?i)\backnowledg(?:e)?ments?\b",
}
fail = False
for t in TARGETS:
    if not t.exists():
        print(f"MISSING {t}"); fail = True; continue
    text = t.read_text()
    print(f"scanning {t.relative_to(ROOT)} ({len(text)} chars)")
    for label, pat in PATTERNS.items():
        hits = re.findall(pat, text)
        if hits:
            fail = True
            print(f"  FAIL  {label}: {sorted(set(map(str, hits)))[:4]}")
        else:
            print(f"  pass  {label}")
print("\nANONYMITY:", "FAIL - fix before upload" if fail else "PASS")
sys.exit(1 if fail else 0)
