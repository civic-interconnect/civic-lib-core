# civic-lib-core

[![Version](https://img.shields.io/badge/version-v0.9.1-blue)](https://github.com/civic-interconnect/civic-lib-core/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/civic-interconnect/civic-lib-core/actions/workflows/tests.yml/badge.svg)](https://github.com/civic-interconnect/civic-lib-core/actions/workflows/tests.yml)

> Shared internal utility library for Civic Interconnect Agents


## Installation When Building Civic Interconnect Agents

Add to the agent’s requirements.txt:

`civic-lib-core` or
`-e git+https://github.com/civic-interconnect/civic-lib-core.git@main#egg=civic-lib-core`

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

1. VERSION file
2. pyproject.toml
3. setup.cfg
4. README.md (update version badge)

Then run the following:

```shell
pip uninstall civic-lib-core -y
pip install -e .
pytest
pre-commit autoupdate --repo https://github.com/pre-commit/pre-commit-hooks
ruff check . --fix
git add .
git commit -m "Release: v0.9.1"
git push origin main
git tag v0.9.1
git push origin v0.9.1
```


## Build and Publish to PyPi

The last command requires a PyPi API token to publish.

```powershell
py -m pip install --upgrade build twine
py -m build
py -m twine upload dist/*
```
