"""
civic_lib_core/fs_utils.py

File and path utility functions for root-relative logic.
Unified utilities used across Civic Interconnect agents and libraries.

MIT License — maintained by Civic Interconnect
"""

from pathlib import Path

from civic_lib_core import log_utils

__all__ = [
    "discover_project_layout",
    "ensure_dir",
    "ensure_docs_output_dir",
    "find_source_dir",
    "find_project_root",
    "get_repo_package_names",
    "get_valid_packages",
    "resolve_path",
    "safe_filename",
]

logger = log_utils.logger


def discover_project_layout() -> dict[str, Path | list[Path]]:
    """Centralized layout discovery with early failure and full logging."""
    root = find_project_root()

    # Use flexible source directory discovery
    src = find_source_dir(root)
    packages = get_valid_packages(src) if src else []
    docs_api = root / "docs" / "api"

    layout = {
        "project_root": root,
        "src_dir": src,
        "packages": packages,
        "docs_api_dir": docs_api,
    }

    logger.debug(f"Discovered project layout: {layout}")
    return layout


def _is_python_package(path: Path) -> bool:
    """
    Check if a directory is a valid Python package.

    A valid package has __init__.py or is a namespace package with .py files.
    """
    if not path.is_dir():
        return False

    # Standard package with __init__.py
    if (path / "__init__.py").exists():
        return True

    # Namespace package - has .py files but no __init__.py
    # Only consider it a package if it has actual Python files
    py_files = list(path.glob("*.py"))
    if py_files:
        logger.debug(f"Found namespace package: {path.name}")
        return True

    return False


def ensure_dir(path: str | Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path (str | Path): The directory path to ensure.

    Returns:
        Path: The resolved Path object of the directory.

    Raises:
        OSError: If directory cannot be created due to permissions or other issues.
    """
    try:
        path = Path(path).resolve()
        path.mkdir(parents=True, exist_ok=True)
        return path
    except OSError as e:
        logger.error(f"Failed to create directory {path}: {e}")
        raise


def ensure_docs_output_dir(output_dir_str: str = "api") -> Path:
    """
    Ensure output directory exists under project_root/docs/.

    Args:
        output_dir_str (str): Subfolder inside docs/, usually "api".

    Returns:
        Path: The created or existing path.

    Raises:
        RuntimeError: If project root cannot be found.
        OSError: If directory cannot be created.
    """
    try:
        project_root = find_project_root()
        docs_dir = project_root / "docs" / output_dir_str
        return ensure_dir(docs_dir)
    except Exception as e:
        logger.error(f"Failed to ensure docs output directory '{output_dir_str}': {e}")
        raise


def find_project_root(start_path: Path | None = None) -> Path:
    """
    Find the root of the repo based on common markers.

    Searches for markers like .git, pyproject.toml, setup.py, etc.

    Args:
        start_path (Optional[Path]): Directory to start search from. Defaults to cwd.

    Returns:
        Path: Project root directory.

    Raises:
        RuntimeError: If project root cannot be found.
    """
    current = start_path or Path.cwd()

    # Common project root markers, in order of preference
    markers = [
        ".git",
        "pyproject.toml",
    ]

    for parent in [current] + list(current.parents):
        for marker in markers:
            if (parent / marker).exists():
                logger.debug(f"Root: {parent} (marker: {marker})")
                return parent.resolve()

    # If no markers found, check if current directory looks like a project
    # (has subdirectories that could be packages)
    if any(p.is_dir() and not p.name.startswith(".") for p in current.iterdir()):
        logger.warning(f"No standard project markers found, using current directory: {current}")
        return current.resolve()

    raise RuntimeError(
        f"Project root not found. Searched from {current} upward for markers: {markers}. "
        f"Consider adding a .git directory or pyproject.toml file to mark your project root."
    )


def find_source_dir(root_dir: Path) -> Path | None:
    """
    Flexibly find the source directory containing Python packages in src/

    Args:
        root_dir (Path): Project root directory

    Returns:
        Optional[Path]: Source directory if found, None if no valid packages found
    """
    candidates = [
        root_dir / "src",
    ]

    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            # Check if this directory contains any Python packages
            packages = [p for p in candidate.iterdir() if p.is_dir() and _is_python_package(p)]
            if packages:
                logger.debug(f"src: {candidate} with packages: {[p.name for p in packages]}")
                return candidate

    logger.warning(f"No source directory with Python packages found in: {root_dir}")
    return None


def get_repo_package_names(root_path: Path | None = None) -> list[str]:
    """
    Return a list of all top-level Python packages in the project.

    Args:
        root_path (Optional[Path]): Optionally specify repo root. Defaults to auto-detection.

    Returns:
        list[str]: List of package names (e.g., 'civic_lib_core', 'civic_dev').
                   Returns empty list if no packages found.
    """
    try:
        root = root_path or find_project_root()
        src_dir = find_source_dir(root)

        if src_dir is None:
            logger.debug("No source directory found, returning empty package list")
            return []

        packages = get_valid_packages(src_dir)
        package_names = [p.name for p in packages]
        return package_names

    except Exception as e:
        logger.warning(f"Failed to get package names: {e}")
        return []


def get_source_dir(root_dir: Path) -> Path | None:
    """Alias for get_source_from_root for backward compatibility."""
    return find_source_dir(root_dir)


def get_valid_packages(src_dir: Path) -> list[Path]:
    """
    Return all top-level valid Python packages in the given directory.

    Args:
        src_dir (Path): Directory to search for packages.

    Returns:
        list[Path]: List of package directory paths.

    Raises:
        FileNotFoundError: If src_dir doesn't exist.
        ValueError: If no valid packages are found.
    """
    if not src_dir.exists() or not src_dir.is_dir():
        raise FileNotFoundError(f"Source directory does not exist: {src_dir}")

    packages = [p for p in src_dir.iterdir() if _is_python_package(p)]

    if not packages:
        raise ValueError(f"No valid Python packages found in: {src_dir}")

    logger.debug(f"Found packages: {[p.name for p in packages]}")
    return packages


def resolve_path(relative_path: str | Path) -> Path:
    """
    Resolve a relative path from the repo root.

    Args:
        relative_path (str | Path): Path to resolve.

    Returns:
        Path: Absolute path resolved from project root.

    Raises:
        RuntimeError: If project root cannot be found.
    """
    root = find_project_root()
    resolved = (root / Path(relative_path)).resolve()
    logger.debug(f"Resolved '{relative_path}' to: {resolved}")
    return resolved


def safe_filename(name: str, max_length: int = 255) -> str:
    """
    Convert a string into a safe, filesystem-compatible filename.

    Args:
        name (str): Original string.
        max_length (int): Maximum filename length. Defaults to 255.

    Returns:
        str: Sanitized filename.
    """
    if not name or not isinstance(name, str):
        return "unnamed"

    # Replace problematic characters
    safe_chars = []
    for char in name:
        if char.isalnum() or char in "._-":
            safe_chars.append(char.lower())
        elif char in " /\\:":
            safe_chars.append("_")
        # Skip other problematic characters

    result = "".join(safe_chars)

    # Handle edge cases
    if not result or result.startswith("."):
        result = "file_" + result

    # Truncate if too long
    if len(result) > max_length:
        result = result[:max_length].rstrip("_")

    # Ensure it doesn't end with just underscores
    result = result.rstrip("_") or "unnamed"

    logger.debug(f"Sanitized filename '{name}' to: '{result}'")
    return result
