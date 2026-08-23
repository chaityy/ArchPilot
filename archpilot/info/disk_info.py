"""Disk partitions, usage, and cumulative I/O counters."""
from __future__ import annotations

from .utils import human_bytes


def gather() -> dict:
    import psutil

    partitions = []
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except (PermissionError, OSError):
            continue
        partitions.append(
            {
                "device": part.device,
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "total": human_bytes(usage.total),
                "used": human_bytes(usage.used),
                "free": human_bytes(usage.free),
                "percent": usage.percent,
            }
        )

    io = None
    try:
        counters = psutil.disk_io_counters()
        if counters:
            io = {
                "read_total": human_bytes(counters.read_bytes),
                "write_total": human_bytes(counters.write_bytes),
            }
    except Exception:
        pass

    return {"partitions": partitions, "io": io}
