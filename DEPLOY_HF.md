# Deploy to Hugging Face Spaces (Private)

Step-by-step — total time ~10 minutes — to put the Indus Valley AI site on a private
Hugging Face Space and grant access to specific people.

---

## What gets deployed

✅ **The full static site** — index.html, all CSS/JS, 92 seal images, 13 sections,
3D scenes, KB, computational analysis, Gemini Nano integration.

❌ **NOT the local RAG backend** (Ollama, FAISS, FastAPI) — that stays on your laptop.
Hugging Face's free tier doesn't run Ollama. The site falls back gracefully to the
keyword KB when the backend is offline — which is what you should demo anyway.

This means: anyone with access can use the site instantly with the **71-topic curated
KB + Gemini Nano** — exactly what you'll show the board.

---

## Step 1 — Create a Hugging Face account

1. Go to https://huggingface.co/join
2. Sign up (free)
3. Verify your email

## Step 2 — Create the Space

1. Click your profile icon (top right) → **+ New Space**
2. Fill in:
   - **Space name**: `indus-valley-ai`
   - **License**: `MIT` (or `cc-by-nc-4.0` for non-commercial)
   - **SDK**: ⚠️ **Static** (very important — pick this, not Gradio/Streamlit)
   - **Hardware**: CPU basic (free)
   - **Visibility**: **Private** (toggle this on!)
3. Click **Create Space**

## Step 3 — Get an access token (for git push)

1. Go to https://huggingface.co/settings/tokens
2. Click **New token**
3. Name: `space-deploy`
4. Type: **Write**
5. Click **Generate** — copy the token (starts with `hf_…`)

## Step 4 — Push your site (run in terminal)

```bash
# 1. Go to your project folder
cd /Users/majeedkhan2005/Desktop/majeedkhanwebsite/indus-valley

# 2. Initialize git if not already
git init
git lfs install            # in case any large files

# 3. Add the HF Space as a remote
#    Replace YOUR_USERNAME with your HF username
git remote add hfspace https://huggingface.co/spaces/YOUR_USERNAME/indus-valley-ai

# 4. Stage everything EXCEPT what shouldn't be uploaded
cat > .gitignore << 'EOF'
backend/venv/
backend/data/index/
backend/data/ocr/
backend/data/pdfs/*.pdf
backend/__pycache__/
backend/**/__pycache__/
training/training_data.jsonl
backup-v1-original/
*.pyc
.DS_Store
EOF

# 5. Commit & push
git add .
git commit -m "Initial deploy of Indus Valley AI"
git branch -M main

# When git asks for password, paste your HF access token (NOT your HF password)
git push hfspace main
```

## Step 5 — Wait for the build

After pushing, the Space will show **"Building"** for ~30 seconds, then **"Running"**.

Your URL: `https://huggingface.co/spaces/YOUR_USERNAME/indus-valley-ai`

## Step 6 — Grant access to board members / professors

Since the Space is Private:

1. Open your Space page on huggingface.co
2. Click **Settings** (top right of the Space)
3. Scroll to **"Repository visibility"** section
4. Click **"Manage access"**
5. Add HF usernames of the people you want to grant access to
   - Each board member / professor needs a (free) HF account
   - You can also generate **link-based access** if available on your tier

Alternatively, for the demo:
- Set Space to **Public** for the day
- Take the demo
- Set back to **Private** afterwards

## Step 7 — Update without redeploying

Any future changes:
```bash
cd /Users/majeedkhan2005/Desktop/majeedkhanwebsite/indus-valley
# … make your edits …
git add .
git commit -m "your change"
git push hfspace main
```

The Space rebuilds automatically in ~30 seconds.

---

## What viewers will experience

When they open the URL:
- ✅ Full site loads instantly (CDN-served by HF)
- ✅ All 13 sections, 3D scenes, animations, gallery work perfectly
- ✅ Chat answers from the **curated 71-topic KB** instantly
- ✅ If they're on Chrome 127+ with Gemini Nano enabled, they get on-device LLM
      enrichment for free
- ⚠️ The RAG backend / Ollama / CISI volumes stay on YOUR machine — they don't
      get those (which is correct: the CISI volumes are copyrighted and shouldn't
      be redistributed anyway)

---

## A note about the CISI volumes

**Do NOT push the CISI PDFs to Hugging Face.** They are copyrighted (Parpola / Helsinki).
The `.gitignore` above already excludes them. Use them only locally on your laptop for
the RAG backend. For the public-facing Space, the curated KB is the right scope.

---

## Recommended tagline for the Space description

```
A domain-restricted research assistant for the Indus Valley Civilization.
Built end-to-end from scratch. Zero external paid APIs.  100% private — runs
entirely in your browser. Curated 71-topic scholarly KB + on-device Gemini Nano +
real-time WebGL 3D + computational script analysis.

Project by AI Hub, Mahindra University.
```
