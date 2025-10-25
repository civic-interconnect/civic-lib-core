"""Automate the release process for Civic Interconnect applications.

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

File: release.py

Example:
    civic-dev bump-version 1.0.3 1.0.4
"""

from pathlib import Path
import shlex
import shutil
import subprocess
import sys

from civic_lib_core import log_utils

logger = log_utils.logger


def run(cmd: str, check: bool = True) -> None:
    """Run a shell command and log it."""
    # Define allowed commands for security
    allowed_commands = {"pre-commit", "uv", "pip", "ruff", "pytest", "git"}

    # Parse and validate the command
    cmd_parts = shlex.split(cmd)
    if not cmd_parts:
        raise RuntimeError("Empty command")

    base_command = cmd_parts[0]
    if base_command not in allowed_commands:
        raise RuntimeError(f"Command not allowed: {base_command}")

    # Additional validation for command arguments
    for arg in cmd_parts:
        if not all(c.isalnum() or c in ".-_/:=[]\"'" for c in arg):
            raise RuntimeError(f"Unsafe argument detected: {arg}")

    logger.info(f"$ {cmd}")
    result = subprocess.run(cmd_parts, shell=False, check=False)  # noqa: S603
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")


def _setup_and_format() -> None:
    """Set up environment and format code."""
    run("pre-commit autoupdate --repo https://github.com/pre-commit/pre-commit-hooks")

    if Path("pyproject.toml").exists():
        run('uv pip install --upgrade --no-cache-dir -e ".[dev]"')
    else:
        logger.warning("pyproject.toml not found — skipping install")

    run("ruff format .")
    run("ruff check . --fix")


def _run_precommit_and_tests() -> None:
    """Run pre-commit hooks and tests."""
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


def _validate_git_executable() -> str:
    """Validate and return git executable path."""
    git_path = shutil.which("git")
    if git_path is None:
        raise RuntimeError("git executable not found")
    if not git_path or not Path(git_path).name.startswith("git"):
        raise RuntimeError("Invalid git executable path")
    if not Path(git_path).is_file() or not git_path.endswith(("git", "git.exe")):
        raise RuntimeError("Invalid git executable")
    return git_path


def _validate_tag(tag: str) -> None:
    """Validate tag format for security."""
    if not tag.replace(".", "").replace("-", "").replace("_", "").replace("v", "").isalnum():
        raise RuntimeError(f"Invalid tag format: {tag}")
    if not all(c.isalnum() or c in ".-_v" for c in tag):
        raise RuntimeError(f"Tag contains unsafe characters: {tag}")
    if not tag or len(tag) > 100 or not tag.startswith("v"):
        raise RuntimeError(f"Invalid tag format: {tag}")


def _commit_and_tag(tag: str, git_path: str) -> None:
    """Commit changes and create tag."""
    result = subprocess.run([git_path, "diff", "--cached", "--quiet"], check=False)  # noqa: S603
    if result.returncode == 1:
        run(f'git commit -m "Release: {tag}"')

    result = subprocess.run([git_path, "tag", "--list", tag], capture_output=True, text=True)  # noqa: S603
    if tag in result.stdout:
        raise RuntimeError(f"Tag {tag} already exists. Please bump the version.")

    run(f"git tag {tag}")
    run(f"git push origin {tag}")


def main() -> int:
    """Complete the release workflow for the current version."""
    version_path = Path("VERSION")
    if not version_path.exists():
        logger.error("VERSION file not found.")
        return 1

    version = version_path.read_text().strip().removeprefix("v")
    tag = f"v{version}"
    logger.info(f"Releasing version {tag}")

    try:
        _validate_tag(tag)
        git_path = _validate_git_executable()

        _setup_and_format()
        _run_precommit_and_tests()
        _commit_and_tag(tag, git_path)

        logger.info(f"Release {tag} completed successfully")
        return 0

    except Exception as e:
        logger.error(f"Release process failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
