"""civic_lib_core/project_layout.py.

Discover and verify basic project layout for any Civic Interconnect client repo.
"""

from pathlib import Path
from typing import NamedTuple

from civic_lib_core import fs_utils

__all__ = [
    "discover_project_layout",
    "format_layout",
    "verify_layout",
    "ProjectLayout",
]


class ProjectLayout(NamedTuple):
    """Represents the layout of a Civic Interconnect project.

    Attributes:
        project_root (Path): Root directory of the project.
        src_dir (Path | None): Source directory, or None if not found.
        docs_dir (Path | None): Documentation directory, or None if not found.
        docs_api_dir (Path | None): API documentation source directory, or None if not found.
        packages (list[Path]): List of package directories under src_dir.
        org_name (str | None): Organization name, if detected.
        policy (dict): Loaded project policy data.
    """

    project_root: Path
    src_dir: Path | None
    docs_dir: Path | None
    docs_api_dir: Path | None
    packages: list[Path]
    org_name: str | None
    policy: dict


def discover_project_layout() -> ProjectLayout:
    """Discover and return the layout of the current Civic Interconnect project.

    Delegates to `fs_utils.discover_project_layout()` to perform actual discovery.

    Returns:
        ProjectLayout: Populated project layout info.
    """
    return fs_utils.discover_project_layout()


def format_layout(layout: ProjectLayout) -> str:
    """Format the layout info for display.

    Args:
        layout (ProjectLayout): The layout info to format.

    Returns:
        str: Formatted layout details.
    """
    parts = [
        f"Org:      {layout.org_name or 'unknown'}",
        f"Root:     {layout.project_root}",
        f"API Docs: {layout.docs_api_dir or 'none'}",
        f"Source:   {layout.src_dir or 'none'}",
        f"Policy:   {layout.policy.get('__policy_path__', 'unknown')}",
        "Packages:",
        *(
            [f"  - {p.relative_to(layout.project_root)}" for p in layout.packages]
            or ["  (no packages found)"]
        ),
    ]
    return "\n".join(parts)


def verify_layout(layout: ProjectLayout) -> list[str]:
    """Verify that the discovered layout satisfies expectations.

    Args:
        layout (ProjectLayout): The layout to check.

    Returns:
        list[str]: List of issues found (empty list means all OK).
    """
    errors: list[str] = []

    if not layout.project_root.exists():
        errors.append(f"Project root not found: {layout.project_root}")
    elif not layout.project_root.is_dir():
        errors.append(f"Project root is not a directory: {layout.project_root}")

    if layout.src_dir:
        if not layout.src_dir.exists():
            errors.append(f"Missing source directory: {layout.src_dir}")
        elif not layout.src_dir.is_dir():
            errors.append(f"Source directory is not a directory: {layout.src_dir}")
        elif not layout.packages:
            errors.append(f"No Python packages found under: {layout.src_dir}")

    if layout.docs_api_dir:
        if not layout.docs_api_dir.exists():
            errors.append(f"Missing API docs source directory: {layout.docs_api_dir}")
        elif not layout.docs_api_dir.is_dir():
            errors.append(f"API docs source directory is not a directory: {layout.docs_api_dir}")

    return errors


def main() -> None:
    """Standalone entry point for manual testing of this layout module.

    Prints layout and any issues found.
    """
    import sys

    try:
        layout = discover_project_layout()
        print("\n" + format_layout(layout) + "\n")

        issues = verify_layout(layout)
        if issues:
            print("\nProblems found:")
            for issue in issues:
                print(f"- {issue}")
            sys.exit(1)
        else:
            print("\nLayout verified successfully.")
            sys.exit(0)
    except Exception as e:
        print(
            f"\nAn error occurred during project layout discovery/verification: {e}",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
