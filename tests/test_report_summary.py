"""
Test cases for civic-lib-core.report_summary module.
"""

from pathlib import Path

from civic_lib_core import report_summary


def test_write_markdown_summary(tmp_path: Path) -> None:
    report = {
        "agent": "summary_agent",
        "timestamp": "2025-06-18 08:00:00 UTC",
        "record_count": 5,
        "agent_version": "v1.1.0",
        "lib_version": "v0.2.0",
        "results": [],
    }

    path = tmp_path / "summary.md"
    report_summary.write_markdown_summary(report, path)

    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "summary_agent" in content
    assert "Record Count: 5" in content or "Record Count:** 5" in content
