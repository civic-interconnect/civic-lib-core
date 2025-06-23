# Module `config_utils`

## Functions

### `load_api_key(env_var, service_name)`

Load an API key from the environment.

Args:
    env_var (str): Environment variable name to load.
    service_name (str): Friendly service name for error messaging.

Returns:
    str: API key value.

Exits:
    If the API key is missing.

### `load_version(filename='VERSION', root_dir=None)`

Load the version string from a VERSION file.

Args:
    filename (str): The version filename (default: "VERSION").
    root_dir (Path | None): Optional base path.

Returns:
    str: Version string.

Exits:
    If the file is missing or unreadable.

### `load_yaml_config(filename='config.yaml', root_dir=None)`

Load a YAML configuration file from the given root directory.

Args:
    filename (str): The config file name (default: "config.yaml").
    root_dir (Path | None): Root directory to search (default: Path.cwd()).

Returns:
    dict: Parsed configuration as a dictionary.

Raises:
    FileNotFoundError: If the config file cannot be found.

### `parse_version(version)`

Parse a version string like '1.2.3' into a tuple.

Raises:
    ValueError: if the version is not properly formatted.
