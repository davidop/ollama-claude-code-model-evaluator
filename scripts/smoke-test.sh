#!/usr/bin/env bash
set -euo pipefail

OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://localhost:11434}"

echo "[1/6] Checking python3 availability"
if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 not found. Install Python 3.10+ and retry."
    exit 1
fi

if ! python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)'; then
    echo "ERROR: Python 3.10+ required. Found: $(python3 --version 2>&1)"
    exit 1
fi

echo "[2/6] Checking Ollama endpoint (${OLLAMA_BASE_URL})"
if ! command -v curl >/dev/null 2>&1; then
    echo "ERROR: curl not found. Install curl and retry."
    exit 1
fi

if ! curl -fsS "${OLLAMA_BASE_URL}/api/tags" >/dev/null; then
    echo "ERROR: Ollama is not reachable at ${OLLAMA_BASE_URL}"
    echo "Start Ollama in another terminal: ollama serve"
    exit 1
fi

echo "[3/6] Checking required project files"
for file in eval_ollama_models.py gen_dashboard.py hwdetect.py dashboard.html; do
    if [ ! -f "$file" ]; then
        echo "ERROR: Missing required file: $file"
        exit 1
    fi
    echo "  OK: $file"
done

echo "[4/6] Compiling Python scripts"
python3 -m py_compile eval_ollama_models.py gen_dashboard.py hwdetect.py scripts/validate-benchmark-json.py

echo "[5/6] Validating benchmark JSON"
python3 scripts/validate-benchmark-json.py

echo "[6/6] Ensuring dashboard data file exists"
if [ ! -f results/dashboard-data.js ]; then
    python3 gen_dashboard.py --standard ./results/benchmark-standard.json --base-url "${OLLAMA_BASE_URL}"
fi

if [ ! -f results/dashboard-data.js ]; then
    echo "ERROR: results/dashboard-data.js was not generated"
    exit 1
fi

echo ""
echo "Smoke test passed."
echo "Open dashboard: $PWD/dashboard.html"
