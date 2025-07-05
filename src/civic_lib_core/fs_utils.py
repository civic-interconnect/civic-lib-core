"""
civic_lib_core/fs_utils.py

File and path utility functions for root-relative logic.
Unified utilities used across Civic Interconnect agents and libraries.

MIT License — maintained by Civic Interconnect
"""

from pathlib import Path

from civic_lib_core import log_utils
from civic_lib_core.project_layout import ProjectLayout  # Import the ProjectLayout NamedTuple
from civic_lib_core.project_policy import load_project_policy  # Needed for policy in ProjectLayout

__all__ = [
    "discover_project_layout",
    "ensure_dir",
    "ensure_docs_output_dir",  # final HTML output dir (docs/)
    "find_project_root",  # deprecated, kept for compatibility
    "find_source_dir",  # deprecated, kept for compatibility
    "get_api_markdown_source_dir",  # mkdocs_src/api
    "get_data_config_dir",
    "get_mkdocs_paths",  # (mkdocs.yml, mkdocs_src/)
    "get_org_name",
    "get_project_root",
    "get_repo_package_names",
    "get_runtime_config_path",
    "get_source_dir",
    "get_valid_packages",
    "resolve_path",
    "safe_filename",
]

logger = log_utils.logger


def discover_project_layout() -> ProjectLayout:
    """
    Dynamically discovers and returns key layout paths and information for
    the current Civic Interconnect project, encapsulated in a ProjectLayout NamedTuple.

    This function performs the following steps:
    1. Determines the project root directory.
    2. Loads the project policy configuration.
    3. Identifies the primary source directory (e.g., 'src/').
    4. Lists all top-level Python packages within the source directory.
    5. Calculates the path to the API documentation *source* directory (mkdocs_src/api).
    6. Attempts to determine the organization name associated with the project.

    The returned ProjectLayout object provides structured, type-hinted access
    to these essential project paths and configurations, simplifying their
    consumption by other parts of the system and improving type safety.

    Returns:
        ProjectLayout: A NamedTuple containing structured layout information,
                        including project_root, src_dir, packages, docs_api_dir,
                        org_name, and the loaded policy.
    """
    root = get_project_root()
    policy = load_project_policy(root)
    src = get_source_dir(root)
    packages = get_valid_packages(src) if src else []
    docs_api_markdown_src_dir = get_api_markdown_source_dir(policy, root)
    org_name = get_org_name(root)

    layout = ProjectLayout(
        project_root=root,
        src_dir=src,
        packages=packages,
        api_markdown_src_dir=docs_api_markdown_src_dir,
        org_name=org_name,
        policy=policy,
    )

    logger.debug(f"Discovered project layout: {layout}")
    return layout


