"""
prep_code.py

Prepare Civic Interconnect code for release or commit.

This script:
- Verifies or reinstalls the virtual environment if core dependencies changed
- Formats code using Ruff
- Lints and fixes issues with Ruff
- Runs pre-commit hooks twice (first to fix, then to verify)
- Executes unit tests via pytest

Reinstalls .venv if pyproject.toml, requirements.txt, or poetry.lock are newer.
"""

import subprocess
from pathlib import Path

import typer

from civic_dev import install_deps
from civic_lib_core import version_utils
from civic_lib_core.version_utils import get_lib_version

app = typer.Typer(help="Format, lint, and test code with environment check.")


def should_reinstall() -> bool:
    """
    Determine whether the virtual environment should be reinstalled
    based on timestamps of dependency files.
    """
    venv_dir = install_deps.get_venv_dir()
    if not venv_dir.exists():
        return True

    venv_time = venv_dir.stat().st_mtime
    for fname in ["pyproject.toml", "requirements.txt", "poetry.lock"]:
        path = Path(fname)
        if path.exists() and path.stat().st_mtime > venv_time:
            return True
    return False


@app.command("prep-code")
def main():
    """
    Run full code preparation sequence.
    """
    typer.echo("Checking virtual environment...")
    install_deps.main()

    typer.echo("Checking version compatibility...")

    version_file = Path("VERSION")
    config_file = Path("config.yaml")

    if not version_file.exists():
        typer.secho("VERSION file not found — skipping version check.", fg=typer.colors.YELLOW)
    else:
        try:
            agent_version = version_file.read_text(encoding="utf-8").strip()
            compatible = version_utils.check_version(agent_version, get_lib_version())
            if not compatible:
                typer.secho(
                    f"Version mismatch: agent={agent_version}, lib={get_lib_version()}",
                    fg=typer.colors.BRIGHT_YELLOW,
                )
            else:
                typer.echo(f"✓ Versions compatible: agent={agent_version}, lib={get_lib_version()}")
        except Exception as e:
            typer.secho(f"Error checking version: {e}", fg=typer.colors.RED)

    if not config_file.exists():
        typer.secho(
            "config.yaml not found — logger may fall back to defaults.", fg=typer.colors.YELLOW
        )

    typer.echo("Formatting code with Ruff...")
    subprocess.run(["ruff", "format", "."], check=True)

    typer.echo("Linting and fixing issues with Ruff...")
    subprocess.run(["ruff", "check", ".", "--fix"], check=True)

    typer.echo("Running pre-commit hooks (1st pass, allow fixes)...")
    subprocess.run(["pre-commit", "run", "--all-files"], check=False)

    typer.echo("Running pre-commit hooks (2nd pass, verify clean)...")
    subprocess.run(["pre-commit", "run", "--all-files"], check=True)

    typer.echo("Running unit tests...")
    subprocess.run(["pytest", "tests"], check=True)

    typer.echo("Code formatted, linted, and tested successfully.")


if __name__ == "__main__":
    main()
