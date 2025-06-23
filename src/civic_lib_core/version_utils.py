"""
version_utils.py

Tools for checking and reporting agent/library compatibility.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
"""

import re
from pathlib import Path

from civic_lib_core import log_utils

__all__ = [
    "bump_version",
    "check_version",
    "find_init_files",
    "get_lib_version",
    "get_version",
    "lib_version",
    "parse_version",
    "update_version_in_init",
    "update_version_string",
]

log_utils.init_logger()
logger = log_utils.logger


def bump_version(old_version: str, new_version: str) -> int:
    files_to_update = [
        Path("VERSION"),
        Path("pyproject.toml"),
        Path("README.md"),
    ]

    updated_count = sum(
        update_version_string(path, old_version, new_version) for path in files_to_update
    )

    # Update __version__ in all __init__.py files
    init_files = find_init_files(Path("."))
    for path in init_files:
        if update_version_in_init(path, new_version):
            updated_count += 1

    return updated_count


def check_version(agent_version: str, lib_version: str, strict: bool = False) -> bool:
    """
    Check compatibility of agent and lib versions using SemVer rules.

    Args:
        agent_version (str): Version string for the agent.
        lib_version (str): Version string for the shared library.
        strict (bool): If True, requires exact version match.

    Returns:
        bool: True if compatible, False otherwise.
    """
    try:
        agent_major, agent_minor, agent_patch = parse_version(agent_version)
        lib_major, lib_minor, lib_patch = parse_version(lib_version)
    except ValueError as e:
        logger.warning(str(e))
        return False

    if strict:
        if (agent_major, agent_minor, agent_patch) != (lib_major, lib_minor, lib_patch):
            logger.warning(f"Strict version mismatch: agent={agent_version}, lib={lib_version}")
            return False
        return True

    if agent_major != lib_major:
        logger.warning(f"Major version mismatch: agent={agent_version}, lib={lib_version}")
        return False

    return True


def find_init_files(root_dir: Path) -> list[Path]:
    """
    Recursively find all __init__.py files under the given directory.
    """
    return list(root_dir.rglob("__init__.py"))


def get_lib_version() -> str:
    """
    Get the current library version.

    Returns:
        str: The semantic version string (e.g., "1.2.3").
    """
    try:
        # Try to read from VERSION file first
        version_file = Path(__file__).parent / "VERSION"
        if version_file.exists():
            return version_file.read_text(encoding="utf-8").strip()

        # Fallback to reading from __init__.py
        init_file = Path(__file__).parent / "__init__.py"
        if init_file.exists():
            content = init_file.read_text(encoding="utf-8")
            match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)

        logger.warning("Could not determine library version")
        return "0.0.0"

    except Exception as e:
        logger.warning(f"Error reading library version: {e}")
        return "0.0.0"


def get_version() -> str:
    """Convenience alias for get_lib_version()."""
    return get_lib_version()


def lib_version() -> str:
    """Convenience alias for get_lib_version()."""
    return get_lib_version()


def parse_version(version: str) -> tuple[int, int, int]:
    """
    Parse a version string into a tuple of integers.

    Args:
        version (str): A semantic version string, e.g., "1.2.3".

    Returns:
        tuple[int, int, int]: A tuple of (major, minor, patch) version numbers.

    Raises:
        ValueError: If the version string is not in the expected format.
    """
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")
    major, minor, patch = match.groups()
    return int(major), int(minor), int(patch)


def update_version_in_init(path: Path, new_version: str) -> bool:
    """
    Update __version__ assignment in a given __init__.py file.
    Only works for simple string assignment: __version__ = "..."
    """
    content = path.read_text(encoding="utf-8")
    pattern = re.compile(r'(__version__\s*=\s*["\'])([\d.]+)(["\'])')
    updated_content, count = pattern.subn(rf"\1{new_version}\3", content)

    if count > 0:
        path.write_text(updated_content, encoding="utf-8")
        logger.info(f"Updated __version__ in {path}")
        return True
    return False


def update_version_string(path: Path, old: str, new: str) -> bool:
    if not path.exists():
        return False
    content = path.read_text(encoding="utf-8")
    updated = content.replace(old, new)
    if content != updated:
        path.write_text(updated, encoding="utf-8")
        return True
    return False
