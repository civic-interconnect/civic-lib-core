# Module `schema_utils`

## Functions

### `detect_schema_change(old_file, new_data)`

Detect if the schema has changed by comparing the old file's hash with the new data.
Args:
    old_file (Path): The path to the old schema file.
    new_data (dict): The new schema data to compare against.
Returns:
    bool: True if the schema has changed (i.e., hashes differ), False otherwise.

### `hash_dict(data)`

Hash a JSON-serializable dictionary for change detection.
Args:
    data (dict): The dictionary to hash.
Returns:
    str: The SHA-256 hash of the JSON-encoded dictionary.

### `load_json(path)`

Load a JSON file and return its contents as a dictionary.
Args:
    path (str | Path): The path to the JSON file.
Returns:
    dict: The parsed JSON data.
Raises:
    FileNotFoundError: If the file does not exist.
    json.JSONDecodeError: If the file is not valid JSON.
