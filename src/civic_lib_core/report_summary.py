"""
civic_lib_core/report_summary.py

Generates human-readable Markdown summaries of Civic Interconnect agent reports.
Used optionally by agents or admin tools alongside JSON output.

MIT License — maintained by Civic Interconnect
"""

from pathlib import Path

from civic_lib_core import log_utils

__all__ = ["write_markdown_summary"]

logger = log_utils.logger


def write_markdown_summary(report: dict, path: Path) -> None:
    """
    Write a Markdown summary of a report's key metadata.

    Args:
        report (dict): The report data (already parsed).
        path (Path): The output path to write the .md file.
    """
    lines = [
        f"# Report Summary for {report.get('agent', 'Unknown Agent')}",
        f"**Date:** {report.get('timestamp', 'Unknown')}",
        f"**Agent Version:** {report.get('agent_version', 'N/A')}",
        f"**Library Version:** {report.get('lib_version', 'N/A')}",
        f"**Record Count:** {report.get('record_count', 'N/A')}",
        "",
        "Auto-generated summary. Data is available in the JSON report.",
    ]

    path.write_text("\n".join(lines), encoding="utf-8")
    logger.info(f"Markdown summary written to {path}")
