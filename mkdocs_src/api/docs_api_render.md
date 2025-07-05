# Module `docs_api_render`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `write_markdown_docs(api_data: dict, output_dir: pathlib.Path) -> None`

Write full Markdown documentation for all extracted modules.

Args:
    api_data (dict): Dictionary from extract_module_api.
    output_dir (Path): Path to folder where Markdown files will be written.

### `write_module_markdown(file_path: pathlib.Path, module_name: str, functions: list[dict[str, str]], classes: list[dict[str, str]]) -> None`

Write Markdown documentation for a single Python module.

Args:
    file_path (Path): Output file path.
    module_name (str): Name of the module being documented.
    functions (list[dict]): Public functions extracted from the module.
    classes (list[dict]): Public classes extracted from the module.

### `write_yaml_summary(api_data: dict, output_dir: pathlib.Path) -> None`

Write a minimal YAML summary listing module names and their function names.

Args:
    api_data (dict): Dictionary from extract_module_api.
    output_dir (Path): Path to folder where API.yaml will be written.
