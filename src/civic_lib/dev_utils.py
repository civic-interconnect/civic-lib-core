"""
civic_lib/dev_utils.py

Core development utilities.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
"""

from civic_lib import log_utils

__all__ = [
    "log_suggested_paths",
    "suggest_paths",
]


logger = log_utils.logger


def log_suggested_paths(
    response: dict,
    max_depth: int = 3,
    source_label: str = "response",
) -> None:
    """
    Log inferred paths to nested keys in a response dictionary.

    Args:
        response (dict): Parsed API response.
        max_depth (int): Maximum depth to explore.
        source_label (str): Label for context in logs.
    """
    logger.info(f"Suggested paths in {source_label}:")

    if not isinstance(response, dict):
        logger.warning("Response is not a dict; cannot analyze.")
        return

    logger.info(f"Top-level keys: {sorted(response.keys())}")
    paths = suggest_paths(response, max_depth=max_depth)
    for path, key, value in paths:
        logger.info(f"Path: {' -> '.join(path)} | Final Key: {key} | Value: {value}")


def suggest_paths(
    response: dict,
    max_depth: int = 3,
    current_path: list[str] | None = None,
) -> list[tuple[list[str], str, str]]:
    """
    Suggest possible nested data paths in a response dictionary.

    Args:
        response (dict): Parsed API response.
        max_depth (int): Maximum traversal depth.
        current_path (list[str] | None): Used internally for recursion.

    Returns:
        list of (path, key, summary): Potential paths to explore.
    """
    if current_path is None:
        current_path = []

    suggestions = []

    if not isinstance(response, dict) or max_depth <= 0:
        return suggestions

    for key, value in response.items():
        path = current_path + [key]
        if isinstance(value, dict):
            suggestions.extend(suggest_paths(value, max_depth - 1, path))
        elif isinstance(value, list):
            summary = f"List[{len(value)}]" if value else "List[empty]"
            suggestions.append((path, key, summary))
        else:
            suggestions.append((path, key, str(value)))

    return suggestions
