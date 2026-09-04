import sys
from pathlib import Path


def resource_path(relative_path: str) -> Path:
    """Return the path for resources in development or in a PyInstaller bundle."""
    candidates = []

    if hasattr(sys, "_MEIPASS"):
        candidates.append(Path(sys._MEIPASS) / relative_path)

    candidates.extend([
        Path(sys.executable).parent / relative_path,
        Path.cwd() / relative_path,
        Path(__file__).resolve().parents[2] / relative_path,
    ])

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return Path(relative_path)
