"""
civic_lib_core/doc_utils.py

Core development utilities.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
"""

import ast
from pathlib import Path

import yaml

from civic_lib_core import log_utils
from civic_lib_core.file_utils import ensure_docs_output_dir, ensure_source_path

__all__ = [
    "extract_module_api",
    "generate_docs",
    "generate_api_docs",
    "generate_summary_yaml",
    "generate_mkdocs_config",
    "publish_api_docs",
]

log_utils.init_logger()
logger = log_utils.logger


def extract_module_api(source_path: Path) -> dict[str, dict[str, list[dict[str, str]]]]:
    """
    Extract public API information from all Python modules in source_path.

    Returns:
        Dict mapping module names to their public functions and classes with docstrings.
    """
    api_data = {}

    for file_path in source_path.rglob("*.py"):
        if "tests" in file_path.parts or file_path.name.startswith("__"):
            continue

        module_name = (
            file_path.relative_to(source_path).with_suffix("").as_posix().replace("/", ".")
        )

        tree = parse_python_file(file_path)
        if tree is None:
            continue

        public_names = extract_public_names(tree)
        functions = find_public_functions(tree, public_names)
        classes = find_public_classes(tree, public_names)

        if not functions and not classes:
            continue

        api_data[module_name] = {}
        if functions:
            api_data[module_name]["functions"] = functions
        if classes:
            api_data[module_name]["classes"] = classes

    return api_data


def extract_public_names(tree: ast.AST) -> set[str]:
    """Extract names from __all__ declaration."""
    public_names = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets)
            and isinstance(node.value, ast.List)
        ):
            public_names |= {elt.s for elt in node.value.elts if isinstance(elt, ast.Str)}
    return public_names


def find_public_classes(tree: ast.AST, public_names: set[str]) -> list[dict[str, str]]:
    """Find all public classes in the AST with their docstrings."""
    classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and (
            not node.name.startswith("_") or node.name in public_names
        ):
            # Extract docstring
            docstring = ast.get_docstring(node) or "No description available."

            # Get base classes
            bases = [ast.unparse(base) for base in node.bases] if node.bases else []
            inheritance = f"({', '.join(bases)})" if bases else ""

            classes.append({
                "name": node.name,
                "signature": f"{node.name}{inheritance}",
                "docstring": docstring,
            })

    return sorted(classes, key=lambda x: x["name"])


def find_public_functions(tree: ast.AST, public_names: set[str]) -> list[dict[str, str]]:
    """Find all public functions in the AST with their docstrings."""
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and (
            not node.name.startswith("_") or node.name in public_names
        ):
            # Extract docstring
            docstring = ast.get_docstring(node) or "No description available."

            # Get function signature
            args = []
            for arg in node.args.args:
                args.append(arg.arg)

            # Add defaults
            defaults = (
                [ast.unparse(default) for default in node.args.defaults]
                if node.args.defaults
                else []
            )

            # Combine args with defaults
            signature_parts = []
            num_defaults = len(defaults)
            for i, arg in enumerate(args):
                if i >= len(args) - num_defaults:
                    default_idx = i - (len(args) - num_defaults)
                    signature_parts.append(f"{arg}={defaults[default_idx]}")
                else:
                    signature_parts.append(arg)

            signature = f"{node.name}({', '.join(signature_parts)})"

            functions.append({"name": node.name, "signature": signature, "docstring": docstring})

    return sorted(functions, key=lambda x: x["name"])


def generate_api_docs(source_dir_str: str = "civic_lib_core", output_dir_str: str = "api"):
    """Generate Markdown API documentation (backward compatibility)."""
    generate_docs(source_dir_str, output_dir_str, formats=["markdown"])


