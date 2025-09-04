#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Start OpenAI on 8010
./run_openai.sh & OPENAI_PID=$!
sleep 2

# Start Local on 8020
./run_local.sh & LOCAL_PID=$!

echo "==> OpenAI   : http://127.0.0.1:8010/docs  (PID: $OPENAI_PID)"
echo "==> Local HF : http://127.0.0.1:8020/docs  (PID: $LOCAL_PID)"
echo "Press Ctrl+C to stop both."
wait
