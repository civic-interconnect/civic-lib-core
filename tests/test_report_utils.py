"""
Test cases for civic-lib-core.report_utils module.
"""

from pathlib import Path

from civic_lib_core import report_utils


def test_is_report_file_true():
    path = Path("reports/my_agent/2024-01-01.json")
    assert report_utils.is_report_file(path)


def test_is_report_file_false_wrong_extension():
    path = Path("reports/my_agent/2024-01-01.txt")
    assert not report_utils.is_report_file(path)


def test_is_report_file_false_non_date_stem():
    path = Path("reports/my_agent/readme.json")
    assert not report_utils.is_report_file(path)


def test_get_agent_name_from_path():
    path = Path("reports/my_test_agent/2024-01-01.json")
    assert report_utils.get_agent_name_from_path(path) == "My Test Agent"
