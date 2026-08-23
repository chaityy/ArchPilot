"""Shared helpers for info-gathering modules."""
from __future__ import annotations

import shutil
import subprocess


def run(cmd: list[str], timeout: float = 2.0) -> str | None:
    """Run a command and return stripped stdout, or None if it fails/missing."""
    if shutil.which(cmd[0]) is None:
        return None
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, check=False
        )
        out = result.stdout.strip()
        return out or None
    except Exception:
        return None


def human_bytes(n: float) -> str:
    """Convert a byte count into a human readable string."""
    for unit in ("B", "KiB", "MiB", "GiB", "TiB", "PiB"):
        if abs(n) < 1024.0:
            return f"{n:3.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} EiB"


def human_seconds(seconds: float) -> str:
    """Convert seconds into a 'Xd Yh Zm' style uptime string."""
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, _ = divmod(seconds, 60)
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes or not parts:
        parts.append(f"{minutes}m")
    return " ".join(parts)
