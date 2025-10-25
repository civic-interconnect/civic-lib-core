"""civic_lib_core/dev_utils.py.

Core development utilities.
Part of the Civic Interconnect agent framework.

"""

from collections.abc import Mapping, Sequence
from typing import Any

from civic_lib_core import log_utils

__all__ = [
    "log_suggested_paths",
    "suggest_paths",
]

logger = log_utils.logger


def log_suggested_paths(
    response: Any,
    max_depth: int = 3,
    source_label: str = "response",
) -> None:
    """Log inferred paths to nested keys in a response object.

    Args:
        response (Any): Parsed API response.
        max_depth (int): Maximum depth to explore.
        source_label (str): Label for context in logs.
    """
    logger.info(f"Suggested paths in {source_label}:")

    if isinstance(response, Mapping):
        logger.info(f"Top-level keys: {sorted(response.keys())}")
        paths = suggest_paths(response, max_depth=max_depth)
        for path, key, value in paths:
            logger.info(f"Path: {' -> '.join(path)} | Final Key: {key} | Value: {value}")
    elif isinstance(response, Sequence) and not isinstance(response, str | bytes):
        logger.info(f"Top-level object is a list with {len(response)} items.")
        for i, item in enumerate(response[:5]):
            logger.info(f"Index {i}: {type(item).__name__}")
    else:
        logger.warning("Response is neither a dict nor a list; cannot analyze paths.")


def suggest_paths(
    response: Any,
    max_depth: int = 3,
    current_path: list[str] | None = None,
) -> list[tuple[list[str], str, str]]:
    """Suggest possible nested data paths in a response object.

    Args:
        response (Any): Parsed API response.
        max_depth (int): Maximum traversal depth.
        current_path (list[str] | None): Used internally for recursion.

    Returns:
        list of (path, key, summary): Potential paths to explore.
    """
    if current_path is None:
        current_path = []

    suggestions: list[tuple[list[str], str, str]] = []

    if max_depth <= 0:
        return suggestions

    if isinstance(response, Mapping):
        for key, value in response.items():
            path = current_path + [key]
            if isinstance(value, Mapping):
                suggestions.extend(suggest_paths(value, max_depth - 1, path))
            elif isinstance(value, list):
                summary = f"List[{len(value)}]" if value else "List[empty]"
                suggestions.append((path, key, summary))
            else:
                suggestions.append((path, key, str(value)))
    elif isinstance(response, list):
        summary = f"List[{len(response)}]" if response else "List[empty]"
        suggestions.append((current_path, "[list]", summary))

    return suggestions
