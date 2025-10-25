"""Developer command-line interface (CLI) for Civic Interconnect projects.

Provides cross-repo automation commands for:
- Installing and verifying the local development environment
- Formatting, linting, and testing the codebase
- Bumping version numbers for release
- Tagging and pushing release commits

Run `civic-dev --help` for usage across all Civic Interconnect repos.

File: cli.py
"""

import typer  # type: ignore

from . import build_api, bump_version, check_policy, layout, prep_code, release

app = typer.Typer(help="Developer CLI for Civic Interconnect projects.")  # type: ignore


@app.command("build-api")  # type: ignore
def build_api_command():
    """Build the docs."""
    build_api.main()


@app.command("bump-version")  # type: ignore
def bump_version_command(old_version: str, new_version: str):
    """Update version strings across the project."""
    return bump_version.main(old_version, new_version)


@app.command("check-policy")  # type: ignore
def check_policy_command():
    """Check policies."""
    check_policy.main()


@app.command("layout")  # type: ignore
def layout_command():
    """Show the current project layout."""
    layout.main()


@app.command("prep-code")  # type: ignore
def prepare_code():
    """Format, lint, and test the codebase."""
    prep_code.main()


@app.command("release")  # type: ignore
def release_command():
    """Tag and push the current version to GitHub."""
    release.main()


def main():
    """Entry point for the CLI application.

    This function serves as the main entry point that initializes and runs the
    CLI application using the app() function.
    """
    app()


if __name__ == "__main__":
    main()
