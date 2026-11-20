"""Explicit, user-triggered window geometry snapshots."""

from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path

from kali_ux.core.paths import DATA_HOME
from kali_ux.platform.commands import run_command

_WINDOW_ID = re.compile(r"0x[0-9a-fA-F]+\Z")


class LayoutMemory:
    def __init__(self, path: Path | None = None):
        self.path = path or DATA_HOME / "layouts.json"

    @staticmethod
    def _valid_name(name: str) -> str | None:
        if not isinstance(name, str):
            return None
        clean = name.strip()
        if (
            not clean
            or clean in {".", ".."}
            or "/" in clean
            or "\\" in clean
            or len(clean) > 64
            or any(ord(char) < 32 for char in clean)
        ):
            return None
        return clean

    def _read(self) -> dict[str, list[dict[str, object]]]:
        if not self.path.exists():
            return {}
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}
        if not isinstance(data, dict):
            return {}
        return {
            key: value
            for key, value in data.items()
            if isinstance(key, str) and isinstance(value, list)
        }

    def _write(self, data: dict[str, list[dict[str, object]]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary = tempfile.mkstemp(prefix=".layouts-", dir=self.path.parent)
        try:
            os.fchmod(descriptor, 0o600)
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                json.dump(data, stream, indent=2)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.path)
            self.path.chmod(0o600)
        except Exception:
            try:
                os.unlink(temporary)
            except OSError:
                pass
            raise

    def capture(self, name: str) -> bool:
        clean_name = self._valid_name(name)
        if clean_name is None:
            return False
        result = run_command(["wmctrl", "-lG"])
        if not result.available or result.returncode != 0:
            return False
        windows: list[dict[str, object]] = []
        for line in result.stdout.splitlines():
            parts = line.split(None, 7)
            if len(parts) < 7 or not _WINDOW_ID.fullmatch(parts[0]):
                continue
            try:
                desktop, x, y, width, height = map(int, parts[1:6])
            except ValueError:
                continue
            if width <= 0 or height <= 0:
                continue
            # Do not persist window titles: they can contain private information.
            windows.append(
                {
                    "id": parts[0],
                    "desktop": desktop,
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height,
                }
            )
        data = self._read()
        data[clean_name] = windows
        try:
            self._write(data)
        except OSError:
            return False
        return True

    def names(self) -> list[str]:
        return sorted(self._read())

    def restore(self, name: str) -> int:
        clean_name = self._valid_name(name)
        if clean_name is None:
            return 0
        windows = self._read().get(clean_name, [])
        restored = 0
        for window in windows:
            if not isinstance(window, dict):
                continue
            window_id = window.get("id")
            if not isinstance(window_id, str) or not _WINDOW_ID.fullmatch(window_id):
                continue
            try:
                x, y, width, height = (int(window[key]) for key in ("x", "y", "width", "height"))
            except (KeyError, TypeError, ValueError):
                continue
            if width <= 0 or height <= 0:
                continue
            result = run_command(["wmctrl", "-ir", window_id, "-e", f"0,{x},{y},{width},{height}"])
            restored += int(result.available and result.returncode == 0)
        return restored
