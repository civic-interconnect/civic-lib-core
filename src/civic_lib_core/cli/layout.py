"""CLI utility to discover and print the Civic Interconnect project layout.

File: layout.py
"""

import sys

from civic_lib_core import log_utils, project_layout

logger = log_utils.logger


def main() -> None:
    """Discover and print the project layout.

    Prints a formatted summary of:
    - Project root
    - Docs directories
    - Source packages
    - Organization name
    - Policy file used
    """
    try:
        layout = project_layout.discover_project_layout()
        print()
        print(project_layout.format_layout(layout))
    except Exception as e:
        logger.error(f"Failed to discover project layout: {e}")
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
