# Module `civic_lib_core.config_utils`

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

Load an API key from the environment.

Args:
    env_var (str): Environment variable name to load.
    service_name (str): Friendly service name for error messaging.

Returns:
    str: API key value.

Exits:
    If the API key is missing.

### `load_version(filename: str = 'VERSION', root_dir: pathlib.Path | None = None) -> str`

Load the version string from a VERSION file.

Args:
    filename (str): The version filename (default: "VERSION").
    root_dir (Path | None): Optional base path.

Returns:
    str: Version string.

Exits:
    If the file is missing or unreadable.

### `load_yaml_config(filename: str = 'config.yaml', root_dir: pathlib.Path | None = None) -> dict`

Load a YAML configuration file from the given root directory.

Args:
    filename (str): The config file name (default: "config.yaml").
    root_dir (Path | None): Root directory to search (default: Path.cwd()).

Returns:
    dict: Parsed configuration as a dictionary.

Raises:
    FileNotFoundError: If the config file cannot be found.

### `parse_version(version: str) -> tuple[int, int, int]`

Parse a version string like '1.2.3' into a tuple.

Raises:
    ValueError: if the version is not properly formatted.
