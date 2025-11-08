"""
Test cases for civic-lib-core.date_utils module.
"""

from datetime import datetime
import re

from civic_lib_core import date_utils


def test_now_utc_str_format():
    result = date_utils.now_utc_str()
    # Check format: 'YYYY-MM-DD HH:MM:SS UTC'
    assert isinstance(result, str)
    assert result.endswith("UTC")
    datetime.strptime(result, "%Y-%m-%d %H:%M:%S UTC")


def test_now_utc_str_for_schemas_format():
    ts = date_utils.now_utc_str_for_schemas()
    # Must match RFC3339 UTC form without offset
    pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
    assert re.match(pattern, ts), f"Invalid timestamp format: {ts}"


def test_now_utc_str_for_schemas_parseable():
    ts = date_utils.now_utc_str_for_schemas()
    dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
    assert dt.tzinfo is None  # naive UTC is fine


def test_date_range_length():
    days = 5
    today_utc = date_utils.now_utc().date()
    dates = date_utils.date_range(days)

    assert isinstance(dates, list)
    assert len(dates) == days
    assert dates[-1] == today_utc.strftime("%Y-%m-%d")  # Ensure last date is today in UTC
