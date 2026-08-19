# ArchPilot 🚀

A modern graphical system manager for Arch Linux and its derivatives.

## Current features

- System overview with CPU, memory, disk and uptime
- Package search through pacman
- Package installation/removal with confirmation
- System update check
- Service listing through systemd
- Dark/light UI
- Safe subprocess execution without shell interpolation
- Graceful fallback when Arch-specific commands are unavailable

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
archpilot
```

On Arch/CachyOS, install PySide6 and psutil using your preferred package manager or Python environment.

## Roadmap

- AUR support via paru/yay
- Flatpak support
- Cleanup center
- Kernel manager
- Storage analyzer
- Health score
- Notifications
- Native Arch package
- Automated tests and CI