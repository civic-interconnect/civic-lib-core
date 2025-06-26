# Module `civic_lib_core.version_utils`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `bump_version(old_version: str, new_version: str) -> int`

No description available.

### `check_version(agent_version: str, lib_version: str, strict: bool = False) -> bool`

Check compatibility of agent and lib versions using SemVer rules.

Args:
    agent_version (str): Version string for the agent.
    lib_version (str): Version string for the shared library.
    strict (bool): If True, requires exact version match.

Returns:
    bool: True if compatible, False otherwise.

### `find_init_files(root_dir: pathlib.Path) -> list[pathlib.Path]`

Recursively find all __init__.py files under the given directory.

### `get_lib_version() -> str`

Get the current library version.

Returns:
    str: The semantic version string (e.g., "1.2.3").

### `get_version() -> str`

Convenience alias for get_lib_version().

### `lib_version() -> str`

Convenience alias for get_lib_version().

### `parse_version(version: str) -> tuple[int, int, int]`

Parse a version string into a tuple of integers.

Args:
    version (str): A semantic version string, e.g., "1.2.3".

Returns:
    tuple[int, int, int]: A tuple of (major, minor, patch) version numbers.

Raises:
    ValueError: If the version string is not in the expected format.

### `update_version_in_init(path: pathlib.Path, new_version: str) -> bool`

Update __version__ assignment in a given __init__.py file.
Only works for simple string assignment: __version__ = "..."

### `update_version_string(path: pathlib.Path, old: str, new: str) -> bool`

No description available.
