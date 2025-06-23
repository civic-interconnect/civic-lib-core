"""
cli.py

Developer command-line interface (CLI) for Civic Interconnect projects.

Provides cross-repo automation commands for:
- Installing and verifying the local development environment
- Formatting, linting, and testing the codebase
- Bumping version numbers for release
- Tagging and pushing release commits
- Generating or updating API documentation files

Run `civic-dev --help` for usage across all Civic Interconnect repos.
"""

import typer

from . import bump_version, install_deps, prep_code, publish_api, release

app = typer.Typer(help="Developer CLI for Civic Interconnect projects.")


@app.command("bump-version")
def bump_version_command(old_version: str, new_version: str):
    """
    Update version strings across the project.
    """
    bump_version.main(old_version, new_version)


@app.command("install-deps")
def install_deps_command(is_editable: bool = False):
    """
    Install project dependencies into the existing virtual environment.
    """
    install_deps.main(is_editable=is_editable)


@app.command("publish-api")
def publish_api_command():
    """
    Fetch or regenerate app api files.
    """
    publish_api.main()


@app.command("prep-code")
def prepare_code():
    """
    Format, lint, and test the codebase.
    """
    prep_code.main()


@app.command("release")
def release_command():
    """
    Tag and push the current version to GitHub.
    """
    release.main()


def main():
    app()


if __name__ == "__main__":
    main()
