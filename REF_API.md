# Civic Interconnect API Documentation

# API for `civic_lib_core.api_utils`

<details>
<summary><code>async_paged_query(url: str, api_key: str, query, data_path: list[str], page_info_path: list[str] | None = None) -> list</code></summary>

Asynchronously fetch paginated GraphQL results.

Args:
    url (str): GraphQL endpoint.
    api_key (str): API key.
    query: gql.Query object.
    data_path (list): Path to the list of edges.
    page_info_path (list | None): Path to pageInfo block. If not provided, attempts to infer.

Returns:
    list: All collected items from all pages.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\api_utils.py#L25)

</details>

<details>
<summary><code>paged_query(url: str, api_key: str, query, data_path: list[str]) -> list</code></summary>

Run a paged GraphQL query synchronously.

Args:
    url (str): GraphQL endpoint.
    api_key (str): API key.
    query: gql.Query object.
    data_path (list): Path to the list of edges.

Returns:
    list: All collected items.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\api_utils.py#L83)

</details>

# API for `civic_lib_core.config_utils`

<details>
<summary><code>load_api_key(env_var: str, service_name: str) -> str</code></summary>

Load an API key from the environment.

Args:
    env_var (str): Environment variable name to load.
    service_name (str): Friendly service name for error messaging.

Returns:
    str: API key value.

Exits:
    If the API key is missing.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\config_utils.py#L27)

</details>

<details>
<summary><code>load_openstates_api_key() -> str</code></summary>

Load the OpenStates API key from environment variables.

Returns:
    str: The OpenStates API key.

Exits:
    If the API key is not set in the environment.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\config_utils.py#L51)

</details>

<details>
<summary><code>load_version(filename: str = 'VERSION', root_dir: pathlib.Path | None = None) -> str</code></summary>

Load the version string from a VERSION file.

Args:
    filename (str): The version filename (default: "VERSION").
    root_dir (Path | None): Optional base path.

Returns:
    str: Version string.

Exits:
    If the file is missing or unreadable.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\config_utils.py#L93)

</details>

<details>
<summary><code>load_yaml_config(filename: str = 'config.yaml', root_dir: pathlib.Path | None = None) -> dict</code></summary>

Load a YAML configuration file from the given root directory.

Args:
    filename (str): The config file name (default: "config.yaml").
    root_dir (Path | None): Root directory to search (default: Path.cwd()).

Returns:
    dict: Parsed configuration as a dictionary.

Raises:
    FileNotFoundError: If the config file cannot be found.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\config_utils.py#L64)

</details>

<details>
<summary><code>parse_version(version: str) -> tuple[int, int, int]</code></summary>

Parse a version string like '1.2.3' into a tuple.

Raises:
    ValueError: if the version is not properly formatted.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\config_utils.py#L119)

</details>

# API for `civic_lib_core.date_utils`

<details>
<summary><code>date_range(days_back: int) -> list[str]</code></summary>

Generate a list of date strings from `days_back` days ago up to today (UTC).

Args:
    days_back (int): Number of days to include, ending with today (inclusive).

Returns:
    list[str]: List of UTC dates in 'YYYY-MM-DD', earliest to latest.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\date_utils.py#L20)

</details>

<details>
<summary><code>now_utc() -> datetime.datetime</code></summary>

Return the current UTC datetime object.

Returns:
    datetime: Current UTC datetime.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\date_utils.py#L37)

</details>

<details>
<summary><code>now_utc_str(fmt: str = '%Y-%m-%d %H:%M:%S UTC') -> str</code></summary>

Return the current time in UTC as a formatted string.

Args:
    fmt (str): Format string for datetime output. Default includes 'UTC'.

Returns:
    str: Formatted current UTC time.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\date_utils.py#L47)

</details>

<details>
<summary><code>today_utc_str() -> str</code></summary>

Return today's date in UTC in 'YYYY-MM-DD' format.

Returns:
    str: Current UTC date as a string.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\date_utils.py#L60)

</details>

# API for `civic_lib_core.dev_utils`

<details>
<summary><code>log_suggested_paths(response: dict, max_depth: int = 3, source_label: str = 'response') -> None</code></summary>

Log inferred paths to nested keys in a response dictionary.

