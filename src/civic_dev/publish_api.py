# publish_api.py

"""
Generate and update application interface documentation.

This script:
- Locates project root
- Extracts public API from source
- Writes Markdown and YAML summaries to mkdocs_src/api/
- Generates mkdocs.yml and index.md
- **Does NOT perform the final `mkdocs build` to HTML; that's a separate step.**
"""

import sys

from civic_lib_core import (
    docs_api_build,
    log_utils,
)

logger = log_utils.logger


def main() -> int:
    """
    Regenerate summary and reference API documentation for all packages in src/.
    The generated Markdown and YAML files are placed into the MkDocs source directory
    (typically `mkdocs_src/api/`).

    Returns:
        int: exit code (0 if successful, nonzero otherwise)
    """
    logger.info("Generating API documentation...")

    try:
        # The entire orchestration logic is now encapsulated within publish_api_docs
        docs_api_build.publish_api_docs()

        logger.info("API documentation source files generated successfully.")
        logger.info("To build the final HTML documentation, run 'mkdocs build'.")
        return 0

    except SystemExit as e:
        # Catch SystemExit specifically, which publish_api_docs might raise for controlled exits
        logger.error(f"Documentation publishing aborted: {e}")
        return int(e.code) if e.code is not None else 1
    except Exception as e:
        logger.error(f"An unexpected error occurred during API generation: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
