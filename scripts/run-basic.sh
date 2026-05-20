#!/usr/bin/env bash
set -euo pipefail
mkdir -p results
python eval_ollama_models.py --pull --num-ctx 8192 --output ./results/benchmark-standard.json --models qwen2.5-coder:3b qwen2.5-coder:7b deepseek-coder:6.7b
python gen_dashboard.py --standard ./results/benchmark-standard.json
echo "Dashboard data generated at results/dashboard-data.js"
