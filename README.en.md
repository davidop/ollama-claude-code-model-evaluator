# Ollama Claude Code Model Evaluator

[![Validate](https://github.com/davidop/ollama-claude-code-model-evaluator/actions/workflows/validate.yml/badge.svg)](https://github.com/davidop/ollama-claude-code-model-evaluator/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/runtime-Ollama-black.svg)](https://ollama.com/)
[![Claude Code](https://img.shields.io/badge/works%20with-Claude%20Code-blueviolet.svg)](https://docs.anthropic.com/en/docs/claude-code)

English README. For Spanish, see [README.md](README.md).

**Benchmark your local Ollama models and find the best one for coding tasks and Claude Code — in minutes, on your own hardware.**

> If this project helps you choose the right local model for your machine, consider giving it a ⭐ star and sharing your benchmark results.
>
> You can share yours using the [Benchmark result](.github/ISSUE_TEMPLATE/benchmark_result.md) issue template.

Quick links:

- Interactive dashboard: [dashboard.html](dashboard.html)
- Standard benchmark JSON: [results/benchmark-standard.json](results/benchmark-standard.json)
- 16384 context + 14b benchmark JSON: [results/benchmark-ctx16384-plus14b.json](results/benchmark-ctx16384-plus14b.json)
- Changelog: [CHANGELOG.md](CHANGELOG.md)

## Dashboard preview

![Dashboard preview](docs/assets/dashboard-preview.svg)

## Who is this for?

- **Developers using local LLMs** who want to know which model is fastest and most accurate for coding tasks on their specific hardware.
- **People testing Claude Code with local models** who need a reproducible way to pick the right model without trial-and-error.
- **Teams comparing model performance across machines** — share your JSON results and let others reproduce them.
- **AI engineers benchmarking coding models** who want a lightweight, dependency-free CLI tool they can run anywhere.

## Why This Matters

- **Lower cost:** benchmark local models before paying for cloud API usage.
- **Better privacy:** keep your code and prompts on your machine.
- **Better fit:** choose based on your real hardware, not generic leaderboard results.

The benchmark measures:

- Average tokens per second.
- Average latency.
- Approximate quality using coding-oriented tests.
- Recommended winner model for use with Claude Code.

> The script is dependency-free and uses only the Python standard library.

## Quick Start

> **Requirements:** Python 3.10+, [Ollama](https://ollama.com/) installed.

**1. Start Ollama:**

```bash
ollama serve
```

**2. Run the benchmark (Linux/macOS):**

```bash
python eval_ollama_models.py --pull --num-ctx 8192 \
  --output ./results/benchmark-standard.json \
  --models qwen2.5-coder:3b qwen2.5-coder:7b deepseek-coder:6.7b
```

**3. Use the winning model with Claude Code:**

The script prints the ready-to-use command at the end:

```bash
ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY="" ANTHROPIC_BASE_URL=http://localhost:11434 claude --model qwen2.5-coder:3b
```

Script shortcuts:

- Windows: `scripts/run-basic.ps1`
- Linux/macOS: `scripts/run-basic.sh`

## Example Output

After the benchmark completes, you get a ranked table like this:

```
Rank  Model                  Score   Quality  Tokens/s  Latency(s)  Passed
1     qwen2.5-coder:3b       0.428   0.530    9.49      28.49       1/4
2     qwen2.5-coder:7b       0.406   0.573    3.86      53.15       1/4
3     deepseek-coder:6.7b    0.308   0.430    3.31      117.90      1/4

Winner: qwen2.5-coder:3b

To use with Claude Code:
  ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY="" ANTHROPIC_BASE_URL=http://localhost:11434 claude --model qwen2.5-coder:3b
```

Full results are also saved to JSON for sharing and reproducibility.

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

- If you prioritize speed and low latency: use `qwen2.5-coder:3b`.
- If you prioritize final quality for Claude Code: use `qwen2.5-coder:14b`.

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

## DevContainer

This repo includes `/.devcontainer/devcontainer.json` to open it with Python ready inside a container — useful if you have Python issues on Windows.

1. Install Docker Desktop and the `Dev Containers` extension in VS Code.
2. With Ollama running on your host (`ollama serve`), open: `Dev Containers: Reopen in Container`.
3. Run the benchmark normally inside the container.

The DevContainer uses `OLLAMA_BASE_URL=http://host.docker.internal:11434` to connect to Ollama on the host machine.

## Mobile Execution Against Your PC

The model runs on your PC. Your phone only runs the script and calls Ollama over the local network.

See [docs/mobile.md](docs/mobile.md).

## Use The Winning Model With Claude Code

The script prints the ready-to-run command. Example:

```bash
ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY="" ANTHROPIC_BASE_URL=http://localhost:11434 claude --model qwen2.5-coder:7b
```

Windows PowerShell:

```powershell
$env:ANTHROPIC_AUTH_TOKEN="ollama"
$env:ANTHROPIC_API_KEY=""
$env:ANTHROPIC_BASE_URL="http://localhost:11434"
claude --model qwen2.5-coder:7b
```

## About the Score

The score is not meant to replace an academic benchmark. It helps with a practical decision: which local model is most useful for coding tasks on your own machine.

Current formula:

- 65% approximate quality (keyword-based coding tests)
- 35% speed, normalized against 40 tokens/s

You can modify the tests in the `TESTS` constant in `eval_ollama_models.py`.

## Release Checklist (v0.1.0)

Steps to publish the first release:

1. Run standard benchmark and confirm [results/benchmark-standard.json](results/benchmark-standard.json) exists.
2. Update the "Recent Results" table in both README files.
3. Run `bash scripts/release-check.sh` and confirm all checks pass.
4. Confirm GitHub Actions `Validate` workflow passes.
5. Update [CHANGELOG.md](CHANGELOG.md): move `[Unreleased]` items under `[0.1.0]` with today's date.
6. Create a git tag `v0.1.0` and push it.
7. Create a GitHub Release from that tag, using [docs/release/v0.1.0-release-notes.md](docs/release/v0.1.0-release-notes.md) as the body.
8. Attach `results/benchmark-standard.json` and `results/benchmark-ctx16384-plus14b.json` to the release.
9. Open at least one roadmap issue to show project direction.

Ready-to-use publication assets:

- v0.1.0 release notes: [docs/release/v0.1.0-release-notes.md](docs/release/v0.1.0-release-notes.md)
- Social launch pack: [docs/release/launch-pack.md](docs/release/launch-pack.md)
- Automated release checklist: [scripts/release-check.sh](scripts/release-check.sh)

## Public launch checklist

Once the technical release is published:

- [ ] Configure the GitHub repository description (About → Description).
- [ ] Configure the GitHub repository homepage (About → Website).
- [ ] Add the recommended GitHub topics (About → Topics).
- [ ] Convert `v0.1.0` from pre-release to stable release when ready.
- [ ] Open at least one roadmap issue to show project direction.
- [ ] Add a dashboard screenshot to the README.
- [ ] Publish a LinkedIn post with a clear feedback and star request.

> v0.1.0 can be promoted from pre-release to stable once metadata, roadmap issues and dashboard screenshot are ready.

## Roadmap

- [ ] LM Studio / OpenAI-compatible provider support
- [ ] vLLM provider support
- [ ] Richer benchmark tasks (.NET, Azure, Python, frontend)
- [ ] Hardware-aware model recommendations
- [ ] Benchmark dashboard improvements (filtering, export)
- [ ] GitHub Actions validation for benchmark results
- [ ] Hardware profile export

See also the detailed roadmap docs in [docs/release/](docs/release/).

### Suggested initial roadmap issues

Issues recommended to open as initial roadmap tasks:

- **Add LM Studio / OpenAI-compatible provider support** — extend the evaluator beyond Ollama to any OpenAI-compatible provider.
- **Add vLLM provider support** — high-performance inference support for larger models.
- **Improve benchmark scoring beyond keyword matching** — more accurate quality metrics beyond the current keyword detection.
- **Add hardware-aware model recommendations** — auto-suggest models based on detected GPU and RAM.

## Contributing

Contributions are welcome — new benchmark tests, hardware results, bug reports, new provider support.

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Proposing new models
- Adding benchmark tests
- Sharing your hardware results
- Opening bug reports or feature requests

Ideas for good first issues:

- Add OpenAI-compatible provider support
- Add LM Studio support
- Add vLLM support
- Add GitHub Actions for linting
- Add richer benchmark tasks for .NET, Azure, Python and frontend code
- Add hardware profile export

## GitHub Repository Metadata

The following values should be configured manually in the GitHub repository settings (they are not part of the source code):

**Description:**
> Benchmark local Ollama models for coding tasks and Claude Code. Compare quality, speed and latency on your own hardware.

**Website / homepage:**
> https://github.com/davidop/ollama-claude-code-model-evaluator

**Topics:**
`ollama` `claude-code` `local-ai` `llm` `benchmark` `coding-assistant` `qwen` `deepseek` `python` `developer-tools`

To set these, go to your repository on GitHub → click the ⚙️ gear icon next to "About" on the right sidebar.
