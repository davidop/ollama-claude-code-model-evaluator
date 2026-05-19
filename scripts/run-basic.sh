#!/usr/bin/env bash
set -euo pipefail
python eval_ollama_models.py --pull --models qwen2.5-coder:3b qwen2.5-coder:7b deepseek-coder:6.7b codellama:7b
