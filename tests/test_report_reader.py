"""
civic_lib_core/report_reader.py

Functions for reading and validating Civic Interconnect agent reports.
"""

import json
from pathlib import Path
from typing import Any

from civic_lib_core import log_utils
from civic_lib_core.report_constants import REPORT_EXTENSION
from civic_lib_core.report_utils import is_report_file

__all__ = ["get_latest_report", "read_latest_report", "validate_report_format"]

logger = log_utils.logger


def get_latest_report(agent_dir: Path) -> Path | None:
    """
    Get the most recent report file from the specified agent directory.

    Args:
        agent_dir (Path): Path to the agent's report folder.

    Returns:
        Path | None: The latest report file, or None if none found.
    """
    files = sorted(
        [f for f in agent_dir.glob(f"*{REPORT_EXTENSION}") if is_report_file(f)], reverse=True
    )
    result = files[0] if files else None

    if result:
        logger.debug(f"Latest report for {agent_dir.name}: {result.name}")
    else:
        logger.warning(f"No reports found in {agent_dir.name}")

    return result


def read_latest_report(agent_dir: Path) -> dict[str, Any] | None:
    """
    Read and parse the most recent report from a given agent directory.

    Args:
        agent_dir (Path): Path to the agent's report folder.

    Returns:
        dict | None: Parsed report dictionary, or None if read fails.
    """
    latest = get_latest_report(agent_dir)
    if latest:
        try:
            with open(latest, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to read report {latest}: {e}")
            return None
    return None


def validate_report_format(report: dict[str, Any]) -> bool:
    """
    Check if a report dict includes required fields.

    Args:
        report (dict): The parsed report dictionary.

    Returns:
        bool: True if the report includes all required fields.
    """
    required = {"agent", "timestamp", "record_count", "agent_version", "lib_version", "results"}
    missing = required - report.keys()
    if missing:
        logger.warning(f"Report is missing required fields: {missing}")
        return False
    return True
