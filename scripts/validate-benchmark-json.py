#!/usr/bin/env python3
"""Validate benchmark JSON output structure and value ranges."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_KEYS = {
    "model": str,
    "avg_tokens_per_sec": (int, float),
    "avg_latency_sec": (int, float),
    "quality_score": (int, float),
    "final_score": (int, float),
    "passed_tests": int,
    "total_tests": int,
}


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def validate_entry(entry: object, path: Path, index: int) -> None:
    if not isinstance(entry, dict):
        fail(f"{path}: item {index} is not an object")

    for key, expected_type in REQUIRED_KEYS.items():
        if key not in entry:
            fail(f"{path}: item {index} missing key '{key}'")
        if not isinstance(entry[key], expected_type):
            fail(f"{path}: item {index} key '{key}' has invalid type")

    if not 0 <= float(entry["quality_score"]) <= 1:
        fail(f"{path}: item {index} quality_score out of range [0,1]")
    if not 0 <= float(entry["final_score"]) <= 1:
        fail(f"{path}: item {index} final_score out of range [0,1]")
    if float(entry["avg_tokens_per_sec"]) < 0:
        fail(f"{path}: item {index} avg_tokens_per_sec cannot be negative")
    if float(entry["avg_latency_sec"]) < 0:
        fail(f"{path}: item {index} avg_latency_sec cannot be negative")

    passed = int(entry["passed_tests"])
    total = int(entry["total_tests"])
    if total <= 0:
        fail(f"{path}: item {index} total_tests must be > 0")
    if passed < 0 or passed > total:
        fail(f"{path}: item {index} passed_tests must be between 0 and total_tests")


def validate_file(path: Path) -> None:
    if not path.exists():
        fail(f"Missing file: {path}")

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path}: invalid JSON ({exc})")

    if not isinstance(payload, list) or not payload:
        fail(f"{path}: expected non-empty JSON array")

    for i, entry in enumerate(payload, start=1):
        validate_entry(entry, path, i)

    # Verify descending ranking by final_score for publication consistency.
    scores = [float(item["final_score"]) for item in payload]
    if scores != sorted(scores, reverse=True):
        fail(f"{path}: entries are not sorted by final_score desc")

    print(f"OK: {path}")


def main() -> int:
    required_targets = [
        Path("results/benchmark-standard.json"),
    ]

    optional_targets = [
        Path("results/benchmark-ctx16384-plus14b.json"),
    ]

    for target in required_targets:
        validate_file(target)

    for target in optional_targets:
        if target.exists():
            validate_file(target)
        else:
            print(f"SKIP: optional file not found: {target}")

    print("Benchmark JSON validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
