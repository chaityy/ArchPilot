"""Renders gathered system data as a neofetch/fastfetch-style colored panel."""
from __future__ import annotations

from rich.columns import Columns
from rich.console import Console
from rich.text import Text

from .ascii_art import get_logo

ACCENT = "bold cyan"
LABEL = "bold magenta"
VALUE = "white"


def _line(label: str, value: object) -> Text:
    t = Text()
    padded = f"{label:<12}" if len(label) < 12 else f"{label} "
    t.append(padded, style=LABEL)
    t.append(str(value), style=VALUE)
    return t


def build_lines(data: dict) -> list[Text]:
    lines: list[Text] = []
    os_ = data["os_info"]
    cpu = data["cpu_info"]
    gpu = data["gpu_info"]
    mem = data["memory_info"]
    disk = data["disk_info"]
    net = data["network_info"]
    battery = data["battery_info"]
    py = data["python_info"]
    proc = data["process_info"]

    header = Text()
    header.append(f"{os_['user']}", style=ACCENT)
    header.append("@", style=VALUE)
    header.append(f"{os_['hostname']}", style=ACCENT)
    lines.append(header)
    lines.append(Text("-" * len(header.plain), style="dim"))

    lines.append(_line("OS", os_["os"]))
    lines.append(_line("Kernel", os_["kernel"]))
    lines.append(_line("Arch", os_["architecture"]))
    if os_.get("uptime"):
        lines.append(_line("Uptime", os_["uptime"]))
    if os_.get("de_wm"):
        lines.append(_line("DE/WM", os_["de_wm"]))
    lines.append(_line("Shell", os_["shell"]))
    lines.append(_line("Terminal", os_["terminal"]))
    if os_.get("resolution"):
        lines.append(_line("Resolution", os_["resolution"]))

    lines.append(Text(""))
    cpu_val = f"{cpu['name']}"
    if cpu.get("physical_cores"):
        cpu_val += f" ({cpu['physical_cores']}C/{cpu['logical_cores']}T)"
    lines.append(_line("CPU", cpu_val))
    if cpu.get("current_freq_mhz"):
        lines.append(_line("CPU Freq", f"{cpu['current_freq_mhz']:.0f} MHz"))
    if cpu.get("usage_total_pct") is not None:
        lines.append(_line("CPU Usage", f"{cpu['usage_total_pct']}%"))
    if cpu.get("temperature_c"):
        lines.append(_line("CPU Temp", f"{cpu['temperature_c']:.1f}°C"))

    for i, g in enumerate(gpu):
        label = "GPU" if i == 0 else f"GPU {i+1}"
        lines.append(_line(label, g.get("name", "Unknown")))

    lines.append(Text(""))
    lines.append(
        _line("Memory", f"{mem['used']} / {mem['total']} ({mem['percent']}%)")
    )
    if mem.get("swap_total") and mem["swap_total"] != "0.0 B":
        lines.append(
            _line("Swap", f"{mem['swap_used']} / {mem['swap_total']} ({mem['swap_percent']}%)")
        )

    for part in disk["partitions"][:4]:
        lines.append(
            _line(
                f"Disk ({part['mountpoint']})",
                f"{part['used']} / {part['total']} ({part['percent']}%)",
            )
        )
    if disk.get("io"):
        lines.append(
            _line("Disk I/O", f"R: {disk['io']['read_total']}  W: {disk['io']['write_total']}")
        )

    lines.append(Text(""))
    if net.get("local_ip"):
        lines.append(_line("Local IP", net["local_ip"]))
    lines.append(
        _line("Network", f"↑ {net['traffic']['sent']}  ↓ {net['traffic']['received']}")
    )

    if battery:
        state = "Charging" if battery["plugged_in"] else "Discharging"
        val = f"{battery['percent']}% ({state})"
        if battery.get("time_left"):
            val += f" - {battery['time_left']} left"
        lines.append(_line("Battery", val))

    lines.append(Text(""))
    lines.append(_line("Python", f"{py['version']} ({py['implementation']})"))
    if py.get("installed_packages"):
        lines.append(_line("Packages", py["installed_packages"]))
    lines.append(_line("Processes", proc["total_processes"]))

    return lines


def render(data: dict, no_color: bool = False) -> None:
    console = Console(no_color=no_color, highlight=False)
    logo = Text(get_logo(), style=ACCENT if not no_color else "")
    info = Text("\n").join(build_lines(data))
    console.print(Columns([logo, info], padding=(0, 4), equal=False, expand=False))
