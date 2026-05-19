#!/usr/bin/env python3
"""
Evaluate local Ollama models for coding workloads and Claude Code usage.

The benchmark is intentionally dependency-free. It uses only Python's standard
library so it can run on Windows, macOS, Linux and Android Termux.
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from typing import Any


DEFAULT_MODELS = [
    "qwen2.5-coder:3b",
    "qwen2.5-coder:7b",
    "qwen2.5-coder:14b",
    "deepseek-coder:6.7b",
    "codellama:7b",
    "llama3.1:8b",
]


TESTS = [
    {
        "name": "csharp_refactor",
        "prompt": """You are a senior .NET architect.
Refactor this C# method to be safer, clearer and more testable.
Return only the improved code.

public async Task<string> GetUserName(string id)
{
    var client = new HttpClient();
    var r = await client.GetAsync("https://api.contoso.com/users/" + id);
    var s = await r.Content.ReadAsStringAsync();
    dynamic d = Newtonsoft.Json.JsonConvert.DeserializeObject(s);
    return d.name;
}
""",
        "keywords": [
            "HttpClient",
            "CancellationToken",
            "EnsureSuccessStatusCode",
            "JsonSerializer",
            "ArgumentException",
        ],
    },
    {
        "name": "bicep_azure",
        "prompt": """Create a minimal Azure Bicep file for:
- Azure Storage Account
- secure defaults
- HTTPS only
- TLS 1.2 minimum
- no public blob access
Return only Bicep code.
""",
        "keywords": [
            "Microsoft.Storage/storageAccounts",
            "supportsHttpsTrafficOnly",
            "minimumTlsVersion",
            "allowBlobPublicAccess",
            "kind",
        ],
    },
    {
        "name": "terraform_azure",
        "prompt": """Create a minimal Terraform configuration for Azure:
- resource group
- storage account
- secure defaults
Return only Terraform code.
""",
        "keywords": [
            "azurerm_resource_group",
            "azurerm_storage_account",
            "min_tls_version",
            "allow_nested_items_to_be_public",
            "https_traffic_only_enabled",
        ],
    },
    {
        "name": "reasoning_code_review",
        "prompt": """Review this Python function. Identify the main bug and return a corrected version only.

def average(values):
    total = 0
    for i in range(len(values) + 1):
        total += values[i]
    return total / len(values)
