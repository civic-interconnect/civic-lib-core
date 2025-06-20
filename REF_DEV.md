# Reference: Development Notes

We recommend VS Code and PowerShell for development.

## Local development

```powershell
py -m venv .venv
.\.venv\Scripts\activate
py -m pip install --upgrade pip setuptools wheel --prefer-binary
py -m pip install --upgrade -r requirements-dev.txt --timeout 100 --no-cache-dir
pre-commit install
```

## Before Starting Changes

```shell
git pull
```

## After Tested Changes (New Version Release)

```powershell

# activate .venv (if not already active)
.\.venv\Scripts\activate

# Run ruff to auto-fix style issues
ruff format --check .
ruff check . --fix

# Run precommit twice (first to fix, second to verify)
pre-commit run --all-files
pre-commit run --all-files

# Run any tests
pytest tests

# If New Release: bump from old to new
py _ci_bump_version.py 0.9.0 0.9.1

# If New Release: push commit and tag
.\_ci_release.ps1 -Version 0.9.1
```
