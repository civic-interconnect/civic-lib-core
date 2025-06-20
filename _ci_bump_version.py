"""
_ci_bump_version.py

Update version strings across multiple project files.

Usage:
    python _ci_bump_version.py 0.1.0 0.2.0
"""

import sys
from pathlib import Path


def update_file(path: Path, old: str, new: str) -> None:
    """Replace version string in the specified file if needed."""
    if not path.exists():
        print(f"Skipping: {path} (not found)")
        return

    content = path.read_text()
    updated = content.replace(old, new)

    if content != updated:
        path.write_text(updated)
        print(f"Updated {path}")
    else:
        print(f"No change needed in {path}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python _ci_bump_version.py OLD_VERSION NEW_VERSION")
        sys.exit(1)

    old_version, new_version = sys.argv[1], sys.argv[2]

    files_to_update = [
        Path("VERSION"),
        Path("pyproject.toml"),
        Path("setup.cfg"),
        Path("README.md"),
    ]

    for path in files_to_update:
        update_file(path, old_version, new_version)


if __name__ == "__main__":
    main()
