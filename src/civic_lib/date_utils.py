"""
civic_lib/date_utils.py

Date handling helpers for reports and time-based logic.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
"""

from datetime import UTC, datetime, timedelta

__all__ = [
    "date_range",
    "now_utc",
    "now_utc_str",
    "today_utc_str",
]


def date_range(days_back: int) -> list[str]:
    """
    Generate a list of date strings from `days_back` days ago up to today (UTC).

    Args:
        days_back (int): Number of days to include, ending with today (inclusive).

    Returns:
        list[str]: List of UTC dates in 'YYYY-MM-DD', earliest to latest.
    """
    if days_back < 0:
        raise ValueError("days_back must be non-negative")
    today = now_utc().date()
    start_date = today - timedelta(days=days_back - 1)
    return [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days_back)]


def now_utc() -> datetime:
    """
    Return the current UTC datetime object.

    Returns:
        datetime: Current UTC datetime.
    """
    return datetime.now(UTC)


def now_utc_str(fmt: str = "%Y-%m-%d %H:%M:%S UTC") -> str:
    """
    Return the current time in UTC as a formatted string.

    Args:
        fmt (str): Format string for datetime output. Default includes 'UTC'.

    Returns:
        str: Formatted current UTC time.
    """
    return now_utc().strftime(fmt)


def today_utc_str() -> str:
    """
    Return today's date in UTC in 'YYYY-MM-DD' format.

    Returns:
        str: Current UTC date as a string.
    """
    return now_utc().strftime("%Y-%m-%d")
