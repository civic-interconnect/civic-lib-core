# Module `docs_api_config`

## Classes

### `Any(self, /, *args, **kwargs)`

Special type indicating an unconstrained type.

- Any is compatible with every type.
- Any assumed to have all methods.
- All values assumed to be instances of Any.

Note that all the above statements are true from the point of view of
static type checkers. At runtime, Any should not be used with instance
checks.

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `build_api_nav(api_src_dir: pathlib.Path, mkdocs_base_src_dir: pathlib.Path) -> list[dict[str, str]]`

Scan api_src_dir (e.g., mkdocs_src/api) for .md files and build a flat MkDocs nav entry for each.

Args:
    api_src_dir (Path): The directory containing API Markdown files (e.g., mkdocs_src/api).
    mkdocs_base_src_dir (Path): The base MkDocs source directory (e.g., mkdocs_src).

Returns:
    list[dict[str, str]]: nav entries for mkdocs.yml

### `ensure_dir(path: str | pathlib.Path) -> pathlib.Path`

Ensure a directory exists, creating it if necessary.

Args:
    path (str | Path): The directory path to ensure.

Returns:
    Path: The resolved Path object of the directory.

Raises:
    OSError: If directory cannot be created.

### `extract_module_api(package_path: pathlib.Path) -> dict[str, dict]`

Recursively extract public functions and classes from Python source files.

Args:
    package_path (Path): Path to a Python package directory.

Returns:
    dict[str, dict]: Mapping of module names to their functions and classes.

### `generate_docs(source_pkg_path: pathlib.Path, project_root: pathlib.Path, policy: dict[str, typing.Any], formats: str | list[str] | None = None) -> None`

Generate API documentation in multiple formats for a given source package.

Writes files into the determined API Markdown source directory (e.g., mkdocs_src/api/).

Args:
    source_pkg_path (Path): The absolute path to the Python package directory to document.
    project_root (Path): The root directory of the project.
    policy (dict[str, Any]): The loaded project policy.
    formats (str | list[str] | None): Output formats (e.g., "yaml", "markdown").

### `generate_mkdocs_config(project_name: str, root_dir: pathlib.Path, policy: dict[str, typing.Any], include_api_nav: bool = True, custom_nav: list[dict[str, typing.Any]] | None = None, mkdocs_base_src_dir: pathlib.Path | None = None, api_markdown_src_dir: pathlib.Path | None = None) -> None`

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

### `generate_summary_yaml(source_pkg_path: pathlib.Path, project_root: pathlib.Path, policy: dict[str, typing.Any]) -> None`

Generate YAML API summary (backward compatibility).

### `get_api_markdown_source_dir(policy: dict | None = None, root_dir: pathlib.Path | None = None) -> pathlib.Path`

Determines the specific directory within mkdocs_src where API Markdown files should go.
This is the target for the Python script generating API Markdown.

Args:
    policy (Optional[dict]): The loaded project policy. If None, it will be loaded internally.
    root_dir (Optional[Path]): The project root directory. If None, it will be discovered internally.

Returns:
    Path: The absolute path to the API Markdown source directory (e.g., project_root/mkdocs_src/api).

### `get_mkdocs_paths(policy: dict, project_root: pathlib.Path) -> tuple[pathlib.Path, pathlib.Path]`

Return paths to mkdocs.yml and the mkdocs source folder based on policy.

Args:
    policy (dict): Loaded project policy.
    project_root (Path): Root of the repo.

Returns:
    Tuple[Path, Path]: (mkdocs_config_file_path, mkdocs_src_path)

### `normalize_formats(formats: str | list[str] | None) -> list[str]`

Ensure formats is a list of strings.

### `write_index_md(docs_src_dir: pathlib.Path) -> None`

Write the index.md file to mkdocs_src/.

Args:
    docs_src_dir (Path): The mkdocs source directory.

### `write_markdown_docs(api_data: dict, output_dir: pathlib.Path) -> None`

Write full Markdown documentation for all extracted modules.

Args:
    api_data (dict): Dictionary from extract_module_api.
    output_dir (Path): Path to folder where Markdown files will be written.

### `write_yaml_summary(api_data: dict, output_dir: pathlib.Path) -> None`

Write a minimal YAML summary listing module names and their function names.

Args:
    api_data (dict): Dictionary from extract_module_api.
    output_dir (Path): Path to folder where API.yaml will be written.
