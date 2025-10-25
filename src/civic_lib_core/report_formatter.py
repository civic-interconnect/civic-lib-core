"""civic_lib_core/report_formatter.py.

Format Civic Interconnect agent reports into various human-readable forms.
Supports Markdown, plain text, and CSV formats.

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


def format_report_as_csv(report: dict[str, Any]) -> str:
    """Format a report dictionary as a CSV string.

    Args:
        report (dict): A dictionary containing report data with a 'results' key
                      that holds a list of dictionaries to be formatted as CSV.

    Returns:
        str: A CSV-formatted string with headers and data rows, or a message
             indicating no results are available if the results list is empty.
    """
    results = report.get("results", [])
    if not results:
        return "No results to export."

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)
    return output.getvalue()


def format_report_as_markdown(report: dict[str, Any]) -> str:
    """Format a report dictionary as a markdown string.

    Takes a report dictionary containing agent information, metadata, and results,
    and converts it into a well-formatted markdown document with a summary section
    and a sample result displayed as JSON.

    Args:
        report (dict[str, Any]): A dictionary containing report data with the following
            optional keys:
            - 'agent': Name of the agent that generated the report
            - 'timestamp': When the report was generated
            - 'agent_version': Version of the agent
            - 'lib_version': Version of the library used
            - 'record_count': Number of records processed
            - 'results': List of result objects

    Returns:
        str: A markdown-formatted string containing the report summary and
             the first result from the results list (if available) displayed
             as a JSON code block.

    Example:
        >>> report = {
        ...     'agent': 'DataProcessor',
        ...     'timestamp': '2023-10-01T12:00:00Z',
        ...     'record_count': 100,
        ...     'results': [{'id': 1, 'status': 'success'}],
        ... }
        >>> markdown = format_report_as_markdown(report)
        >>> print(markdown)
        # Report Summary for DataProcessor
        **Date:** 2023-10-01T12:00:00Z
        ...
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


def format_report_as_text(report: dict[str, Any]) -> str:
    """Format a report dictionary as a human-readable text string.

    Args:
        report (dict): A dictionary containing report data with keys like 'agent',
                      'timestamp', 'agent_version', 'lib_version', 'record_count',
                      and 'results'.

    Returns:
        str: A formatted multi-line string representation of the report including
             metadata and the first sample result (if available).

    Example:
        >>> report = {
        ...     'agent': 'DataCollector',
        ...     'timestamp': '2023-10-15 14:30:00',
        ...     'agent_version': '1.2.3',
        ...     'lib_version': '2.1.0',
        ...     'record_count': 150,
        ...     'results': [{'id': 1, 'value': 'sample'}],
        ... }
        >>> print(format_report_as_text(report))
        Report: DataCollector
        Date: 2023-10-15 14:30:00
        Agent Version: 1.2.3
        Library Version: 2.1.0
        Record Count: 150

        Sample Result:
        {
          "id": 1,
          "value": "sample"
        }
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
    if sample:
        lines.append(json.dumps(sample[0], indent=2))
    else:
        lines.append("No results to display.")
    return "\n".join(lines)


def to_csv(data: list[dict[str, Any]], path: Path) -> None:
    """Write a list of dictionaries to a CSV file.

    If the data list is empty, writes "No results to export." to the file instead.
    The CSV header is generated from the keys of the first dictionary in the list.

    Args:
        data: A list of dictionaries to write to CSV. All dictionaries should
              have the same keys for proper CSV formatting.
        path: The file path where the CSV will be written. Will be created
              if it doesn't exist.

    Returns:
        None

    Note:
        The file is written with UTF-8 encoding. If data is empty, a plain text
        message is written instead of CSV format.
    """
    if not data:
        path.write_text("No results to export.", encoding="utf-8")
        return

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def to_markdown(data: list[dict[str, Any]], path: Path) -> None:
    """Convert a list of dictionaries to a Markdown table and write it to a file.

    Takes a list of dictionaries where each dictionary represents a row of data,
    and converts it into a Markdown table format. The keys of the first dictionary
    are used as column headers. If the data list is empty, writes a message
    indicating no results to display.

    Args:
        data (list[dict[str, Any]]): List of dictionaries containing the data to convert.
                                   Each dictionary should have the same keys which will
                                   be used as table headers.
        path (Path): Path object specifying where to write the Markdown table file.

    Returns:
        None: The function writes directly to the specified file path.

    Note:
        - Pipe characters (|) in data values are automatically escaped to preserve
          Markdown table formatting.
        - The file is written with UTF-8 encoding.
        - If data is empty, writes "_No results to display._" to the file.
    """
    if not data:
        path.write_text("_No results to display._", encoding="utf-8")
        return

    headers = list(data[0].keys())
    lines = ["| " + " | ".join(headers) + " |"]
    lines.append("|" + "|".join(["---"] * len(headers)) + "|")

    for row in data:
        # Escape any pipe characters to preserve Markdown table
        row_values = [str(row[h]).replace("|", "\\|") for h in headers]
        lines.append("| " + " | ".join(row_values) + " |")

    path.write_text("\n".join(lines), encoding="utf-8")
