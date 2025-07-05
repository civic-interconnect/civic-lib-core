"""
civic_lib_core/project_layout.py

Discover and verify basic project layout for any Civic Interconnect client repo.

MIT License — maintained by Civic Interconnect
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
    """
    Represents the layout of a project, including key directories and metadata.

    Attributes:
        project_root (Path): The root directory of the project.
        src_dir (Path | None): The source directory containing the main code, or None if not applicable.
        packages (list[Path]): A list of paths to package directories within the project.
        api_markdown_src_dir (Path): The directory containing API documentation *source* Markdown files
                                      (e.g., project_root/mkdocs_src/api).
        org_name (str | None): The name of the organization, or None if not specified.
        policy (dict): A dictionary containing project policy information.
    """

    project_root: Path
    src_dir: Path | None
    packages: list[Path]
    api_markdown_src_dir: Path
    org_name: str | None
    policy: dict


def discover_project_layout() -> ProjectLayout:
    """
    Return key layout paths for the current Civic Interconnect project.

    This function delegates the primary discovery to `fs_utils.discover_project_layout()`
    which is responsible for finding all necessary paths and loading the policy,
    then returns the structured ProjectLayout object.

    Returns:
        ProjectLayout: Structured layout information.
    """
    layout = fs_utils.discover_project_layout()
    return layout


def format_layout(layout: ProjectLayout) -> str:
    """
    Format layout info for display.

    Args:
        layout (ProjectLayout): The layout info to print.

    Returns:
        str: A formatted string for display.
    """
    parts = [
        f"Project Root:      {layout.project_root}",
        f"Org Name:          {layout.org_name or 'unknown'}",
        f"Source Directory:  {layout.src_dir or 'none'}",
        f"API Docs Source Dir: {layout.api_markdown_src_dir}",
        f"Policy file:       {layout.policy.get('__policy_path__', 'unknown')}",
        "Packages:",
        *(
            [f"  - {p.relative_to(layout.project_root)}" for p in layout.packages]
            or ["  (no packages found)"]
        ),
    ]
    return "\n".join(parts)


def verify_layout(layout: ProjectLayout) -> list[str]:
    """
    Verify layout assumptions for a Civic Interconnect repo.

    Args:
        layout (ProjectLayout): The discovered layout.

    Returns:
        list[str]: Any problems detected (empty list means all OK).
    """
    errors = []

    if not layout.project_root.exists():
        errors.append(f"Project root not found: {layout.project_root}")
    elif not layout.project_root.is_dir():
        errors.append(f"Project root is not a directory: {layout.project_root}")

    if layout.src_dir:
        if not layout.src_dir.exists():
            errors.append(f"Missing source directory: {layout.src_dir}")
        elif not layout.src_dir.is_dir():
            errors.append(f"Source directory is not a directory: {layout.src_dir}")
        elif not layout.packages:  # Check packages only if src_dir exists and is a directory
            errors.append(f"No Python packages found under: {layout.src_dir}")
    else:
        pass

    if not layout.api_markdown_src_dir.exists():
        errors.append(f"Missing API docs source directory: {layout.api_markdown_src_dir}")
    elif not layout.api_markdown_src_dir.is_dir():
        errors.append(
            f"API docs source directory is not a directory: {layout.api_markdown_src_dir}"
        )

    return get_errors(layout, errors)


def get_errors(layout, errors):
    policy_errors = []
    required_files = layout.policy.get("required_files", [])
    for f in required_files:
        if not (layout.project_root / f).exists():
            policy_errors.append(f"Required project file missing: {f}")
    if policy_errors:
        errors.append("Project policy violations:")
        errors.extend([f"  - {e}" for e in policy_errors])
    return errors


def main() -> None:
    """
    Standalone entry point for testing this layout module.
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
