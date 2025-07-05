# Module `project_policy`

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

### `load_project_policy(project_root: pathlib.Path | None = None) -> dict`

Load Civic Interconnect project policy, allowing client repos to
optionally override default settings via a custom policy file.

The default policy is loaded from the library's internal `project_policy.yaml`.
If `project_root` is provided and a `project_policy.yaml` exists within it,
this custom policy will be loaded and its values will be recursively
merged into the default policy, overriding any conflicting keys.

Args:
    project_root (Path | None): If provided, looks for `project_policy.yaml`
                                 in this root directory to apply custom overrides.

Returns:
    dict: The combined policy data, with custom settings merged over defaults.
