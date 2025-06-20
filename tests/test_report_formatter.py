"""
Test cases for civic-lib-core.report_formatter module.
"""

from civic_lib_core import report_formatter


def sample_report() -> dict:
    return {
        "agent": "formatter_test",
        "timestamp": "2025-06-18 10:00:00 UTC",
        "record_count": 2,
        "agent_version": "v1.2.3",
        "lib_version": "v0.4.0",
        "results": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ],
    }


def test_format_report_as_markdown() -> None:
    report = sample_report()
    markdown = report_formatter.format_report_as_markdown(report)

    assert "# Report Summary" in markdown
    assert "**Record Count:** 2" in markdown
    assert "```json" in markdown
    assert "'name': 'Alice'" in markdown or '"name": "Alice"' in markdown


def test_format_report_as_text() -> None:
    report = sample_report()
    text = report_formatter.format_report_as_text(report)

    assert "Report: formatter_test" in text
    assert "Record Count: 2" in text
    assert "Alice" in text


def test_format_report_as_csv() -> None:
    report = sample_report()
    csv_str = report_formatter.format_report_as_csv(report)

    assert "id,name" in csv_str
    assert "1,Alice" in csv_str
    assert "2,Bob" in csv_str


def test_format_report_as_csv_empty() -> None:
    empty_report = sample_report()
    empty_report["results"] = []

    csv_str = report_formatter.format_report_as_csv(empty_report)

    assert csv_str.strip() == "No results to export."
