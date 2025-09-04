#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Activate venv
source .venv/bin/activate

# Load env for OpenAI if exists
if [ -f .env.openai ]; then
  # shellcheck disable=SC2046
  export $(grep -v '^#' .env.openai | xargs)
fi

export LLM_BACKEND=openai
# Default model (can be overridden by OPENAI_MODEL in .env.openai)
export OPENAI_MODEL="${OPENAI_MODEL:-gpt-4o-mini}"

# Sanity check
: "${OPENAI_API_KEY:?OPENAI_API_KEY is missing. Edit .env.openai to set it.}"

echo "==> Starting OpenAI backend on http://127.0.0.1:8010 (model: $OPENAI_MODEL)"
python -m uvicorn tutor.api:app --host 127.0.0.1 --port 8010 --reload