Args:
    response (dict): Parsed API response.
    max_depth (int): Maximum depth to explore.
    source_label (str): Label for context in logs.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\dev_utils.py#L21)

</details>

<details>
<summary><code>suggest_paths(response: dict, max_depth: int = 3, current_path: list[str] | None = None) -> list[tuple[list[str], str, str]]</code></summary>

Suggest possible nested data paths in a response dictionary.

Args:
    response (dict): Parsed API response.
    max_depth (int): Maximum traversal depth.
    current_path (list[str] | None): Used internally for recursion.

Returns:
    list of (path, key, summary): Potential paths to explore.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\dev_utils.py#L46)

</details>

# API for `civic_lib_core.error_utils`

<details>
<summary><code>handle_transport_errors(e: Exception, resource_name: str = 'resource') -> str</code></summary>

Handle GraphQL transport errors with consistent logging and friendly feedback.

Args:
    e (Exception): The exception raised by gql transport.
    resource_name (str): Human-readable name of the queried resource (for logs and user messages).

Returns:
    str: A message if the error is a known access denial (403). Re-raises otherwise.

Raises:
    Exception: The original error, unless a known handled case.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\error_utils.py#L23)

</details>

# API for `civic_lib_core.file_utils`

<details>
<summary><code>resolve_path(relative_path: str | pathlib.Path) -> pathlib.Path</code></summary>

Return an absolute Path from project root for a relative path.

Args:
    relative_path (str | Path): The relative or partial path to resolve.

Returns:
    Path: The absolute path resolved from the project root.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\file_utils.py#L15)

</details>

# API for `civic_lib_core.log_utils`

<details>
<summary><code>init_logger() -> None</code></summary>

Initialize loguru logging.

- Creates the logs/ directory if it doesn't exist.
- Sets up daily log rotation.
- Retains logs for 7 days.
- Logs agent start message.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\log_utils.py#L30)

</details>

<details>
<summary><code>lib_version() -> str</code></summary>

Return the version of the Civic Interconnect library.

Reads the VERSION file in the parent directory.

Returns:
    str: The version string.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\log_utils.py#L44)

</details>

<details>
<summary><code>log_agent_end(agent_name: str, status: str = 'success') -> None</code></summary>

Log the end of an agent with its name and status.

Args:
    agent_name (str): The name of the agent ending.
    status (str): The status of the agent at the end (default is "success").


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\log_utils.py#L65)

</details>

<details>
<summary><code>log_agent_start(agent_name: str) -> None</code></summary>

Log the start of an agent with its name.

Args:
    agent_name (str): The name of the agent starting.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\log_utils.py#L77)

</details>

# API for `civic_lib_core.path_utils`

<details>
<summary><code>ensure_dir(path: str | pathlib.Path) -> pathlib.Path</code></summary>

Ensure a directory exists, creating it if necessary.

Args:
    path (str | Path): The directory path to ensure.

Returns:
    Path: The resolved Path object of the directory.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\path_utils.py#L15)

</details>

<details>
<summary><code>safe_filename(name: str) -> str</code></summary>

Convert a string into a safe, lowercase filename.

Replaces spaces and forward slashes with underscores.

Args:
    name (str): Original string.

Returns:
    str: Sanitized, lowercase filename string.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\path_utils.py#L30)

</details>

# API for `civic_lib_core.query_utils`

<details>
<summary><code>fetch_paginated(client: Any, query: Any, data_key: str, variables: dict | None = None) -> list[dict]</code></summary>

Fetch all pages of a paginated GraphQL query.

Args:
    client (gql.Client): Initialized GraphQL client.
    query (gql.Query): The GraphQL query object.
    data_key (str): Key in response that contains the paginated data.
    variables (dict, optional): Initial query variables.

Returns:
    list[dict]: Combined list of all 'node' objects from paginated results.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\query_utils.py#L20)

</details>

# API for `civic_lib_core.report_archiver`

<details>
<summary><code>archive_old_reports(agent_dir: pathlib.Path, keep_latest: bool = True) -> list[pathlib.Path]</code></summary>

Rename old .json reports to .archived.json, optionally keeping the latest.

Args:
    agent_dir (Path): Directory with report files.
    keep_latest (bool): Whether to keep the most recent report unarchived.

Returns:
    list[Path]: List of archived report file paths.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\report_archiver.py#L21)

</details>

