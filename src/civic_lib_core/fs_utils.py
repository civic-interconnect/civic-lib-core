"""civic_lib_core/fs_utils.py.

File and path utility functions for root-relative logic.
Unified utilities used across Civic Interconnect agents and libraries.

"""

from pathlib import Path

from civic_lib_core import log_utils
from civic_lib_core.project_layout import ProjectLayout
from civic_lib_core.project_policy import load_project_policy

__all__ = [
    "discover_project_layout",
    "ensure_dir",
    "get_data_config_dir",
    "get_docs_dir",
    "get_docs_api_dir",
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
    """Discover and analyze the project layout structure.

    Scans the project directory to identify key components including the project root,
    documentation directories, source code location, valid packages, organization name,
    and project policy configuration.

    Returns:
        ProjectLayout: A comprehensive object containing all discovered project structure
            information including:
            - project_root: The root directory of the project
            - docs_dir: Main documentation directory
            - docs_api_dir: API documentation directory
            - src_dir: Source code directory
            - packages: List of valid Python packages found
            - org_name: Organization name associated with the project
            - policy: Loaded project policy configuration

    Note:
        This function performs automatic discovery and may return empty collections
        or None values for components that are not found or configured in the project.
    """
    root = get_project_root()
    policy = load_project_policy(root)
    docs_dir = get_docs_dir(root)
    docs_api_dir = get_docs_api_dir(root)
    src = get_source_dir(root)
    packages = get_valid_packages(src) if src else []
    org_name = get_org_name(root)

    layout = ProjectLayout(
        project_root=root,
        docs_dir=docs_dir,
        docs_api_dir=docs_api_dir,
        src_dir=src,
        packages=packages,
        org_name=org_name,
        policy=policy,
    )

    logger.debug(f"Discovered project layout: {layout}")
    return layout


def _is_python_package(path: Path) -> bool:
    if not path.is_dir():
        return False

    if (path / "__init__.py").exists():
        return True

    py_files = list(path.glob("*.py"))
    if py_files:
        logger.debug(f"Found namespace package: {path.name}")
        return True

    return False


def ensure_dir(path: str | Path) -> Path:
    """Ensure a directory exists, creating it and any parent directories if necessary.

    Args:
        path (str | Path): The directory path to ensure exists. Can be a string or Path object.

    Returns:
        Path: The resolved Path object of the created/existing directory.

    Raises:
        OSError: If the directory cannot be created due to permissions or other filesystem issues.

    Example:
        >>> ensure_dir("/path/to/new/directory")
        PosixPath('/path/to/new/directory')

        >>> ensure_dir(Path("relative/path"))
        PosixPath('/absolute/path/to/relative/path')
    """
    try:
        path = Path(path).resolve()
        path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured directory exists: {path}")
        return path
    except OSError as e:
        logger.error(f"Failed to create directory {path}: {e}")
        raise


def get_data_config_dir(project_root: Path | None = None) -> Path:
    """Get the data configuration directory path.

    Args:
        project_root (Path | None, optional): The project root directory.
            If None, uses the discovered project root. Defaults to None.

    Returns:
        Path: The path to the data-config directory.
    """
    root = project_root or get_project_root()
    return root / "data-config"


def get_docs_dir(root_dir: Path | None = None) -> Path:
    """Determine the project's main docs directory.

    Tries:
    1. Client repo policy (docs.site_dir or docs.docs_dir)
    2. Defaults to 'docs'
    """
    root_dir = root_dir or get_project_root()
    policy = load_project_policy(root_dir)

    docs_dir_name = (
        policy.get("docs", {}).get("site_dir") or policy.get("docs", {}).get("docs_dir") or "docs"
    )
    docs_dir = root_dir / docs_dir_name

    if docs_dir.exists() and docs_dir.is_dir():
        logger.debug(f"Docs dir found: {docs_dir}")
        return docs_dir

    fallback = root_dir / "docs"
    logger.debug(f"Defaulting docs dir to: {fallback}")
    return fallback


def get_docs_api_dir(root_dir: Path | None = None, create: bool = False) -> Path:
    """Determine the project's API docs subdirectory.

    Tries:
    1. Client repo policy (docs.api_markdown_subdir)
    2. Defaults to 'docs/api'
    """
    root_dir = root_dir or get_project_root()
    docs_dir = get_docs_dir(root_dir)
    policy = load_project_policy(root_dir)

    api_subdir = policy.get("docs", {}).get("api_markdown_subdir", "api")
    candidate = docs_dir / api_subdir

    logger.debug(f"API docs dir resolved to: {candidate}")
    return ensure_dir(candidate) if create else candidate


def get_org_name(project_root: Path) -> str | None:
    """Get the organization name from the project root's parent directory.

    Args:
        project_root (Path): The root directory path of the project.

    Returns:
        str | None: The name of the parent directory if it exists, otherwise None.
    """
    return project_root.parent.name if project_root.parent and project_root.parent.name else None


def get_project_root(start_path: Path | None = None) -> Path:
    """Find the project root directory by searching for common project markers.

    Args:
        start_path (Path | None, optional): The starting directory for the search.
            If None, uses the current working directory. Defaults to None.

    Returns:
        Path: The resolved path to the project root directory.

    Raises:
        RuntimeError: If no project root is found by searching upward from the start path.
    """
    current = start_path or Path.cwd()
    markers = [".git", "pyproject.toml"]

    for parent in [current] + list(current.parents):
        for marker in markers:
            if (parent / marker).exists():
                logger.debug(f"Project root found at: {parent.resolve()} (marker: {marker})")
                return parent.resolve()

    raise RuntimeError(
        f"Project root not found. Searched from '{current.resolve()}' upward for markers: {markers}."
    )


def get_repo_package_names(root_path: Path | None = None) -> list[str]:
    """Discover all Python package names under the repo's src directory.

    Returns:
        List[str]: Fully qualified package names, e.g. ['civic_lib_core', 'civic_lib_core.cli']
    """
    try:
        root = root_path or get_project_root()
        src_dir = get_source_dir(root)
        if src_dir is None:
            logger.debug("No source directory found, returning empty package list.")
            return []

        packages: list[str] = []

        for init_file in src_dir.rglob("__init__.py"):
            # Compute relative path from src/ to the package folder
            pkg_path = init_file.parent.relative_to(src_dir)
            if pkg_path.parts:
                package_name = ".".join(pkg_path.parts)
                packages.append(package_name)

        if not packages:
            logger.warning("No packages discovered under src.")

        return sorted(packages)

    except Exception as e:
        logger.warning(f"Failed to get package names: {e}")
        return []


def get_runtime_config_path(project_root: Path | None = None) -> Path:
    """Get the runtime configuration file path.

    Args:
        project_root (Path | None, optional): The project root directory.
            If None, uses the discovered project root. Defaults to None.

    Returns:
        Path: The path to the runtime_config.yaml file.
    """
    root = project_root or get_project_root()
    return root / "runtime_config.yaml"


def get_source_dir(root_dir: Path) -> Path | None:
    """Get the source directory containing Python packages for the project.

    Args:
        root_dir (Path): The root directory path of the project.

    Returns:
        Path | None: The path to the source directory if found and contains valid
            Python packages, otherwise None.
    """
    policy = load_project_policy(root_dir)
    src_dirs_config = policy.get("build", {}).get("src_dirs", ["src"])

    candidates = []
    if isinstance(src_dirs_config, str):
        candidates.append(root_dir / src_dirs_config)
    elif isinstance(src_dirs_config, list):
        candidates.extend([root_dir / s for s in src_dirs_config])

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
        f"No valid source directory with Python packages found in {root_dir} "
        f"based on policy {src_dirs_config} or default 'src'."
    )
    return None


