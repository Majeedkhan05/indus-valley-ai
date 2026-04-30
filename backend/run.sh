#!/bin/bash
# ─────────────────────────────────────────────────────────────────
# Indus Valley AI — Backend launcher
# ─────────────────────────────────────────────────────────────────
set -e
cd "$(dirname "$0")"

echo "── Indus Valley AI — RAG Backend ──"
echo

# 1. Check Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
  echo "⚠️  Ollama is not running."
  echo "   Install:  https://ollama.com/download"
  echo "   Then:     ollama serve  (in another terminal)"
  echo "   And:      ollama pull llama3.1:8b"
  echo
fi

# 2. Check venv
if [ ! -d "venv" ]; then
  echo "Creating venv…"
  python3 -m venv venv
fi
# shellcheck disable=SC1091
source venv/bin/activate

# 3. Install deps
if [ ! -f "venv/.deps_installed" ]; then
  echo "Installing dependencies (this takes ~3 min the first time)…"
  pip install --upgrade pip > /dev/null
  pip install -r requirements.txt
  touch venv/.deps_installed
fi

# 4. Start FastAPI
echo
echo "Starting FastAPI on http://localhost:8000  …"
echo "   • Health:    http://localhost:8000/health"
echo "   • Docs:      http://localhost:8000/docs"
echo "   • Frontend:  open ../index.html in your browser"
echo
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
