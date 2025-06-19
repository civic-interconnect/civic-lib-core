"""
Test cases for civic_lib.report_archiver module.
"""

from datetime import UTC, datetime, timedelta
from pathlib import Path

from civic_lib import report_archiver


def test_archive_old_reports(tmp_path: Path) -> None:
    agent_name = "archive_me"
    agent_dir = tmp_path / agent_name
    agent_dir.mkdir(parents=True)

    # Create fake reports
    (agent_dir / "2022-01-01.json").write_text("{}", encoding="utf-8")
    (agent_dir / "2022-01-02.json").write_text("{}", encoding="utf-8")
    (agent_dir / "2022-01-03.json").write_text("{}", encoding="utf-8")

    archived = report_archiver.archive_old_reports(agent_dir, keep_latest=True)
    archived_names = [f.name for f in archived]

    assert "2022-01-01.archived.json" in archived_names
    assert "2022-01-02.archived.json" in archived_names
    assert "2022-01-03.archived.json" not in archived_names


def test_archive_reports_older_than(tmp_path: Path) -> None:
    agent_dir = tmp_path / "old_reports"
    agent_dir.mkdir(parents=True)

    # Create one old report and one recent report
    old_date = (datetime.now(UTC) - timedelta(days=10)).strftime("%Y-%m-%d")
    recent_date = datetime.now(UTC).strftime("%Y-%m-%d")

    old_report = agent_dir / f"{old_date}.json"
    recent_report = agent_dir / f"{recent_date}.json"

    old_report.write_text("{}", encoding="utf-8")
    recent_report.write_text("{}", encoding="utf-8")

    archived = report_archiver.archive_reports_older_than(agent_dir, days_old=7)
    archived_names = [f.name for f in archived]

    assert f"{old_date}.archived.json" in archived_names
    assert not (agent_dir / f"{old_date}.json").exists()
    assert (agent_dir / f"{recent_date}.json").exists()
    assert (agent_dir / f"{old_date}.archived.json").read_text() == "{}"


def test_archive_with_empty_dir(tmp_path: Path):
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    archived = report_archiver.archive_old_reports(empty_dir)
    assert archived == []


def test_archive_skips_non_date_files(tmp_path: Path):
    agent_dir = tmp_path / "mixed_files"
    agent_dir.mkdir()
    (agent_dir / "readme.txt").write_text("not a report")
    archived = report_archiver.archive_old_reports(agent_dir)
    assert archived == []
