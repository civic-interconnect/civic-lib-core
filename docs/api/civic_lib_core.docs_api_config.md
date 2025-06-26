# Module `civic_lib_core.docs_api_config`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `build_api_nav(output_dir: pathlib.Path) -> list[dict[str, str]]`

Scan output dir (e.g., docs/api) for .md files and build a flat MkDocs nav entry for each.

### `ensure_dir(path: str | pathlib.Path) -> pathlib.Path`

Ensure a directory exists, creating it if necessary.

Args:
    path (str | Path): The directory path to ensure.

Returns:
    Path: The resolved Path object of the directory.

Raises:
    OSError: If directory cannot be created due to permissions or other issues.

### `ensure_docs_output_dir(output_dir_str: str = 'api') -> pathlib.Path`

Ensure output directory exists under project_root/docs/.

Args:
    output_dir_str (str): Subfolder inside docs/, usually "api".

Returns:
    Path: The created or existing path.

Raises:
    RuntimeError: If project root cannot be found.
    OSError: If directory cannot be created.

### `extract_module_api(package_path: pathlib.Path) -> dict[str, dict]`

Recursively extract public functions and classes from Python source files.
Returns a dict with module names as keys.

### `generate_docs(source_pkg_str: str = 'civic_lib_core', output_dir_str: str = 'api', formats: str | list[str] | None = None)`

Generate API documentation in multiple formats.

### `generate_mkdocs_config(project_name: str, root_dir: pathlib.Path, output_dir: pathlib.Path) -> None`

Generate mkdocs.yml configuration file with auto-discovered API docs.
Scans docs/api for Markdown files and builds flat navigation.

Args:
    project_name (str): The name of the project to use in the site config.
    root_dir (Path): The root directory of the project.
    output_dir (Path): The directory where mkdocs.yml will be created (typically project root).

### `generate_summary_yaml(source_pkg_str: str = 'civic_lib_core', docs_output_string: str = 'api')`

Generate YAML API summary (backward compatibility).

### `normalize_formats(formats: str | list[str] | None) -> list[str]`

Ensure formats is a list of strings.

### `write_index_md(docs_dir: pathlib.Path) -> None`

Write the index.md file to the root / docs folder .

### `write_markdown_docs(api_data: dict, output_dir: pathlib.Path) -> None`

Write full Markdown docs for each module.

### `write_yaml_summary(api_data: dict, output_dir: pathlib.Path) -> None`

Write minimal YAML summary with module → [function names].
