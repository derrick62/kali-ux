"""Runtime capability detection; detection does not change system settings."""

from __future__ import annotations

import os
import shutil


def detect() -> dict[str, object]:
    session = os.environ.get("XDG_SESSION_TYPE", "unknown")
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "unknown")
    return {
        "session_type": session,
        "desktop": desktop,
        "x11": bool(os.environ.get("DISPLAY")) and session.lower() != "wayland",
        "wayland": session.lower() == "wayland",
        "xfce": "xfce" in desktop.lower(),
        "wmctrl": bool(shutil.which("wmctrl")),
        "xdotool": bool(shutil.which("xdotool")),
        "libinput": bool(shutil.which("libinput")),
        "xclip": bool(shutil.which("xclip")),
        "xfconf_query": bool(shutil.which("xfconf-query")),
    }
