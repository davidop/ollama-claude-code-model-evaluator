#!/usr/bin/env python3
"""Validate local Markdown links in README files."""

from __future__ import annotations

import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
ROOT_DIR = Path(__file__).resolve().parent.parent


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def is_external(target: str) -> bool:
    return target.startswith("http://") or target.startswith("https://") or target.startswith("mailto:")


def validate_markdown(path: Path) -> None:
    if not path.exists():
        fail(f"Missing file: {path}")

    content = path.read_text(encoding="utf-8")
    bad_links: list[str] = []

    for raw_target in LINK_RE.findall(content):
        target = raw_target.strip()
        if not target or is_external(target):
            continue

        # Strip anchor and query for local file existence checks.
        local_target = target.split("#", 1)[0].split("?", 1)[0]
        if not local_target:
            continue

        resolved_from_file = (path.parent / local_target).resolve()
        resolved_from_root = (ROOT_DIR / local_target).resolve()
        if not resolved_from_file.exists() and not resolved_from_root.exists():
            bad_links.append(target)

    if bad_links:
        fail(f"{path}: broken local links: {', '.join(sorted(set(bad_links)))}")

    print(f"OK: {path}")


def main() -> int:
    targets = [
        Path("README.md"),
        Path("README.en.md"),
        Path("CONTRIBUTING.md"),
    ]

    docs_dir = Path("docs")
    if docs_dir.exists():
        targets.extend(sorted(docs_dir.rglob("*.md")))

    for target in targets:
        validate_markdown(target)

    print("Markdown link validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
