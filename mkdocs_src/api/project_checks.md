# Module `project_checks`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `check_empty_dirs(project_root: pathlib.Path) -> list[str]`

No description available.

### `check_mkdocs_consistency(project_root: pathlib.Path, policy: dict) -> list[str]`

No description available.

### `check_oversized_py_files(project_root: pathlib.Path, src_dir: pathlib.Path, policy: dict) -> list[str]`

No description available.

### `check_py_files_outside_src(project_root: pathlib.Path, src_dir: pathlib.Path) -> list[str]`

No description available.

### `check_python_project_dirs(project_root: pathlib.Path, policy: dict) -> list[str]`

No description available.

### `check_python_project_files(project_root: pathlib.Path, policy: dict) -> list[str]`

No description available.

### `check_required_files(project_root: pathlib.Path, policy: dict) -> list[str]`

No description available.

### `main() -> None`

Main entry point to run all checks and print results.

### `run_all_checks() -> list[str] | None`

Run all project-level checks and return a list of issues.

Returns:
    list[str]: Descriptions of issues found.
