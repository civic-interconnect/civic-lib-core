"""civic_lib_core/report_writer.py.

Functions for writing timestamped agent reports in multiple formats.
Used by daily Civic Interconnect agents.

"""

from datetime import datetime
import json
from pathlib import Path
from typing import Any

from civic_lib_core import log_utils, report_formatter, version_utils
from civic_lib_core.date_utils import now_utc_str
from civic_lib_core.fs_utils import ensure_dir, safe_filename
from civic_lib_core.report_constants import DATE_ONLY_FORMAT, REPORTS_DIR, TIMESTAMP_FORMAT

__all__ = ["write_report"]

logger = log_utils.logger


def write_report(
    data: list[dict[str, Any]],
    agent_name: str,
    agent_version: str,
    schema_version: str = "1.0.0",
    report_dir: str | Path = REPORTS_DIR,
    file_format: str = "json",
) -> Path:
    """Write agent output to a timestamped report file with metadata.

    Args:
        data (list[dict[str, Any]]): The results to include in the report.
        agent_name (str): The name of the agent generating the report.
        agent_version (str): The version of the agent code.
        schema_version (str): The version of the report schema (default: "1.0.0").
        report_dir (str | Path): Root directory where reports are saved (default: REPORTS_DIR).
        file_format (str): Output format, one of "json" or "csv" (default: "json").

    Returns:
        Path: The full path to the saved report file.
    """
    timestamp = now_utc_str(TIMESTAMP_FORMAT)
    date_str = datetime.strptime(timestamp, TIMESTAMP_FORMAT).strftime(DATE_ONLY_FORMAT)

    agent_folder = ensure_dir(Path(report_dir) / safe_filename(agent_name))
    report_path = agent_folder / f"{date_str}.{file_format}"

    if file_format == "json":
        report = {
            "agent": agent_name,
            "timestamp": timestamp,
            "record_count": len(data),
            "agent_version": agent_version,
            "schema_version": schema_version,
            "lib_version": version_utils.get_repo_version(),
            "results": data,
        }
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    elif file_format == "csv":
        report_formatter.to_csv(data, report_path)

    else:
        raise ValueError(f"Unsupported report format: {file_format}")

    logger.info(f"Report written: {report_path}")
    return report_path
