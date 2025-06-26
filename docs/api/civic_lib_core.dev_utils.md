# Module `civic_lib_core.dev_utils`

## Functions

### `log_suggested_paths(response: dict, max_depth: int = 3, source_label: str = 'response') -> None`

Log inferred paths to nested keys in a response dictionary.

Args:
    response (dict): Parsed API response.
    max_depth (int): Maximum depth to explore.
    source_label (str): Label for context in logs.

### `suggest_paths(response: dict, max_depth: int = 3, current_path: list[str] | None = None) -> list[tuple[list[str], str, str]]`

Suggest possible nested data paths in a response dictionary.

Args:
    response (dict): Parsed API response.
    max_depth (int): Maximum traversal depth.
    current_path (list[str] | None): Used internally for recursion.

Returns:
    list of (path, key, summary): Potential paths to explore.
