"""
civic_lib_core/path_utils.py

Cross-platform path helpers for reports and file management.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
"""

from pathlib import Path

__all__ = ["ensure_dir", "safe_filename"]


def ensure_dir(path: str | Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path (str | Path): The directory path to ensure.

    Returns:
        Path: The resolved Path object of the directory.
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_filename(name: str) -> str:
    """
    Convert a string into a safe, lowercase filename.

    Replaces spaces and forward slashes with underscores.

    Args:
        name (str): Original string.

    Returns:
        str: Sanitized, lowercase filename string.
    """
    return name.replace(" ", "_").replace("/", "_").lower()
