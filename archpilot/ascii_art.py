"""Small ASCII-art logos shown next to the info panel, picked by OS."""
from __future__ import annotations

import platform

LINUX = r"""
      /\
     /  \
    /\   \
   /      \
  /   ,,   \
 /   |  |  -\
/_-''    ''-_\
"""

WINDOWS = r"""
 __     __
|  |__ |  |
|__  __|__|
 __  __ __
|  ||  |  |
|__||__|__|
"""

MACOS = r"""
      _
    ,(_)
    |  \
  ,-'   `-.
 ( ' ) ( ' )
  \    Y    /
   `-.___.-'
"""

GENERIC = r"""
   ___
  |   |
  | > |
  |___|
"""


def get_logo() -> str:
    system = platform.system()
    if system == "Linux":
        return LINUX
    if system == "Windows":
        return WINDOWS
    if system == "Darwin":
        return MACOS
    return GENERIC
