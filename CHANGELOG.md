# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

_v0.1.0 can be promoted from pre-release to stable once metadata, roadmap issues and dashboard screenshot are ready._

## [0.1.0] - 2026-05-19

### Added

- Initial benchmark script (`eval_ollama_models.py`) for local Ollama models
- Quality, latency and tokens/sec scoring with weighted composite score
- Claude Code command recommendation printed after benchmark run
- JSON results export (`--output` flag)
- PC and mobile execution support (Android Termux → local PC Ollama)
- Bash helper script (`scripts/run-basic.sh`) for Linux/macOS
- PowerShell helper script (`scripts/run-basic.ps1`) for Windows
- DevContainer support (`.devcontainer/devcontainer.json`) for Python-ready environment
- Interactive result dashboard (`dashboard.html`)
- Hardware-oriented model recommendations table in README
- GitHub Actions validation workflow
- Standard benchmark JSON output (`results/benchmark-standard.json`)
- Extended context benchmark JSON output (`results/benchmark-ctx16384-plus14b.json`)
- System report helper (`system_report.py`)
- Benchmark JSON validator (`scripts/validate-benchmark-json.py`)
- Markdown link validator (`scripts/validate-markdown-links.py`)
- Pre-release checklist script (`scripts/release-check.sh`)

[Unreleased]: https://github.com/davidop/ollama-claude-code-model-evaluator/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/davidop/ollama-claude-code-model-evaluator/releases/tag/v0.1.0
