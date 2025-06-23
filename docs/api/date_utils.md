# Module `date_utils`

## Functions

### `date_range(days_back)`

Generate a list of date strings from `days_back` days ago up to today (UTC).

Args:
    days_back (int): Number of days to include, ending with today (inclusive).

Returns:
    list[str]: List of UTC dates in 'YYYY-MM-DD', earliest to latest.

### `now_utc()`

Return the current UTC datetime object.

Returns:
    datetime: Current UTC datetime.

### `now_utc_str(fmt='%Y-%m-%d %H:%M:%S UTC')`

Return the current time in UTC as a formatted string.

Args:
    fmt (str): Format string for datetime output. Default includes 'UTC'.

Returns:
    str: Formatted current UTC time.

### `today_utc_str()`

Return today's date in UTC in 'YYYY-MM-DD' format.

Returns:
    str: Current UTC date as a string.
