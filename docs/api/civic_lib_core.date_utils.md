# Module `civic_lib_core.date_utils`

## Classes

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

### `date_range(days_back: int) -> list[str]`

Generate a list of date strings from `days_back` days ago up to today (UTC).

Args:
    days_back (int): Number of days to include, ending with today (inclusive).

Returns:
    list[str]: List of UTC dates in 'YYYY-MM-DD', earliest to latest.

### `now_utc() -> datetime.datetime`

Return the current UTC datetime object.

Returns:
    datetime: Current UTC datetime.

### `now_utc_str(fmt: str = '%Y-%m-%d %H:%M:%S UTC') -> str`

Return the current time in UTC as a formatted string.

Args:
    fmt (str): Format string for datetime output. Default includes 'UTC'.

Returns:
    str: Formatted current UTC time.

### `today_utc_str() -> str`

Return today's date in UTC in 'YYYY-MM-DD' format.

Returns:
    str: Current UTC date as a string.
