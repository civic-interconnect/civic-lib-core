"""
civic_lib/version_utils.py

Tools for checking and reporting agent/library compatibility.
Part of the Civic Interconnect agent framework.

MIT License — maintained by Civic Interconnect
"""

import re

from civic_lib import log_utils

__all__ = ["check_version", "parse_version"]

logger = log_utils.logger


def check_version(agent_version: str, lib_version: str, strict: bool = False) -> bool:
    """
    Check compatibility of agent and lib versions using SemVer rules.

    Args:
        agent_version (str): Version string for the agent.
        lib_version (str): Version string for the shared library.
        strict (bool): If True, requires exact version match.

    Returns:
        bool: True if compatible, False otherwise.
    """
    try:
        agent_major, agent_minor, agent_patch = parse_version(agent_version)
        lib_major, lib_minor, lib_patch = parse_version(lib_version)
    except ValueError as e:
        logger.warning(str(e))
        return False

    if strict:
        if (agent_major, agent_minor, agent_patch) != (lib_major, lib_minor, lib_patch):
            logger.warning(f"Strict version mismatch: agent={agent_version}, lib={lib_version}")
            return False
        return True

    if agent_major != lib_major:
        logger.warning(f"Major version mismatch: agent={agent_version}, lib={lib_version}")
        return False

    return True


def parse_version(version: str) -> tuple[int, int, int]:
    """
    Parse a version string into a tuple of integers.

    Args:
        version (str): A semantic version string, e.g., "1.2.3".

    Returns:
        tuple[int, int, int]: A tuple of (major, minor, patch) version numbers.

    Raises:
        ValueError: If the version string is not in the expected format.
    """
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")
    major, minor, patch = match.groups()
    return int(major), int(minor), int(patch)
