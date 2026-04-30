# How to Revert to the Original Version

The original v1 project files (before the seal-corpus expansion, the script-analysis section, and the training pipeline) are saved in `backup-v1-original/`.

## Quick revert (one command)

```bash
cd indus-valley
cp backup-v1-original/*.* .
```

This restores: `index.html`, `styles.css`, `app.js`, `knowledge-base.js`, `data.js`, `vision.js`, `gemini-nano.js`, `three-scene.js`, `three-routes.js`.

## To also remove the new additions

```bash
# Remove the script analysis module
rm script-analysis.js

# Remove the training pipeline
rm -rf training/

# (optional) remove the 80 added seal images — keep the original 12
cd assets/seals
ls seal-*.jpg | grep -vE "seal-(1|7|14|22|35|48|60|72|89|100|115|130)\.jpg" | xargs rm
```

## What was added (so you know what reverting removes)

| File | Status | Purpose |
|---|---|---|
| `script-analysis.js` | NEW | Frequency, positional, bigram, Z-score data |
| `training/extract_data.py` | NEW | KB → training JSONL converter |
| `training/finetune_colab.ipynb` | NEW | Mistral-7B QLoRA fine-tuning notebook |
| `training/requirements.txt` | NEW | Python deps |
| `training/README.md` | NEW | Pipeline instructions |
| `assets/seals/seal-2..117.jpg` | NEW | 80 seals from the dataset |
| `index.html` | MODIFIED | Added `<section id="analysis">` and spine node |
| `styles.css` | MODIFIED | Added analysis section styles |
| `app.js` | MODIFIED | Added analysis renderer, fixed upload bug |
| `knowledge-base.js` | MODIFIED | +19 PD-source topics + 4 analysis topics |
| `data.js` | MODIFIED | seals[] expanded from 12 → 92 |

## What stays the same after reverting

- The 3D scenes (hero seal + trade routes)
- The chat UI and Gemini Nano integration
- The vision module
- The original 49 KB topics
- The original 12 seal images
- All other behaviour
