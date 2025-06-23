# Module `file_utils`

## Functions

### `ensure_docs_output_dir(output_dir_str='api')`

Ensure output directory exists under project root/docs.

### `ensure_source_path(source_pkg_str='civic_lib_core')`

Resolve and validate the source package path.

### `find_project_root()`

Find the actual project root, whether civic_lib_core is installed or local.

Returns:
    Path: The project root directory

### `resolve_path(relative_path)`

Return an absolute Path from project root for a relative path.

Args:
    relative_path (str | Path): The relative or partial path to resolve.

Returns:
    Path: The absolute path resolved from the project root.
