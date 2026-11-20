"""Small, dependency-free configuration loader with safe defaults."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .paths import CONFIG_HOME

DEFAULTS: dict[str, Any] = {
    "version": 1,
    "features": {
        k: {"enabled": False}
        for k in (
            "window_switcher",
            "gesture_control",
            "window_overview",
            "snap_assist",
            "clipboard_history",
            "quick_panel",
            "focus_tools",
            "launcher",
            "window_peek",
            "layout_memory",
        )
    },
    "gestures": {"enabled": False, "provider": "external", "conflict_policy": "warn"},
    "clipboard": {
        "max_items": 50,
        "max_item_bytes": 65536,
        "persist": False,
    },
    "window": {"exclude_skip_tasklist": True, "show_thumbnails": False},
}


def load_config(path: Path | None = None) -> dict[str, Any]:
    target = path or CONFIG_HOME / "config.json"
    if not target.exists():
        return json.loads(json.dumps(DEFAULTS))
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read config {target}: {exc}") from exc
    if not isinstance(data, dict) or type(data.get("version")) is not int or data["version"] != 1:
        raise ValueError("Unsupported or invalid Kali UX configuration")

    for section in ("features", "gestures", "clipboard", "window"):
        if section in data and not isinstance(data[section], dict):
            raise ValueError(f"Configuration section '{section}' must be an object")
    if "features" in data:
        for feature, settings in data["features"].items():
            if not isinstance(settings, dict):
                raise ValueError(f"Feature configuration '{feature}' must be an object")
    if "clipboard" in data:
        for key, maximum in (("max_items", 500), ("max_item_bytes", 1048576)):
            value = data["clipboard"].get(key, DEFAULTS["clipboard"][key])
            if type(value) is not int or not 1 <= value <= maximum:
                raise ValueError(f"clipboard.{key} must be an integer between 1 and {maximum}")
        if "persist" in data["clipboard"] and type(data["clipboard"]["persist"]) is not bool:
            raise ValueError("clipboard.persist must be a boolean")

    merged = json.loads(json.dumps(DEFAULTS))
    for key, value in data.items():
        if key == "features" and isinstance(value, dict):
            for feature, settings in value.items():
                if isinstance(settings, dict) and isinstance(merged["features"].get(feature), dict):
                    merged["features"][feature].update(settings)
                else:
                    merged["features"][feature] = settings
        elif isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key].update(value)
        else:
            merged[key] = value
    return merged


def write_default_config(path: Path | None = None) -> Path:
    target = path or CONFIG_HOME / "config.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text(json.dumps(DEFAULTS, indent=2) + "\n", encoding="utf-8")
        target.chmod(0o600)
    return target
