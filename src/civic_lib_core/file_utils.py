"""
civic_lib_core/file_utils.py

Utility functions for root-relative logic.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
"""

import inspect
from pathlib import Path

__all__ = ["resolve_path", "find_project_root", "ensure_source_path", "ensure_docs_output_dir"]


def resolve_path(relative_path: str | Path) -> Path:
    """
    Return an absolute Path from project root for a relative path.

    Args:
        relative_path (str | Path): The relative or partial path to resolve.

    Returns:
        Path: The absolute path resolved from the project root.
    """
    return Path(__file__).parent.parent.resolve() / Path(relative_path)


def find_project_root() -> Path:
    """
    Find the actual project root, whether civic_lib_core is installed or local.

    Returns:
        Path: The project root directory
    """
    # Try to find calling project first
    frame = inspect.currentframe()
    try:
        while frame:
            caller_file = frame.f_globals.get("__file__")
            if caller_file:
                caller_path = Path(caller_file).resolve()
                # If caller is NOT in civic_lib_core or site-packages, use their project
                if (
                    "civic_lib_core" not in caller_path.parts
                    and "site-packages" not in caller_path.parts
                ):
                    project_root = caller_path.parent
                    break
            frame = frame.f_back
        else:
            # No external caller, start from current working directory
            project_root = Path.cwd()
    finally:
        del frame

    # Walk up to find project root markers
    while project_root.parent != project_root:
        if (
            (project_root / "pyproject.toml").exists()
            or (project_root / "setup.py").exists()
            or (project_root / ".git").exists()
        ):
            break
        project_root = project_root.parent

    return project_root


def ensure_source_path(source_pkg_str: str = "civic_lib_core") -> Path:
    """Resolve and validate the source package path."""
    source_path = resolve_path(source_pkg_str)
    if not source_path.exists():
        raise FileNotFoundError(f"Source directory not found: {source_path}")
    return source_path


def ensure_docs_output_dir(output_dir_str: str = "api") -> Path:
    """Ensure output directory exists under project root/docs."""
    project_root = find_project_root()
    # Always put API docs in docs/api to avoid conflicts with GitHub Pages
    docs_dir = project_root / "docs" / output_dir_str
    docs_dir.mkdir(parents=True, exist_ok=True)
    return docs_dir
