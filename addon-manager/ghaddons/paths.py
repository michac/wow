"""Where the app keeps its config + manifest (next to the project, so the
whole thing stays self-contained and trivially relocatable to its own repo)."""

from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent   # addon-manager/
CONFIG_PATH = APP_DIR / "config.json"
MANIFEST_PATH = APP_DIR / "installed.json"
