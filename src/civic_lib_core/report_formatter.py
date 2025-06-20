"""
civic_lib_core/report_formatter.py

Format Civic Interconnect agent reports into various human-readable forms.
Supports Markdown, plain text, and CSV formats.

MIT License — maintained by Civic Interconnect
"""

import csv
import io
import json
from pathlib import Path
from typing import Any

__all__ = [
    "format_report_as_csv",
    "format_report_as_markdown",
    "format_report_as_text",
    "to_csv",
    "to_markdown",
]


def format_report_as_csv(report: dict) -> str:
    """
    Convert report results to CSV format.

    Args:
        report (dict): Parsed report dictionary.

    Returns:
        str: CSV-formatted string of the report results.
    """
    results = report.get("results", [])
    if not results:
        return "No results to export."

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)
    return output.getvalue()


def format_report_as_markdown(report: dict) -> str:
    """
    Convert a report dictionary to a Markdown summary string.

    Args:
        report (dict): Parsed report dictionary.

    Returns:
        str: Markdown-formatted report summary.
    """
    lines = [
        f"# Report Summary for {report.get('agent', 'Unknown Agent')}",
        f"**Date:** {report.get('timestamp', 'Unknown')}",
        f"**Agent Version:** {report.get('agent_version', 'N/A')}",
        f"**Library Version:** {report.get('lib_version', 'N/A')}",
        f"**Record Count:** {report.get('record_count', 'N/A')}",
        "",
        "## Sample Result",
    ]
    sample = report.get("results", [])
    if sample:
        lines.append("```json")
        lines.append(json.dumps(sample[0], indent=2))
        lines.append("```")
    else:
        lines.append("_No results to display._")

    return "\n".join(lines)


def format_report_as_text(report: dict) -> str:
    """
    Convert a report dictionary to a plain text summary string.

    Args:
        report (dict): Parsed report dictionary.

    Returns:
        str: Text-formatted report summary.
    """
    lines = [
        f"Report: {report.get('agent', 'Unknown Agent')}",
        f"Date: {report.get('timestamp', 'Unknown')}",
        f"Agent Version: {report.get('agent_version', 'N/A')}",
        f"Library Version: {report.get('lib_version', 'N/A')}",
        f"Record Count: {report.get('record_count', 'N/A')}",
        "",
        "Sample Result:",
    ]
    sample = report.get("results", [])
    lines.append(json.dumps(sample[0], indent=2)) if sample else lines.append(
        "No results to display."
    )
    return "\n".join(lines)


def to_csv(data: list[dict[str, Any]], path: Path) -> None:
    """
    Write raw result data to a CSV file.

    Args:
        data (list[dict]): Result rows to write.
        path (Path): File path to write CSV to.
    """
    if not data:
        path.write_text("No results to export.", encoding="utf-8")
        return

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def to_markdown(data: list[dict[str, Any]], path: Path) -> None:
    """
    Write raw result data to a Markdown table.

    Args:
        data (list[dict]): Result rows to write.
        path (Path): File path to write Markdown to.
    """
    if not data:
        path.write_text("_No results to display._", encoding="utf-8")
        return

    headers = data[0].keys()
    lines = ["| " + " | ".join(headers) + " |"]
    lines.append("|" + "|".join(["---"] * len(headers)) + "|")

    for row in data:
        lines.append("| " + " | ".join(str(row[h]) for h in headers) + " |")

    path.write_text("\n".join(lines), encoding="utf-8")
