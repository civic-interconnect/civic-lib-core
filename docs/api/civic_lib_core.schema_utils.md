# Module `civic_lib_core.schema_utils`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `detect_schema_change(old_file: pathlib.Path, new_data: dict) -> bool`

Detect if the schema has changed by comparing the old file's hash with the new data.
Args:
    old_file (Path): The path to the old schema file.
    new_data (dict): The new schema data to compare against.
Returns:
    bool: True if the schema has changed (i.e., hashes differ), False otherwise.

### `hash_dict(data: dict) -> str`

Hash a JSON-serializable dictionary for change detection.
Args:
    data (dict): The dictionary to hash.
Returns:
    str: The SHA-256 hash of the JSON-encoded dictionary.

### `load_json(path: str | pathlib.Path) -> dict`

Load a JSON file and return its contents as a dictionary.
Args:
    path (str | Path): The path to the JSON file.
Returns:
    dict: The parsed JSON data.
Raises:
    FileNotFoundError: If the file does not exist.
    json.JSONDecodeError: If the file is not valid JSON.
