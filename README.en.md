# Ollama Claude Code Model Evaluator

[![Validate](https://github.com/davidop/ollama-claude-code-model-evaluator/actions/workflows/validate.yml/badge.svg)](https://github.com/davidop/ollama-claude-code-model-evaluator/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/runtime-Ollama-black.svg)](https://ollama.com/)

English README. For Spanish, see [README.md](README.md).

Minimal repository to benchmark which local Ollama model works best for coding tasks and Claude Code usage.

Compare quality and speed on your own hardware, publish reproducible results, and run Claude Code with the winning local model in one command.

Quick links:

- Interactive dashboard: [dashboard.html](dashboard.html)
- Standard benchmark JSON: [results/benchmark-standard.json](results/benchmark-standard.json)
- 16384 context + 14b benchmark JSON: [results/benchmark-ctx16384-plus14b.json](results/benchmark-ctx16384-plus14b.json)

Dashboard preview:

![Dashboard preview](docs/assets/dashboard-preview.svg)

## Why This Matters

- Lower cost: benchmark local models before paying for cloud API usage.
- Better privacy: keep your code and prompts on your machine.
- Better fit: choose based on your real hardware, not generic leaderboard results.

## What The Benchmark Measures

- Average tokens per second.
- Average latency.
- Approximate quality using coding-oriented tests.
- Recommended winner for Claude Code.

> The script is dependency-free and uses only Python standard library.

## Requirements

- Python 3.10+
- Ollama installed
- One or more local models, or use --pull

## Quick Start

Start Ollama:

```bash
ollama serve
```

Run standard benchmark (Linux/macOS):

```bash
python eval_ollama_models.py --pull --num-ctx 8192 --output ./results/benchmark-standard.json --models qwen2.5-coder:3b qwen2.5-coder:7b deepseek-coder:6.7b
```

Shortcuts:

- Windows: `scripts/run-basic.ps1`
- Linux/macOS: `scripts/run-basic.sh`

## Recent Results (This PC)

### Standard benchmark (num_ctx=8192)

| Rank | Model | Score | Quality | Tokens/s | Latency (s) | Passed |
| ---- | ----- | ----- | ------- | -------- | ----------- | ------ |
| 1 | qwen2.5-coder:3b | 0.428 | 0.530 | 9.49 | 28.49 | 1/4 |
| 2 | qwen2.5-coder:7b | 0.406 | 0.573 | 3.86 | 53.15 | 1/4 |
| 3 | deepseek-coder:6.7b | 0.308 | 0.430 | 3.31 | 117.90 | 1/4 |

Standard winner on this machine: **qwen2.5-coder:3b**.

### Quality-focused benchmark (num_ctx=16384, includes 14b)

| Rank | Model | Score | Quality | Tokens/s | Latency (s) | Passed |
| ---- | ----- | ----- | ------- | -------- | ----------- | ------ |
| 1 | qwen2.5-coder:14b | 0.441 | 0.660 | 1.41 | 135.42 | 2/4 |
| 2 | qwen2.5-coder:3b | 0.379 | 0.480 | 7.65 | 41.13 | 1/4 |
| 3 | qwen2.5-coder:7b | 0.371 | 0.522 | 3.55 | 94.89 | 1/4 |
| 4 | deepseek-coder:6.7b | 0.307 | 0.430 | 3.16 | 141.75 | 1/4 |

Quality winner on this machine: **qwen2.5-coder:14b**.

Quick interpretation:

- If you prioritize speed and low latency, use qwen2.5-coder:3b.
- If you prioritize final quality for Claude Code, use qwen2.5-coder:14b.

## Basic Usage

Evaluate installed models:

```bash
python eval_ollama_models.py --models qwen2.5-coder:7b deepseek-coder:6.7b codellama:7b
```

Pull missing models and evaluate:

```bash
python eval_ollama_models.py --pull --models qwen2.5-coder:3b qwen2.5-coder:7b
```

Use larger context:

```bash
python eval_ollama_models.py --pull --num-ctx 16384 --models qwen2.5-coder:7b qwen2.5-coder:14b
```

Save output to custom file:

```bash
python eval_ollama_models.py --output results.json --models qwen2.5-coder:7b
```

## Hardware Recommendations

| Approx hardware | Models to try |
| --------------- | ------------- |
| CPU / 16 GB RAM | `qwen2.5-coder:3b`, `qwen2.5-coder:7b` |
| NVIDIA 8 GB VRAM | `qwen2.5-coder:7b`, `deepseek-coder:6.7b` |
| NVIDIA 12 GB VRAM | `qwen2.5-coder:7b`, `qwen2.5-coder:14b` |
| NVIDIA 16 GB VRAM | `qwen2.5-coder:14b` |
| NVIDIA 24 GB VRAM | `qwen2.5-coder:32b` |

## Mobile Execution Against Your PC

The model runs on your PC. Your phone only runs the script and calls Ollama over local network.

See [docs/mobile.md](docs/mobile.md).

## Use The Winning Model With Claude Code

Example command:

```bash
ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY="" ANTHROPIC_BASE_URL=http://localhost:11434 claude --model qwen2.5-coder:7b
```

## Publishing Checklist

1. Run standard benchmark and confirm [results/benchmark-standard.json](results/benchmark-standard.json) exists.
2. Add benchmark summary to README.
3. Confirm GitHub Actions Validate passes.
4. Open at least one roadmap issue.
5. Publish initial release v0.1.0 with JSON result link.

Ready-to-use publication assets:

- v0.1.0 release notes: [docs/release/v0.1.0-release-notes.md](docs/release/v0.1.0-release-notes.md)
- Roadmap 01 (global reach): [docs/release/roadmap-01-english-readme-and-global-distribution.md](docs/release/roadmap-01-english-readme-and-global-distribution.md)
- Roadmap 02 (benchmark expansion): [docs/release/roadmap-02-benchmark-suite-expansion.md](docs/release/roadmap-02-benchmark-suite-expansion.md)
- Roadmap 03 (dashboard and assets): [docs/release/roadmap-03-dashboard-and-sharing-assets.md](docs/release/roadmap-03-dashboard-and-sharing-assets.md)
- Roadmap 04 (CI guardrails): [docs/release/roadmap-04-ci-and-quality-guardrails.md](docs/release/roadmap-04-ci-and-quality-guardrails.md)
- Social launch pack: [docs/release/launch-pack.md](docs/release/launch-pack.md)
- Automated release checklist: [scripts/release-check.sh](scripts/release-check.sh)
- v0.1.0 publication runbook: [docs/release/publish-v0.1.0.md](docs/release/publish-v0.1.0.md)
