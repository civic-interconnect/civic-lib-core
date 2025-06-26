# Module `civic_dev.release`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `main() -> int`

Complete the release workflow for the current version.

### `publish_api_docs() -> None`

One-liner to generate complete API documentation for release.

### `run(cmd: str, check: bool = True) -> None`

Run a shell command and log it.
