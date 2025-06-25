# Module `doc_utils`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `build_api_nav(project_root: pathlib.Path) -> list[dict[str, str]]`

Scan docs/api/ for .md files and build a flat MkDocs nav entry for each.

### `dynamic_import_from_path(file_path: pathlib.Path, module_name: str)`

No description available.

### `ensure_docs_output_dir(output_dir_str: str = 'api') -> pathlib.Path`

Ensure output directory exists under project root/docs.

### `ensure_source_path(source_pkg_str: str = 'civic_lib_core') -> pathlib.Path`

Resolve and validate the source package path.

### `extract_module_api(source_path: pathlib.Path) -> dict[str, dict]`

Recursively extract public functions and classes from Python source files.
Returns a dict with module names as keys.

### `extract_public_names(tree: ast.AST) -> set[str]`

Extract names from __all__ declaration.

### `find_public_classes(tree: ast.AST, public_names: set[str]) -> list[dict[str, str]]`

Find all public classes in the AST with their docstrings.

### `find_public_functions(tree: ast.AST, public_names: set[str]) -> list[dict[str, str]]`

Find all public functions in the AST with their docstrings.

### `generate_api_docs(source_dir_str: str = 'civic_lib_core', output_dir_str: str = 'api')`

Generate Markdown API documentation (backward compatibility).

### `generate_docs(source_pkg_str: str = 'civic_lib_core', output_dir_str: str = 'api', formats: str | list[str] | None = None)`

Generate API documentation in multiple formats.

### `generate_mkdocs_config(project_name: str | None = None, source_pkg_str: str = 'civic_lib_core') -> None`

Generate mkdocs.yml configuration file with auto-discovered API docs.
Scans docs/api for Markdown files and builds flat navigation.

### `generate_summary_yaml(source_pkg_str: str = 'civic_lib_core', docs_output_string: str = 'api')`

Generate YAML API summary (backward compatibility).

### `get_public_members(module)`

No description available.

### `normalize_formats(formats: str | list[str] | None) -> list[str]`

Ensure formats is a list of strings.

### `parse_python_file(file_path: pathlib.Path) -> ast.AST | None`

Parse a Python file and return its AST, or None if there's a syntax error.

### `publish_api_docs(source_pkg_str: str = 'civic_lib_core') -> None`

One-liner to generate complete API documentation for release.

Generates YAML summary, Markdown docs, and MkDocs config in one call.
Perfect for automated release workflows.

Args:
    source_pkg_str: Source package to document (auto-detects project)

### `write_index_md(project_root: pathlib.Path) -> None`

Write the index.md file to the docs/ folder with a standard welcome message.

### `write_markdown_docs(api_data: dict, output_dir: pathlib.Path) -> None`

Write full Markdown docs for each module.

### `write_module_markdown(file_path: pathlib.Path, module_name: str, functions: list[dict[str, str]], classes: list[dict[str, str]])`

Write markdown documentation for a single module.

### `write_yaml_summary(api_data: dict, output_dir: pathlib.Path) -> None`

Write minimal YAML summary with module → [function names].
