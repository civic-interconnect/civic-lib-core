"""civic_lib_core/project_policy.py.

Load the project policy for any Civic Interconnect client repo.

"""

import logging
from pathlib import Path
from typing import Any

import yaml

__all__ = ["load_project_policy"]

logger = logging.getLogger(__name__)

DEFAULT_POLICY_PATH = Path(__file__).parent / "project_policy.yaml"


def _deep_merge_dicts(dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge dict2 into dict1.

    Values from dict2 overwrite values from dict1.

    Args:
        dict1: The base dictionary.
        dict2: The dictionary to merge into dict1.

    Returns:
        dict: A merged dictionary.
    """
    merged_dict = dict1.copy()
    for key, value in dict2.items():
        if key in merged_dict and isinstance(merged_dict[key], dict) and isinstance(value, dict):
            merged_dict[key] = _deep_merge_dicts(merged_dict[key], value)
        else:
            merged_dict[key] = value
    return merged_dict


def load_project_policy(
    project_root: Path | None = None,
    override_file: Path | None = None,
) -> dict[str, Any]:
    """Load Civic Interconnect project policy.

    Behavior:
    - Load defaults from civic_lib_core's bundled `project_policy.yaml`.
    - If a client repo defines its own `project_policy.yaml`, merge its
      overrides into the default policy.

    Args:
        project_root: Optional project root to look for client `project_policy.yaml`.
        override_file: Optional path to explicitly provide a custom policy file.

    Returns:
        dict: Combined policy dictionary.
    """
    # Load default policy
    try:
        with DEFAULT_POLICY_PATH.open(encoding="utf-8") as f:
            policy_data = yaml.safe_load(f) or {}
    except FileNotFoundError:
        logger.warning(f"Default policy file not found at {DEFAULT_POLICY_PATH}")
        policy_data = {}
    except yaml.YAMLError as e:
        logger.error(f"Failed to parse default policy file at {DEFAULT_POLICY_PATH}: {e}")
        raise

    # Load client-specific override if provided
    custom_policy_path = None

    if override_file:
        custom_policy_path = Path(override_file)
    elif project_root:
        custom_policy_path = Path(project_root) / "project_policy.yaml"

    if custom_policy_path and custom_policy_path.exists():
        try:
            with custom_policy_path.open(encoding="utf-8") as f:
                custom_data = yaml.safe_load(f) or {}

            policy_data = _deep_merge_dicts(policy_data, custom_data)
            policy_data["__policy_path__"] = str(custom_policy_path)

            logger.debug(f"Loaded custom policy from {custom_policy_path}")

        except yaml.YAMLError as e:
            logger.error(f"Failed to parse custom policy at {custom_policy_path}: {e}")
            raise

    # Indicate the policy file used
    if "__policy_path__" not in policy_data:
        policy_data["__policy_path__"] = str(DEFAULT_POLICY_PATH)

    return policy_data
