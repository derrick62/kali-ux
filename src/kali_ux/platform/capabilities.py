"""Read-only runtime capability detection; never changes system settings."""

from __future__ import annotations

import os
import shutil


def _gtk_capabilities() -> tuple[bool, bool]:
    """Check GTK3 and libwnck introspection namespaces without loading the UI."""
    try:
        import gi
    except ImportError:
        return False, False

    try:
        gi.require_version("Gtk", "3.0")
        gi.require_version("Gdk", "3.0")
        gi.require_version("Pango", "1.0")
        from gi.repository import Gdk, Gtk, Pango  # noqa: F401
    except (ValueError, gi.RepositoryError):
        return False, False

    try:
        gi.require_version("Wnck", "3.0")
        from gi.repository import Wnck  # noqa: F401
    except (ValueError, gi.RepositoryError):
        return True, False
    return True, True


def detect() -> dict[str, object]:
    session = os.environ.get("XDG_SESSION_TYPE", "unknown")
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "unknown")
    gtk3, libwnck = _gtk_capabilities()
    providers = ("touchegg", "libinput-gestures", "fusuma", "gebaar")
    return {
        "session_type": session,
        "desktop": desktop,
        "x11": bool(os.environ.get("DISPLAY")) and session.lower() != "wayland",
        "wayland": session.lower() == "wayland",
        "xfce": "xfce" in desktop.lower(),
        "xfwm4": bool(shutil.which("xfwm4")),
        "gtk3": gtk3,
        "libwnck": libwnck,
        "wmctrl": bool(shutil.which("wmctrl")),
        "gio": bool(shutil.which("gio")),
        "xdotool": bool(shutil.which("xdotool")),
        "libinput": bool(shutil.which("libinput")),
        "xclip": bool(shutil.which("xclip")),
        "xfconf_query": bool(shutil.which("xfconf-query")),
        "gesture_provider": any(shutil.which(provider) for provider in providers),
        # Compositor-aware preview support is not implemented yet. Do not infer it
        # merely from the presence of a running compositor.
        "compositor": False,
    }
