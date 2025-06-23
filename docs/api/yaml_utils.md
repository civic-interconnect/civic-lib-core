# Module `yaml_utils`

## Functions

### `read_yaml(path)`

Read and parse a YAML file into a dictionary.

Args:
    path (str | Path): YAML file path.

Returns:
    dict: Parsed YAML data.

### `write_yaml(data, path)`

Write a dictionary to a YAML file.

Args:
    data (dict): Data to write.
    path (str | Path): File path to write to.

Returns:
    Path: The path the file was written to.
