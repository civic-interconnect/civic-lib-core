# civic_lib_core/docs_api_config.py

"""
Core logic for generating and configuring MkDocs documentation
for Civic Interconnect repositories.

Provides:
- Functions to generate MkDocs YAML configurations
- Index page content for documentation portals
- Navigation building for API modules
- Helpers for writing documentation source files

Designed for both API-only repos and mixed-use repositories
(e.g. web apps with optional API references).
"""

from pathlib import Path
from typing import Any

import yaml

from civic_lib_core import log_utils
from civic_lib_core.docs_api_extract import extract_module_api
from civic_lib_core.docs_api_render import write_markdown_docs, write_yaml_summary
from civic_lib_core.fs_utils import (
    ensure_dir,
    get_api_markdown_source_dir,
    get_mkdocs_paths,
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

Welcome to the documentation for Civic Interconnect (CI) projects.

Use the navigation menu to explore available modules, APIs, and tools.

For more information, visit the [Civic Interconnect GitHub organization](https://github.com/civic-interconnect).
"""
    return s.strip()


def build_api_nav(api_src_dir: Path, mkdocs_base_src_dir: Path) -> list[dict[str, str]]:
    """
    Scan api_src_dir (e.g., mkdocs_src/api) for .md files and build a flat MkDocs nav entry for each.

    Args:
        api_src_dir (Path): The directory containing API Markdown files (e.g., mkdocs_src/api).
        mkdocs_base_src_dir (Path): The base MkDocs source directory (e.g., mkdocs_src).

    Returns:
        list[dict[str, str]]: nav entries for mkdocs.yml
    """
    if not api_src_dir.exists():
        logger.warning(f"API source directory not found: {api_src_dir}")
        return []

    api_nav = []
    for md_file in sorted(api_src_dir.glob("*.md")):
        title = md_file.stem.replace("_", " ").title()
        try:
            relative_path = md_file.relative_to(mkdocs_base_src_dir).as_posix()
            api_nav.append({title: relative_path})
        except ValueError:
            logger.error(
                f"Could not get relative path for '{md_file}' relative to '{mkdocs_base_src_dir}'. "
                "This file will not be included in API navigation.",
                exc_info=True,
            )
            continue

    if not api_nav:
        logger.info("No markdown files found in the API source directory. Skipping API nav.")

    logger.info(f"Included {len(api_nav)} API modules in MkDocs navigation.")
    return api_nav


def generate_docs(
    source_pkg_path: Path,
    project_root: Path,
    policy: dict[str, Any],
    formats: str | list[str] | None = None,
) -> None:
    """
    Generate API documentation in multiple formats for a given source package.

    Writes files into the determined API Markdown source directory (e.g., mkdocs_src/api/).

    Args:
        source_pkg_path (Path): The absolute path to the Python package directory to document.
        project_root (Path): The root directory of the project.
        policy (dict[str, Any]): The loaded project policy.
        formats (str | list[str] | None): Output formats (e.g., "yaml", "markdown").
    """
    formats = normalize_formats(formats)
    logger.info(f"Generating API docs from package '{source_pkg_path.name}' in formats: {formats}")

    # Validate inputs
    if not isinstance(source_pkg_path, Path):
        raise TypeError(f"source_pkg_path must be a Path object, got {type(source_pkg_path)}")
    if not source_pkg_path.is_dir():
        logger.error(
            f"Source package path '{source_pkg_path}' is not a directory. Cannot extract API."
        )
        return

    if not isinstance(project_root, Path):
        raise TypeError(f"project_root must be a Path object, got {type(project_root)}")
    if not isinstance(policy, dict):
        raise TypeError(f"policy must be a dictionary, got {type(policy)}")

    api_output_dir = get_api_markdown_source_dir(policy, project_root)
    ensure_dir(api_output_dir)

    api_data = extract_module_api(source_pkg_path)

    if not api_data:
        logger.warning(f"No public API found in source code for {source_pkg_path.name}")
        return

    if "yaml" in formats:
        write_yaml_summary(api_data, api_output_dir)

    if "markdown" in formats:
        write_markdown_docs(api_data, api_output_dir)


def generate_mkdocs_config(
    project_name: str,
    root_dir: Path,
    policy: dict[str, Any],
    include_api_nav: bool = True,
    custom_nav: list[dict[str, Any]] | None = None,
    mkdocs_base_src_dir: Path | None = None,
    api_markdown_src_dir: Path | None = None,
) -> None:
    """
    Generate mkdocs.yml configuration file.

    Args:
        project_name (str): The name of the project.
        root_dir (Path): The repo root.
        policy (dict[str, Any]): The loaded project policy.
        include_api_nav (bool): Whether to scan for API docs.
        custom_nav (list[dict[str, Any]] | None): Additional nav entries.
        mkdocs_base_src_dir (Path | None): The base directory for MkDocs source files (e.g., mkdocs_src).
                                             If None, it will be derived from policy.
        api_markdown_src_dir (Path | None): The directory where API markdown files are generated.
                                               If None, it will be derived from policy.
    """
    logger.info(f"Generating MkDocs config for {project_name} in {root_dir}")

    mkdocs_config_path_relative_to_root = policy.get("mkdocs_config", "mkdocs.yml")
    mkdocs_src_dir_name = policy.get("mkdocs_src_dir", "mkdocs_src")
    site_dir_name = policy.get("site_dir", "docs")

    if mkdocs_base_src_dir is None:
        _mkdocs_config_path, mkdocs_base_src_dir = get_mkdocs_paths(policy, root_dir)
        logger.debug(f"generate_mkdocs_config: Derived mkdocs_base_src_dir: {mkdocs_base_src_dir}")
    if api_markdown_src_dir is None:
        api_markdown_src_dir = get_api_markdown_source_dir(policy, root_dir)
        logger.debug(
            f"generate_mkdocs_config: Derived api_markdown_src_dir: {api_markdown_src_dir}"
        )

    nav: list[dict[str, Any]] = [{"Home": "index.md"}]

    if include_api_nav:
        api_nav = build_api_nav(api_markdown_src_dir, mkdocs_base_src_dir)
        if api_nav:
            nav.append({"API Reference": api_nav})

    if custom_nav:
        nav.extend(custom_nav)

    theme_name = policy.get("mkdocs_theme_name", "material")
    theme_palette = policy.get(
        "mkdocs_theme_palette", [{"scheme": "default", "primary": "indigo", "accent": "indigo"}]
    )
    theme_features = policy.get("mkdocs_theme_features", ["navigation.expand"])
    plugins = policy.get("mkdocs_plugins", ["search"])
    markdown_extensions = policy.get(
        "mkdocs_markdown_extensions", ["toc", "codehilite", "admonition"]
    )

    config: dict[str, Any] = {
        "site_name": f"{project_name} Documentation",
        "site_description": f"Documentation for {project_name}",
        "docs_dir": mkdocs_src_dir_name,
        "site_dir": site_dir_name,
        "theme": {
            "name": theme_name,
            "palette": theme_palette,
            "features": theme_features,
        },
        "nav": nav,
        "plugins": plugins,
        "markdown_extensions": markdown_extensions,
    }

    config_path: Path = root_dir / mkdocs_config_path_relative_to_root
    with config_path.open("w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    logger.info(f"MkDocs config written: {config_path}")


def generate_summary_yaml(
    source_pkg_path: Path,
    project_root: Path,
    policy: dict[str, Any],
) -> None:
    """Generate YAML API summary (backward compatibility)."""
    generate_docs(source_pkg_path, formats=["yaml"], project_root=project_root, policy=policy)


def normalize_formats(formats: str | list[str] | None) -> list[str]:
    """Ensure formats is a list of strings."""
    if formats is None:
        return ["yaml", "markdown"]

    if isinstance(formats, str):
        logger.warning(f"Expected list for 'formats' but got string: {formats!r}. Converting.")
        return [formats]

    if not isinstance(formats, list) or not all(isinstance(f, str) for f in formats):
        raise TypeError(f"'formats' must be a list of strings, got: {formats!r}")

    return formats


def write_index_md(docs_src_dir: Path) -> None:
    """
    Write the index.md file to mkdocs_src/.

    Args:
        docs_src_dir (Path): The mkdocs source directory.
    """
    ensure_dir(docs_src_dir)
    index_path = docs_src_dir / "index.md"
    with index_path.open("w", encoding="utf-8") as f:
        f.write(_get_index_content().strip() + "\n")
    logger.info(f"Wrote home page: {index_path}")
