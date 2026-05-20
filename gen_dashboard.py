#!/usr/bin/env python3
"""Generate dashboard data JS from benchmark outputs and machine hardware."""

from __future__ import annotations

import argparse
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from hwdetect import get_hardware_profile


def _load_json(path: Path, required: bool) -> list[dict[str, Any]]:
    if not path.exists():
        if required:
            raise FileNotFoundError(f"Missing required file: {path}")
        return []

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"Expected JSON array in {path}")
    return payload


def _save_history(path: Path, history_dir: Path, stamp: str) -> None:
    if not path.exists():
        return

    history_dir.mkdir(parents=True, exist_ok=True)
    target = history_dir / f"{path.stem}-{stamp}{path.suffix}"
    shutil.copy2(path, target)


def _load_latest_history(history_dir: Path, stem: str) -> tuple[list[dict[str, Any]], str]:
    if not history_dir.exists():
        return [], ""

    candidates = sorted(history_dir.glob(f"{stem}-*.json"))
    if not candidates:
        return [], ""

    latest = candidates[-1]
    payload = _load_json(latest, required=False)
    return payload, latest.name


def _extract_snapshot_label(snapshot_name: str) -> str:
    # Expected: benchmark-standard-YYYYmmdd-HHMMSS.json
    name = snapshot_name.removesuffix(".json")
    parts = name.rsplit("-", 2)
    if len(parts) < 3:
        return snapshot_name

    date_raw = parts[-2]
    time_raw = parts[-1]
    if len(date_raw) == 8 and len(time_raw) == 6:
        return (
            f"{date_raw[0:4]}-{date_raw[4:6]}-{date_raw[6:8]} "
            f"{time_raw[0:2]}:{time_raw[2:4]}:{time_raw[4:6]}"
        )
    return snapshot_name


def _load_recent_history(history_dir: Path, stem: str, limit: int) -> list[dict[str, Any]]:
    if not history_dir.exists():
        return []

    candidates = sorted(history_dir.glob(f"{stem}-*.json"))
    if not candidates:
        return []

    selected = candidates[-limit:]
    runs: list[dict[str, Any]] = []
    for snapshot in selected:
        data = _load_json(snapshot, required=False)
        if not data:
            continue
        runs.append(
            {
                "label": _extract_snapshot_label(snapshot.name),
                "snapshot": snapshot.name,
                "results": data,
            }
        )
    return runs


def generate_dashboard_data(
    standard_path: Path,
    ctx_path: Path,
    output_path: Path,
    history_dir: Path,
    ollama_base_url: str,
    history_limit: int,
) -> None:
    standard = _load_json(standard_path, required=True)
    ctx = _load_json(ctx_path, required=False)
    hardware = get_hardware_profile()
    previous_standard, previous_standard_snapshot = _load_latest_history(history_dir, standard_path.stem)
    history_runs = _load_recent_history(history_dir, standard_path.stem, max(1, history_limit))

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "benchmarkStandard": standard,
        "benchmarkCtx": ctx,
        "previousBenchmarkStandard": previous_standard,
        "previousStandardSnapshot": previous_standard_snapshot,
        "historyStandardRuns": history_runs
        + [{"label": generated_at, "snapshot": "current", "results": standard}],
        "hardwareProfile": hardware,
        "generatedAt": generated_at,
        "ollamaBaseUrl": ollama_base_url.rstrip("/"),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    js = (
        "window.benchmarkStandard = "
        + json.dumps(payload["benchmarkStandard"], ensure_ascii=True)
        + ";\n"
        + "window.benchmarkCtx = "
        + json.dumps(payload["benchmarkCtx"], ensure_ascii=True)
        + ";\n"
        + "window.previousBenchmarkStandard = "
        + json.dumps(payload["previousBenchmarkStandard"], ensure_ascii=True)
        + ";\n"
        + "window.previousStandardSnapshot = "
        + json.dumps(payload["previousStandardSnapshot"], ensure_ascii=True)
        + ";\n"
        + "window.historyStandardRuns = "
        + json.dumps(payload["historyStandardRuns"], ensure_ascii=True)
        + ";\n"
        + "window.hardwareProfile = "
        + json.dumps(payload["hardwareProfile"], ensure_ascii=True)
        + ";\n"
        + "window.generatedAt = "
        + json.dumps(payload["generatedAt"], ensure_ascii=True)
        + ";\n"
        + "window.ollamaBaseUrl = "
        + json.dumps(payload["ollamaBaseUrl"], ensure_ascii=True)
        + ";\n"
    )

    output_path.write_text(js, encoding="utf-8")

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    _save_history(standard_path, history_dir, stamp)
    _save_history(ctx_path, history_dir, stamp)

    print(f"Generated: {output_path}")
    print(f"History directory: {history_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate dashboard data for dashboard.html")
    parser.add_argument(
        "--standard",
        default="results/benchmark-standard.json",
        help="Path to standard benchmark JSON",
    )
    parser.add_argument(
        "--ctx",
        default="results/benchmark-ctx16384-plus14b.json",
        help="Path to 16k benchmark JSON (optional)",
    )
    parser.add_argument(
        "--output",
        default="results/dashboard-data.js",
        help="Output path for generated dashboard data JavaScript",
    )
    parser.add_argument(
        "--history-dir",
        default="results/history",
        help="Directory to store timestamped snapshots",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
        help="Base URL used in Claude Code command examples",
    )
    parser.add_argument(
        "--history-limit",
        type=int,
        default=8,
        help="How many previous standard snapshots to include in trend view",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    generate_dashboard_data(
        standard_path=Path(args.standard),
        ctx_path=Path(args.ctx),
        output_path=Path(args.output),
        history_dir=Path(args.history_dir),
        ollama_base_url=args.base_url,
        history_limit=args.history_limit,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
