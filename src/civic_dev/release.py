"""
release.py

Automate the release process for Civic Interconnect applications.

This script:
- Reads the version from the VERSION file
- Updates pre-commit hooks
- Installs the package in editable mode
- Formats and lints the code
- Generates up-to-date API documentation
- Runs pre-commit hooks twice (fix + verify)
- Runs unit tests if present
- Commits changes if any are staged
- Creates a new Git tag for the release
- Pushes the commit and tag to the remote repository

Update the VERSION file before running this script.
Example:
    civic-dev bump-version 1.0.3 1.0.4
"""

import subprocess
import sys
from pathlib import Path

from civic_lib_core import log_utils
from civic_lib_core.doc_utils import publish_api_docs

logger = log_utils.logger


def run(cmd: str, check: bool = True) -> None:
    """
    Run a shell command and log it.
    """
    logger.info(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")


def main() -> int:
    """
    Complete the release workflow for the current version.
    """
    version_path = Path("VERSION")
    if not version_path.exists():
        logger.error("VERSION file not found.")
        return 1

    version = version_path.read_text().strip().removeprefix("v")
    tag = f"v{version}"
    logger.info(f"Releasing version {tag}")

    try:
        run("pre-commit autoupdate --repo https://github.com/pre-commit/pre-commit-hooks")

        if Path("pyproject.toml").exists():
            run("python -m pip install -e .")
        else:
            logger.warning("pyproject.toml not found — skipping install")

        run("ruff format .")
        run("ruff check . --fix")

        publish_api_docs()

        run("pre-commit run --all-files", check=False)
        run("git add .")
        run("pre-commit run --all-files", check=False)
        run("git add .")
        run("pre-commit run --all-files")

        if Path("tests").exists():
            run("pytest")
        else:
            logger.info("No tests directory — skipping tests")

        run("git add .")
        result = subprocess.run("git diff --cached --quiet", shell=True)
        if result.returncode == 1:
            run(f'git commit -m "Release: {tag}"')
            run("git push origin main")
        else:
            logger.info("No changes to commit")

        result = subprocess.run(f"git tag --list {tag}", shell=True, capture_output=True, text=True)
        if tag in result.stdout:
            logger.error(f"Tag {tag} already exists. Please bump the version.")
            return 1

        run(f"git tag {tag}")
        run(f"git push origin {tag}")

        logger.info(f"Release {tag} completed successfully")
        return 0

    except Exception as e:
        logger.error(f"Release process failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
