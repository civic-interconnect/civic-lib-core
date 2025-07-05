"""
civic_lib_core/docs_api_render.py

Renders extracted API metadata into documentation files for Civic Interconnect
projects.

Responsibilities:
- Generate Markdown files documenting Python modules
- Produce YAML summaries for quick API overviews
- Format class and function details into readable outputs

This module converts structured API data into human-readable documentation
for inclusion in Civic Interconnect documentation sites.
"""

from pathlib import Path

import yaml

from civic_lib_core import log_utils

__all__ = [
    "write_markdown_docs",
    "write_module_markdown",
    "write_yaml_summary",
]

logger = log_utils.logger


def write_markdown_docs(api_data: dict, output_dir: Path) -> None:
    """
    Write full Markdown documentation for all extracted modules.

    Args:
        api_data (dict): Dictionary from extract_module_api.
        output_dir (Path): Path to folder where Markdown files will be written.
    """
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    for module_name, module_data in api_data.items():
        if not isinstance(module_data, dict):
            logger.warning(f"Skipping {module_name} due to unexpected type: {type(module_data)}")
            continue

        functions = module_data.get("functions", [])
        classes = module_data.get("classes", [])

        if not functions and not classes:
            logger.info(f"Skipping {module_name}. No public API elements found.")
            continue

        md_path = output_dir / f"{module_name}.md"
        write_module_markdown(md_path, module_name, functions, classes)
        logger.debug(f"Wrote markdown: {md_path}")

    logger.info(f"Markdown API docs written to: {output_dir}")


def write_module_markdown(
    file_path: Path,
    module_name: str,
    functions: list[dict[str, str]],
    classes: list[dict[str, str]],
) -> None:
    """
    Write Markdown documentation for a single Python module.

    Args:
        file_path (Path): Output file path.
        module_name (str): Name of the module being documented.
        functions (list[dict]): Public functions extracted from the module.
        classes (list[dict]): Public classes extracted from the module.
    """
    with file_path.open("w", encoding="utf-8") as out:
        out.write(f"# Module `{module_name}`\n\n")

        if classes:
            out.write("## Classes\n\n")
            for cls in classes:
                out.write(f"### `{cls['signature']}`\n\n")
                out.write(f"{cls['docstring']}\n\n")

        if functions:
            out.write("## Functions\n\n")
            for func in functions:
                out.write(f"### `{func['signature']}`\n\n")
                out.write(f"{func['docstring']}\n\n")


def write_yaml_summary(api_data: dict, output_dir: Path) -> None:
    """
    Write a minimal YAML summary listing module names and their function names.

    Args:
        api_data (dict): Dictionary from extract_module_api.
        output_dir (Path): Path to folder where API.yaml will be written.
    """
    minimal_yaml = {}
    for module_name, module_data in api_data.items():
        if isinstance(module_data, dict):
            functions = module_data.get("functions", [])
            if isinstance(functions, list):
                names = [f["name"] for f in functions if isinstance(f, dict) and "name" in f]
                if names:
                    minimal_yaml[module_name] = names

    if not minimal_yaml:
        logger.warning("No function data found to write to YAML summary.")
        return

    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    yaml_path = output_dir / "API.yaml"
    with yaml_path.open("w", encoding="utf-8") as f:
        yaml.dump(
            minimal_yaml,
            f,
            sort_keys=True,
            default_flow_style=False,
            allow_unicode=True,
            indent=2,
        )

    logger.info(f"YAML API summary written to: {yaml_path}")
