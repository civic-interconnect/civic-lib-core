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
py -m pip install -e .[dev]
civic-dev prep-code      # repeat if needed
civic-dev publish-api
mkdocs serve
```

Visit local API docs at: <http://localhost:8000>

## Releasing New Version

Run pre-release preparation and verification.
Delete .venv. Recreate and activate.

```powershell
git pull
py -m venv .venv
.\.venv\Scripts\activate
py -m pip install --upgrade pip setuptools wheel --prefer-binary
py -m pip install .[dev]
civic-dev prep-code        # repeat if needed
civic-dev publish-api
mkdocs serve
```

After verifying changes:

```powershell
civic-dev bump-version 0.9.3 0.9.4
civic-dev release
```

## Publishing Library to PyPI

Requires valid PyPI token:

```powershell
py -m build
py -m twine upload dist/*
```
