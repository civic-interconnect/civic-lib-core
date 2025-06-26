# Module `civic_dev.bump_version`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `bump_version_cmd(old_version: str, new_version: str) -> int`

CLI subcommand handler for version bump.

Returns:
    int: Exit code (0 on success, 1 if no updates).

### `main(old_version: str, new_version: str) -> int`

Script-style entry point.

Returns:
    int: Exit code.

### `update_file(path: pathlib.Path, old: str, new: str) -> bool`

Replace version string in the specified file if found.

Returns:
    bool: True if file was modified, False otherwise.
