# Module `yaml_utils`

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

### `read_yaml(path: str | pathlib.Path) -> dict[str, typing.Any]`

Read and parse a YAML file into a dictionary.

Args:
    path (str | Path): YAML file path.

Returns:
    dict: Parsed YAML data.

### `write_yaml(data: dict[str, typing.Any], path: str | pathlib.Path) -> pathlib.Path`

Write a dictionary to a YAML file.

Args:
    data (dict): Data to write.
    path (str | Path): File path to write to.

Returns:
    Path: The path the file was written to.
