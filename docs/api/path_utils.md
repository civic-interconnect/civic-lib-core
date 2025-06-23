# Module `path_utils`

## Functions

### `ensure_dir(path)`

Ensure a directory exists, creating it if necessary.

Args:
    path (str | Path): The directory path to ensure.

Returns:
    Path: The resolved Path object of the directory.

### `safe_filename(name)`

Convert a string into a safe, lowercase filename.

Replaces spaces and forward slashes with underscores.

Args:
    name (str): Original string.

Returns:
    str: Sanitized, lowercase filename string.
