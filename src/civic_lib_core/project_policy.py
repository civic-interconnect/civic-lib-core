"""
civic_lib_core/project_policy.py

Load the project policy for any Civic Interconnect client repo.

MIT License — maintained by Civic Interconnect
"""

from pathlib import Path
from typing import Any

import yaml

__all__ = ["load_project_policy"]

DEFAULT_POLICY_PATH = Path(__file__).parent / "project_policy.yaml"


def _deep_merge_dicts(dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]:
    """
    Recursively merges dict2 into dict1.
    Values from dict2 overwrite values from dict1.
    """
    merged_dict = dict1.copy()
    for key, value in dict2.items():
        if key in merged_dict and isinstance(merged_dict[key], dict) and isinstance(value, dict):
            merged_dict[key] = _deep_merge_dicts(merged_dict[key], value)
        else:
            merged_dict[key] = value
    return merged_dict


def load_project_policy(project_root: Path | None = None) -> dict:
    """
    Load Civic Interconnect project policy, allowing client repos to
    optionally override default settings via a custom policy file.

    The default policy is loaded from the library's internal `project_policy.yaml`.
    If `project_root` is provided and a `project_policy.yaml` exists within it,
    this custom policy will be loaded and its values will be recursively
    merged into the default policy, overriding any conflicting keys.

    Args:
        project_root (Path | None): If provided, looks for `project_policy.yaml`
                                     in this root directory to apply custom overrides.

    Returns:
        dict: The combined policy data, with custom settings merged over defaults.
    """
    # 1. Load the default policy from the library
    try:
        with open(DEFAULT_POLICY_PATH, encoding="utf-8") as f:
            policy_data = yaml.safe_load(f) or {}  # Ensure it's a dict even if file is empty
    except FileNotFoundError:
        policy_data = {}  # Start with empty if default is missing (though it shouldn't be)
        # Consider logging a warning here if default is missing
        print(f"Warning: Default policy file not found at {DEFAULT_POLICY_PATH}")
    except yaml.YAMLError as e:
        policy_data = {}
        print(f"Error loading default policy from {DEFAULT_POLICY_PATH}: {e}")
        # Re-raise or handle as appropriate for your error policy
        raise

    # 2. Check for and load a custom policy from the project root
    if project_root:
        custom_policy_path = project_root / "project_policy.yaml"
        if custom_policy_path.exists():
            try:
                with open(custom_policy_path, encoding="utf-8") as f:
                    custom_data = yaml.safe_load(f) or {}
                # 3. Merge custom policy into the default policy
                policy_data = _deep_merge_dicts(policy_data, custom_data)
                # Add a special key to indicate which policy file was used
                policy_data["__policy_path__"] = str(custom_policy_path)
            except FileNotFoundError:
                # Should not happen given custom_policy_path.exists() check
                pass
            except yaml.YAMLError as e:
                print(f"Error loading custom policy from {custom_policy_path}: {e}")
                # Log a warning or error, but continue with default policy
                # Or re-raise if custom policy is critical and must be valid
                raise  # Re-raising might be appropriate if custom policy is malformed

    # If no custom policy was loaded or merged, and the default was used, set its path
    if "__policy_path__" not in policy_data:
        policy_data["__policy_path__"] = str(DEFAULT_POLICY_PATH)

    return policy_data
