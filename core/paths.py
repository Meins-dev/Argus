"""Paths for packaged resources and writable Argus user data."""

from __future__ import annotations

import os
from pathlib import Path
import sys


def get_resource_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    return Path(__file__).resolve().parent.parent


def get_data_dir() -> Path:
    if not getattr(sys, "frozen", False):
        return get_resource_dir()

    override = os.environ.get("ARGUS_DATA_DIR", "").strip()
    if override:
        return Path(override).expanduser()
    if sys.platform == "win32":
        return Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local") / "Argus"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Argus"
    return Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local" / "share") / "argus"
