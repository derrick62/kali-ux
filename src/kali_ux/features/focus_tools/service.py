"""Reversible XFCE focus-mode helper; does not kill notifications or processes."""

from __future__ import annotations

from kali_ux.platform.commands import run_command


class FocusMode:
    def __init__(self):
        self._previous: str | None = None
        self.active = False

    def enable(self) -> bool:
        # Repeated enable requests must not replace the original value with True.
        if self.active:
            return True
        current = run_command(["xfconf-query", "-c", "xfce4-notifyd", "-p", "/do-not-disturb"])
        if not current.available or current.returncode != 0:
            return False
        previous = current.stdout.strip()
        if previous.lower() not in {"true", "false", "1", "0", "yes", "no"}:
            return False
        updated = run_command(
            [
                "xfconf-query",
                "-c",
                "xfce4-notifyd",
                "-p",
                "/do-not-disturb",
                "-n",
                "-t",
                "bool",
                "-s",
                "true",
            ]
        )
        if not updated.available or updated.returncode != 0:
            return False
        self._previous = previous
        self.active = True
        return True

    def disable(self) -> bool:
        if self._previous is None:
            return False
        previous = self._previous.lower() in ("true", "1", "yes")
        restored = run_command(
            [
                "xfconf-query",
                "-c",
                "xfce4-notifyd",
                "-p",
                "/do-not-disturb",
                "-n",
                "-t",
                "bool",
                "-s",
                str(previous).lower(),
            ]
        )
        if not restored.available or restored.returncode != 0:
            # Keep the recovery value so the user can retry.
            return False
        self.active = False
        self._previous = None
        return True
