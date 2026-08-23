"""RAM and swap memory information."""
from __future__ import annotations

from .utils import human_bytes


def gather() -> dict:
    import psutil

    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return {
        "total": human_bytes(vm.total),
        "used": human_bytes(vm.used),
        "available": human_bytes(vm.available),
        "percent": vm.percent,
        "swap_total": human_bytes(swap.total),
        "swap_used": human_bytes(swap.used),
        "swap_percent": swap.percent,
    }
