# Module `civic_lib_core.docs_api_render`

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

Write full Markdown docs for each module.

### `write_module_markdown(file_path: pathlib.Path, module_name: str, functions: list[dict[str, str]], classes: list[dict[str, str]])`

Write markdown documentation for a single module.

### `write_yaml_summary(api_data: dict, output_dir: pathlib.Path) -> None`

Write minimal YAML summary with module → [function names].
