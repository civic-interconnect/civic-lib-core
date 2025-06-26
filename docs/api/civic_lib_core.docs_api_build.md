# Module `civic_lib_core.docs_api_build`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `generate_api_docs(source_dir_str: str = 'civic_lib_core', output_dir_str: str = 'api')`

Generate Markdown API documentation (backward compatibility).

### `generate_docs(source_pkg_str: str = 'civic_lib_core', output_dir_str: str = 'api', formats: str | list[str] | None = None)`

Generate API documentation in multiple formats.

### `publish_api_docs() -> None`

One-liner to generate complete API documentation for release.
