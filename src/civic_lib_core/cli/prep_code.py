"""Prepare Civic Interconnect code for release or commit.

This script:
- Checks whether the virtual environment may be stale (based on dependency file timestamps)
- Formats code using Ruff
- Lints and fixes issues with Ruff
- Runs pre-commit hooks twice (first to fix, then to verify)
- Executes unit tests via pytest

If dependency files changed since .venv was created, the script warns the user
to rerun their setup script (e.g. setup.ps1) to reinstall the environment.

File: prep_code.py

"""

from pathlib import Path
import subprocess
import sys

from civic_lib_core import log_utils
from civic_lib_core.version_utils import get_repo_version

logger = log_utils.logger


def run_check(command: list[str], label: str) -> None:
    """Run a shell command and fail fast if it errors."""
    # Validate that the command is from our allowed list of tools
    allowed_commands = {"ruff", "pre-commit", "pytest"}
    if not command or command[0] not in allowed_commands:
        raise ValueError(f"Untrusted command attempted: {command}")

    logger.info(f"{label} ...")
    result = subprocess.run(command, shell=False, check=False)  # noqa: S603
    if result.returncode != 0:
        logger.error(
            f"{label} failed.\n\nPlease RE-RUN your setup script to apply and verify all fixes.\n"
        )
        raise subprocess.CalledProcessError(result.returncode, command)


def should_reinstall() -> bool:
    """Determine whether the virtual environment should be reinstalled.

    Based on timestamps of dependency files.
    """
    venv_dir = Path(".venv")
    if not venv_dir.exists():
        logger.info(".venv does not exist. A fresh install will be required.")
        return True

    venv_time = venv_dir.stat().st_mtime
    for fname in ["pyproject.toml", "requirements.txt", "poetry.lock"]:
        path = Path(fname)
        if path.exists() and path.stat().st_mtime > venv_time:
            logger.info(f"Dependency file changed: {fname}")
            return True
    return False


def main() -> int:
    """Prepare code using a comprehensive workflow.

    This function performs a comprehensive code preparation workflow including:
    - Virtual environment validation and dependency checking
    - Code formatting using Ruff
    - Linting and automatic fixing of issues
    - Pre-commit hook execution and validation
    - Unit test execution

    The function checks if the virtual environment needs to be reinstalled by
    comparing dependency file timestamps, then runs a series of code quality
    tools in sequence. If any step fails, the process is terminated early.

    Returns:
        int: Exit code (0 for success, non-zero for failure). Returns 1 if
             virtual environment needs reinstalling, or the return code of
             any failed subprocess.

    Raises:
        subprocess.CalledProcessError: When any of the code preparation steps
                                     fail during execution.
    """
    try:
        logger.info("Checking virtual environment...")

        if should_reinstall():
            logger.warning(
                "Dependency files changed since the virtual environment was created.\n\n"
                "Please rerun your setup script (e.g. setup.ps1) to rebuild your environment.\n"
            )
            return 1
        logger.info(
            ".venv is up-to-date. Skipping environment reinstall. "
            "Rerun your setup script manually if needed."
        )

        # Log the library version for reference
        lib_version = get_repo_version()
        logger.info(f"Current library version: {lib_version}")

        config_file = Path("config.yaml")
        if not config_file.exists():
            logger.warning("config.yaml not found — logger may fall back to defaults.")

        run_check(["ruff", "format", "."], "Formatting code with Ruff")
        run_check(["ruff", "check", ".", "--fix"], "Linting and fixing issues with Ruff")
        run_check(["pre-commit", "run", "--all-files"], "Running pre-commit hooks (allowing fixes)")
        run_check(["pre-commit", "run", "--all-files"], "Verifying pre-commit hooks (must pass)")
        run_check(["pytest", "tests"], "Running unit tests")

        logger.info("Code formatted, linted, and tested successfully.")
        return 0

    except subprocess.CalledProcessError as e:
        logger.error(f"Process failed: {e}")
        return e.returncode


if __name__ == "__main__":
    sys.exit(main())
