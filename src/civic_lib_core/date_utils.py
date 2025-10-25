"""civic_lib_core/date_utils.py.

Date and time utilities for Civic Interconnect projects.

Provides helpers to:
- Generate date ranges for reports
- Retrieve current UTC time or date
- Format UTC datetimes into strings

Typical usage:

    from civic_lib_core import date_utils

    # Get today's UTC date string
    today = date_utils.today_utc_str()

    # Get current UTC datetime as a string
    timestamp = date_utils.now_utc_str()

    # Generate list of dates for the past 7 days
    dates = date_utils.date_range(7)
"""

from datetime import UTC, datetime, timedelta

__all__ = [
    "date_range",
    "now_utc",
    "now_utc_str",
    "today_utc_str",
]


def date_range(days_back: int) -> list[str]:
    """Generate a list of date strings from `days_back` days ago up to today (UTC).

    Args:
        days_back (int): Number of days to include, ending with today (inclusive).
                         For example, days_back=7 returns 7 dates.

    Returns:
        list[str]: List of UTC dates in 'YYYY-MM-DD' format, earliest to latest.

    Raises:
        ValueError: If days_back is negative.
    """
    if days_back < 0:
        raise ValueError("days_back must be non-negative")

    if days_back == 0:
        return []

    today = now_utc().date()
    start_date = today - timedelta(days=days_back - 1)
    return [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days_back)]


def now_utc() -> datetime:
    """Return the current UTC datetime object.

    Returns:
        datetime: Current UTC datetime.
    """
    return datetime.now(UTC)


def now_utc_str(fmt: str = "%Y-%m-%d %H:%M:%S UTC") -> str:
    """Return the current time in UTC as a formatted string.

    Args:
        fmt (str): Format string for datetime output. Default includes 'UTC'.

    Returns:
        str: Formatted current UTC time.
    """
    return now_utc().strftime(fmt)


def today_utc_str() -> str:
    """Return today's date in UTC in 'YYYY-MM-DD' format.

    Returns:
        str: Current UTC date as a string.
    """
    return now_utc().strftime("%Y-%m-%d")
