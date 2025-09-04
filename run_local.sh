#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Activate venv
source .venv/bin/activate

# Local / HF Transformers
export LLM_BACKEND=transformers
# You can change to another small model if you want
export LLM_MODEL_ID="${LLM_MODEL_ID:-TinyLlama/TinyLlama-1.1B-Chat-v1.0}"

echo "==> Starting LOCAL (HF Transformers) backend on http://127.0.0.1:8020 (model: $LLM_MODEL_ID)"
python -m uvicorn tutor.api:app --host 127.0.0.1 --port 8020 --reload
