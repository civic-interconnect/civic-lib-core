# civic-interconnect-lib

> Shared internal utility library for Civic Interconnect Agents

[![Version](https://img.shields.io/badge/version-v0.9.0-blue)](https://github.com/civic-interconnect/civic-interconnect-lib/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/civic-interconnect/civic-interconnect-lib/actions/workflows/tests.yml/badge.svg)](https://github.com/civic-interconnect/civic-interconnect-lib/actions/workflows/tests.yml)

Provides common reusable functions used by multiple agents in the Civic Interconnect project.

## Key Design Rules

- This package is for widely shared functionality only.
- Each agent using this library remains independent.
- Code in the library must be:
  - Stateless
  - Simple
  - Easy to maintain
- The library contains cross-cutting helpers such as:
  - API key loading
  - Config loading
  - Query execution (GraphQL pagination)
  - Exception handling
  - Logging setup


## Installation When Building Civic Interconnect Agents

Add to the agent’s requirements.txt:

`civic-lib` or
`-e git+https://github.com/civic-interconnect/civic-interconnect-lib.git@main#egg=civic-lib`

## Local Development (of this library)

```powershell
py -m venv .venv
.\.venv\Scripts\activate
py -m pip install --upgrade pip setuptools wheel --prefer-binary
py -m pip install --upgrade -r requirements-dev.txt --timeout 100
pre-commit install
pytest tests
```

## Before Starting Changes

```shell
git pull
```

## After Tested Changes (New Version Release)

First: Update these files to the new version:

1. **VERSION file**
2. **pyproject.toml**
3. **setup.cfg**
4. **README.md** (update version badge)

Then run the following:

```shell
pip uninstall civic-lib -y
pip install -e .
pytest
pre-commit autoupdate --repo https://github.com/pre-commit/pre-commit-hooks
ruff check . --fix
git add .
git commit -m "Release: civic-lib v0.9.0"
git push origin main
git tag v0.9.0
git push origin v0.9.0
```


## Build and Publish to PyPi

The last command requires a PyPi API token to publish.

```powershell
py -m pip install --upgrade build twine
py -m build
py -m twine upload dist/*
```
