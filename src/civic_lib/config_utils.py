"""
civic_lib/config_utils.py

Service-specific configuration and environment helpers.
"""

import os
import re
import sys
from pathlib import Path

import yaml

from civic_lib import log_utils

__all__ = [
    "load_api_key",
    "load_openstates_api_key",
    "load_yaml_config",
    "load_version",
    "parse_version",
]

logger = log_utils.logger


def load_api_key(env_var: str, service_name: str) -> str:
    """
    Load an API key from the environment.

    Args:
        env_var (str): Environment variable name to load.
        service_name (str): Friendly service name for error messaging.

    Returns:
        str: API key value.

    Exits:
        If the API key is missing.
    """
    key = (os.getenv(env_var) or "").strip()
    if not key:
        logger.error(
            f"Missing {service_name} API key.\n"
            f"Fix: Add {env_var!r} to your .env file or system environment variables."
        )
        sys.exit(f"Error: {env_var} is required for {service_name}.")
    return key


def load_openstates_api_key() -> str:
    """
    Load the OpenStates API key from environment variables.

    Returns:
        str: The OpenStates API key.

    Exits:
        If the API key is not set in the environment.
    """
    return load_api_key("OPENSTATES_API_KEY", "OpenStates")


def load_yaml_config(filename: str = "config.yaml", root_dir: Path | None = None) -> dict:
    """
    Load a YAML configuration file from the given root directory.

    Args:
        filename (str): The config file name (default: "config.yaml").
        root_dir (Path | None): Root directory to search (default: Path.cwd()).

    Returns:
        dict: Parsed configuration as a dictionary.

    Raises:
        FileNotFoundError: If the config file cannot be found.
    """
    root = root_dir or Path.cwd()
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
    Load the version string from a VERSION file.

    Args:
        filename (str): The version filename (default: "VERSION").
        root_dir (Path | None): Optional base path.

    Returns:
        str: Version string.

    Exits:
        If the file is missing or unreadable.
    """
    root = root_dir or Path.cwd()
    version_path = root / filename

    try:
        version = version_path.read_text(encoding="utf-8").strip()
        logger.info(f"Loaded version: {version}")
        return version
    except Exception as e:
        logger.error(f"Error reading VERSION file at {version_path}: {str(e)}")
        sys.exit("Error: VERSION file is missing or unreadable.")


def parse_version(version: str) -> tuple[int, int, int]:
    """
    Parse a version string like '1.2.3' into a tuple.

    Raises:
        ValueError: if the version is not properly formatted.
    """
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")
    major, minor, patch = match.groups()
    return int(major), int(minor), int(patch)


if __name__ == "__main__":
    print("This module provides utilities and should not be run directly.")
