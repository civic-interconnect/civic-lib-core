"""
Test cases for civic_lib.date_utils module.
"""

from datetime import datetime

from civic_lib import date_utils


def test_now_utc_str_format():
    result = date_utils.now_utc_str()
    # Check format: 'YYYY-MM-DD HH:MM:SS UTC'
    assert isinstance(result, str)
    assert result.endswith("UTC")
    datetime.strptime(result, "%Y-%m-%d %H:%M:%S UTC")


def test_date_range_length():
    days = 5
    today_utc = date_utils.now_utc().date()
    dates = date_utils.date_range(days)

    assert isinstance(dates, list)
    assert len(dates) == days
    assert dates[-1] == today_utc.strftime("%Y-%m-%d")  # Ensure last date is today in UTC
