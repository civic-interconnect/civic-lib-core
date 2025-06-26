# Module `civic_lib_core.report_archiver`

## Classes

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

### `timedelta(self, /, *args, **kwargs)`

Difference between two datetime values.

timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

All arguments are optional and default to 0.
Arguments may be integers or floats, and may be positive or negative.

## Functions

### `archive_old_reports(agent_dir: pathlib.Path, keep_latest: bool = True) -> list[pathlib.Path]`

Rename old .json reports to .archived.json, optionally keeping the latest.

Args:
    agent_dir (Path): Directory with report files.
    keep_latest (bool): Whether to keep the most recent report unarchived.

Returns:
    list[Path]: List of archived report file paths.

### `archive_reports_older_than(agent_dir: pathlib.Path, days_old: int) -> list[pathlib.Path]`

Archive reports older than a specified number of days.
