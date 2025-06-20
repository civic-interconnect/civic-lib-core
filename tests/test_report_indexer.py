"""
Test cases for civic-lib-core.report_indexer module.
"""

from pathlib import Path

from civic_lib_core import report_indexer, report_writer


def test_generate_index_creates_index_md(tmp_path: Path) -> None:
    agent_name = "index_test_agent"
    report_writer.write_report([{"foo": "bar"}], agent_name, "v0.1.0", report_dir=tmp_path)

    reports_dir = tmp_path
    report_indexer.generate_index(report_dir=reports_dir)

    index_file = reports_dir / "index.md"
    assert index_file.exists()
    content = index_file.read_text(encoding="utf-8")
    assert agent_name.replace("_", " ").title() in content
    assert "Latest Report" in content
