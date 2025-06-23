# Module `report_reader`

## Functions

### `check_schema_version(report, required, strict=False)`

Check if the report's schema version matches the required version.
Args:
    report (dict): The parsed report dictionary.
    required (str): The required schema version to check against.
    strict (bool): If True, raise an error if the version does not match.
                   If False, return False and log a warning.
Returns:
    bool: True if the schema version matches, False otherwise.

### `get_latest_report(agent_dir)`

Get the most recent report file from the specified agent directory.

Args:
    agent_dir (Path): Path to the agent's report folder.

Returns:
    Path | None: The latest report file, or None if none found.

### `read_latest_report(agent_dir, strict=False)`

Read and return the contents of the latest report for a given agent.

Args:
    agent_dir (Path): Path to the agent's report folder.
    strict (bool): If True, raise errors on missing or invalid reports.
                   If False, return None and log a warning.

Returns:
    dict | None: Parsed report contents, or None if no report exists or format is invalid (in non-strict mode).

### `validate_report_format(report)`

Validate that a report contains all expected top-level keys.

Args:
    report (dict): The parsed report to validate.

Returns:
    bool: True if valid, False otherwise.
