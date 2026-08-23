# ArchPilot

A system information tool written entirely in Python — in the spirit of
**neofetch** / **fastfetch**, but pulling a lot more detail: per-core CPU
usage and temperature, GPU (NVIDIA / generic detection), memory + swap,
per-partition disk usage and I/O totals, network interfaces and throughput,
battery status, Python environment info, and top processes by CPU/RAM.

```
                  chaity@desktop
      /\          -------
     /  \         OS          Windows 11 Pro (build 26100)
    /\   \        Kernel      10.0.26100
   /      \       Arch        AMD64
  /   ,,   \      Uptime      2h 14m
 /   |  |  -\     Shell       powershell.exe
/_-''    ''-_\    Terminal    Windows Terminal

                  CPU         AMD Ryzen 7 5800X (8C/16T)
                  CPU Usage   12.4%
                  GPU         NVIDIA GeForce RTX 3070

                  Memory      9.8 GiB / 32.0 GiB (30.6%)
                  Disk (C:)   412.1 GiB / 953.0 GiB (43.2%)

                  Local IP    192.168.1.42
                  Network     ↑ 1.2 GiB  ↓ 8.4 GiB

                  Python      3.12.4 (CPython)
                  Packages    118
                  Processes   287
```

## Install

```bash
pip install -r requirements.txt
```

or install it as a proper command:

```bash
pip install .
archpilot
```

## Usage

```bash
python -m archpilot                  # colored neofetch-style panel
python -m archpilot --processes      # also show top CPU/RAM process tables
python -m archpilot --top 10         # show top 10 instead of top 5
python -m archpilot --json           # machine-readable output
python -m archpilot --no-color       # disable ANSI colors
```

If installed via `pip install .`, you can just run `archpilot` from anywhere.

## Project layout

```
archpilot/
├── archpilot/
│   ├── cli.py            # argument parsing + orchestration
│   ├── display.py        # rich-based colored rendering
│   ├── ascii_art.py       # per-OS ASCII logos
│   └── info/
│       ├── os_info.py     # OS, kernel, shell, terminal, DE/WM, resolution
│       ├── cpu_info.py    # CPU model, cores, freq, per-core usage, temp
│       ├── gpu_info.py    # GPU detection (nvidia-smi / wmic / lspci / macOS)
│       ├── memory_info.py # RAM + swap
│       ├── disk_info.py   # per-partition usage + I/O totals
│       ├── network_info.py# interfaces, local IP, traffic totals
│       ├── battery_info.py
│       ├── python_info.py # interpreter, venv, installed package count
│       └── process_info.py# total process count + top by CPU/RAM
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Building a standalone .exe (Windows)

Same PyInstaller pattern used for other packaged tools:

```bash
pip install pyinstaller
pyinstaller --onefile --name ArchPilot --console -m archpilot
```

The binary will be in `dist/ArchPilot.exe` — no Python install required to run it.

## Notes on data availability

- **GPU** detection uses `nvidia-smi` first (gives VRAM/temp/utilization on
  NVIDIA cards), then falls back to `wmic` (Windows), `lspci` (Linux), or
  `system_profiler` (macOS) for a name-only listing.
- **CPU temperature** depends on OS sensor access — often unavailable on
  Windows without extra drivers/permissions, more reliable on Linux.
- **Battery** section is simply omitted on desktops with no battery.
