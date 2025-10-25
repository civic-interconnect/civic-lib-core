"""Command-line tool to update version strings across key project files.

This tool replaces the old version with the new version in:
- VERSION
- pyproject.toml
- README.md

Usage:
    python -m cli.bump_version OLD_VERSION NEW_VERSION
    or as a subcommand: `civic-dev bump-version OLD_VERSION NEW_VERSION`
    or shorthand: `civic-dev bump OLD_VERSION NEW_VERSION`

File:   bump_version.py
Module: cli.bump_version
"""

from pathlib import Path
import sys

from civic_lib_core import log_utils

logger = log_utils.logger


def update_file(path: Path, old: str, new: str) -> bool:
    """Replace version string in the specified file if found.

    Returns:
        bool: True if file was modified, False otherwise.
    """
    if not path.exists():
        logger.info(f"Skipping: {path} (not found)")
        return False

    content = path.read_text(encoding="utf-8")
    updated = content.replace(old, new)

    if content != updated:
        path.write_text(updated, encoding="utf-8")
        logger.info(f"Updated: {path}")
        return True
    logger.info(f"No changes needed in: {path}")
    return False


def _bump_version(old_version: str, new_version: str) -> int:
    """Perform the version bump across all relevant files.

    Returns:
        int: Number of files updated.
    """
    files_to_update = [
        Path("pyproject.toml"),
        Path("README.md"),
        Path("VERSION"),
        Path("package.json"),
    ]

    return sum(update_file(path, old_version, new_version) for path in files_to_update)


def bump_version_cmd(old_version: str, new_version: str) -> int:
    """CLI subcommand handler for version bump.

    Returns:
        int: Exit code (0 on success, 1 if no updates).
    """
    updated = _bump_version(old_version, new_version)
    if updated:
        logger.info(f"{updated} file(s) updated.")
        return 0
    logger.info("No files were updated.")
    return 1


def main(old_version: str, new_version: str) -> int:
    """Script-style entry point.

    Returns:
        int: Exit code.
    """
    return bump_version_cmd(old_version, new_version)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        sys.exit(main(sys.argv[1], sys.argv[2]))
    else:
        print("Usage: python -m cli.bump_version OLD_VERSION NEW_VERSION")
        sys.exit(1)
