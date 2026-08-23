"""Operating system, host, shell, kernel and uptime information."""
from __future__ import annotations

import getpass
import os
import platform
import socket
import sys
import time

from .utils import human_seconds, run


def _linux_distro() -> str:
    try:
        import distro  # type: ignore

        name = distro.name(pretty=True)
        if name:
            return name
    except Exception:
        pass
    return platform.platform()


def _os_pretty_name() -> str:
    system = platform.system()
    if system == "Linux":
        return _linux_distro()
    if system == "Windows":
        ver = platform.win32_ver()
        release, build = ver[0], ver[1]
        edition = platform.win32_edition() if hasattr(platform, "win32_edition") else ""
        pieces = ["Windows", release, edition].__iter__()
        name = " ".join(p for p in [f"Windows {release}", edition] if p)
        return f"{name} (build {build})" if build else name
    if system == "Darwin":
        mac_ver = platform.mac_ver()[0]
        return f"macOS {mac_ver}"
    return f"{system} {platform.release()}"


def _de_wm() -> str | None:
    """Best-effort desktop environment / window manager detection on Linux."""
    de = os.environ.get("XDG_CURRENT_DESKTOP") or os.environ.get("DESKTOP_SESSION")
    wm = None
    if not de:
        session_type = os.environ.get("XDG_SESSION_TYPE")
        wm = session_type
    result = de or wm
    return result


def _shell() -> str:
    if platform.system() == "Windows":
        return os.environ.get("COMSPEC", "cmd.exe").split(os.sep)[-1]
    shell_path = os.environ.get("SHELL")
    return shell_path.split("/")[-1] if shell_path else "unknown"


def _terminal() -> str:
    for var in ("TERM_PROGRAM", "WT_SESSION", "TERM"):
        val = os.environ.get(var)
        if val:
            if var == "WT_SESSION":
                return "Windows Terminal"
            return val
    return "unknown"


def _resolution() -> str | None:
    try:
        if platform.system() == "Windows":
            import ctypes

            user32 = ctypes.windll.user32  # type: ignore[attr-defined]
            w, h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
            return f"{w}x{h}"
        else:
            import tkinter

            root = tkinter.Tk()
            root.withdraw()
            w, h = root.winfo_screenwidth(), root.winfo_screenheight()
            root.destroy()
            return f"{w}x{h}"
    except Exception:
        xrandr = run(["xrandr"])
        if xrandr:
            for line in xrandr.splitlines():
                if "*" in line:
                    return line.split()[0]
        return None


def gather() -> dict:
    boot_time = None
    try:
        import psutil

        boot_time = psutil.boot_time()
    except Exception:
        pass

    uptime_str = None
    if boot_time:
        uptime_str = human_seconds(time.time() - boot_time)

    return {
        "user": getpass.getuser(),
        "hostname": socket.gethostname(),
        "os": _os_pretty_name(),
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "uptime": uptime_str,
        "shell": _shell(),
        "terminal": _terminal(),
        "de_wm": _de_wm(),
        "resolution": _resolution(),
    }
