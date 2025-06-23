# Module `dev_utils`

## Functions

### `log_suggested_paths(response, max_depth=3, source_label='response')`

Log inferred paths to nested keys in a response dictionary.

Args:
    response (dict): Parsed API response.
    max_depth (int): Maximum depth to explore.
    source_label (str): Label for context in logs.

### `suggest_paths(response, max_depth=3, current_path=None)`

Suggest possible nested data paths in a response dictionary.

Args:
    response (dict): Parsed API response.
    max_depth (int): Maximum traversal depth.
    current_path (list[str] | None): Used internally for recursion.

Returns:
    list of (path, key, summary): Potential paths to explore.
