"""
civic_lib_core/doc_utils.py

Core development utilities.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
"""

from pathlib import Path

import yaml

from civic_lib_core import log_utils
from civic_lib_core.docs_api_extract import extract_module_api
from civic_lib_core.docs_api_render import write_markdown_docs, write_yaml_summary
from civic_lib_core.fs_utils import (
    ensure_dir,
    ensure_docs_output_dir,
)

__all__ = [
    "build_api_nav",
    "generate_docs",
    "generate_mkdocs_config",
    "generate_summary_yaml",
    "write_index_md",
]

logger = log_utils.logger


def _get_index_content() -> str:
    s = """
# Civic Interconnect Project Documentation

Welcome to the documentation hub for Civic Interconnect (CI) projects.

Use the navigation menu to explore available modules, APIs, and tools.

For more information, visit the [Civic Interconnect GitHub organization](https://github.com/civic-interconnect).
"""
    return s.strip()


def build_api_nav(output_dir: Path) -> list[dict[str, str]]:
    """
    Scan output dir (e.g., docs/api) for .md files and build a flat MkDocs nav entry for each.
    """
    if not output_dir.exists():
        logger.error(f"Missing expected path: {output_dir}")
        raise SystemExit(1)

    api_nav = []
    for md_file in sorted(output_dir.glob("*.md")):
        title = md_file.stem.replace("_", " ").title()
        api_nav.append({title: f"api/{md_file.name}"})

    if not api_nav:
        logger.error("No markdown files found in docs/api/. Navigation will be empty.")
        raise SystemExit(1)

    logger.info(f"Included {len(api_nav)} API modules in MkDocs navigation.")
    return api_nav


def generate_docs(
    source_pkg_str: str = "civic_lib_core",
    output_dir_str: str = "api",
    formats: str | list[str] | None = None,
):
    """
    Generate API documentation in multiple formats.
    """
    formats = normalize_formats(formats)
    logger.info(f"Generating API docs from {source_pkg_str} in formats: {formats}")

    source_path = ensure_dir(source_pkg_str)
    output_dir = ensure_docs_output_dir(output_dir_str)
    api_data = extract_module_api(source_path)

    if not api_data:
        logger.warning("No public API found in source code")
        return

    if "yaml" in formats:
        write_yaml_summary(api_data, output_dir)

    if "markdown" in formats:
        write_markdown_docs(api_data, output_dir)


def generate_mkdocs_config(project_name: str, root_dir: Path, output_dir: Path) -> None:
    """
    Generate mkdocs.yml configuration file with auto-discovered API docs.
    Scans docs/api for Markdown files and builds flat navigation.

    Args:
        project_name (str): The name of the project to use in the site config.
        root_dir (Path): The root directory of the project.
        output_dir (Path): The directory where mkdocs.yml will be created (typically project root).
    """
    logger.info(f"Generating MkDocs config for {project_name} \nin {root_dir} \nto {output_dir}")
    if not root_dir.exists():
        logger.error("Project root not found. Cannot generate mkdocs config.")
        raise SystemExit(1)

    api_nav: list[dict[str, str]] = build_api_nav(output_dir)

    if not api_nav:
        logger.error("No markdown files found in docs/api/. Navigation will be empty.")
        raise SystemExit(1)

    nav: list[dict[str, object]] = [{"Home": "index.md"}, {"API Reference": api_nav}]

    config: dict[str, object] = {
        "site_name": f"{project_name} Documentation",
        "site_description": f"Documentation for {project_name}",
        "theme": {
            "name": "material",
            "palette": [{"scheme": "default", "primary": "indigo", "accent": "indigo"}],
            "features": ["navigation.expand"],
        },
        "nav": nav,
        "plugins": ["search"],
        "markdown_extensions": ["toc", "codehilite", "admonition"],
    }

    config_path: Path = root_dir / "mkdocs.yml"
    with config_path.open("w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    logger.info(f"MkDocs config written: {config_path}")


def generate_summary_yaml(source_pkg_str: str = "civic_lib_core", docs_output_string: str = "api"):
    """Generate YAML API summary (backward compatibility)."""
    generate_docs(source_pkg_str, docs_output_string, formats=["yaml"])


def normalize_formats(formats: str | list[str] | None) -> list[str]:
    """Ensure formats is a list of strings."""
    if formats is None:
        return ["yaml", "markdown"]

    if isinstance(formats, str):
        logger.warning(f"Expected list for 'formats' but got string: {formats!r}")
        return [formats]

    if not isinstance(formats, list) or not all(isinstance(f, str) for f in formats):
        raise TypeError(f"'formats' must be a list of strings, got: {formats!r}")

    return formats


def write_index_md(docs_dir: Path) -> None:
    """
    Write the index.md file to the root / docs folder .
    """
    if not docs_dir.exists():
        docs_dir.mkdir(parents=True, exist_ok=True)
    index_path = docs_dir / "index.md"
    with index_path.open("w", encoding="utf-8") as f:
        f.write(_get_index_content().strip() + "\n")
    logger.info(f"Wrote home page: {index_path}")
