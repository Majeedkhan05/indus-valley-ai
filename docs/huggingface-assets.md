# Hugging Face Assets — PRESERVED

**Rule: this deployment is legacy/preserved. Do not delete, migrate, force-push, or reconfigure it.**

| Field | Value |
|---|---|
| Resource | Space (static) |
| Repo ID | `AIHub-Mu/indus-valley-ai` |
| URL | https://huggingface.co/spaces/AIHub-Mu/indus-valley-ai |
| Git remote | `hfspace` |
| Branch | `main` |
| Entrypoint | `index.html` (static, no build) |
| Runtime | Static Space — **no Python process** |
| Large files | `assets/seals/*` via **Git LFS** |
| Env vars | none required |
| Backend | **NOT deployed here.** FastAPI runs locally only. |
| Used by current project | Yes — public demo |
| Reuse | Yes, as-is |
| Needs new version | No — new work goes to a *separate* target |

## What HF depends on (do not remove)
`index.html`, `app.js`, `styles.css`, `data.js`, `knowledge-base.js`, `gemini-nano.js`,
`vision.js`, `three-scene.js`, `three-routes.js`, `script-analysis.js`, `rag-client.js`,
`assets/seals/`, `.gitattributes` (LFS rules).

`rag-client.js` points at `http://127.0.0.1:8000`, so on the Space the backend probe fails
and the app falls back to the curated KB + Gemini Nano. **This is intended behaviour** —
the Space is meant to work with no server.

## Known issue (open, not fixed in this audit)
Seal images have reportedly not rendered on the Space. Probable cause: Git LFS pointer
files served instead of image bytes. **Not investigated or changed here** — flagged only.

## Rules going forward
- New research version → **separate deployment target**, separate branch.
- Never `git push --force` to `hfspace/main`.
- Never delete the Space to "clean up".