<details>
<summary><code>archive_reports_older_than(agent_dir: pathlib.Path, days_old: int) -> list[pathlib.Path]</code></summary>

Archive reports older than a specified number of days.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\report_archiver.py#L55)

</details>

# API for `civic_lib_core.report_constants`

# API for `civic_lib_core.report_formatter`

<details>
<summary><code>format_report_as_csv(report: dict) -> str</code></summary>

Convert report results to CSV format.

Args:
    report (dict): Parsed report dictionary.

Returns:
    str: CSV-formatted string of the report results.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\report_formatter.py#L25)

</details>

<details>
<summary><code>format_report_as_markdown(report: dict) -> str</code></summary>

Convert a report dictionary to a Markdown summary string.

Args:
    report (dict): Parsed report dictionary.

Returns:
    str: Markdown-formatted report summary.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\report_formatter.py#L46)

</details>

<details>
<summary><code>format_report_as_text(report: dict) -> str</code></summary>

Convert a report dictionary to a plain text summary string.

Args:
    report (dict): Parsed report dictionary.

Returns:
    str: Text-formatted report summary.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\report_formatter.py#L76)

</details>

<details>
<summary><code>to_csv(data: list[dict[str, typing.Any]], path: pathlib.Path) -> None</code></summary>

Write raw result data to a CSV file.

Args:
    data (list[dict]): Result rows to write.
    path (Path): File path to write CSV to.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\report_formatter.py#L102)

</details>

<details>
<summary><code>to_markdown(data: list[dict[str, typing.Any]], path: pathlib.Path) -> None</code></summary>

Write raw result data to a Markdown table.

Args:
    data (list[dict]): Result rows to write.
    path (Path): File path to write Markdown to.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\report_formatter.py#L120)

</details>

# API for `civic_lib_core.report_indexer`

<details>
<summary><code>generate_index(report_dir: pathlib.Path = WindowsPath('reports')) -> None</code></summary>

Generate a Markdown index listing the latest report from each agent.

Args:
    report_dir (Path): The base `reports/` directory to scan.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\report_indexer.py#L14)

</details>

# API for `civic_lib_core.report_reader`

<details>
<summary><code>check_schema_version(report: dict[str, typing.Any], required: str, strict: bool = False) -> bool</code></summary>

Check if the report's schema version matches the required version.
Args:
    report (dict): The parsed report dictionary.
    required (str): The required schema version to check against.
    strict (bool): If True, raise an error if the version does not match.
                   If False, return False and log a warning.
Returns:
    bool: True if the schema version matches, False otherwise.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\report_reader.py#L29)

</details>

<details>
<summary><code>get_latest_report(agent_dir: pathlib.Path) -> pathlib.Path | None</code></summary>

Get the most recent report file from the specified agent directory.

Args:
    agent_dir (Path): Path to the agent's report folder.

Returns:
    Path | None: The latest report file, or None if none found.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\report_reader.py#L44)

</details>

<details>
<summary><code>read_latest_report(agent_dir: pathlib.Path, strict: bool = False) -> dict | None</code></summary>

Read and return the contents of the latest report for a given agent.

Args:
    agent_dir (Path): Path to the agent's report folder.
    strict (bool): If True, raise errors on missing or invalid reports.
                   If False, return None and log a warning.

Returns:
    dict | None: Parsed report contents, or None if no report exists or format is invalid (in non-strict mode).


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\report_reader.py#L68)

</details>

<details>
<summary><code>validate_report_format(report: dict) -> bool</code></summary>

Validate that a report contains all expected top-level keys.

Args:
    report (dict): The parsed report to validate.

Returns:
    bool: True if valid, False otherwise.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\report_reader.py#L107)

</details>

# API for `civic_lib_core.report_summary`

<details>
<summary><code>write_markdown_summary(report: dict, path: pathlib.Path) -> None</code></summary>

Write a Markdown summary of a report's key metadata.

Args:
    report (dict): The report data (already parsed).
    path (Path): The output path to write the .md file.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\report_summary.py#L19)

</details>

# API for `civic_lib_core.report_utils`

<details>
<summary><code>get_agent_name_from_path(path: pathlib.Path) -> str</code></summary>

Extract and format the agent name from a report file path.

The agent name is derived from the parent folder of the report file,
with underscores replaced by spaces and title-cased.

