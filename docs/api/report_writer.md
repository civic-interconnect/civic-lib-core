# Module `report_writer`

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

### `datetime(self, /, *args, **kwargs)`

datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])

The year, month and day arguments are required. tzinfo may be None, or an
instance of a tzinfo subclass. The remaining arguments may be ints.

## Functions

### `ensure_dir(path: str | pathlib.Path) -> pathlib.Path`

Ensure a directory exists, creating it if necessary.

Args:
    path (str | Path): The directory path to ensure.

Returns:
    Path: The resolved Path object of the directory.

### `now_utc_str(fmt: str = '%Y-%m-%d %H:%M:%S UTC') -> str`

Return the current time in UTC as a formatted string.

Args:
    fmt (str): Format string for datetime output. Default includes 'UTC'.

Returns:
    str: Formatted current UTC time.

### `safe_filename(name: str) -> str`

Convert a string into a safe, lowercase filename.

Replaces spaces and forward slashes with underscores.

Args:
    name (str): Original string.

Returns:
    str: Sanitized, lowercase filename string.

### `write_report(data: list[dict[str, typing.Any]], agent_name: str, agent_version: str, schema_version: str = '1.0.0', report_dir: str | pathlib.Path = WindowsPath('reports'), file_format: str = 'json') -> pathlib.Path`

Write agent output to a timestamped report file with metadata.

Args:
    data (list[dict[str, Any]]): The results to include in the report.
    agent_name (str): The name of the agent generating the report.
    agent_version (str): The version of the agent code.
    report_dir (str | Path): Root directory where reports are saved (default: REPORTS_DIR).
    file_format (str): Output format, one of "json" or "csv" (default: "json").

Returns:
    Path: The full path to the saved report file.
