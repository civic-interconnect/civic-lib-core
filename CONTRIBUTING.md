# Contributing to Civic Interconnect

Thank you for your interest in contributing.  
This document provides a lightweight, consistent workflow used across all Civic Interconnect repositories.

## 1. Prerequisites

Install the following tools:

- Git  
- VS Code (recommended)  
- Python 3.12+  
- **uv** (package and environment manager)  
- pre-commit (installed via uv)

## 2. Fork and Clone

1. Fork the repository on GitHub.  
2. Clone your fork and open it in VS Code.

```
git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
cd REPO_NAME
```

## 3. One-Time Setup

Create a local environment and install dependencies.

```shell
uv python pin 3.12
uv venv
.venv/Scripts/activate        # Windows
# source .venv/bin/activate   # Mac or Linux

uv sync --extra dev --extra docs --upgrade
uv run pre-commit install
```

## 4. Validate Your Changes

Run standard local checks.

```
git pull origin main
uvx ruff check . --fix
uvx ruff format .
uvx deptry .
uv run pyright
uv run pytest
uvx pre-commit autoupdate
uvx pre-commit run --all-files
```

## 5. Provenance Tag (ptag.json)

Most repositories include a `provenance/ptag.json` file that records:

- who created the repo  
- data sources used  
- scripts or adapters used  
- schema versions

This file is validated automatically by the GitHub Actions
workflow against the canonical PTag core schema.
If the file is invalid, the action will fail with details.

For more on how provenance and schemas fit together across the organization, see: `docs/provenance-and-schemas-overview.md`.

## 6. Building Package and/or Docs

```
uv build
uv run mkdocs build --strict
uv run mkdocs serve
```

## 7. Commit and Push

```
git add .
git commit -m "Your message"
git push -u origin main
```

## 8. Open a Pull Request

Open a PR from your fork to the `main` branch of the target repository.

Guidelines for good PRs are here:  
`REF_PULL_REQUESTS.md`

---

If you have questions, open an issue in the target repository.  
Thank you for contributing.
