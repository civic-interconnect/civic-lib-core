"""
civic_lib_core/config_utils.py

Utilities for managing configuration and environment data in Civic Interconnect projects.

Provides:
- Loading environment-based API keys
- Reading YAML configuration files
- Reading project version information
- Parsing version strings into numeric tuples

Typical usage:

    from civic_lib_core import config_utils

    # Load an API key from the environment
    api_key = config_utils.load_api_key("MY_API_KEY", "MyService")

    # Load a YAML configuration
    config = config_utils.load_yaml_config()

    # Load version from VERSION file
    version = config_utils.load_version()

    # Parse version string into numbers
    major, minor, patch = config_utils.parse_version("1.2.3")
"""

import os
import re
import sys
from pathlib import Path

import yaml

from civic_lib_core import fs_utils, log_utils

__all__ = [
    "load_api_key",
    "load_yaml_config",
    "load_version",
    "parse_version",
]

logger = log_utils.logger


def load_api_key(env_var: str, service_name: str) -> str:
    """
    Load an API key from the environment variables.

    Args:
        env_var (str): The name of the environment variable to read.
        service_name (str): A friendly name for the service (for error messages).

    Returns:
        str: The API key value.

    Exits:
        If the environment variable is missing or empty.
    """
    key = (os.getenv(env_var) or "").strip()
    if not key:
        logger.error(
            f"Missing API key for {service_name}.\n"
            f"Fix: Add {env_var!r} to your .env file or system environment variables."
        )
        sys.exit(f"Error: Environment variable {env_var} is required for {service_name}.")
    return key


def load_yaml_config(filename: str = "config.yaml", root_dir: Path | None = None) -> dict:
    """
    Load a YAML configuration file from the project root.

    Args:
        filename (str): Name of the config file (default: "config.yaml").
        root_dir (Optional[Path]): Directory to search (default: detected project root).

    Returns:
        dict: Parsed configuration as a Python dictionary.

    Raises:
        FileNotFoundError: If the config file cannot be found.
    """
    root = root_dir or fs_utils.get_project_root()
    config_path = root / filename

    if not config_path.exists():
        msg = f"Config file not found: {config_path}"
        logger.error(msg)
        raise FileNotFoundError(msg)

    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    logger.debug(f"Loaded config from {config_path}")
    return config


def load_version(filename: str = "VERSION", root_dir: Path | None = None) -> str:
    """
    Load the version string from a VERSION file in the project.

    Args:
        filename (str): Name of the version file (default: "VERSION").
        root_dir (Optional[Path]): Base path to search (default: detected project root).

    Returns:
        str: Version string (e.g., "1.2.3").

    Exits:
        If the version file is missing or unreadable.
    """
    root = root_dir or fs_utils.get_project_root()
    version_path = root / filename

    try:
        version = version_path.read_text(encoding="utf-8").strip()
        logger.info(f"Loaded version: {version}")
        return version
    except Exception as e:
        logger.error(f"Error reading VERSION file at {version_path}: {str(e)}")
        sys.exit(f"Error: VERSION file missing or unreadable at {version_path}.")


def parse_version(version: str) -> tuple[int, int, int]:
    """
    Parse a version string (e.g., "1.2.3") into a tuple of integers.

    Args:
        version (str): Version string.

    Returns:
        tuple[int, int, int]: A tuple of (major, minor, patch).

    Raises:
        ValueError: If the version string is improperly formatted.
    """
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")
    major, minor, patch = match.groups()
    return int(major), int(minor), int(patch)


if __name__ == "__main__":
    print("This module provides configuration utilities and is not intended to be run directly.")
