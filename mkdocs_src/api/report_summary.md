# Module `report_summary`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `write_markdown_summary(report: dict, path: pathlib.Path) -> None`

Write a Markdown summary of a report's key metadata.

Args:
    report (dict): The report data (already parsed).
    path (Path): The output path to write the .md file.
