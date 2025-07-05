# Module `fs_utils`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

### `ProjectLayout(self, /, *args, **kwargs)`

Represents the layout of a project, including key directories and metadata.

Attributes:
    project_root (Path): The root directory of the project.
    src_dir (Path | None): The source directory containing the main code, or None if not applicable.
    packages (list[Path]): A list of paths to package directories within the project.
    api_markdown_src_dir (Path): The directory containing API documentation *source* Markdown files
                                  (e.g., project_root/mkdocs_src/api).
    org_name (str | None): The name of the organization, or None if not specified.
    policy (dict): A dictionary containing project policy information.

## Functions

### `discover_project_layout() -> civic_lib_core.project_layout.ProjectLayout`

Dynamically discovers and returns key layout paths and information for
the current Civic Interconnect project, encapsulated in a ProjectLayout NamedTuple.

This function performs the following steps:
1. Determines the project root directory.
2. Loads the project policy configuration.
3. Identifies the primary source directory (e.g., 'src/').
4. Lists all top-level Python packages within the source directory.
5. Calculates the path to the API documentation *source* directory (mkdocs_src/api).
6. Attempts to determine the organization name associated with the project.

The returned ProjectLayout object provides structured, type-hinted access
to these essential project paths and configurations, simplifying their
consumption by other parts of the system and improving type safety.

Returns:
    ProjectLayout: A NamedTuple containing structured layout information,
                    including project_root, src_dir, packages, docs_api_dir,
                    org_name, and the loaded policy.

### `ensure_dir(path: str | pathlib.Path) -> pathlib.Path`

Ensure a directory exists, creating it if necessary.

Args:
    path (str | Path): The directory path to ensure.

Returns:
    Path: The resolved Path object of the directory.

Raises:
    OSError: If directory cannot be created.

### `ensure_docs_output_dir(project_root: pathlib.Path | None = None, policy: dict | None = None) -> pathlib.Path`

Ensures the *final HTML output directory* for MkDocs exists.
This is typically `project_root/docs/`, as defined in the project policy.

Args:
    project_root (Optional[Path]): The project root directory. If None, it will be discovered internally.
    policy (Optional[dict]): The loaded project policy. If None, it will be loaded internally.

Returns:
    Path: The created or existing path to the main HTML output directory.

Raises:
    Exception: If the directory cannot be located or created.

### `find_project_root(start_path: pathlib.Path | None = None) -> pathlib.Path`

DEPRECATED: Use get_project_root instead.

### `find_source_dir(root_dir: pathlib.Path) -> pathlib.Path | None`

DEPRECATED: Use get_source_dir instead.

### `get_api_markdown_source_dir(policy: dict | None = None, root_dir: pathlib.Path | None = None) -> pathlib.Path`

Determines the specific directory within mkdocs_src where API Markdown files should go.
This is the target for the Python script generating API Markdown.

Args:
    policy (Optional[dict]): The loaded project policy. If None, it will be loaded internally.
    root_dir (Optional[Path]): The project root directory. If None, it will be discovered internally.

Returns:
    Path: The absolute path to the API Markdown source directory (e.g., project_root/mkdocs_src/api).

### `get_data_config_dir(project_root: pathlib.Path | None = None) -> pathlib.Path`

Return the standard data-config folder path for the repo.

Args:
    project_root (Path | None): Optionally provide the repo root.

Returns:
    Path: Full path to <repo-root>/data-config.

### `get_mkdocs_paths(policy: dict, project_root: pathlib.Path) -> tuple[pathlib.Path, pathlib.Path]`

Return paths to mkdocs.yml and the mkdocs source folder based on policy.

Args:
    policy (dict): Loaded project policy.
    project_root (Path): Root of the repo.

Returns:
    Tuple[Path, Path]: (mkdocs_config_file_path, mkdocs_src_path)

### `get_org_name(project_root: pathlib.Path) -> str | None`

Return the organization folder name, assuming the repo path
follows /path/to/<org>/<repo> convention.

Args:
    project_root (Path): The project root path.

Returns:
    Optional[str]: Organization name, or None if not found.

### `get_project_root(start_path: pathlib.Path | None = None) -> pathlib.Path`

Return the root of the repo based on common markers.

Searches for markers like .git or pyproject.toml in the current
directory and its parents.

Args:
    start_path (Optional[Path]): Directory to start search from. Defaults to cwd.

Returns:
    Path: Project root directory.

Raises:
    RuntimeError: If project root cannot be found based on the markers.

### `get_repo_package_names(root_path: pathlib.Path | None = None) -> list[str]`

Return a list of all top-level Python packages in the project.

Args:
    root_path (Optional[Path]): Optionally specify repo root. Defaults to auto-detection.

Returns:
    list[str]: List of package names (e.g. 'civic_lib_core', 'civic_dev').

### `get_runtime_config_path(project_root: pathlib.Path | None = None) -> pathlib.Path`

Return the path to runtime_config.yaml under the project root.

Args:
    project_root (Path | None): Optionally provide the repo root.

Returns:
    Path: Full path to <repo-root>/runtime_config.yaml.

### `get_source_dir(root_dir: pathlib.Path) -> pathlib.Path | None`

Return the source directory containing Python packages under src/.

Args:
    root_dir (Path): Project root directory

Returns:
    Optional[Path]: The source directory if found, otherwise None.

### `get_valid_packages(src_dir: pathlib.Path) -> list[pathlib.Path]`

Return all top-level valid Python packages in the given directory.

Args:
    src_dir (Path): Directory to search for packages.

Returns:
    list[Path]: List of package directory paths.

Raises:
    FileNotFoundError: If src_dir doesn't exist.
    ValueError: If no valid packages are found.

### `load_project_policy(project_root: pathlib.Path | None = None) -> dict`

Load Civic Interconnect project policy, allowing client repos to
optionally override default settings via a custom policy file.

The default policy is loaded from the library's internal `project_policy.yaml`.
If `project_root` is provided and a `project_policy.yaml` exists within it,
this custom policy will be loaded and its values will be recursively
merged into the default policy, overriding any conflicting keys.

Args:
    project_root (Path | None): If provided, looks for `project_policy.yaml`
                                 in this root directory to apply custom overrides.

Returns:
    dict: The combined policy data, with custom settings merged over defaults.

### `resolve_path(relative_path: str | pathlib.Path) -> pathlib.Path`

Resolve a relative path from the repo root.

Args:
    relative_path (str | Path): Path to resolve.

Returns:
    Path: Absolute path resolved from project root.

### `safe_filename(name: str, max_length: int = 255) -> str`

Convert a string into a safe, filesystem-compatible filename.

Args:
    name (str): Original string.
    max_length (int): Maximum filename length.

Returns:
    str: Sanitized filename.
