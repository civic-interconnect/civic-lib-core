# Module `docs_api_extract`

## Classes

### `ModuleType(self, /, *args, **kwargs)`

Create a module object.

The name must be a string; the optional doc argument can have any type.

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `dynamic_import_from_path(file_path: pathlib.Path, module_name: str) -> module`

Dynamically import a Python module from a file path.

Args:
    file_path (Path): Path to the .py file.
    module_name (str): Name to assign to the imported module.

Returns:
    ModuleType: Imported Python module object.

Raises:
    ImportError: If module cannot be loaded.

### `extract_module_api(package_path: pathlib.Path) -> dict[str, dict]`

Recursively extract public functions and classes from Python source files.

Args:
    package_path (Path): Path to a Python package directory.

Returns:
    dict[str, dict]: Mapping of module names to their functions and classes.

### `extract_public_names(tree: ast.AST) -> set[str]`

Extract names listed in a module's __all__ variable.

Args:
    tree (ast.AST): Parsed AST tree.

Returns:
    set[str]: Public names listed in __all__, if any.

### `find_public_classes(tree: ast.AST, public_names: set[str]) -> list[dict[str, str]]`

Find all public classes in a Python module AST.

Args:
    tree (ast.AST): Parsed AST tree.
    public_names (set[str]): Names explicitly marked public in __all__.

Returns:
    list[dict[str, str]]: Class info dicts.

### `find_public_functions(tree: ast.AST, public_names: set[str]) -> list[dict[str, str]]`

Find all public functions in a Python module AST.

Args:
    tree (ast.AST): Parsed AST tree.
    public_names (set[str]): Names explicitly marked public in __all__.

Returns:
    list[dict[str, str]]: Function info dicts.

### `get_public_members(module) -> tuple[list[dict[str, str]], list[dict[str, str]]]`

Inspect a live imported Python module for public classes and functions.

Args:
    module (ModuleType): Imported Python module.

Returns:
    tuple: (functions, classes)
        Each is a list of dicts with name, signature, and docstring.

### `parse_python_file(file_path: pathlib.Path) -> ast.AST | None`

Parse a Python file into an AST.

Args:
    file_path (Path): Path to a Python file.

Returns:
    ast.AST | None: AST object if parsing succeeds, else None.
