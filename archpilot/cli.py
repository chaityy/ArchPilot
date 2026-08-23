"""Command-line interface for ArchPilot."""
from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .display import render
from .info import (
    battery_info,
    cpu_info,
    disk_info,
    gpu_info,
    memory_info,
    network_info,
    os_info,
    process_info,
    python_info,
)


def gather_all(top_n: int = 5) -> dict:
    return {
        "os_info": os_info.gather(),
        "cpu_info": cpu_info.gather(),
        "gpu_info": gpu_info.gather(),
        "memory_info": memory_info.gather(),
        "disk_info": disk_info.gather(),
        "network_info": network_info.gather(),
        "battery_info": battery_info.gather(),
        "python_info": python_info.gather(),
        "process_info": process_info.gather(top_n=top_n),
    }


def print_top_processes(data: dict, no_color: bool) -> None:
    from rich.console import Console
    from rich.table import Table

    console = Console(no_color=no_color)
    proc = data["process_info"]

    table = Table(title="Top Processes by CPU")
    table.add_column("PID", justify="right")
    table.add_column("Name")
    table.add_column("CPU %", justify="right")
    for p in proc["top_cpu"]:
        table.add_row(str(p["pid"]), p["name"], f"{p['cpu_pct']}")
    console.print(table)

    table2 = Table(title="Top Processes by Memory")
    table2.add_column("PID", justify="right")
    table2.add_column("Name")
    table2.add_column("Mem %", justify="right")
    for p in proc["top_mem"]:
        table2.add_row(str(p["pid"]), p["name"], f"{p['mem_pct']}")
    console.print(table2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="archpilot",
        description="ArchPilot - a detailed, Python-powered system info tool "
        "(neofetch/fastfetch alternative).",
    )
    parser.add_argument("--json", action="store_true", help="output raw data as JSON")
    parser.add_argument("--no-color", action="store_true", help="disable colored output")
    parser.add_argument(
        "--processes",
        action="store_true",
        help="also show tables of top CPU/memory processes",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        metavar="N",
        help="number of top processes to include (default: 5)",
    )
    parser.add_argument("--version", action="version", version=f"ArchPilot {__version__}")
    args = parser.parse_args(argv)

    data = gather_all(top_n=args.top)

    if args.json:
        print(json.dumps(data, indent=2, default=str))
        return 0

    render(data, no_color=args.no_color)

    if args.processes:
        print_top_processes(data, no_color=args.no_color)

    return 0


if __name__ == "__main__":
    sys.exit(main())
