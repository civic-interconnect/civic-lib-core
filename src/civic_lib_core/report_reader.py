"""
civic_lib_core/report_reader.py

Functions for reading, inspecting, and validating Civic Interconnect agent reports.
Used by dashboards, CLI tools, and indexing utilities.

MIT License — maintained by Civic Interconnect
"""

import json
from pathlib import Path
from typing import Any

from civic_lib_core import log_utils
from civic_lib_core.report_constants import EXPECTED_REPORT_KEYS, REPORT_EXTENSION
from civic_lib_core.report_utils import is_report_file
from civic_lib_core.version_utils import check_version

__all__ = [
    "check_schema_version",
    "get_latest_report",
    "read_latest_report",
    "validate_report_format",
]

logger = log_utils.logger


def check_schema_version(report: dict[str, Any], required: str, strict: bool = False) -> bool:
    """
    Check if the report's schema version matches the required version.
    Args:
        report (dict): The parsed report dictionary.
        required (str): The required schema version to check against.
        strict (bool): If True, raise an error if the version does not match.
                       If False, return False and log a warning.
    Returns:
        bool: True if the schema version matches, False otherwise.
    """
    actual = report.get("schema_version", "0.0.0")
    return check_version(required, actual, strict=strict)


def get_latest_report(agent_dir: Path) -> Path | None:
    """
    Get the most recent report file from the specified agent directory.

    Args:
        agent_dir (Path): Path to the agent's report folder.

    Returns:
        Path | None: The latest report file, or None if none found.
    """
    report_files = sorted(
        (f for f in agent_dir.glob(f"*{REPORT_EXTENSION}") if is_report_file(f)),
        reverse=True,
    )
    latest = report_files[0] if report_files else None

    if latest:
        logger.debug(f"Latest report for {agent_dir.name}: {latest.name}")
    else:
        logger.warning(f"No reports found in {agent_dir.name}")

    return latest


def read_latest_report(agent_dir: Path, strict: bool = False) -> dict | None:
    """
    Read and return the contents of the latest report for a given agent.

    Args:
        agent_dir (Path): Path to the agent's report folder.
        strict (bool): If True, raise errors on missing or invalid reports.
                       If False, return None and log a warning.

    Returns:
        dict | None: Parsed report contents, or None if no report exists or format is invalid (in non-strict mode).
    """
    latest = get_latest_report(agent_dir)
    if not latest:
        msg = f"No report found in {agent_dir}"
        if strict:
            raise FileNotFoundError(msg)
        logger.warning(msg)
        return None

    try:
        data = json.loads(latest.read_text(encoding="utf-8"))
    except Exception as e:
        msg = f"Failed to read report: {latest} — {e}"
        if strict:
            raise ValueError(msg) from e
        logger.warning(msg)
        return None

    if not validate_report_format(data):
        msg = f"Invalid report format in: {latest}"
        if strict:
            raise ValueError(msg)
        logger.warning(msg)
        return None

    return data


def validate_report_format(report: dict) -> bool:
    """
    Validate that a report contains all expected top-level keys.

    Args:
        report (dict): The parsed report to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    keys = set(report.keys())
    missing = EXPECTED_REPORT_KEYS - keys
    if missing:
        logger.warning(f"Report missing expected keys: {missing}")
        return False
    return True
