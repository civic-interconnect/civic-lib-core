# Module `civic_lib_core.docs_api_extract`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `dynamic_import_from_path(file_path: pathlib.Path, module_name: str)`

No description available.

### `extract_module_api(package_path: pathlib.Path) -> dict[str, dict]`

Recursively extract public functions and classes from Python source files.
Returns a dict with module names as keys.

### `extract_public_names(tree: ast.AST) -> set[str]`

Extract names from __all__ declaration.

### `find_public_classes(tree: ast.AST, public_names: set[str]) -> list[dict[str, str]]`

Find all public classes in the AST with their docstrings.

### `find_public_functions(tree: ast.AST, public_names: set[str]) -> list[dict[str, str]]`

Find all public functions in the AST with their docstrings.

### `get_public_members(module)`

No description available.

### `parse_python_file(file_path: pathlib.Path) -> ast.AST | None`

Parse a Python file and return its AST, or None if there's a syntax error.
