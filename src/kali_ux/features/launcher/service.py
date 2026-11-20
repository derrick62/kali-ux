"""XDG desktop-entry discovery and safe application launching."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from kali_ux.platform.commands import start_command


@dataclass(frozen=True)
class AppEntry:
    name: str
    command: str
    path: str


class ApplicationLauncher:
    def __init__(self):
        self.entries = self._scan()

    def _scan(self) -> list[AppEntry]:
        entries: dict[str, AppEntry] = {}
        seen_files: set[str] = set()
        roots = (
            Path.home() / ".local/share/applications",
            Path("/usr/local/share/applications"),
            Path("/usr/share/applications"),
        )
        for root in roots:
            if not root.exists():
                continue
            for path in root.rglob("*.desktop"):
                # A user-local Hidden/NoDisplay entry must mask a system entry
                # with the same desktop-file ID, not reveal it as a fallback.
                desktop_id = path.relative_to(root).as_posix().replace("/", "-")
                if desktop_id in seen_files:
                    continue
                seen_files.add(desktop_id)
                try:
                    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
                except OSError:
                    continue
                in_desktop_entry = False
                values: dict[str, str] = {}
                for line in lines:
                    if line.startswith("[") and line.endswith("]"):
                        in_desktop_entry = line == "[Desktop Entry]"
                    elif in_desktop_entry and "=" in line:
                        key, value = line.split("=", 1)
                        values.setdefault(key, value)
                name = values.get("Name")
                command = values.get("Exec")
                if (
                    not name
                    or not command
                    or values.get("NoDisplay", "false").lower() == "true"
                    or values.get("Hidden", "false").lower() == "true"
                ):
                    continue
                entries[desktop_id] = AppEntry(name, command, str(path))
        return sorted(entries.values(), key=lambda item: item.name.casefold())

    def search(self, query: str) -> list[AppEntry]:
        needle = query.casefold().strip()
        return sorted(
            (entry for entry in self.entries if needle in entry.name.casefold()),
            key=lambda entry: entry.name.casefold(),
        )[:80]

    def launch(self, entry: AppEntry) -> bool:
        result = start_command(["gio", "launch", entry.path])
        return result.started
