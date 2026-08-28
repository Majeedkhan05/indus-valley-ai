# Deployment Architecture

```
                 EXISTING REPOSITORY (branch: main)
                              |
              +---------------+---------------+
              |                               |
       HUGGING FACE                    NEW RESEARCH TARGET
       AIHub-Mu/indus-valley-ai        (Vercel — NOT YET CREATED)
       remote: hfspace / main          branch: NOT YET CREATED
       STATUS: LIVE — PRESERVE         STATUS: PLANNED
              |                               |
        DO NOT TOUCH                   develop + deploy
```

## Target A — Hugging Face (PRESERVE)
See `docs/huggingface-assets.md`. Static Space, no backend, LFS-tracked images.
Rules: do not migrate, do not force-push, do not delete, do not reconfigure.

## Target B — Vercel (NOT YET CREATED)

**Status: PLANNED / NEEDS DECISION.** Nothing has been created or configured.

Key architectural fact discovered in the audit: the frontend is **vanilla JS + Three.js
via CDN importmap — there is no bundler, no React, no Next.js, no `package.json`.**

Consequences:
- Vercel can host it as a **pure static deployment** — no framework, no build command,
  output directory = repo root. It does **not** need to be rewritten into Next.js.
- **Do not convert the site to Next.js just to deploy on Vercel.** That would violate the
  preservation rule and risks the 3D experience for zero research benefit.
- The **FastAPI backend cannot run on Vercel** as-is: it loads sentence-transformers,
  FAISS, torch and CLIP into memory, and calls a local Ollama server. That exceeds
  serverless limits and has no Ollama host.

### Recommended split
| Layer | Where | Notes |
|---|---|---|
| Static 3D frontend | Vercel (static, no build) | preserve as-is |
| RAG/CV/KG backend | Separate always-on host, or local-only | needs persistent RAM + Ollama |

If no backend host is available, the Vercel deployment behaves exactly like the HF Space:
KB + Gemini Nano fallback. That is acceptable for a demo.

### Not yet determined (do not guess)
- Vercel project name — **UNKNOWN**
- Production URL — **UNKNOWN**
- Backend host — **UNKNOWN / NEEDS DECISION**
- Branch strategy — **NEEDS DECISION** (suggest a new branch; none created yet)

### Environment isolation (when created)
`.env.example` only, never real values:
```
PUBLIC_API_URL=
PUBLIC_APP_ENV=
```
No API keys, HF tokens, or credentials are currently committed — verified during audit.
