"""
project_checks.py

Run structural and policy checks on the project.
"""

from civic_lib_core import project_layout


def run_all_checks() -> list[str]:
    """Run all project-level checks and return a list of issues."""
    issues = []
    layout = project_layout.discover_project_layout()
    layout_errors = project_layout.verify_layout(layout)
    issues.extend(layout_errors)

    # TODO: Add more checks here as needed
    # For example:
    # - Check for required files (README.md, pyproject.toml)
    # - Check that no .py files exist outside packages

    return issues
