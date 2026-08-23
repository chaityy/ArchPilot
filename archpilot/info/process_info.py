"""Top processes by CPU and memory usage, plus total process count."""
from __future__ import annotations


def gather(top_n: int = 5) -> dict:
    import psutil

    procs = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    by_cpu = sorted(procs, key=lambda p: p.get("cpu_percent") or 0, reverse=True)[:top_n]
    by_mem = sorted(procs, key=lambda p: p.get("memory_percent") or 0, reverse=True)[:top_n]

    return {
        "total_processes": len(procs),
        "top_cpu": [
            {"name": p["name"], "pid": p["pid"], "cpu_pct": round(p.get("cpu_percent") or 0, 1)}
            for p in by_cpu
        ],
        "top_mem": [
            {
                "name": p["name"],
                "pid": p["pid"],
                "mem_pct": round(p.get("memory_percent") or 0, 1),
            }
            for p in by_mem
        ],
    }
