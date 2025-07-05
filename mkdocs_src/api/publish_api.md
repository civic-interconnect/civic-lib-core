# Module `publish_api`

## Functions

### `main() -> int`

Regenerate summary and reference API documentation for all packages in src/.
The generated Markdown and YAML files are placed into the MkDocs source directory
(typically `mkdocs_src/api/`).

Returns:
    int: exit code (0 if successful, nonzero otherwise)
