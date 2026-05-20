#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[1/5] Python syntax check"
python3 -m py_compile eval_ollama_models.py

echo "[2/5] CLI help check"
python3 eval_ollama_models.py --help >/dev/null

echo "[3/6] Benchmark JSON validation"
python3 scripts/validate-benchmark-json.py

echo "[4/6] README/docs link validation"
python3 scripts/validate-markdown-links.py

echo "[5/6] Required benchmark files"
[[ -f results/benchmark-standard.json ]]
if [[ -f results/benchmark-ctx16384-plus14b.json ]]; then
	echo "- Extended benchmark: results/benchmark-ctx16384-plus14b.json"
else
	echo "- Extended benchmark: not present (optional)"
fi

echo "[6/6] Required docs"
[[ -f README.md ]]
[[ -f README.en.md ]]
[[ -f docs/release/v0.1.0-release-notes.md ]]

echo "Quick release summary"
echo "- Standard benchmark: results/benchmark-standard.json"
echo "- Release notes: docs/release/v0.1.0-release-notes.md"

echo "Release check passed."
