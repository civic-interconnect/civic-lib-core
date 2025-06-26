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
import sys
from pathlib import Path

from civic_dev import install_deps
from civic_lib_core import log_utils, version_utils
from civic_lib_core.version_utils import get_lib_version

logger = log_utils.logger


def run_check(command: list[str], label: str) -> None:
    """Run a shell command and fail fast if it errors."""
    logger.info(f"{label} ...")
    result = subprocess.run(command)
    if result.returncode != 0:
        logger.error(
            f"{label} failed. \n\nPlease RE-RUN `civic-dev prep-code` to apply and verify all fixes.\n"
        )
        raise subprocess.CalledProcessError(result.returncode, command)


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


def main() -> int:
    try:
        logger.info("Checking virtual environment...")
        install_deps.main()

        logger.info("Checking version compatibility...")
        version_file = Path("VERSION")
        config_file = Path("config.yaml")

        if version_file.exists():
            try:
                agent_version = version_file.read_text(encoding="utf-8").strip()
                compatible = version_utils.check_version(agent_version, get_lib_version())
                if compatible:
                    logger.info(
                        f"Versions compatible: agent={agent_version}, lib={get_lib_version()}"
                    )
                else:
                    logger.warning(
                        f"Version mismatch: agent={agent_version}, lib={get_lib_version()}"
                    )
            except Exception as e:
                logger.warning(f"Error checking version: {e}")
        else:
            logger.warning("VERSION file not found — skipping version check.")

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
