"""civic_lib_core/schema_utils.py.

Centralized schema change detection utilities for Civic Interconnect agents.
Part of the Civic Interconnect agent framework.

"""

import hashlib
import json
from pathlib import Path
from typing import Any

from civic_lib_core import log_utils

__all__ = ["detect_schema_change", "hash_dict", "load_json"]

logger = log_utils.logger


def detect_schema_change(old_file: Path, new_data: dict[str, Any]) -> bool:
    """Detect if the schema has changed by comparing the old file's hash with the new data.

    Args:
        old_file (Path): The path to the old schema file.
        new_data (dict[str, Any]): The new schema data to compare against.

    Returns:
        bool: True if the schema has changed (i.e., hashes differ), False otherwise.
    """
    if not old_file.exists():
        logger.info(f"Old schema file not found: {old_file}. Treating as changed.")
        return True

    old_data = load_json(old_file)
    changed = hash_dict(old_data) != hash_dict(new_data)
    if changed:
        logger.info("Schema change detected.")
    else:
        logger.info("No schema change detected.")
    return changed


def hash_dict(data: dict[str, Any]) -> str:
    """Hash a JSON-serializable dictionary for change detection.

    Args:
        data (dict[str, Any]): The dictionary to hash.

    Returns:
        str: The SHA-256 hash of the JSON-encoded dictionary.
    """
    encoded = json.dumps(data, sort_keys=True).encode("utf-8")
    digest = hashlib.sha256(encoded).hexdigest()
    logger.debug(f"Computed hash: {digest}")
    return digest


def load_json(path: str | Path) -> dict[str, Any]:
    """Load a JSON file and return its contents as a dictionary.

    Args:
        path (str | Path): The path to the JSON file.

    Returns:
        dict[str, Any]: The parsed JSON data.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    path = Path(path)
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    logger.debug(f"Loaded JSON from {path}")
    return data
