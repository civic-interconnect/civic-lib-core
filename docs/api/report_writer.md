# Module `report_writer`

## Functions

### `write_report(data, agent_name, agent_version, schema_version='1.0.0', report_dir=REPORTS_DIR, file_format='json')`

Write agent output to a timestamped report file with metadata.

Args:
    data (list[dict[str, Any]]): The results to include in the report.
    agent_name (str): The name of the agent generating the report.
    agent_version (str): The version of the agent code.
    report_dir (str | Path): Root directory where reports are saved (default: REPORTS_DIR).
    file_format (str): Output format, one of "json" or "csv" (default: "json").

Returns:
    Path: The full path to the saved report file.
