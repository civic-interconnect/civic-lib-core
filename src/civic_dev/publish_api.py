"""
publish_api.py

Generate and update application interface documentation.

This script:
- Locates project root
- Extracts public API from source
- Writes Markdown and YAML summaries
- Generates mkdocs.yml and index.md
"""

import sys
from pathlib import Path
from typing import Any

from civic_lib_core import (
    docs_api_config,
    docs_api_extract,
    docs_api_render,
    fs_utils,
    log_utils,
)

logger = log_utils.logger


def main() -> None:
    """
    Regenerate summary and reference API documentation for all packages in src/.
    """
    logger.info("Generating API documentation...")

    try:
        root_dir: Path | None = fs_utils.find_project_root()
        if not root_dir:
            logger.error("Project root directory not found.")
            return

        src_dir: Path = root_dir / "src"
        if not src_dir.exists():
            logger.error(f"Source root not found: {src_dir}")
            return

        output_dir: Path = root_dir / "docs" / "api"
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"To: {output_dir}")

        package_names: list[str] = fs_utils.get_repo_package_names(root_dir)
        if not package_names:
            logger.error("No packages with __init__.py found under src/.")
            return

        all_modules_info: dict[str, dict[str, Any]] = {}

        for pkg_name in package_names:
            pkg_path: Path = src_dir / pkg_name
            logger.debug(f"Processing package: {pkg_name} at {pkg_path}")
            if not pkg_path.exists():
                logger.warning(f"Package path does not exist: {pkg_path}")
                continue

            modules_info = docs_api_extract.extract_module_api(pkg_path)

            # Prefix keys with package name
            namespaced_info = {f"{pkg_name}.{k}": v for k, v in modules_info.items()}
            all_modules_info.update(namespaced_info)

        # Write docs for all packages together
        docs_api_render.write_markdown_docs(all_modules_info, output_dir)
        docs_api_render.write_yaml_summary(all_modules_info, output_dir)

        # Generate mkdocs.yml configuration in the project root
        logger.debug("Generating mkdocs.yml configuration...")
        project_name: str = root_dir.name
        docs_api_config.generate_mkdocs_config(project_name, root_dir, output_dir)

        # Write index.md for the docs directory
        logger.debug("Writing index.md for documentation...")
        docs_dir = root_dir / "docs"
        if not docs_dir.exists():
            docs_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Writing index.md to {docs_dir}")
        docs_api_config.write_index_md(docs_dir)

        logger.info("API documentation generation complete.")

    except Exception as e:
        logger.error(f"Error during API generation: {e}")
        logger.info("Failed to generate API documentation.")


if __name__ == "__main__":
    sys.exit(main())
