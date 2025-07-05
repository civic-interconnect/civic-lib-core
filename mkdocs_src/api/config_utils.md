# Module `config_utils`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `load_api_key(env_var: str, service_name: str) -> str`

Load an API key from the environment variables.

Args:
    env_var (str): The name of the environment variable to read.
    service_name (str): A friendly name for the service (for error messages).

Returns:
    str: The API key value.

Exits:
    If the environment variable is missing or empty.

### `load_version(filename: str = 'VERSION', root_dir: pathlib.Path | None = None) -> str`

Load the version string from a VERSION file in the project.

Args:
    filename (str): Name of the version file (default: "VERSION").
    root_dir (Optional[Path]): Base path to search (default: detected project root).

Returns:
    str: Version string (e.g., "1.2.3").

Exits:
    If the version file is missing or unreadable.

### `load_yaml_config(filename: str = 'config.yaml', root_dir: pathlib.Path | None = None) -> dict`

Load a YAML configuration file from the project root.

Args:
    filename (str): Name of the config file (default: "config.yaml").
    root_dir (Optional[Path]): Directory to search (default: detected project root).

Returns:
    dict: Parsed configuration as a Python dictionary.

Raises:
    FileNotFoundError: If the config file cannot be found.

### `parse_version(version: str) -> tuple[int, int, int]`

Parse a version string (e.g., "1.2.3") into a tuple of integers.

Args:
    version (str): Version string.

Returns:
    tuple[int, int, int]: A tuple of (major, minor, patch).

Raises:
    ValueError: If the version string is improperly formatted.
