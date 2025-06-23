"""
install_deps.py

Install Civic Interconnect project dependencies into an existing `.venv`.

This script:
- Verifies `.venv` exists and is usable
- Installs required and dev dependencies via pyproject.toml
- Installs pre-commit hooks

Does NOT create or activate the virtual environment.
"""

import os
import subprocess
import sys
from pathlib import Path

__all__ = [
    "get_python_bin",
    "get_venv_dir",
    "install_dependencies",
    "run",
    "verify_venv",
]


VENV_DIR = Path(".venv")


def get_python_bin():
    """Return the path to the Python binary in the virtual environment."""
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def get_venv_dir():
    """Return the absolute path to the .venv directory."""
    return VENV_DIR.resolve()


def install_dependencies(python_bin: Path, is_editable: bool = False):
    """Install pip tools, project dependencies, and pre-commit hooks."""
    # Upgrade base tools
    run([
        str(python_bin),
        "-m",
        "pip",
        "install",
        "--upgrade",
        "pip",
        "setuptools",
        "wheel",
        "--prefer-binary",
    ])

    # Install with dev extras
    install_cmd = [
        str(python_bin),
        "-m",
        "pip",
        "install",
        "-e" if is_editable else ".",
        ".[dev]",
        "--timeout",
        "100",
        "--no-cache-dir",
        "--prefer-binary",
    ]
    run(install_cmd)

    # Install from requirements-dev.txt if present
    req_file = Path("requirements-dev.txt")
    if req_file.exists():
        run([
            str(python_bin),
            "-m",
            "pip",
            "install",
            "-r",
            str(req_file),
            "--timeout",
            "100",
            "--no-cache-dir",
        ])

    # Install pre-commit hooks if possible
    try:
        run([str(python_bin), "-m", "pre_commit", "install"])
    except subprocess.CalledProcessError:
        print("Skipped pre-commit installation — not installed?")


def run(cmd, shell=False):
    print(f"$ {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
    subprocess.run(cmd, shell=shell, check=True)


def verify_venv():
    """Ensure .venv exists and contains a Python binary."""
    if not VENV_DIR.exists():
        print("Error: .venv directory not found.")
        sys.exit(1)

    python_bin = get_python_bin()
    if not python_bin.exists():
        print(f"Error: Python not found in {python_bin}")
        sys.exit(1)

    return python_bin


def main(is_editable: bool = False):
    print("Verifying .venv...")
    python_bin = verify_venv()

    print("Installing dependencies...")
    install_dependencies(python_bin, is_editable)

    print("Environment setup complete.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"Setup failed: {e}")
        sys.exit(1)
