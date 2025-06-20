"""
Test cases for civic-lib-core.report_writer module.
"""

import json
from pathlib import Path

from civic_lib_core import report_writer


def test_write_report_creates_file(tmp_path: Path) -> None:
    data = [{"id": 1, "name": "Test"}]
    agent_name = "test_agent"
    agent_version = "v1.2.3"

    result_path = report_writer.write_report(data, agent_name, agent_version, report_dir=tmp_path)
    result_file = Path(result_path)

    assert result_file.exists()
    report = json.loads(result_file.read_text(encoding="utf-8"))
    assert report["agent"] == agent_name
    assert report["agent_version"] == agent_version
    assert report["record_count"] == 1
    assert report["schema_version"] == "1.0.0"
    assert isinstance(report["results"], list)


def test_write_report_csv_format(tmp_path: Path) -> None:
    data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    agent_name = "csv_agent"
    agent_version = "v0.9.0"

    result_path = report_writer.write_report(
        data, agent_name, agent_version, report_dir=tmp_path, file_format="csv"
    )

    result_file = Path(result_path)
    assert result_file.exists()
    content = result_file.read_text(encoding="utf-8")
    assert "id,name" in content
    assert "1,Alice" in content
    assert "2,Bob" in content
