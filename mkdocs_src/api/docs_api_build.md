# Module `docs_api_build`

## Classes

### `Any(self, /, *args, **kwargs)`

Special type indicating an unconstrained type.

- Any is compatible with every type.
- Any assumed to have all methods.
- All values assumed to be instances of Any.

Note that all the above statements are true from the point of view of
static type checkers. At runtime, Any should not be used with instance
checks.

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `generate_api_docs(source_pkg_path: pathlib.Path, project_root: pathlib.Path, policy: dict[str, typing.Any]) -> None`

Generate Markdown API documentation for a single package.

Writes output into mkdocs_src/api. This function is a wrapper for
docs_api_config.generate_docs, ensuring 'markdown' format by default.

Args:
    source_pkg_path (Path): The absolute path to the Python package directory to document.
    project_root (Path): The root directory of the project.
    policy (Dict[str, Any]): The loaded project policy.

### `publish_api_docs() -> None`

One-liner to generate complete API documentation for release.

- Discovers all Python packages in src/.
- Generates Markdown & YAML docs for each into mkdocs_src/api.
- Writes mkdocs.yml to repo root.
- Writes index.md to mkdocs_src.
