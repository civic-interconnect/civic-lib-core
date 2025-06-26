# Module `civic_dev.prep_code`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `get_lib_version() -> str`

Get the current library version.

Returns:
    str: The semantic version string (e.g., "1.2.3").

### `main() -> int`

No description available.

### `run_check(command: list[str], label: str) -> None`

Run a shell command and fail fast if it errors.

### `should_reinstall() -> bool`

Determine whether the virtual environment should be reinstalled
based on timestamps of dependency files.