""",
        "keywords": [
            "if not values",
            "ZeroDivisionError",
            "sum",
            "len",
            "ValueError",
        ],
    },
]


@dataclass(frozen=True)
class Result:
    model: str
    avg_tokens_per_sec: float
    avg_latency_sec: float
    quality_score: float
    final_score: float
    passed_tests: int
    total_tests: int


def post_json(base_url: str, path: str, payload: dict[str, Any], timeout: int = 600) -> dict[str, Any]:
    url = base_url.rstrip("/") + path
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read().decode("utf-8", errors="replace")
        return json.loads(raw)


def get_json(base_url: str, path: str, timeout: int = 30) -> dict[str, Any]:
    url = base_url.rstrip("/") + path
    with urllib.request.urlopen(url, timeout=timeout) as response:
        raw = response.read().decode("utf-8", errors="replace")
        return json.loads(raw)


def list_local_models(base_url: str) -> list[str]:
    data = get_json(base_url, "/api/tags")
    return [m["name"] for m in data.get("models", [])]


def pull_model(base_url: str, model: str) -> bool:
    print(f"Pulling {model}...")
    try:
        post_json(base_url, "/api/pull", {"name": model, "stream": False}, timeout=3600)
        return True
    except Exception as ex:  # noqa: BLE001 - CLI tool should print operational errors
        print(f"  Cannot pull {model}: {ex}")
        return False


def keyword_quality(response: str, keywords: list[str]) -> float:
    if not response:
        return 0.0

    text = response.lower()
    hits = sum(1 for kw in keywords if kw.lower() in text)
    keyword_score = hits / max(len(keywords), 1)

    code_bonus = 0.0
    if "```" in response:
        code_bonus += 0.03
    if len(response) > 200:
        code_bonus += 0.05
    if any(bad in text for bad in ["i cannot", "i can't", "as an ai"]):
        code_bonus -= 0.2

    return max(0.0, min(1.0, keyword_score + code_bonus))


def evaluate_model(base_url: str, model: str, num_ctx: int, temperature: float) -> Result | None:
    latencies: list[float] = []
    token_speeds: list[float] = []
    qualities: list[float] = []
    passed = 0

    print(f"\nEvaluating {model}")

    for test in TESTS:
        print(f"  Test: {test['name']}")
        payload = {
            "model": model,
            "prompt": test["prompt"],
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_ctx": num_ctx,
            },
        }

        start = time.perf_counter()
        try:
            data = post_json(base_url, "/api/generate", payload)
        except urllib.error.HTTPError as ex:
            print(f"    HTTP error: {ex}")
            return None
        except Exception as ex:  # noqa: BLE001
            print(f"    Error: {ex}")
            return None

        elapsed = time.perf_counter() - start
        response = data.get("response", "")
        eval_count = data.get("eval_count", 0)
        eval_duration_ns = data.get("eval_duration", 0)

        if eval_duration_ns and eval_count:
            tokens_per_sec = eval_count / (eval_duration_ns / 1_000_000_000)
        else:
            tokens_per_sec = eval_count / elapsed if elapsed > 0 else 0.0

        quality = keyword_quality(response, test["keywords"])
        if quality >= 0.55:
            passed += 1

        latencies.append(elapsed)
        token_speeds.append(tokens_per_sec)
        qualities.append(quality)

        print(
            f"    tokens/sec={tokens_per_sec:.2f}, "
            f"latency={elapsed:.2f}s, "
            f"quality={quality:.2f}"
        )

    avg_tps = statistics.mean(token_speeds) if token_speeds else 0.0
    avg_latency = statistics.mean(latencies) if latencies else 0.0
    avg_quality = statistics.mean(qualities) if qualities else 0.0

    speed_score = min(avg_tps / 40.0, 1.0)
    final_score = (avg_quality * 0.65) + (speed_score * 0.35)

    return Result(
        model=model,
        avg_tokens_per_sec=avg_tps,
        avg_latency_sec=avg_latency,
        quality_score=avg_quality,
        final_score=final_score,
        passed_tests=passed,
        total_tests=len(TESTS),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate local Ollama models for coding and Claude Code usage."
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
        help="Ollama base URL. Default: http://localhost:11434",
    )
    parser.add_argument("--models", nargs="*", default=DEFAULT_MODELS, help="Models to evaluate.")
    parser.add_argument("--pull", action="store_true", help="Pull missing models before evaluating.")
    parser.add_argument("--num-ctx", type=int, default=8192, help="Context size. Default: 8192")
    parser.add_argument("--temperature", type=float, default=0.1, help="Temperature. Default: 0.1")
    parser.add_argument(
        "--output",
        default="ollama_model_eval_results.json",
        help="JSON output file. Default: ollama_model_eval_results.json",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_url = args.base_url.rstrip("/")

    print(f"Ollama endpoint: {base_url}")
    print(f"Context size: {args.num_ctx}")
    print(f"Models requested: {', '.join(args.models)}")

    try:
        local_models = list_local_models(base_url)
    except Exception as ex:  # noqa: BLE001
        print(f"Cannot connect to Ollama at {base_url}: {ex}")
        return 1

    print(f"Local models found: {', '.join(local_models) if local_models else 'none'}")

    available_models: list[str] = []
    for model in args.models:
        if model in local_models:
            available_models.append(model)
            continue
        if args.pull and pull_model(base_url, model):
            available_models.append(model)
        elif not args.pull:
            print(f"Skipping {model}: not installed. Use --pull to download it.")

    if not available_models:
        print("No models available to evaluate.")
        return 1

    results = [r for model in available_models if (r := evaluate_model(base_url, model, args.num_ctx, args.temperature))]

    if not results:
        print("No model completed the evaluation.")
        return 1

    results.sort(key=lambda r: r.final_score, reverse=True)
    winner = results[0]

    print("\n==============================")
    print("RESULTS")
    print("==============================")
    for idx, r in enumerate(results, start=1):
        print(
            f"{idx}. {r.model} | "
            f"score={r.final_score:.3f} | "
            f"quality={r.quality_score:.3f} | "
            f"tokens/sec={r.avg_tokens_per_sec:.2f} | "
            f"latency={r.avg_latency_sec:.2f}s | "
            f"passed={r.passed_tests}/{r.total_tests}"
        )

    print("\n==============================")
    print("BEST MODEL")
    print("==============================")
    print(winner.model)

    print("\nClaude Code command:")
    print(
        f'ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY="" '
        f"ANTHROPIC_BASE_URL={base_url} claude --model {winner.model}"
    )

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump([asdict(r) for r in results], f, indent=2)

    print(f"\nSaved results to: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
