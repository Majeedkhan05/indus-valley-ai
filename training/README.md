# Indus Valley AI — Fine-tuning Pipeline

Convert your knowledge base into a real LLM specialised in the Indus / Harappan civilization. **Total cost: $0.** Uses Google Colab's free GPU.

## What this gives you

| Before | After |
|---|---|
| Keyword-matching expert system | Real LLM that generates new answers |
| 70 pre-written topics | Full Mistral-7B specialised on Indus Valley |
| Static — only answers known phrasings | Generative — handles any phrasing |
| Domain-locked via gate | Domain-locked via training + system prompt |

## Pipeline

```
Step 1: extract_data.py  →  training_data.jsonl  (run locally)
Step 2: Upload to Colab  →  finetune_colab.ipynb  (run on Colab GPU)
Step 3: Push to HF Hub   →  free inference endpoint
Step 4: Update app.js    →  call your model API
```

## Quick start

### Step 1 — Extract training data (local, 5 seconds)

```bash
cd training
python3 extract_data.py
```

Output: `training_data.jsonl` (~600 KB, 425 examples).

### Step 2 — Run the Colab notebook (4–6 hours, free GPU)

1. Open https://colab.research.google.com/
2. Upload `finetune_colab.ipynb`
3. **Runtime → Change runtime type → T4 GPU** (free)
4. Run all cells in order
5. When prompted, upload `training_data.jsonl`
6. Wait for training to finish (~4–6 hrs)

### Step 3 — Push model to Hugging Face

In the notebook, the last cell pushes your fine-tuned LoRA adapter to Hugging Face Hub. Get a free token at https://huggingface.co/settings/tokens.

### Step 4 — Connect your website to the model

Hugging Face Inference Endpoints are free for public models. Replace `IVA_KB.bestTopic()` calls in `app.js` with `fetch()` calls to your endpoint.

## Files in this folder

| File | Purpose |
|---|---|
| `extract_data.py` | Parses `knowledge-base.js` into `training_data.jsonl` |
| `training_data.jsonl` | Generated training dataset (425 examples) |
| `finetune_colab.ipynb` | Google Colab notebook for QLoRA fine-tuning |
| `requirements.txt` | Python deps if running locally with a GPU |
| `README.md` | This file |

## Reverting

The original (pre-expansion) project files are in `../backup-v1-original/`. To revert:

```bash
cp ../backup-v1-original/*.* ../
```

## Notes

- **Mistral-7B-Instruct-v0.2** is open-source and free (Apache 2.0)
- **QLoRA** (4-bit quantized LoRA) keeps memory under 16 GB — fits free Colab T4
- **The original keyword-matching system stays as a fallback** — your site keeps working even if the LLM endpoint is down
- For larger corpora (Marshall 1931 PDF + Mahadevan 1977 PDF + ASI reports), add a `prepare_pdfs.py` script that converts PDFs to text and chunks them into instruction pairs
