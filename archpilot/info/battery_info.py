"""Battery status, if the device has one."""
from __future__ import annotations

from .utils import human_seconds


def gather() -> dict | None:
    try:
        import psutil

        battery = psutil.sensors_battery()
        if battery is None:
            return None
        return {
            "percent": round(battery.percent, 1),
            "plugged_in": battery.power_plugged,
            "time_left": (
                human_seconds(battery.secsleft)
                if battery.secsleft and battery.secsleft > 0
                else None
            ),
        }
    except Exception:
        return None
