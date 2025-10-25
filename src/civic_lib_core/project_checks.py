"""civic_lib_core/project_checks.py.

Run structural and policy checks on a Civic Interconnect project.

"""

from pathlib import Path

from civic_lib_core import fs_utils, project_policy

__all__ = [
    "check_additional_files",
    "check_empty_dirs",
    "check_oversized_py_files",
    "check_py_files_outside_src",
    "check_python_project_dirs",
    "check_python_project_files",
    "check_required_files",
    "run_all_checks",
]


def check_additional_files(project_root: Path, policy: dict, key: str) -> list[str]:
    """Check additional file requirements from project policy.

    Args:
        project_root (Path): Project root.
        policy (dict): Project policy.
        key (str): Policy key like 'node_project_files' or 'pwa_project_files'.

    Returns:
        list[str]: Issues for missing files.
    """
    issues = []
    required = policy.get(key, [])
    for filename in required:
        if not (project_root / filename).exists():
            issues.append(f"Missing {key.replace('_', ' ')} file: {filename}")
    return issues


def check_empty_dirs(project_root: Path) -> list[str]:
    """Find empty directories in the project.

    Args:
        project_root (Path): Root of the project.

    Returns:
        list[str]: Issues for empty directories.
    """
    issues = []
    for path in project_root.rglob("*"):
        if path.is_dir() and not any(path.iterdir()):
            issues.append(f"Empty directory found: {path.relative_to(project_root)}")
    return issues


def check_oversized_py_files(project_root: Path, src_dir: Path, policy: dict) -> list[str]:
    """Check for Python files exceeding allowed line limits.

    Args:
        project_root (Path): Project root.
        src_dir (Path): Source directory.
        policy (dict): Project policy.

    Returns:
        list[str]: Issues for oversized files.
    """
    issues = []
    max_py_length = policy.get("max_python_file_length", 1000)

    for py_file in src_dir.rglob("*.py"):
        try:
            lines = py_file.read_text(encoding="utf-8", errors="ignore").splitlines()
            if len(lines) > max_py_length:
                issues.append(
                    f"Python file too long ({len(lines)} lines): {py_file.relative_to(project_root)}"
                )
        except Exception as e:
            issues.append(f"Could not read file {py_file}: {e}")

    return issues


def check_py_files_outside_src(project_root: Path, src_dir: Path) -> list[str]:
    """Check for .py files outside src_dir, ignoring top-level scripts.

    Args:
        project_root (Path): Project root.
        src_dir (Path): Source directory.

    Returns:
        list[str]: Issues for files outside src.
    """
    issues = []
    for py_file in project_root.rglob("*.py"):
        if src_dir in py_file.parents:
            continue
        # Ignore top-level scripts in the repo root
        if py_file.parent == project_root:
            continue
        issues.append(f"Python file outside src/ directory: {py_file.relative_to(project_root)}")
    return issues


def check_python_project_dirs(project_root: Path, policy: dict) -> list[str]:
    """Check required directories for Python projects.

    Args:
        project_root (Path): Project root.
        policy (dict): Project policy.

    Returns:
        list[str]: Issues for missing dirs.
    """
    issues = []
    for dirname in policy.get("python_project_dirs", []):
        if not (project_root / dirname).exists():
            issues.append(f"Missing Python project directory: {dirname}/")
    return issues


def check_python_project_files(project_root: Path, policy: dict) -> list[str]:
    """Check required files for Python projects.

    Args:
        project_root (Path): Project root.
        policy (dict): Project policy.

    Returns:
        list[str]: Issues for missing files.
    """
    issues = []
    for filename in policy.get("python_project_files", []):
        if not (project_root / filename).exists():
            issues.append(f"Missing Python project file: {filename}")
    return issues


def check_required_files(project_root: Path, policy: dict) -> list[str]:
    """Check files required in all Civic Interconnect repos.

    Args:
        project_root (Path): Project root.
        policy (dict): Project policy.

    Returns:
        list[str]: Issues for missing required files.
    """
    issues = []
    for filename in policy.get("required_files", []):
        if not (project_root / filename).exists():
            issues.append(f"Missing required file: {filename}")
    return issues


def run_all_checks() -> list[str]:
    """Run all project-level checks.

    Returns:
        list[str]: List of issues found.
    """
    issues = []

    project_root = fs_utils.get_project_root()
    policy = project_policy.load_project_policy(project_root)
    layout = fs_utils.discover_project_layout()
    src_dir = getattr(layout, "src_dir", None)

    issues.extend(check_required_files(project_root, policy))

    # Check Python-specific files
    if isinstance(src_dir, Path):
        issues.extend(check_python_project_files(project_root, policy))
        issues.extend(check_python_project_dirs(project_root, policy))
        issues.extend(check_oversized_py_files(project_root, src_dir, policy))
        issues.extend(check_py_files_outside_src(project_root, src_dir))
    else:
        issues.append("No source directory found. Skipping Python file checks.")

    # Check Node.js files if applicable
    issues.extend(check_additional_files(project_root, policy, key="node_project_files"))

    # Check PWA files if applicable
    issues.extend(check_additional_files(project_root, policy, key="pwa_project_files"))

    issues.extend(check_empty_dirs(project_root))

    return issues


def main() -> None:
    """Run all checks from CLI entry point.

    Prints results and exits with appropriate code.
    """
    import sys

    issues = run_all_checks()
    if issues:
        print("Project checks found the following issues:\n")
        for issue in issues:
            print(f"- {issue}")
        sys.exit(1)
    else:
        print("All project checks passed successfully.")
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error running project checks: {e}")
        import sys

        sys.exit(1)
