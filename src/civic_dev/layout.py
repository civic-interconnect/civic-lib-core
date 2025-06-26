"""
layout.py

Project layout discovery and verification logic.
"""

from civic_lib_core import project_layout


def main() -> None:
    """Discover and print the project layout."""
    layout = project_layout.discover_project_layout()
    print(project_layout.format_layout(layout))
