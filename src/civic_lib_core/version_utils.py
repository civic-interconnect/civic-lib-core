"""civic_lib_core/version_utils.py.

Version discovery utilities for Civic Interconnect projects.

Supports:
- Python projects (via importlib.metadata or pyproject.toml)
- Non-Python projects (via VERSION file)
- JavaScript/NodeJS projects (via package.json)

This allows the Civic CLI and shared tools to work seamlessly across mixed
technology stacks, ensuring consistent version handling even in frontend-only
repos.

"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as get_python_version
import json
from pathlib import Path
import tomllib

from civic_lib_core import fs_utils, log_utils

__all__ = ["get_repo_version"]

logger = log_utils.logger


def get_version_from_python_metadata(package_name: str) -> str | None:
    """Try reading the version from installed Python package metadata."""
    try:
        version_str = get_python_version(package_name)
        logger.info(f"Version found via Python metadata: {version_str}")
        return version_str
    except PackageNotFoundError:
        logger.debug(f"Package {package_name} not installed.")
    except Exception as e:
        logger.warning(f"Unexpected error reading Python version metadata: {e}")
    return None


def get_version_from_files(root: Path) -> str | None:
    """Check pyproject.toml, VERSION, or package.json for the project version."""
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        try:
            with pyproject.open("rb") as f:
                data = tomllib.load(f)
            version_str = data.get("project", {}).get("version")
            if version_str:
                logger.info(f"Version found in pyproject.toml: {version_str}")
                return version_str
        except Exception as e:
            logger.warning(f"Error parsing pyproject.toml: {e}")

    version_file = root / "VERSION"
    if version_file.exists():
        try:
            version_str = version_file.read_text(encoding="utf-8").strip()
            if version_str:
                logger.info(f"Version found in VERSION file: {version_str}")
                return version_str
        except Exception as e:
            logger.warning(f"Error reading VERSION file: {e}")

    package_json = root / "package.json"
    if package_json.exists():
        try:
            data = json.loads(package_json.read_text(encoding="utf-8"))
            version_str = data.get("version")
            if version_str:
                logger.info(f"Version found in package.json: {version_str}")
                return version_str
        except Exception as e:
            logger.warning(f"Error reading package.json: {e}")

    return None


def get_repo_version(
    package_name: str = "civic-lib-core",
    root_dir: Path | None = None,
) -> str:
    """Retrieve the project version from various sources.

    1. Python metadata (if package installed)
    2. pyproject.toml
    3. VERSION file
    4. package.json.

    Returns:
        str: The discovered version string, or "0.0.0" if none found.
    """
    # 1. Check Python metadata
    version_str = get_version_from_python_metadata(package_name)
    if version_str:
        return version_str

    # 2. Determine root
    try:
        root = root_dir or fs_utils.get_project_root()
    except Exception as e:
        logger.warning(f"Could not detect project root. Defaulting to cwd. Error: {e}")
        root = Path.cwd()

    # 3. Check files in root
    version_str = get_version_from_files(root)
    if version_str:
        return version_str

    logger.info("No version found in repo. Defaulting to 0.0.0")
    return "0.0.0"
