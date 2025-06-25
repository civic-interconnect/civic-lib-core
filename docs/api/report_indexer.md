# Module `report_indexer`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `ensure_dir(path: str | pathlib.Path) -> pathlib.Path`

Ensure a directory exists, creating it if necessary.

Args:
    path (str | Path): The directory path to ensure.

Returns:
    Path: The resolved Path object of the directory.

### `generate_index(report_dir: pathlib.Path = WindowsPath('reports')) -> None`

Generate a Markdown index listing the latest report from each agent.

Args:
    report_dir (Path): The base `reports/` directory to scan.

### `get_agent_name_from_path(path: pathlib.Path) -> str`

Extract and format the agent name from a report file path.

The agent name is derived from the parent folder of the report file,
with underscores replaced by spaces and title-cased.

If the path does not have a parent directory, returns 'Unknown Agent'.

Args:
    path (Path): The path to a report file.

Returns:
    str: Formatted agent name or fallback string.

### `get_latest_report(agent_dir: pathlib.Path) -> pathlib.Path | None`

Get the most recent report file from the specified agent directory.

Args:
    agent_dir (Path): Path to the agent's report folder.

Returns:
    Path | None: The latest report file, or None if none found.
