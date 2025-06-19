"""
yaml_utils.py

Lightweight helpers for reading and writing YAML files.

MIT License — maintained by Civic Interconnect
"""

from pathlib import Path
from typing import Any

import yaml

__all__ = ["write_yaml", "read_yaml"]


def write_yaml(data: dict[str, Any], path: str | Path) -> Path:
    """
    Write a dictionary to a YAML file.

    Args:
        data (dict): Data to write.
        path (str | Path): File path to write to.

    Returns:
        Path: The path the file was written to.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False)
    return path


def read_yaml(path: str | Path) -> dict[str, Any]:
    """
    Read and parse a YAML file into a dictionary.

    Args:
        path (str | Path): YAML file path.

    Returns:
        dict: Parsed YAML data.
    """
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)
