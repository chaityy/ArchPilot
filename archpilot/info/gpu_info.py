"""GPU information: best-effort detection across NVIDIA / Windows / Linux."""
from __future__ import annotations

import platform

from .utils import run


def _nvidia_smi() -> list[dict] | None:
    out = run(
        [
            "nvidia-smi",
            "--query-gpu=name,memory.total,memory.used,temperature.gpu,utilization.gpu",
            "--format=csv,noheader,nounits",
        ]
    )
    if not out:
        return None
    gpus = []
    for line in out.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 5:
            gpus.append(
                {
                    "name": parts[0],
                    "vram_total_mb": parts[1],
                    "vram_used_mb": parts[2],
                    "temperature_c": parts[3],
                    "utilization_pct": parts[4],
                }
            )
    return gpus or None


def _windows_wmic() -> list[dict] | None:
    out = run(["wmic", "path", "win32_VideoController", "get", "name"])
    if not out:
        return None
    lines = [l.strip() for l in out.splitlines() if l.strip() and l.strip() != "Name"]
    return [{"name": name} for name in lines] or None


def _linux_lspci() -> list[dict] | None:
    out = run(["lspci"])
    if not out:
        return None
    gpus = []
    for line in out.splitlines():
        low = line.lower()
        if "vga compatible controller" in low or "3d controller" in low:
            name = line.split(":", 2)[-1].strip()
            gpus.append({"name": name})
    return gpus or None


def _macos_system_profiler() -> list[dict] | None:
    out = run(["system_profiler", "SPDisplaysDataType"])
    if not out:
        return None
    gpus = []
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("Chipset Model:"):
            gpus.append({"name": line.split(":", 1)[1].strip()})
    return gpus or None


def gather() -> list[dict]:
    gpus = _nvidia_smi()
    if gpus:
        return gpus

    system = platform.system()
    if system == "Windows":
        gpus = _windows_wmic()
    elif system == "Linux":
        gpus = _linux_lspci()
    elif system == "Darwin":
        gpus = _macos_system_profiler()

    return gpus or [{"name": "Not detected"}]
