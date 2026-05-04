---
title: Indus Valley AI
emoji: 🏺
colorFrom: yellow
colorTo: red
sdk: static
pinned: true
license: mit
short_description: Indus Valley AI research assistant
---

# Indus Valley AI

A **domain-restricted research assistant** for the Indus / Harappan Civilization
(c. 3300–1300 BCE), built end-to-end from scratch by **AI Hub, Mahindra University**.

> **Zero external paid APIs.** Runs entirely in your browser. 100% private.

## What it does

- Answers Indus / Harappan questions from a hand-curated **71-topic scholarly knowledge base**
- Uses on-device **Gemini Nano** (Chrome 127+) for free LLM enrichment
- Real-time **3D WebGL** scenes (procedural unicorn seal + trade-routes globe)
- **92 real Harappan seal photographs** in a clickable gallery
- **Computational script analysis** dashboard (frequency, positional, bigram, Z-score)
- Client-side image classification (no upload, no vision API)
- 5-part academic answer structure: *Direct Answer · Evidence · Interpretation · Alternative · Limitation*

## What it does NOT do

- No external paid API calls — everything runs locally
- No data leaves your device
- No video / multimedia generation
- No phonetic readings of the (still-undeciphered) Indus script
- No out-of-domain answers — politely refused

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | Vanilla HTML5 / CSS3 / JS (zero build step) |
| 3D | Three.js 0.160 |
| On-device LLM | Gemini Nano (`window.LanguageModel`) |
| Knowledge base | 71 hand-written scholarly topics |
| Vision | HTML Canvas pixel statistics |

A complete optional **RAG backend** with FastAPI + FAISS + Ollama (LLaMA 3.2) + CLIP
exists in the repo for ingesting scholarly PDFs locally. It is intentionally not
deployed here — the curated KB is the public-facing path.

## Sources

The knowledge base draws on:

- Marshall 1931 *Mohenjo-daro and the Indus Civilization* (PD)
- Mackay 1937–38 *Further Excavations at Mohenjo-daro* (PD)
- Vats 1940 *Excavations at Harappa* (PD)
- Wheeler 1947 ASI reports (PD)
- Mahadevan 1977 *Indus Script Concordance* (PD ASI)
- Parpola 1994 *Deciphering the Indus Script* (cited)
- Shinde et al. 2019 *Cell* (Rakhigarhi aDNA, open access)
- Yajnadevam *Indus Inscriptions*
- Authority Structure & Evolution of Early Writing Systems

## Project documents

- `HOW_IT_WORKS.md` — full technical explanation
- `Indus_Valley_AI_Project_Report.pdf` — publication-grade report

## Author

**Mohammed Majeed Khan** — President, AI Hub, Mahindra University, Hyderabad
Computer Science · Google Student Ambassador
`majeedkhan2005.cc@gmail.com`

## License

MIT for code. Knowledge-base content cites primary public-domain sources or
academic open-access papers.
