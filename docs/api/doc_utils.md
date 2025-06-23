# Module `doc_utils`

## Functions

### `extract_module_api(source_path)`

Extract public API information from all Python modules in source_path.

Returns:
    Dict mapping module names to their public functions and classes with docstrings.

### `extract_public_names(tree)`

Extract names from __all__ declaration.

### `find_public_classes(tree, public_names)`

Find all public classes in the AST with their docstrings.

### `find_public_functions(tree, public_names)`

Find all public functions in the AST with their docstrings.

### `generate_api_docs(source_dir_str='civic_lib_core', output_dir_str='api')`

Generate Markdown API documentation (backward compatibility).

### `generate_docs(source_pkg_str='civic_lib_core', output_dir_str='api', formats=None)`

Generate API documentation in multiple formats.

Args:
    source_pkg_str: Package directory containing Python source files
    output_dir_str: Output directory name (will be created under docs/)
    formats: List of formats to generate ("yaml", "markdown", or both)

### `generate_mkdocs_config(project_name=None, source_pkg_str='civic_lib_core')`

Generate mkdocs.yml configuration file with auto-discovered API docs.

Args:
    project_name: Name for the documentation site (auto-detected if None)
    source_pkg_str: Source package to scan for modules

### `generate_summary_yaml(source_pkg_str='civic_lib_core', docs_output_string='api')`

Generate YAML API summary (backward compatibility).

### `parse_python_file(file_path)`

Parse a Python file and return its AST, or None if there's a syntax error.

### `publish_api_docs(source_pkg_str='civic_lib_core')`

One-liner to generate complete API documentation for release.

Generates YAML summary, Markdown docs, and MkDocs config in one call.
Perfect for automated release workflows.

Args:
    source_pkg_str: Source package to document (auto-detects project)

### `write_module_markdown(file_path, module_name, functions, classes)`

Write markdown documentation for a single module.
