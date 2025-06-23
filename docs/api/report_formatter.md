# Module `report_formatter`

## Functions

### `format_report_as_csv(report)`

Convert report results to CSV format.

Args:
    report (dict): Parsed report dictionary.

Returns:
    str: CSV-formatted string of the report results.

### `format_report_as_markdown(report)`

Convert a report dictionary to a Markdown summary string.

Args:
    report (dict): Parsed report dictionary.

Returns:
    str: Markdown-formatted report summary.

### `format_report_as_text(report)`

Convert a report dictionary to a plain text summary string.

Args:
    report (dict): Parsed report dictionary.

Returns:
    str: Text-formatted report summary.

### `to_csv(data, path)`

Write raw result data to a CSV file.

Args:
    data (list[dict]): Result rows to write.
    path (Path): File path to write CSV to.

### `to_markdown(data, path)`

Write raw result data to a Markdown table.

Args:
    data (list[dict]): Result rows to write.
    path (Path): File path to write Markdown to.
