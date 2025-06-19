"""
civic_lib/file_utils.py

Utility functions for root-relative logic.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
"""

from pathlib import Path

__all__ = ["resolve_path"]


def resolve_path(relative_path: str | Path) -> Path:
    """
    Return an absolute Path from project root for a relative path.

    Args:
        relative_path (str | Path): The relative or partial path to resolve.

    Returns:
        Path: The absolute path resolved from the project root.
    """
    return Path(__file__).parent.parent.resolve() / Path(relative_path)
