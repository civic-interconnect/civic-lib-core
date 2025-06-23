"""
cli.bump_version

Command-line tool to update version strings across key project files.

This tool replaces the old version with the new version in:
- VERSION
- pyproject.toml
- README.md

Usage:
    python -m cli.bump_version OLD_VERSION NEW_VERSION
    or as a subcommand: `civic-dev bump-version OLD_VERSION NEW_VERSION`
    or shorthand: `civic-dev bump OLD_VERSION NEW_VERSION`
"""

from pathlib import Path

import typer

app = typer.Typer(help="Update version strings across project files.")


def update_file(path: Path, old: str, new: str) -> bool:
    """Replace version string in the specified file if needed."""
    if not path.exists():
        typer.echo(f"Skipping: {path} (not found)")
        return False

    content = path.read_text(encoding="utf-8")
    updated = content.replace(old, new)

    if content != updated:
        path.write_text(updated, encoding="utf-8")
        typer.echo(f"Updated {path}")
        return True
    else:
        typer.echo(f"No changes needed in {path}")
        return False


def _bump_version(old_version: str, new_version: str) -> int:
    """Perform the version bump logic and return number of updated files."""
    files_to_update = [
        Path("VERSION"),
        Path("pyproject.toml"),
        Path("README.md"),
    ]

    updated_count = 0
    for path in files_to_update:
        if update_file(path, old_version, new_version):
            updated_count += 1

    return updated_count


@app.command("bump-version")
@app.command("bump")
def bump_version_cmd(old_version: str, new_version: str):
    """Update version strings across key project files."""
    updated = _bump_version(old_version, new_version)
    typer.echo(f"\n{updated} file(s) updated." if updated else "\nNo files were updated.")


def main(old_version: str, new_version: str):
    """Script-style entry point."""
    updated = _bump_version(old_version, new_version)
    print(f"\n{updated} file(s) updated." if updated else "\nNo files were updated.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python -m cli.bump_version OLD_VERSION NEW_VERSION")
