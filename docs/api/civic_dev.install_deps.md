# Module `civic_dev.install_deps`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `get_python_bin()`

Return the path to the Python binary in the virtual environment.

### `get_venv_dir()`

Return the absolute path to the .venv directory.

### `install_dependencies(python_bin: pathlib.Path, is_editable: bool = False)`

Install pip tools, project dependencies, and pre-commit hooks.

### `main(is_editable: bool = False) -> int`

No description available.

### `run(cmd, shell=False)`

No description available.

### `verify_venv()`

Ensure .venv exists and contains a Python binary.
