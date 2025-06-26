# Module `civic_lib_core.report_formatter`

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

### `format_report_as_csv(report: dict) -> str`

Convert report results to CSV format.

Args:
    report (dict): Parsed report dictionary.

Returns:
    str: CSV-formatted string of the report results.

### `format_report_as_markdown(report: dict) -> str`

Convert a report dictionary to a Markdown summary string.

Args:
    report (dict): Parsed report dictionary.

Returns:
    str: Markdown-formatted report summary.

### `format_report_as_text(report: dict) -> str`

Convert a report dictionary to a plain text summary string.

Args:
    report (dict): Parsed report dictionary.

Returns:
    str: Text-formatted report summary.

### `to_csv(data: list[dict[str, typing.Any]], path: pathlib.Path) -> None`

Write raw result data to a CSV file.

Args:
    data (list[dict]): Result rows to write.
    path (Path): File path to write CSV to.

### `to_markdown(data: list[dict[str, typing.Any]], path: pathlib.Path) -> None`

Write raw result data to a Markdown table.

Args:
    data (list[dict]): Result rows to write.
    path (Path): File path to write Markdown to.
