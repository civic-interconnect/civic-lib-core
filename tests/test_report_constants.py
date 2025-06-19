"""
Test cases for civic_lib.report_constants module.
"""

from civic_lib import report_constants


def test_timestamp_format_constant_exists() -> None:
    assert isinstance(report_constants.TIMESTAMP_FORMAT, str)
    assert "%Y" in report_constants.TIMESTAMP_FORMAT  # basic check


def test_reports_dir_constant_exists(tmp_path, monkeypatch):
    # Redirect REPORTS_DIR to a temporary path for test safety
    monkeypatch.setattr(report_constants, "REPORTS_DIR", tmp_path)

    # Ensure directory creation (same as production)
    report_constants.REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    assert report_constants.REPORTS_DIR.exists()
    assert report_constants.REPORTS_DIR.is_dir()
