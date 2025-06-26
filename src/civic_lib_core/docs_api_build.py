"""
civic_lib_core/doc_utils.py

Core development utilities.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
"""

from pathlib import Path

from civic_lib_core import (
    docs_api_config,
    fs_utils,
    log_utils,
)
from civic_lib_core.docs_api_config import generate_docs

__all__ = [
    "generate_api_docs",
    "publish_api_docs",
]

logger = log_utils.logger


def generate_api_docs(source_dir_str: str = "civic_lib_core", output_dir_str: str = "api"):
    """Generate Markdown API documentation (backward compatibility)."""
    generate_docs(source_dir_str, output_dir_str, formats=["markdown"])


def publish_api_docs() -> None:
    """
    One-liner to generate complete API documentation for release.
    """
    logger.info("Publishing API documentation...")

    try:
        project_root: Path | None = fs_utils.find_project_root()
        if not project_root:
            logger.error("Project root directory not found.")
            raise SystemExit(1)

        package_names: list[str] = fs_utils.get_repo_package_names(project_root)

        if not package_names:
            logger.error("No packages detected in src/. Nothing to document.")
            raise SystemExit(1)

        for package_name in package_names:
            generate_docs(package_name, formats=["yaml", "markdown"])

        project_name: str = project_root.name
        output_dir: Path = fs_utils.ensure_docs_output_dir(str(project_root))
        docs_api_config.generate_mkdocs_config(project_name, project_root, output_dir)

        logger.info("API documentation published successfully.")

    except Exception as e:
        logger.error(f"Error publishing API documentation: {e}")
        raise


if __name__ == "__main__":
    publish_api_docs()
    logger.info("All documentation generated.")
