# DEVELOPER.md

## Setup

1. Fork the repo.
2. Clone your fork and open it in VS Code.
3. Open a terminal (examples below use PowerShell on Windows).

```powershell
git clone https://github.com/civic-interconnect/civic-lib-core.git
cd civic-lib-core

py -m venv .venv
.\.venv\Scripts\activate
py -m pip install --upgrade pip setuptools wheel --prefer-binary
py -m pip install -e ".[dev]"

civic-dev prep-code
civic-dev publish-api
mkdocs serve
```

Visit local API docs at: <http://localhost:8000>

## Before Starting Changes

```shell
git pull
```

## Releasing New Version

After verifying changes:

```powershell
civic-dev bump-version 0.9.1 0.9.2
civic-dev release
```

## Publishing to PyPI

Requires valid PyPI token:

```powershell
py -m build
py -m twine upload dist/*
```
