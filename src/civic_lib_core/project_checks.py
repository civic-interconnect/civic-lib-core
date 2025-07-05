"""
civic_lib_core/project_checks.py

Run structural and policy checks on a Civic Interconnect project.

MIT License — maintained by Civic Interconnect
"""

from pathlib import Path

from civic_lib_core import fs_utils, project_policy

__all__ = [
    "check_empty_dirs",
    "check_mkdocs_consistency",
    "check_oversized_py_files",
    "check_py_files_outside_src",
    "check_python_project_dirs",
    "check_python_project_files",
    "check_required_files",
    "run_all_checks",
]


def check_empty_dirs(project_root: Path) -> list[str]:
    issues = []
    for path in project_root.rglob("*"):
        if path.is_dir() and not any(path.iterdir()):
            issues.append(f"Empty directory found: {path.relative_to(project_root)}")
    return issues


def check_mkdocs_consistency(project_root: Path, policy: dict) -> list[str]:
    issues = []

    mkdocs_file_path = policy.get("mkdocs_file")
    mkdocs_src_dir_name = policy.get("mkdocs_src_dir")

    if mkdocs_file_path and mkdocs_src_dir_name:
        mkdocs_file = project_root / mkdocs_file_path
        mkdocs_src = project_root / mkdocs_src_dir_name

        if mkdocs_src.exists() and not mkdocs_file.exists():
            issues.append(f"{mkdocs_src_dir_name}/ exists but {mkdocs_file_path} is missing.")

        if mkdocs_file.exists() and not mkdocs_src.exists():
            issues.append(
                f"{mkdocs_file_path} exists but {mkdocs_src_dir_name}/ folder is missing."
            )

    return issues


def check_oversized_py_files(project_root: Path, src_dir: Path, policy: dict) -> list[str]:
    issues = []
    max_py_length = policy.get("max_python_file_length", 1000)

    for py_file in src_dir.rglob("*.py"):
        try:
            lines = py_file.read_text(encoding="utf-8").splitlines()
            if len(lines) > max_py_length:
                issues.append(
                    f"Python file too long ({len(lines)} lines): {py_file.relative_to(project_root)}"
                )
        except Exception as e:
            issues.append(f"Could not read file {py_file}: {e}")

    return issues


def check_py_files_outside_src(project_root: Path, src_dir: Path) -> list[str]:
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
    issues = []
    for dirname in policy.get("python_project_dirs", []):
        if not (project_root / dirname).exists():
            issues.append(f"Missing Python project directory: {dirname}/")
    return issues


def check_python_project_files(project_root: Path, policy: dict) -> list[str]:
    issues = []
    for filename in policy.get("python_project_files", []):
        if not (project_root / filename).exists():
            issues.append(f"Missing Python project file: {filename}")
    return issues


def check_required_files(project_root: Path, policy: dict) -> list[str]:
    issues = []
    for filename in policy.get("required_files", []):
        if not (project_root / filename).exists():
            issues.append(f"Missing required file: {filename}")
    return issues


def run_all_checks() -> list[str] | None:
    """
    Run all project-level checks and return a list of issues.

    Returns:
        list[str]: Descriptions of issues found.
    """
    issues = []

    project_root = fs_utils.get_project_root()
    policy = project_policy.load_project_policy(project_root)
    layout = fs_utils.discover_project_layout()
    src_dir = getattr(layout, "src_dir", None)

    issues.extend(check_required_files(project_root, policy))

    if isinstance(src_dir, Path):
        issues.extend(check_python_project_files(project_root, policy))
        issues.extend(check_python_project_dirs(project_root, policy))
        issues.extend(check_oversized_py_files(project_root, src_dir, policy))
        issues.extend(check_py_files_outside_src(project_root, src_dir))
    else:
        # Optionally, warn that no src dir was found
        issues.append("No source directory found. Skipping Python file checks.")

    issues.extend(check_empty_dirs(project_root))
    issues.extend(check_mkdocs_consistency(project_root, policy))

    return issues


def main() -> None:
    """
    Main entry point to run all checks and print results.
    """
    issues = run_all_checks()
    if issues:
        print("Project checks found the following issues:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("All project checks passed successfully.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error running project checks: {e}")