def generate_docs(
    source_pkg_str: str = "civic_lib_core",
    output_dir_str: str = "api",
    formats: list[str] | None = None,
):
    """
    Generate API documentation in multiple formats.

    Args:
        source_pkg_str: Package directory containing Python source files
        output_dir_str: Output directory name (will be created under docs/)
        formats: List of formats to generate ("yaml", "markdown", or both)
    """
    if formats is None:
        formats = ["yaml", "markdown"]
    logger.info(f"Generating API docs from {source_pkg_str} in formats: {formats}")

    source_path = ensure_source_path(source_pkg_str)
    output_dir = ensure_docs_output_dir(output_dir_str)

    logger.debug(f"Source: {source_path.resolve()}")
    logger.debug(f"Output: {output_dir.resolve()}")

    # Extract API data once
    api_data = extract_module_api(source_path)

    if not api_data:
        logger.warning("No public API found in source code")
        return

    # Generate requested formats
    if "yaml" in formats:
        yaml_path = output_dir / "API.yaml"
        with yaml_path.open("w", encoding="utf-8") as f:
            yaml.dump(api_data, f, sort_keys=False)
        logger.info(f"YAML API summary: {yaml_path}")

    if "markdown" in formats:
        for module_name, module_data in api_data.items():
            md_path = output_dir / f"{module_name}.md"
            write_module_markdown(
                md_path,
                module_name,
                module_data.get("functions", []),
                module_data.get("classes", []),
            )
            logger.debug(f"Wrote markdown: {md_path}")
        logger.info(f"Markdown API docs: {output_dir}")


def generate_mkdocs_config(
    project_name: str | None = None, source_pkg_str: str = "civic_lib_core"
) -> None:
    """
    Generate mkdocs.yml configuration file with auto-discovered API docs.

    Args:
        project_name: Name for the documentation site (auto-detected if None)
        source_pkg_str: Source package to scan for modules
    """
    from civic_lib_core.file_utils import find_project_root

    # Auto-detect project name if not provided
    if project_name is None:
        project_root = find_project_root()
        project_name = project_root.name.replace("-", " ").replace("_", " ").title()

    # Get list of API modules
    source_path = ensure_source_path(source_pkg_str)
    api_data = extract_module_api(source_path)

    # Create API navigation list
    api_nav = [{"Overview": "api/index.md"}]
    api_nav.extend([
        {module.replace("_", " ").replace(".", " > ").title(): f"api/{module}.md"}
        for module in sorted(api_data.keys())
    ])

    # Create mkdocs config
    config = {
        "site_name": f"{project_name} Documentation",
        "site_description": f"Documentation for {project_name}",
        "theme": {
            "name": "material",
            "palette": [
                {
                    "scheme": "default",
                    "primary": "indigo",  # Darker blue
                    "accent": "indigo",
                }
            ],
        },
        "nav": [{"Home": "index.md"}, {"API Reference": api_nav}],
        "plugins": ["search"],
        "markdown_extensions": ["toc", "codehilite", "admonition"],
    }

    # Write to project root
    project_root = find_project_root()
    config_path = project_root / "mkdocs.yml"

    with config_path.open("w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    logger.info(f"MkDocs config written: {config_path}")


def generate_summary_yaml(source_pkg_str: str = "civic_lib_core", docs_output_string: str = "api"):
    """Generate YAML API summary (backward compatibility)."""
    generate_docs(source_pkg_str, docs_output_string, formats=["yaml"])


def parse_python_file(file_path: Path) -> ast.AST | None:
    """Parse a Python file and return its AST, or None if there's a syntax error."""
    try:
        with open(file_path, encoding="utf-8") as f:
            return ast.parse(f.read(), filename=str(file_path))
    except SyntaxError as e:
        logger.warning(f"Syntax error in {file_path}: {e}")
        return None


def publish_api_docs(source_pkg_str: str = "civic_lib_core") -> None:
    """
    One-liner to generate complete API documentation for release.

    Generates YAML summary, Markdown docs, and MkDocs config in one call.
    Perfect for automated release workflows.

    Args:
        source_pkg_str: Source package to document (auto-detects project)
    """
    logger.info("Publishing API documentation...")
    try:
        # Generate all documentation formats
        generate_docs(source_pkg_str, formats=["yaml", "markdown"])
        generate_mkdocs_config(source_pkg_str=source_pkg_str)
        logger.info("API documentation published successfully")
    except Exception as e:
        logger.error(f"Error publishing API documentation: {e}")
        raise


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


if __name__ == "__main__":
    publish_api_docs()
    logger.info("All documentation generated.")
