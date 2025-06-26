"""
civic_lib_core/doc_utils.py

Core development utilities.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
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
    """Write full Markdown docs for each module."""
    for module_name, module_data in api_data.items():
        if not isinstance(module_data, dict):
            logger.warning(f"Skipping {module_name} due to unexpected type: {type(module_data)}")
            continue

        functions = module_data.get("functions", [])
        classes = module_data.get("classes", [])
        md_path = output_dir / f"{module_name}.md"
        write_module_markdown(md_path, module_name, functions, classes)
        logger.debug(f"Wrote markdown: {md_path}")

    logger.info(f"Markdown API docs: {output_dir}")


def write_module_markdown(
    file_path: Path,
    module_name: str,
    functions: list[dict[str, str]],
    classes: list[dict[str, str]],
):
    """Write markdown documentation for a single module."""
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
    """Write minimal YAML summary with module → [function names]."""
    minimal_yaml = {}
    for module_name, module_data in api_data.items():
        if isinstance(module_data, dict):
            functions = module_data.get("functions", [])
            if isinstance(functions, list):
                names = [f["name"] for f in functions if isinstance(f, dict) and "name" in f]
                if names:
                    minimal_yaml[module_name] = names

    yaml_path = output_dir / "API.yaml"
    with yaml_path.open("w", encoding="utf-8") as f:
        yaml.dump(minimal_yaml, f, sort_keys=True)

    logger.info(f"YAML API summary: {yaml_path}")