def get_valid_packages(src_dir: Path) -> list[Path]:
    """Get all valid Python packages found in the source directory.

    Args:
        src_dir (Path): The source directory to search for Python packages.

    Returns:
        list[Path]: A list of Path objects representing valid Python packages.
            Returns an empty list if no packages are found or if the source
            directory doesn't exist.
    """
    if not src_dir.exists() or not src_dir.is_dir():
        logger.warning(f"Source directory does not exist or is not a directory: {src_dir}")
        return []

    packages = [p for p in src_dir.iterdir() if _is_python_package(p)]
    if not packages:
        logger.debug(f"No valid Python packages found in: {src_dir}")
        return []

    logger.debug(f"Found packages: {[p.name for p in packages]}")
    return packages


def resolve_path(relative_path: str | Path) -> Path:
    """Resolve a relative path against the project root directory.

    Args:
        relative_path (str | Path): The relative path to resolve. Can be a string or Path object.

    Returns:
        Path: The resolved absolute path relative to the project root.

    Example:
        >>> resolve_path("src/package")
        PosixPath('/absolute/path/to/project/src/package')
    """
    root = get_project_root()
    resolved = (root / Path(relative_path)).resolve()
    logger.debug(f"Resolved '{relative_path}' to: {resolved}")
    return resolved


def safe_filename(name: str, max_length: int = 255) -> str:
    """Create a safe filename by sanitizing input string.

    Args:
        name (str): The original filename or string to sanitize.
        max_length (int, optional): Maximum length of the resulting filename. Defaults to 255.

    Returns:
        str: A sanitized filename safe for filesystem use, containing only alphanumeric
            characters, dots, underscores, and hyphens. Spaces and path separators
            are converted to underscores.

    Example:
        >>> safe_filename("My File/Name:Test")
        'my_file_name_test'

        >>> safe_filename("", 10)
        'unnamed'
    """
    if not name:
        return "unnamed"

    safe_chars = []
    for char in name:
        if char.isalnum() or char in "._-":
            safe_chars.append(char.lower())
        elif char in " /\\:":
            safe_chars.append("_")

    result = "".join(safe_chars)
    if not result:
        result = "file"
    if result.startswith("."):
        result = "_" + result
    if len(result) > max_length:
        result = result[:max_length].rstrip("_")
    result = result.rstrip("_") or "unnamed"

    logger.debug(f"Sanitized filename '{name}' to: '{result}'")
    return result
