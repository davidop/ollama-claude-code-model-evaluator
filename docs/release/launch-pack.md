# Launch Pack

Use these templates to announce the project with consistent messaging and reproducible claims.

## Core Message

Find the best local Ollama coding model for your own hardware in minutes, then run it directly with Claude Code.

## Post Template - X

I built a local benchmark to pick the best Ollama model for coding on real hardware.

- No Python dependencies (stdlib only)
- Reproducible JSON outputs
- Claude Code-ready winner command

Results + dashboard:
- https://github.com/davidop/ollama-claude-code-model-evaluator

## Post Template - Reddit

Title: Benchmarking local Ollama coding models for Claude Code (reproducible, no deps)

Body:
I made a small benchmark tool to compare local Ollama coding models on your own machine. It scores quality and speed, exports JSON, and recommends a winner command for Claude Code.

What it includes:
- standard benchmark script
- dashboard for visual comparison
- hardware-oriented recommendations
- mobile execution from Termux to local Ollama

Repo:
https://github.com/davidop/ollama-claude-code-model-evaluator

## Post Template - Hacker News

Title:
Show HN: Ollama Claude Code Model Evaluator

Body:
I built a small dependency-free benchmark to choose the best local Ollama model for coding tasks and Claude Code. It measures quality and speed, exports reproducible JSON results, and includes a dashboard.

Repo:
https://github.com/davidop/ollama-claude-code-model-evaluator

## Short Benchmark Snapshot Block

Standard benchmark on this machine:
- qwen2.5-coder:3b, score 0.428, 9.49 tok/s, 28.49s latency
- qwen2.5-coder:7b, score 0.406, 3.86 tok/s, 53.15s latency
- deepseek-coder:6.7b, score 0.308, 3.31 tok/s, 117.90s latency

Quality-focused benchmark (16384 + 14b):
- qwen2.5-coder:14b, score 0.441, quality 0.660

## Hashtags

#ollama #localai #llm #claudecode #opensource
