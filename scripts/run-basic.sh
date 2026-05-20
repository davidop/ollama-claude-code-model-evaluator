#!/usr/bin/env bash
set -euo pipefail

OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://localhost:11434}"

if ! command -v python3 >/dev/null 2>&1; then
	echo "ERROR: python3 not found. Install Python 3.10+ and try again."
	exit 1
fi

if ! python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)'; then
	echo "ERROR: Python 3.10+ is required. Found: $(python3 --version 2>&1)"
	exit 1
fi

if ! command -v curl >/dev/null 2>&1; then
	echo "ERROR: curl not found. Install curl to run preflight checks."
	exit 1
fi

if ! curl -fsS "${OLLAMA_BASE_URL}/api/tags" >/dev/null; then
	echo "ERROR: Cannot reach Ollama at ${OLLAMA_BASE_URL}."
	echo "Start Ollama in another terminal, for example:"
	echo "  ollama serve"
	exit 1
fi

mkdir -p results

python3 eval_ollama_models.py --pull --num-ctx 8192 --output ./results/benchmark-standard.json --models qwen2.5-coder:3b qwen2.5-coder:7b deepseek-coder:6.7b

if [ ! -f ./results/benchmark-standard.json ]; then
	echo "ERROR: Benchmark completed without creating results/benchmark-standard.json"
	exit 1
fi

python3 gen_dashboard.py --standard ./results/benchmark-standard.json --base-url "${OLLAMA_BASE_URL}"
echo "Dashboard data generated at results/dashboard-data.js"
