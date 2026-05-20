#!/usr/bin/env python3
"""Cross-platform hardware detection helpers for dashboard generation."""

from __future__ import annotations

import json
import os
import platform
import re
import shutil
import subprocess
from typing import Any


def _run(cmd: list[str]) -> str:
    try:
        completed = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
        )
        return completed.stdout.strip()
    except Exception:
        return ""


def _linux_cpu() -> tuple[str, int, int]:
    model = "Unknown CPU"
    cores = os.cpu_count() or 0
    threads_per_core = 1

    out = _run(["lscpu"])
    if not out:
        return model, cores, threads_per_core

    for line in out.splitlines():
        if line.startswith("Model name:"):
            model = line.split(":", 1)[1].strip()
        elif line.startswith("CPU(s):") and "NUMA" not in line:
            value = line.split(":", 1)[1].strip()
            if value.isdigit():
                cores = int(value)
        elif line.startswith("Thread(s) per core:"):
            value = line.split(":", 1)[1].strip()
            if value.isdigit():
                threads_per_core = int(value)

    return model, cores, threads_per_core


def _mac_cpu() -> tuple[str, int, int]:
    model = _run(["sysctl", "-n", "machdep.cpu.brand_string"]) or "Unknown CPU"
    logical = _run(["sysctl", "-n", "hw.logicalcpu"]) or "0"
    physical = _run(["sysctl", "-n", "hw.physicalcpu"]) or "0"

    try:
        logical_cpu = int(logical)
    except ValueError:
        logical_cpu = os.cpu_count() or 0

    try:
        physical_cpu = int(physical)
    except ValueError:
        physical_cpu = 0

    threads_per_core = max(1, logical_cpu // physical_cpu) if physical_cpu else 1
    return model, logical_cpu, threads_per_core


def _windows_cpu() -> tuple[str, int, int]:
    model = platform.processor() or "Unknown CPU"
    logical = os.cpu_count() or 0
    threads_per_core = 1

    out = _run([
        "powershell",
        "-NoProfile",
        "-Command",
        "Get-CimInstance Win32_Processor | Select-Object -First 1 Name,NumberOfCores,NumberOfLogicalProcessors | ConvertTo-Json -Compress",
    ])
    if out:
        try:
            payload = json.loads(out)
            model = payload.get("Name") or model
            logical = int(payload.get("NumberOfLogicalProcessors") or logical)
            cores = int(payload.get("NumberOfCores") or 0)
            if cores > 0:
                threads_per_core = max(1, logical // cores)
        except Exception:
            pass

    return model, logical, threads_per_core


def _detect_cpu() -> dict[str, Any]:
    system = platform.system().lower()
    if system == "linux":
        model, cores, tpc = _linux_cpu()
    elif system == "darwin":
        model, cores, tpc = _mac_cpu()
    elif system == "windows":
        model, cores, tpc = _windows_cpu()
    else:
        model, cores, tpc = "Unknown CPU", os.cpu_count() or 0, 1

    return {
        "model": model,
        "cores": int(cores),
        "threads_per_core": int(tpc),
    }


def _detect_ram_gb() -> int:
    system = platform.system().lower()

    if system == "linux":
        out = _run(["cat", "/proc/meminfo"])
        match = re.search(r"MemTotal:\s+(\d+)\s+kB", out)
        if match:
            kb = int(match.group(1))
            return max(1, round(kb / 1024 / 1024))

    if system == "darwin":
        out = _run(["sysctl", "-n", "hw.memsize"])
        if out.isdigit():
            bytes_total = int(out)
            return max(1, round(bytes_total / 1024 / 1024 / 1024))

    if system == "windows":
        out = _run([
            "powershell",
            "-NoProfile",
            "-Command",
            "(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory",
        ])
        out = out.strip()
        if out.isdigit():
            bytes_total = int(out)
            return max(1, round(bytes_total / 1024 / 1024 / 1024))

    return 0


def _detect_gpu() -> str:
    nvidia = shutil.which("nvidia-smi")
    if nvidia:
        out = _run([nvidia, "--query-gpu=name,memory.total", "--format=csv,noheader"])
        if out:
            first = out.splitlines()[0].strip()
            return first

    system = platform.system().lower()
    if system == "darwin":
        out = _run(["system_profiler", "SPDisplaysDataType"])
        for line in out.splitlines():
            if "Chipset Model:" in line:
                return line.split(":", 1)[1].strip()

    if system == "linux":
        out = _run(["lspci"])
        for line in out.splitlines():
            if "VGA" in line or "3D controller" in line:
                return line.split(":", 2)[-1].strip()

    return "No detectada"


def get_hardware_profile() -> dict[str, Any]:
    cpu = _detect_cpu()
    return {
        "cpu": cpu["model"],
        "cores": cpu["cores"],
        "threadsPerCore": cpu["threads_per_core"],
        "ramGb": _detect_ram_gb(),
        "gpu": _detect_gpu(),
    }


if __name__ == "__main__":
    print(json.dumps(get_hardware_profile(), indent=2, ensure_ascii=True))
