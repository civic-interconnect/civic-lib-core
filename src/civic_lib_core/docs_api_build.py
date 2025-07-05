"""
civic_lib_core/docs_api_build.py

High-level utilities to orchestrate the generation of API documentation
for Civic Interconnect projects.

- Discovers Python packages in the project
- Generates Markdown and YAML API documentation into mkdocs_src/api
- Writes MkDocs configuration for publishing documentation sites

This script serves as the entry point for automated documentation builds.
"""

from pathlib import Path
from typing import TYPE_CHECKING, Any

from civic_lib_core import (
    docs_api_config,
    fs_utils,
    log_utils,
)

if TYPE_CHECKING:
    from civic_lib_core.project_layout import ProjectLayout

__all__ = [
    "generate_api_docs",
    "publish_api_docs",
]

logger = log_utils.logger


def generate_api_docs(source_pkg_path: Path, project_root: Path, policy: dict[str, Any]) -> None:
    """
    Generate Markdown API documentation for a single package.

    Writes output into mkdocs_src/api. This function is a wrapper for
    docs_api_config.generate_docs, ensuring 'markdown' format by default.

    Args:
        source_pkg_path (Path): The absolute path to the Python package directory to document.
        project_root (Path): The root directory of the project.
        policy (Dict[str, Any]): The loaded project policy.
    """
    docs_api_config.generate_docs(
        source_pkg_path=source_pkg_path,
        project_root=project_root,
        policy=policy,
        formats=["markdown"],
    )


def publish_api_docs() -> None:
    """
    One-liner to generate complete API documentation for release.

    - Discovers all Python packages in src/.
    - Generates Markdown & YAML docs for each into mkdocs_src/api.
    - Writes mkdocs.yml to repo root.
    - Writes index.md to mkdocs_src.
    """
    logger.info("Publishing API documentation for all packages...")

    try:
        # Discover project layout first to get all necessary info efficiently
        layout: ProjectLayout = fs_utils.discover_project_layout()

        project_root: Path = layout.project_root
        packages: list[Path] = layout.packages  # List of Path objects for packages
        api_markdown_src_dir: Path = layout.api_markdown_src_dir
        policy: dict = layout.policy  # Get the policy directly from the layout

        if not project_root:
            logger.error("Project root directory not found via discover_project_layout.")
            raise SystemExit(1)

        # --- Generate docs for each discovered package using docs_api_config.generate_docs ---
        if packages:
            for pkg_path in packages:
                logger.info(
                    f"Generating API docs for package: {pkg_path.name} (located at {pkg_path.relative_to(project_root)})"
                )
                # Call generate_api_docs with the Path object and resolved context
                generate_api_docs(
                    source_pkg_path=pkg_path, project_root=project_root, policy=policy
                )
        else:
            logger.warning(
                "No Python packages found in the project's src directory. Skipping API documentation generation for specific packages."
            )

        # Ensure index.md exists in the base mkdocs_src directory
        # This function now correctly leverages the policy and project_root
        _, mkdocs_base_src_dir = fs_utils.get_mkdocs_paths(policy, project_root)
        docs_api_config.write_index_md(mkdocs_base_src_dir)

        # --- Write mkdocs.yml config ---
        project_name: str = project_root.name
        docs_api_config.generate_mkdocs_config(
            project_name=project_name,
            root_dir=project_root,
            include_api_nav=True,
            policy=policy,  # Pass the policy obtained from layout
            mkdocs_base_src_dir=mkdocs_base_src_dir,  # Pass the base mkdocs source dir
            api_markdown_src_dir=api_markdown_src_dir,  # Pass the API markdown source dir
        )

        logger.info("API documentation published successfully.")

    except SystemExit as e:
        logger.error(f"Documentation publishing aborted: {e}")
        # Make sure to exit with the code from SystemExit
        import sys

        sys.exit(e.code)
    except Exception as e:
        logger.error(
            f"An unexpected error occurred during API documentation publishing: {e}", exc_info=True
        )
        import sys

        sys.exit(1)


if __name__ == "__main__":
    logger.info("Starting API documentation generation process...")
    publish_api_docs()
    logger.info("All documentation generation process completed.")
