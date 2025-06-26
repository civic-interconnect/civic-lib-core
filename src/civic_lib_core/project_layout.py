"""
project_layout.py

Discover and verify basic project layout.
"""

from pathlib import Path
from typing import NamedTuple

from civic_lib_core.fs_utils import find_project_root, get_repo_package_names


class ProjectLayout(NamedTuple):
    project_root: Path
    src_dir: Path
    packages: list[Path]
    docs_api_dir: Path


def discover_project_layout() -> ProjectLayout:
    """Return key layout paths for the current project."""
    project_root = find_project_root()
    src_dir = project_root / "src"
    docs_api_dir = project_root / "docs" / "api"

    packages = [src_dir / name for name in get_repo_package_names(project_root)]

    return ProjectLayout(
        project_root=project_root,
        src_dir=src_dir,
        packages=packages,
        docs_api_dir=docs_api_dir,
    )


def format_layout(layout: ProjectLayout) -> str:
    """Format layout info for display."""
    parts = [
        f"Project Root:     {layout.project_root}",
        f"Source Directory: {layout.src_dir}",
        f"Docs API Dir:     {layout.docs_api_dir}",
        "Packages:",
        *[f"  - {p}" for p in layout.packages],
    ]
    return "\n".join(parts)


def verify_layout(layout: ProjectLayout) -> list[str]:
    """Verify layout assumptions. Return list of errors (empty = all good)."""
    errors = []

    if not layout.src_dir.exists():
        errors.append(f"Missing source directory: {layout.src_dir}")

    if not layout.docs_api_dir.exists():
        errors.append(f"Missing docs/api directory: {layout.docs_api_dir}")

    if not layout.packages:
        errors.append(f"No packages with __init__.py found in: {layout.src_dir}")

    return errors
