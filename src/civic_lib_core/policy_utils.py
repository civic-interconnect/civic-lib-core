"""Policy enforcement utilities for Civic Interconnect projects."""

from pathlib import Path

from civic_lib_core import project_checks, project_policy


def check_policy(repo_root: Path, repo_type: str) -> list[str]:
    """Check the project at repo_root against policy for the given repo_type.

    Returns:
        List of issues (empty list = all good)
    """
    policy = project_policy.load_project_policy(repo_root)

    issues = []

    # Check required files for all repos
    issues.extend(project_checks.check_required_files(repo_root, policy))

    if repo_type == "python":
        issues.extend(project_checks.check_python_project_files(repo_root, policy))
        issues.extend(project_checks.check_python_project_dirs(repo_root, policy))
        layout = _safe_discover_layout(repo_root)
        if layout and layout.src_dir:
            issues.extend(
                project_checks.check_oversized_py_files(repo_root, layout.src_dir, policy)
            )
            issues.extend(project_checks.check_py_files_outside_src(repo_root, layout.src_dir))
        else:
            issues.append("No src/ directory found; skipping Python file checks.")

    if repo_type == "node":
        issues.extend(
            project_checks.check_additional_files(repo_root, policy, "node_project_files")
        )

    if repo_type == "pwa":
        issues.extend(project_checks.check_additional_files(repo_root, policy, "pwa_project_files"))

    # Check for empty directories
    issues.extend(project_checks.check_empty_dirs(repo_root))

    return issues


def _safe_discover_layout(repo_root: Path):
    """Discover layout safely without crashing if not a Python project."""
    try:
        from civic_lib_core import project_layout

        return project_layout.discover_project_layout()
    except Exception:
        return None
