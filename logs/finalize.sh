#!/bin/bash
cd "$(dirname "$0")/.."
while pgrep -f "run_rag_answer_eval" >/dev/null; do sleep 20; done
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
backend/venv/bin/python scripts/experiments/generate_tables_figures.py >> logs/finalize.log 2>&1
backend/venv/bin/python scripts/paper/generate_paper.py           >> logs/finalize.log 2>&1
backend/venv/bin/python scripts/submission/check_anonymity.py     >> logs/finalize.log 2>&1
echo "FINALIZE_DONE $(date)" >> logs/finalize.log