If the path does not have a parent directory, returns 'Unknown Agent'.

Args:
    path (Path): The path to a report file.

Returns:
    str: Formatted agent name or fallback string.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\report_utils.py#L16)

</details>

<details>
<summary><code>is_report_file(path: pathlib.Path) -> bool</code></summary>

Determine whether the given file path is a valid report file.

A valid report file must:
- Have a ".json" extension
- Begin with a date prefix (e.g., "2024-01-01")

Args:
    path (Path): The path to check.

Returns:
    bool: True if the path matches report file format, False otherwise.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\report_utils.py#L38)

</details>

# API for `civic_lib_core.report_writer`

<details>
<summary><code>write_report(data: list[dict[str, typing.Any]], agent_name: str, agent_version: str, schema_version: str = '1.0.0', report_dir: str | pathlib.Path = WindowsPath('reports'), file_format: str = 'json') -> pathlib.Path</code></summary>

Write agent output to a timestamped report file with metadata.

Args:
    data (list[dict[str, Any]]): The results to include in the report.
    agent_name (str): The name of the agent generating the report.
    agent_version (str): The version of the agent code.
    report_dir (str | Path): Root directory where reports are saved (default: REPORTS_DIR).
    file_format (str): Output format, one of "json" or "csv" (default: "json").

Returns:
    Path: The full path to the saved report file.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\report_writer.py#L25)

</details>

# API for `civic_lib_core.schema_utils`

<details>
<summary><code>detect_schema_change(old_file: pathlib.Path, new_data: dict) -> bool</code></summary>

Detect if the schema has changed by comparing the old file's hash with the new data.
Args:
    old_file (Path): The path to the old schema file.
    new_data (dict): The new schema data to compare against.
Returns:
    bool: True if the schema has changed (i.e., hashes differ), False otherwise.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\schema_utils.py#L21)

</details>

<details>
<summary><code>hash_dict(data: dict) -> str</code></summary>

Hash a JSON-serializable dictionary for change detection.
Args:
    data (dict): The dictionary to hash.
Returns:
    str: The SHA-256 hash of the JSON-encoded dictionary.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\schema_utils.py#L36)

</details>

<details>
<summary><code>load_json(path: str | pathlib.Path) -> dict</code></summary>

Load a JSON file and return its contents as a dictionary.
Args:
    path (str | Path): The path to the JSON file.
Returns:
    dict: The parsed JSON data.
Raises:
    FileNotFoundError: If the file does not exist.
    json.JSONDecodeError: If the file is not valid JSON.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\schema_utils.py#L47)

</details>

# API for `civic_lib_core.version_utils`

<details>
<summary><code>check_version(agent_version: str, lib_version: str, strict: bool = False) -> bool</code></summary>

Check compatibility of agent and lib versions using SemVer rules.

Args:
    agent_version (str): Version string for the agent.
    lib_version (str): Version string for the shared library.
    strict (bool): If True, requires exact version match.

Returns:
    bool: True if compatible, False otherwise.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\version_utils.py#L19)

</details>

<details>
<summary><code>parse_version(version: str) -> tuple[int, int, int]</code></summary>

Parse a version string into a tuple of integers.

Args:
    version (str): A semantic version string, e.g., "1.2.3".

Returns:
    tuple[int, int, int]: A tuple of (major, minor, patch) version numbers.

Raises:
    ValueError: If the version string is not in the expected format.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\version_utils.py#L51)

</details>

# API for `civic_lib_core.yaml_utils`

<details>
<summary><code>read_yaml(path: str | pathlib.Path) -> dict[str, typing.Any]</code></summary>

Read and parse a YAML file into a dictionary.

Args:
    path (str | Path): YAML file path.

Returns:
    dict: Parsed YAML data.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\yaml_utils.py#L35)

</details>

<details>
<summary><code>write_yaml(data: dict[str, typing.Any], path: str | pathlib.Path) -> pathlib.Path</code></summary>

Write a dictionary to a YAML file.

Args:
    data (dict): Data to write.
    path (str | Path): File path to write to.

Returns:
    Path: The path the file was written to.


[View source](https://github.com/civic-interconnect/civic-lib-core/blob/main/civic-lib-core\src\civic_lib_core\yaml_utils.py#L17)

</details>
