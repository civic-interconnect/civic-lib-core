# Module `file_utils`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `ensure_docs_output_dir(output_dir_str: str = 'api') -> pathlib.Path`

Ensure output directory exists under project root/docs.

### `ensure_source_path(source_pkg_str: str = 'civic_lib_core') -> pathlib.Path`

Resolve and validate the source package path.

### `find_project_root() -> pathlib.Path`

Find the actual project root, whether civic_lib_core is installed or local.

Returns:
    Path: The project root directory

### `resolve_path(relative_path: str | pathlib.Path) -> pathlib.Path`

Return an absolute Path from project root for a relative path.

Args:
    relative_path (str | Path): The relative or partial path to resolve.

Returns:
    Path: The absolute path resolved from the project root.
