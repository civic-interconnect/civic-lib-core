"""CLI utility to check Civic Interconnect project policy compliance."""

import sys

from civic_lib_core import fs_utils, log_utils, policy_utils

logger = log_utils.logger


def main() -> int:
    """Check current repo against Civic Interconnect policy.

    Returns:
        int: exit code (0 = OK, nonzero = errors)
    """
    try:
        repo_root = fs_utils.get_project_root()

        # Default to python for now
        repo_type = "python"

        issues = policy_utils.check_policy(repo_root, repo_type)

        if issues:
            print("Policy check failed with issues:")
            for issue in issues:
                print(f"  - {issue}")
            return 1
        print("Policy check passed. All required files/directories exist.")
        return 0

    except Exception as e:
        logger.error(f"Failed to check project policy: {e}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
