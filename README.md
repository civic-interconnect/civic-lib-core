# civic-interconnect-lib

> Shared internal utility library for Civic Interconnect Agents

[![Version](https://img.shields.io/badge/version-v0.1.0-blue)](https://github.com/civic-interconnect/civic-interconnect-lib/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/civic-interconnect/civic-interconnect-lib/actions/workflows/agent-runner.yml/badge.svg)](https://github.com/civic-interconnect/civic-interconnect-lib/actions)

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

`civic-lib`

## Local Development (of this library)

```powershell
py -m venv .venv
.\.venv\Scripts\activate
py -m pip install --upgrade pip setuptools wheel --prefer-binary
py -m pip install --upgrade -r requirements.txt --timeout 100
py -m pip install --upgrade -r requirements-dev.txt --timeout 100
pytest tests
```

## Before Starting Changes

```shell
git pull
```

## After Tested Changes (New Version Release)

First: **Modify VERSION file.** 

```shell
git add .
git commit -m "Release: civic-lib v0.1.0"
git push origin main
git tag v0.1.0
git push origin v0.1.0
```


## Build and Publish to PyPi

```powershell
py -m pip install --upgrade build twine
py -m build
py -m twine upload dist/*
```
