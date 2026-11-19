"""XDG-compliant application paths."""
from __future__ import annotations
import os
from pathlib import Path

def _xdg(name: str, fallback: str) -> Path:
    value = os.environ.get(name)
    return Path(value).expanduser() if value else Path.home() / fallback

CONFIG_HOME = _xdg('XDG_CONFIG_HOME', '.config') / 'kali-ux'
DATA_HOME = _xdg('XDG_DATA_HOME', '.local/share') / 'kali-ux'
CACHE_HOME = _xdg('XDG_CACHE_HOME', '.cache') / 'kali-ux'
RUNTIME_HOME = Path(os.environ.get('XDG_RUNTIME_DIR', '/tmp')) / 'kali-ux'
