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
Command should look something like:
    civic-dev bump-version 1.0.3 1.0.4
"""

import subprocess
from pathlib import Path

import typer

from civic_lib_core.doc_utils import publish_api_docs

app = typer.Typer(help="Run formatting, tests, and tagging to publish a release.")


def run(cmd: str, check: bool = True) -> None:
    """
    Run a shell command and echo it.
    """
    typer.echo(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if check and result.returncode != 0:
        typer.echo(f"Command failed: {cmd}")
        raise typer.Exit(result.returncode)


@app.command("release")
def main() -> None:
    """
    Complete the release workflow for the current version.
    """
    version_path = Path("VERSION")
    if not version_path.exists():
        typer.echo("VERSION file not found.")
        raise typer.Exit(1)

    version = version_path.read_text().strip().removeprefix("v")
    tag = f"v{version}"

    typer.echo(f"Releasing version {tag}...")

    try:
        # Update pre-commit hooks
        run("pre-commit autoupdate --repo https://github.com/pre-commit/pre-commit-hooks")

        # Install editable package
        if Path("pyproject.toml").exists():
            run("python -m pip install -e .")
        else:
            typer.echo("pyproject.toml not found — skipping install.")

        # Format and lint
        run("ruff format .")
        run("ruff check . --fix")

        # Generate fresh API documentation after formatting
        publish_api_docs()

        # Pre-commit: first pass may fix
        run("pre-commit run --all-files", check=False)

        # Stage changes
        run("git add .")

        # Pre-commit: second pass (verify)
        run("pre-commit run --all-files", check=False)

        # Stage again after fixes
        run("git add .")

        # Final check must pass
        run("pre-commit run --all-files")

        # Run tests if present
        if Path("tests").exists():
            run("pytest")
        else:
            typer.echo("No tests/ folder — skipping tests.")

        # Commit changes if any are staged
        run("git add .")
        result = subprocess.run("git diff --cached --quiet", shell=True)
        if result.returncode == 1:
            run(f'git commit -m "Release: {tag}"')
            run("git push origin main")
        else:
            typer.echo("No changes to commit.")

        # Ensure tag doesn't already exist
        result = subprocess.run(f"git tag --list {tag}", shell=True, capture_output=True, text=True)
        if tag in result.stdout:
            typer.echo(f"Error: Tag {tag} already exists. Please bump the version.")
            raise typer.Exit(1)

        # Tag and push release
        run(f"git tag {tag}")
        run(f"git push origin {tag}")

        typer.echo(f"Release {tag} completed successfully.")
    except typer.Exit:
        typer.echo("Warning: Release process halted due to errors.")
        raise


if __name__ == "__main__":
    main()
