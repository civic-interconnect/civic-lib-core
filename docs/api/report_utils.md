# Module `report_utils`

## Functions

### `get_agent_name_from_path(path)`

Extract and format the agent name from a report file path.

The agent name is derived from the parent folder of the report file,
with underscores replaced by spaces and title-cased.

If the path does not have a parent directory, returns 'Unknown Agent'.

Args:
    path (Path): The path to a report file.

Returns:
    str: Formatted agent name or fallback string.

### `is_report_file(path)`

Determine whether the given file path is a valid report file.

A valid report file must:
- Have a ".json" extension
- Begin with a date prefix (e.g., "2024-01-01")

Args:
    path (Path): The path to check.

Returns:
    bool: True if the path matches report file format, False otherwise.
