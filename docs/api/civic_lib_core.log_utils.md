# Module `civic_lib_core.log_utils`

## Functions

### `ensure_dir(path: str | pathlib.Path) -> pathlib.Path`

Ensure a directory exists, creating it if necessary.

Args:
    path (str | Path): The directory path to ensure.

Returns:
    Path: The resolved Path object of the directory.

Raises:
    OSError: If directory cannot be created due to permissions or other issues.

### `init_logger(log_level: str | None = None, log_to_console: bool = True) -> None`

Initialize loguru logging once per session.

If no log level is provided, attempts to load it from config.yaml as 'log_level'.
Defaults to INFO if not found or config is missing.

Args:
    log_level (str | None): Optional log level override (default: config.yaml or "INFO").
    log_to_console (bool): If True, logs to stderr in addition to file.

### `log_agent_end(agent_name: str, status: str = 'success') -> None`

Log the end of an agent with its status and UTC timestamp.

### `log_agent_start(agent_name: str) -> None`

Log the start of an agent by name.

### `now_utc_str(fmt: str = '%Y-%m-%d %H:%M:%S UTC') -> str`

Return the current time in UTC as a formatted string.

Args:
    fmt (str): Format string for datetime output. Default includes 'UTC'.

Returns:
    str: Formatted current UTC time.
