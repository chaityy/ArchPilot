"""Details about the running Python interpreter and environment."""
from __future__ import annotations

import platform
import sys


def gather() -> dict:
    in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)

    pkg_count = None
    try:
        import importlib.metadata as md

        pkg_count = len(list(md.distributions()))
    except Exception:
        pass

    return {
        "version": platform.python_version(),
        "implementation": platform.python_implementation(),
        "executable": sys.executable,
        "virtual_env": in_venv,
        "installed_packages": pkg_count,
    }