def _is_python_package(path: Path) -> bool:
    """
    Check if a directory is a valid Python package.

    A valid package has __init__.py or is a namespace package with .py files.
    """
    if not path.is_dir():
        return False

    if (path / "__init__.py").exists():
        return True

    # Namespace package with Python files
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
        OSError: If directory cannot be created.
    """
    try:
        path = Path(path).resolve()
        path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured directory exists: {path}")
        return path
    except OSError as e:
        logger.error(f"Failed to create directory {path}: {e}")
        raise


def ensure_docs_output_dir(project_root: Path | None = None, policy: dict | None = None) -> Path:
    """
    Ensures the *final HTML output directory* for MkDocs exists.
    This is typically `project_root/docs/`, as defined in the project policy.

    Args:
        project_root (Optional[Path]): The project root directory. If None, it will be discovered internally.
        policy (Optional[dict]): The loaded project policy. If None, it will be loaded internally.

    Returns:
        Path: The created or existing path to the main HTML output directory.

    Raises:
        Exception: If the directory cannot be located or created.
    """
    try:
        # Discover project_root if not provided
        actual_project_root = project_root or get_project_root()

        # Load policy if not provided
        actual_policy = policy or load_project_policy(actual_project_root)

        # Get the site_dir from policy, defaulting to "docs"
        site_dir_name = actual_policy.get("docs", {}).get("site_dir", "docs")
        final_html_output_dir = actual_project_root / site_dir_name

        logger.debug(f"Ensuring final HTML output directory: {final_html_output_dir.resolve()}")
        return ensure_dir(final_html_output_dir)
    except Exception as e:
        logger.error(f"Failed to ensure final HTML output directory: {e}")
        raise


def get_api_markdown_source_dir(policy: dict | None = None, root_dir: Path | None = None) -> Path:
    """
    Determines the specific directory within mkdocs_src where API Markdown files should go.
    This is the target for the Python script generating API Markdown.

    Args:
        policy (Optional[dict]): The loaded project policy. If None, it will be loaded internally.
        root_dir (Optional[Path]): The project root directory. If None, it will be discovered internally.

    Returns:
        Path: The absolute path to the API Markdown source directory (e.g., project_root/mkdocs_src/api).
    """
    actual_root_dir = root_dir or get_project_root()
    actual_policy = policy or load_project_policy(actual_root_dir)

    _, mkdocs_source_root_dir = get_mkdocs_paths(actual_policy, actual_root_dir)

    api_source_dir_rel = actual_policy.get("docs", {}).get("api_markdown_subdir", "api")
    api_markdown_output_dir = mkdocs_source_root_dir / api_source_dir_rel
    logger.debug(f"API Markdown source directory (calculated): {api_markdown_output_dir.resolve()}")
    return ensure_dir(api_markdown_output_dir)


def get_data_config_dir(project_root: Path | None = None) -> Path:
    """
    Return the standard data-config folder path for the repo.

    Args:
        project_root (Path | None): Optionally provide the repo root.

    Returns:
        Path: Full path to <repo-root>/data-config.
    """
    root = project_root or get_project_root()
    data_config_dir = root / "data-config"
    return data_config_dir


def get_mkdocs_paths(policy: dict, project_root: Path) -> tuple[Path, Path]:
    """
    Return paths to mkdocs.yml and the mkdocs source folder based on policy.

    Args:
        policy (dict): Loaded project policy.
        project_root (Path): Root of the repo.

    Returns:
        Tuple[Path, Path]: (mkdocs_config_file_path, mkdocs_src_path)
    """
    # Access these from the 'docs' section of the policy
    mkdocs_file_name = policy.get("docs", {}).get("mkdocs_config", "mkdocs.yml")
    mkdocs_src_dir_name = policy.get("docs", {}).get("mkdocs_src_dir", "mkdocs_src")

    mkdocs_config_file_path = project_root / mkdocs_file_name
    mkdocs_src_path = project_root / mkdocs_src_dir_name

    logger.debug(f"get_mkdocs_paths: Config file: {mkdocs_config_file_path.resolve()}")
    logger.debug(f"get_mkdocs_paths: Docs Source Dir: {mkdocs_src_path.resolve()}")
    return mkdocs_config_file_path, mkdocs_src_path


def get_org_name(project_root: Path) -> str | None:
    """
    Return the organization folder name, assuming the repo path
    follows /path/to/<org>/<repo> convention.

    Args:
        project_root (Path): The project root path.

    Returns:
        Optional[str]: Organization name, or None if not found.
    """
    parent = project_root.parent
    if parent and parent.name != "":
        return parent.name
    return None


def get_project_root(start_path: Path | None = None) -> Path:
    """
    Return the root of the repo based on common markers.

    Searches for markers like .git or pyproject.toml in the current
    directory and its parents.

    Args:
        start_path (Optional[Path]): Directory to start search from. Defaults to cwd.

    Returns:
        Path: Project root directory.

    Raises:
        RuntimeError: If project root cannot be found based on the markers.
    """
    current = start_path or Path.cwd()

    # Define the markers that signify a project root
    markers = [".git", "pyproject.toml"]

    # Traverse up the directory tree
    for parent in [current] + list(current.parents):
        # Check if any of the markers exist in the current parent directory
        for marker in markers:
            if (parent / marker).exists():
                logger.debug(f"Project root found at: {parent.resolve()} (marker: {marker})")
                return parent.resolve()

    # If the loop completes without finding a marker, raise an error
    raise RuntimeError(
        f"Project root not found. Searched from '{current.resolve()}' upward for markers: {markers}. "
        f"A '{markers[0]}' directory or '{markers[1]}' file is required to mark your project root."
    )


def get_repo_package_names(root_path: Path | None = None) -> list[str]:
    """
    Return a list of all top-level Python packages in the project.

    Args:
        root_path (Optional[Path]): Optionally specify repo root. Defaults to auto-detection.

    Returns:
        list[str]: List of package names (e.g. 'civic_lib_core', 'civic_dev').
    """
    try:
        root = root_path or get_project_root()
        src_dir = get_source_dir(root)

        if src_dir is None:
            logger.debug("No source directory found, returning empty package list")
            return []

        packages = get_valid_packages(src_dir)
        package_names = [p.name for p in packages]
        return package_names

    except Exception as e:
        logger.warning(f"Failed to get package names: {e}")
        return []


def get_runtime_config_path(project_root: Path | None = None) -> Path:
    """
    Return the path to runtime_config.yaml under the project root.

    Args:
        project_root (Path | None): Optionally provide the repo root.

    Returns:
        Path: Full path to <repo-root>/runtime_config.yaml.
    """
    root = project_root or get_project_root()
    return root / "runtime_config.yaml"


def get_source_dir(root_dir: Path) -> Path | None:
    """
    Return the source directory containing Python packages under src/.

    Args:
        root_dir (Path): Project root directory

    Returns:
        Optional[Path]: The source directory if found, otherwise None.
    """
    # Policy can specify src_dirs, otherwise default to 'src'
    # Assuming discover_project_layout or load_project_policy makes policy available
    # For standalone use, load it here
    policy = load_project_policy(root_dir)
    src_dirs_config = policy.get("build", {}).get("src_dirs", ["src"])

    candidates = []
    if isinstance(src_dirs_config, str):
        candidates.append(root_dir / src_dirs_config)
    elif isinstance(src_dirs_config, list):
        candidates.extend([root_dir / s for s in src_dirs_config])

    # Fallback if policy doesn't specify or is empty
    if not candidates and (root_dir / "src").is_dir():
        candidates.append(root_dir / "src")

    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            packages = [p for p in candidate.iterdir() if p.is_dir() and _is_python_package(p)]
            if packages:
                logger.debug(
                    f"Source directory: {candidate} with packages: {[p.name for p in packages]}"
                )
                return candidate

    logger.warning(
        f"No valid source directory with Python packages found in {root_dir} based on policy {src_dirs_config} or default 'src'."
    )
    return None


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
        logger.warning(f"Source directory does not exist or is not a directory: {src_dir}")
        return []  # Return empty list

    packages = [p for p in src_dir.iterdir() if _is_python_package(p)]

    if not packages:
        logger.debug(f"No valid Python packages found in: {src_dir}")
        return []  # Return empty list

    logger.debug(f"Found packages: {[p.name for p in packages]}")
    return packages


def resolve_path(relative_path: str | Path) -> Path:
    """
    Resolve a relative path from the repo root.

    Args:
        relative_path (str | Path): Path to resolve.

    Returns:
        Path: Absolute path resolved from project root.
    """
    root = get_project_root()
    resolved = (root / Path(relative_path)).resolve()
    logger.debug(f"Resolved '{relative_path}' to: {resolved}")
    return resolved


def safe_filename(name: str, max_length: int = 255) -> str:
    """
    Convert a string into a safe, filesystem-compatible filename.

    Args:
        name (str): Original string.
        max_length (int): Maximum filename length.

    Returns:
        str: Sanitized filename.
    """
    if not name or not isinstance(name, str):
        return "unnamed"

    safe_chars = []
    for char in name:
        if char.isalnum() or char in "._-":
            safe_chars.append(char.lower())
        elif char in " /\\:":  # Replace common path/forbidden chars with underscore
            safe_chars.append("_")

    result = "".join(safe_chars)

    # Ensure it's not empty or starts with a forbidden char
    if not result:
        result = "file"
    if result.startswith("."):  # Prevent hidden files unless intended
        result = "_" + result

    if len(result) > max_length:
        result = result[:max_length].rstrip("_")  # Remove trailing underscores from truncation

    result = result.rstrip("_") or "unnamed"  # Final check for empty after rstrip or just "_"

    logger.debug(f"Sanitized filename '{name}' to: '{result}'")
    return result


# ----------------------------------------
# DEPRECATED ALIASES FOR BACKWARD COMPATIBILITY
# ----------------------------------------


def find_project_root(start_path: Path | None = None) -> Path:
    """
    DEPRECATED: Use get_project_root instead.
    """
    logger.warning("find_project_root() is deprecated. Use get_project_root().")
    return get_project_root(start_path)


def find_source_dir(root_dir: Path) -> Path | None:
    """
    DEPRECATED: Use get_source_dir instead.
    """
    logger.warning("find_source_dir() is deprecated. Use get_source_dir().")
    return get_source_dir(root_dir)
