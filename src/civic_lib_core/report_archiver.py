"""
civic_lib_core/report_archiver.py

Archives old Civic Interconnect agent reports by renaming them with `.archived.json`.
Used by admin and maintenance tools, not daily agents.

MIT License — maintained by Civic Interconnect
"""

from datetime import UTC, datetime, timedelta
from pathlib import Path

from civic_lib_core import log_utils
from civic_lib_core.report_constants import DATE_ONLY_FORMAT

__all__ = ["archive_old_reports", "archive_reports_older_than"]

logger = log_utils.logger


def archive_old_reports(agent_dir: Path, keep_latest: bool = True) -> list[Path]:
    """
    Rename old .json reports to .archived.json, optionally keeping the latest.

    Args:
        agent_dir (Path): Directory with report files.
        keep_latest (bool): Whether to keep the most recent report unarchived.

    Returns:
        list[Path]: List of archived report file paths.
    """
    if not agent_dir.exists() or not agent_dir.is_dir():
        logger.warning(f"Agent report directory does not exist: {agent_dir}")
        return []

    json_reports = sorted(agent_dir.glob("*.json"), reverse=True)

    if keep_latest and json_reports:
        json_reports = json_reports[1:]  # Skip most recent

    archived = []

    for path in json_reports:
        archived_path = path.with_suffix(".archived.json")
        try:
            path.rename(archived_path)
            logger.info(f"Archived report: {archived_path}")
            archived.append(archived_path)
        except Exception as e:
            logger.error(f"Failed to archive {path}: {e}")

    return archived


def archive_reports_older_than(agent_dir: Path, days_old: int) -> list[Path]:
    """
    Archive reports older than a specified number of days.
    """
    cutoff_date = datetime.now(UTC) - timedelta(days=days_old)
    archived = []

    for path in agent_dir.glob("*.json"):
        try:
            date_str = path.stem  # e.g., "2024-07-17"
            report_date = datetime.strptime(date_str, DATE_ONLY_FORMAT).replace(tzinfo=UTC)
            if report_date < cutoff_date:
                archived_path = path.with_suffix(".archived.json")
                path.rename(archived_path)
                logger.info(f"Archived report older than {days_old} days: {archived_path}")
                archived.append(archived_path)
        except ValueError:
            logger.warning(f"Skipping non-date report file: {path.name}")
        except Exception as e:
            logger.error(f"Failed to archive {path.name}: {e}")

    return archived
