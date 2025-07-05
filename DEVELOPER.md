# DEVELOPER.md

## Setup for Libraries

1. Fork the repo.
2. Clone your fork and open it in VS Code.
3. Open a terminal (examples below use PowerShell on Windows).

```powershell
git clone https://github.com/civic-interconnect/civic-lib-core.git
cd civic-lib-core
py -m venv .venv
.\.venv\Scripts\activate
py -m pip install --upgrade pip setuptools wheel --prefer-binary
py -m pip install --upgrade -e .[dev]
pytest tests
civic-dev layout
civic-dev prep-code
civic-dev publish-api
mkdocs serve
```

Visit local API docs at: <http://localhost:8000>

## Releasing New Version

Before publishing a new version, delete .venv. and recreate and activate.
Run pre-release preparation, installing and upgrading without the -e editable flag.
Verify all tests pass. Run prep-code (twice if needed).
Verify the docs are generated and appear correctly.

```powershell
git pull
py -m venv .venv
.\.venv\Scripts\activate
py -m pip install --upgrade pip setuptools wheel --prefer-binary
py -m pip install --upgrade .[dev]
pytest tests

civic-dev layout
civic-dev install-deps
civic-dev prep-code
civic-dev publish-api
mkdocs build
mkdocs serve
```

After verifying changes:

```powershell
civic-dev bump-version 0.9.5 0.9.6
civic-dev release
```

## Publishing Library to PyPI

Requires a valid PyPI token set in your environment or `~/.pypirc`.

```powershell
py -m build
py -m twine upload dist/*
```

## Publishing an API for a repo

| Module                    | Purpose                                              |
| ------------------------- | ---------------------------------------------------- |
| **docs\_api\_build.py**   | top-level commands for generating/publishing docs    |
| **docs\_api\_config.py**  | orchestrates config files and navigation bar         |
| **docs\_api\_extract.py** | parses Python code to extract docstrings, signatures |
| **docs\_api\_render.py**  | generates Markdown and YAML files                    |


## Folders

- Markdown lives in: mkdocs_src/
- API Markdown lives in: mkdocs_src/api/
- Built HTML goes into: docs/

## Publish API

Client repos can publish their api with with:

```powershell
civic-dev publish-api
```
