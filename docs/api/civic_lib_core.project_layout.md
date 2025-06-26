# Module `civic_lib_core.project_layout`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

### `ProjectLayout(self, /, *args, **kwargs)`

ProjectLayout(project_root, src_dir, packages, docs_api_dir)

## Functions

### `NamedTuple(typename, fields=None, /, **kwargs)`

Typed version of namedtuple.

Usage::

    class Employee(NamedTuple):
        name: str
        id: int

This is equivalent to::

    Employee = collections.namedtuple('Employee', ['name', 'id'])

The resulting class has an extra __annotations__ attribute, giving a
dict that maps field names to types.  (The field names are also in
the _fields attribute, which is part of the namedtuple API.)
An alternative equivalent functional syntax is also accepted::

    Employee = NamedTuple('Employee', [('name', str), ('id', int)])

### `discover_project_layout() -> project_layout.ProjectLayout`

Return key layout paths for the current project.

### `find_project_root(start_path: pathlib.Path | None = None) -> pathlib.Path`

Find the root of the repo based on common markers.

Searches for markers like .git, pyproject.toml, setup.py, etc.

Args:
    start_path (Optional[Path]): Directory to start search from. Defaults to cwd.

Returns:
    Path: Project root directory.

Raises:
    RuntimeError: If project root cannot be found.

### `format_layout(layout: project_layout.ProjectLayout) -> str`

Format layout info for display.

### `get_repo_package_names(root_path: pathlib.Path | None = None) -> list[str]`

Return a list of all top-level Python packages in the project.

Args:
    root_path (Optional[Path]): Optionally specify repo root. Defaults to auto-detection.

Returns:
    list[str]: List of package names (e.g., 'civic_lib_core', 'civic_dev').
               Returns empty list if no packages found.

### `verify_layout(layout: project_layout.ProjectLayout) -> list[str]`

Verify layout assumptions. Return list of errors (empty = all good).
