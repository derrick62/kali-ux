"""Small, dependency-free configuration loader with safe defaults."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from .paths import CONFIG_HOME

DEFAULTS: dict[str, Any] = {
 'version': 1,
 'features': {k: {'enabled': False} for k in ('window_switcher','gesture_control','window_overview','snap_assist','clipboard_history','quick_panel','focus_tools','launcher','window_peek','layout_memory')},
 'gestures': {'enabled': False, 'provider': 'external', 'conflict_policy': 'warn'},
 'clipboard': {'max_items': 50, 'max_item_bytes': 65536, 'persist': False, 'exclude_password_managers': True},
 'window': {'exclude_skip_tasklist': True, 'show_thumbnails': False},
}

def load_config(path: Path | None = None) -> dict[str, Any]:
    target = path or CONFIG_HOME / 'config.json'
    if not target.exists(): return json.loads(json.dumps(DEFAULTS))
    try: data = json.loads(target.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc: raise ValueError(f'Cannot read config {target}: {exc}') from exc
    if not isinstance(data, dict) or data.get('version') != 1: raise ValueError('Unsupported or invalid Kali UX configuration')
    merged = json.loads(json.dumps(DEFAULTS))
    for key, value in data.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict): merged[key].update(value)
        else: merged[key] = value
    return merged

def write_default_config(path: Path | None = None) -> Path:
    target = path or CONFIG_HOME / 'config.json'; target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists(): target.write_text(json.dumps(DEFAULTS, indent=2)+'\n', encoding='utf-8'); target.chmod(0o600)
    return target
