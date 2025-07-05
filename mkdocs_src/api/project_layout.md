# Module `project_layout`

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

Return key layout paths for the current Civic Interconnect project.

This function delegates the primary discovery to `fs_utils.discover_project_layout()`
which is responsible for finding all necessary paths and loading the policy,
then returns the structured ProjectLayout object.

Returns:
    ProjectLayout: Structured layout information.

### `format_layout(layout: project_layout.ProjectLayout) -> str`

Format layout info for display.

Args:
    layout (ProjectLayout): The layout info to print.

Returns:
    str: A formatted string for display.

### `get_errors(layout, errors)`

No description available.

### `main() -> None`

Standalone entry point for testing this layout module.
Prints layout and any issues found.

### `verify_layout(layout: project_layout.ProjectLayout) -> list[str]`

Verify layout assumptions for a Civic Interconnect repo.

Args:
    layout (ProjectLayout): The discovered layout.

Returns:
    list[str]: Any problems detected (empty list means all OK).
