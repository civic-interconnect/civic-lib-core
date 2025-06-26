# Module `civic_lib_core.report_reader`

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

### `check_schema_version(report: dict[str, typing.Any], required: str, strict: bool = False) -> bool`

Check if the report's schema version matches the required version.
Args:
    report (dict): The parsed report dictionary.
    required (str): The required schema version to check against.
    strict (bool): If True, raise an error if the version does not match.
                   If False, return False and log a warning.
Returns:
    bool: True if the schema version matches, False otherwise.

### `check_version(agent_version: str, lib_version: str, strict: bool = False) -> bool`

Check compatibility of agent and lib versions using SemVer rules.

Args:
    agent_version (str): Version string for the agent.
    lib_version (str): Version string for the shared library.
    strict (bool): If True, requires exact version match.

Returns:
    bool: True if compatible, False otherwise.

### `get_latest_report(agent_dir: pathlib.Path) -> pathlib.Path | None`

Get the most recent report file from the specified agent directory.

Args:
    agent_dir (Path): Path to the agent's report folder.

Returns:
    Path | None: The latest report file, or None if none found.

### `is_report_file(path: pathlib.Path) -> bool`

Determine whether the given file path is a valid report file.

A valid report file must:
- Have a ".json" extension
- Begin with a date prefix (e.g., "2024-01-01")

Args:
    path (Path): The path to check.

Returns:
    bool: True if the path matches report file format, False otherwise.

### `read_latest_report(agent_dir: pathlib.Path, strict: bool = False) -> dict | None`

Read and return the contents of the latest report for a given agent.

Args:
    agent_dir (Path): Path to the agent's report folder.
    strict (bool): If True, raise errors on missing or invalid reports.
                   If False, return None and log a warning.

Returns:
    dict | None: Parsed report contents, or None if no report exists or format is invalid (in non-strict mode).

### `validate_report_format(report: dict) -> bool`

Validate that a report contains all expected top-level keys.

Args:
    report (dict): The parsed report to validate.

Returns:
    bool: True if valid, False otherwise.
