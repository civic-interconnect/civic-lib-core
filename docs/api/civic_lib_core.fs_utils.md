# Module `civic_lib_core.fs_utils`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `discover_project_layout() -> dict[str, pathlib.Path | list[pathlib.Path]]`

Centralized layout discovery with early failure and full logging.

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

### `find_project_root(start_path: pathlib.Path | None = None) -> pathlib.Path`

Find the root of the repo based on common markers.

Searches for markers like .git, pyproject.toml, setup.py, etc.

Args:
    start_path (Optional[Path]): Directory to start search from. Defaults to cwd.

Returns:
    Path: Project root directory.

Raises:
    RuntimeError: If project root cannot be found.

### `find_source_dir(root_dir: pathlib.Path) -> pathlib.Path | None`

Flexibly find the source directory containing Python packages in src/

Args:
    root_dir (Path): Project root directory

Returns:
    Optional[Path]: Source directory if found, None if no valid packages found

### `get_repo_package_names(root_path: pathlib.Path | None = None) -> list[str]`

Return a list of all top-level Python packages in the project.

Args:
    root_path (Optional[Path]): Optionally specify repo root. Defaults to auto-detection.

Returns:
    list[str]: List of package names (e.g., 'civic_lib_core', 'civic_dev').
               Returns empty list if no packages found.

### `get_source_dir(root_dir: pathlib.Path) -> pathlib.Path | None`

Alias for get_source_from_root for backward compatibility.

### `get_valid_packages(src_dir: pathlib.Path) -> list[pathlib.Path]`

Return all top-level valid Python packages in the given directory.

Args:
    src_dir (Path): Directory to search for packages.

Returns:
    list[Path]: List of package directory paths.

Raises:
    FileNotFoundError: If src_dir doesn't exist.
    ValueError: If no valid packages are found.

### `resolve_path(relative_path: str | pathlib.Path) -> pathlib.Path`

Resolve a relative path from the repo root.

Args:
    relative_path (str | Path): Path to resolve.

Returns:
    Path: Absolute path resolved from project root.

Raises:
    RuntimeError: If project root cannot be found.

### `safe_filename(name: str, max_length: int = 255) -> str`

Convert a string into a safe, filesystem-compatible filename.

Args:
    name (str): Original string.
    max_length (int): Maximum filename length. Defaults to 255.

Returns:
    str: Sanitized filename.
