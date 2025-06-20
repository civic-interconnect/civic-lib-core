"""
civic_lib_core/schema_utils.py

Centralized schema change detection utilities for Civic Interconnect agents.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
"""

import hashlib
import json
from pathlib import Path

from civic_lib_core import log_utils

__all__ = ["detect_schema_change", "hash_dict", "load_json"]

logger = log_utils.logger


def detect_schema_change(old_file: Path, new_data: dict) -> bool:
    """
    Detect if the schema has changed by comparing the old file's hash with the new data.
    Args:
        old_file (Path): The path to the old schema file.
        new_data (dict): The new schema data to compare against.
    Returns:
        bool: True if the schema has changed (i.e., hashes differ), False otherwise.
    """
    if not old_file.exists():
        return True
    old_data = load_json(old_file)
    return hash_dict(old_data) != hash_dict(new_data)


def hash_dict(data: dict) -> str:
    """Hash a JSON-serializable dictionary for change detection.
    Args:
        data (dict): The dictionary to hash.
    Returns:
        str: The SHA-256 hash of the JSON-encoded dictionary.
    """
    encoded = json.dumps(data, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: str | Path) -> dict:
    """
    Load a JSON file and return its contents as a dictionary.
    Args:
        path (str | Path): The path to the JSON file.
    Returns:
        dict: The parsed JSON data.
    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    with open(path) as f:
        return json.load(f)
