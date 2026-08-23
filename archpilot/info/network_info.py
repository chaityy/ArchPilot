"""Network interfaces, local IPs, and cumulative traffic counters."""
from __future__ import annotations

import socket

from .utils import human_bytes


def _local_ip() -> str | None:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None


def gather() -> dict:
    import psutil

    interfaces = []
    stats = psutil.net_if_stats()
    addrs = psutil.net_if_addrs()
    for name, addr_list in addrs.items():
        is_up = stats.get(name).isup if name in stats else False
        if not is_up:
            continue
        ipv4 = next((a.address for a in addr_list if a.family == socket.AF_INET), None)
        if ipv4:
            interfaces.append({"name": name, "ip": ipv4})

    io = psutil.net_io_counters()
    traffic = {
        "sent": human_bytes(io.bytes_sent),
        "received": human_bytes(io.bytes_recv),
    }

    return {
        "hostname": socket.gethostname(),
        "local_ip": _local_ip(),
        "interfaces": interfaces,
        "traffic": traffic,
    }
