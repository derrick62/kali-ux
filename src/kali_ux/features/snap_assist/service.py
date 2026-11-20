"""Snap presets using wmctrl geometry requests; xfwm4 remains authoritative."""

from __future__ import annotations

from kali_ux.platform.commands import run_command

PRESETS = {
    "left": (0, 0, 0.5, 1),
    "right": (0.5, 0, 0.5, 1),
    "top": (0, 0, 1, 0.5),
    "bottom": (0, 0.5, 1, 0.5),
    "top-left": (0, 0, 0.5, 0.5),
    "top-right": (0.5, 0, 0.5, 0.5),
    "bottom-left": (0, 0.5, 0.5, 0.5),
    "bottom-right": (0.5, 0.5, 0.5, 0.5),
}


class SnapService:
    def snap_active(
        self,
        preset: str,
        screen_width: int,
        screen_height: int,
        x: int = 0,
        y: int = 0,
    ) -> bool:
        if preset not in PRESETS or screen_width <= 0 or screen_height <= 0:
            return False
        fx, fy, fw, fh = PRESETS[preset]
        gx = x + round(fx * screen_width)
        gy = y + round(fy * screen_height)
        gw = max(1, round(fw * screen_width))
        gh = max(1, round(fh * screen_height))

        # Do not send geometry if the active window could not be unmaximized.
        unmaximize = run_command(
            ["wmctrl", "-r", ":ACTIVE:", "-b", "remove,maximized_vert,maximized_horz"]
        )
        if not unmaximize.available or unmaximize.returncode != 0:
            return False
        result = run_command(["wmctrl", "-r", ":ACTIVE:", "-e", f"0,{gx},{gy},{gw},{gh}"])
        return result.available and result.returncode == 0
