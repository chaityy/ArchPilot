"""CPU information: model, cores, frequency, per-core usage, temperature."""
from __future__ import annotations

import platform

from .utils import run


def _cpu_name() -> str:
    system = platform.system()
    if system == "Linux":
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if line.lower().startswith("model name"):
                        return line.split(":", 1)[1].strip()
        except Exception:
            pass
    elif system == "Windows":
        out = run(["wmic", "cpu", "get", "name"])
        if out:
            lines = [l.strip() for l in out.splitlines() if l.strip() and "Name" not in l]
            if lines:
                return lines[0]
    elif system == "Darwin":
        out = run(["sysctl", "-n", "machdep.cpu.brand_string"])
        if out:
            return out
    try:
        import cpuinfo  # py-cpuinfo

        return cpuinfo.get_cpu_info().get("brand_raw", platform.processor())
    except Exception:
        return platform.processor() or "Unknown CPU"


def _cpu_temp() -> float | None:
    try:
        import psutil

        temps = psutil.sensors_temperatures()
        for _, entries in temps.items():
            for entry in entries:
                if entry.current:
                    return entry.current
    except Exception:
        pass
    return None


def gather() -> dict:
    import psutil

    freq = psutil.cpu_freq()
    per_core = psutil.cpu_percent(percpu=True, interval=0.15)

    return {
        "name": _cpu_name(),
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "max_freq_mhz": round(freq.max, 0) if freq and freq.max else None,
        "current_freq_mhz": round(freq.current, 0) if freq else None,
        "usage_total_pct": round(sum(per_core) / len(per_core), 1) if per_core else None,
        "usage_per_core": [round(p, 0) for p in per_core] if per_core else [],
        "temperature_c": _cpu_temp(),
    }
