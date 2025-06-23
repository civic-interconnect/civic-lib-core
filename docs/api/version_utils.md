# Module `version_utils`

## Functions

### `bump_version(old_version, new_version)`

No description available.

### `check_version(agent_version, lib_version, strict=False)`

Check compatibility of agent and lib versions using SemVer rules.

Args:
    agent_version (str): Version string for the agent.
    lib_version (str): Version string for the shared library.
    strict (bool): If True, requires exact version match.

Returns:
    bool: True if compatible, False otherwise.

### `find_init_files(root_dir)`

Recursively find all __init__.py files under the given directory.

### `get_lib_version()`

Get the current library version.

Returns:
    str: The semantic version string (e.g., "1.2.3").

### `get_version()`

Convenience alias for get_lib_version().

### `lib_version()`

Convenience alias for get_lib_version().

### `parse_version(version)`

Parse a version string into a tuple of integers.

Args:
    version (str): A semantic version string, e.g., "1.2.3".

Returns:
    tuple[int, int, int]: A tuple of (major, minor, patch) version numbers.

Raises:
    ValueError: If the version string is not in the expected format.

### `update_version_in_init(path, new_version)`

Update __version__ assignment in a given __init__.py file.
Only works for simple string assignment: __version__ = "..."

### `update_version_string(path, old, new)`

No description available.
