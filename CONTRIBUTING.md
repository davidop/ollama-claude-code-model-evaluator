# Contributing

Thank you for contributing to Ollama Claude Code Model Evaluator!

Contributions of all kinds are welcome: new benchmark tests, hardware results, bug reports, documentation improvements, and new provider support.

For the Spanish README and contribution guidelines see [README.md](README.md).

## Local requirements

- Python 3.10+
- Ollama installed and running locally

## Recommended workflow

1. Fork the repo and create a branch from `main`.
2. Run a minimal local validation:
   ```bash
   python -m py_compile eval_ollama_models.py
   python eval_ollama_models.py --help
   ```
3. If your change touches the benchmark, run at least one short evaluation:
   ```bash
   python eval_ollama_models.py --models qwen2.5-coder:3b
   ```
4. Open a PR with a clear description of the problem and expected result.

## Proposing a new model

Open an issue using the **Model request** template and include:

- Model name and size (e.g. `mistral:7b`)
- Why it is a good candidate for coding tasks
- Your hardware (CPU, GPU, RAM) so others can judge feasibility
- Any benchmark numbers you already have

If you want to run the benchmark yourself, add the model to your Ollama instance and run:

```bash
python eval_ollama_models.py --pull --models <your-model>
```

Then share the JSON output from `results/` in the issue or PR.

## Adding a new benchmark test

1. Edit the `TESTS` constant in `eval_ollama_models.py`.
2. Add an entry with:
   - a unique `name`
   - a focused `prompt` (short and deterministic for reproducibility)
   - a list of `keywords` that a correct answer should contain
3. Keep prompts short and deterministic to make cross-machine comparison meaningful.
4. Run the full benchmark locally and confirm the new test produces sensible results.

## Sharing your hardware results

Hardware results are valuable for the community. To share yours:

1. Run the standard benchmark:
   ```bash
   python eval_ollama_models.py --pull --num-ctx 8192 --output ./results/benchmark-standard.json --models qwen2.5-coder:3b qwen2.5-coder:7b deepseek-coder:6.7b
   ```
2. Run `python system_report.py` to capture your hardware profile.
3. Open a **Benchmark result** issue (or PR) with both outputs attached.

## Opening a bug or improvement issue

Use the appropriate issue template:

- **Bug report** — benchmark errors, crashes, incorrect output
- **Model request** — propose a new model to evaluate
- **Benchmark result** — share your hardware results with the community
- **Feature request** — propose new benchmark tasks, provider support, or DX improvements

Ideas for good first issues:

- Add OpenAI-compatible provider support
- Add LM Studio support
- Add vLLM support
- Add GitHub Actions for linting
- Add richer benchmark tasks for .NET, Azure, Python and frontend code
- Add hardware profile export

## Conventions

- Keep Python stdlib compatibility — no external dependencies.
- Avoid unrelated changes in the same PR.
- Document any new CLI flag in both README files (`README.md` and `README.en.md`).
- Update `CHANGELOG.md` with your changes under `[Unreleased]`.

## Code of conduct

Be respectful and constructive. This is a welcoming project for developers of all skill levels.
