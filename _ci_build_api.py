"""
_ci_build_api.py - Generate Markdown API docs for Civic Interconnect libraries.

- Scans the package for public functions/classes.
- Captures signatures and docstrings.
- Flags missing docstrings.
- Writes output to REF_API.md.

Intended for Civic Interconnect developer use.
"""

import contextlib
import importlib
import inspect
import sys
from pathlib import Path


def add_src_to_syspath():
    """Ensure src is on sys.path for dynamic imports."""
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))
    return src_path


def find_package_dir(src_dir: Path) -> tuple[str, Path]:
    """Find the top-level package (e.g., civic_lib_core) inside src/."""
    for path in src_dir.iterdir():
        if path.is_dir() and path.name.startswith("civic_"):
            return path.name, path
    raise RuntimeError("Could not find a top-level 'civic_' package folder in src/.")


def find_modules(package_dir: Path, base_module: str):
    """Yield fully qualified module names inside the package."""
    for py_file in package_dir.rglob("*.py"):
        if py_file.name.startswith("_") or py_file.name == "__init__.py":
            continue
        parts = py_file.relative_to(package_dir.parent).with_suffix("").parts
        module = ".".join(parts)
        if module.startswith(base_module):
            yield module


def format_function_or_class(name: str, obj, module_name: str, url_base: str):
    """Return markdown lines for a single function or class if it belongs to this module, using collapsible details."""
    module = inspect.getmodule(obj)
    if module is None or module.__name__ != module_name:
        return []  # Skip imported symbols

    lines = []
    sig = "(...)"
    with contextlib.suppress(Exception):
        sig = str(inspect.signature(obj))

    lines.append("<details>")
    lines.append(f"<summary><code>{name}{sig}</code></summary>\n")

    doc = inspect.getdoc(obj)
    lines.append(doc if doc else "WARNING: Missing docstring.")

    with contextlib.suppress(Exception):
        file_path = Path(inspect.getfile(obj)).relative_to(Path(__file__).parent.parent)
        line_no = inspect.getsourcelines(obj)[1]
        url = f"{url_base}{file_path}#L{line_no}"
        lines.append(f"\n\n[View source]({url})")

    lines.append("\n</details>\n")
    return lines


def generate_module_doc(module_name: str, url_base: str):
    """Return formatted API docs for a module, or an error block."""
    lines = [f"# API for `{module_name}`\n"]
    try:
        mod = importlib.import_module(module_name)
    except Exception as e:
        return [f"ERROR: Failed to import `{module_name}`: {e}\n"]

    for name, obj in inspect.getmembers(mod):
        if name.startswith("_"):
            continue
        lines += format_function_or_class(name, obj, mod.__name__, url_base)
    return lines


def write_api_doc(output_path: Path, doc_lines: list[str]):
    """Write the final documentation file."""
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text("\n".join(doc_lines), encoding="utf-8")


def main():
    print("Starting API documentation generation...")

    root_dir = Path(__file__).resolve().parent
    src_dir = add_src_to_syspath()
    package_name, package_dir = find_package_dir(src_dir)

    print(f"Package: {package_name}")
    print(f"Scanning: {package_dir}")

    # 🔧 Dynamically generate GitHub URL base
    repo_name = package_name.replace("_", "-")
    url_base = f"https://github.com/civic-interconnect/{repo_name}/blob/main/"

    output_file = root_dir / "REF_API.md"
    all_lines = ["# Civic Interconnect API Documentation\n"]

    for mod_name in sorted(find_modules(package_dir, package_name)):
        print(f"Processing module: {mod_name}")
        all_lines.extend(generate_module_doc(mod_name, url_base))

    write_api_doc(output_file, all_lines)
    print(f"API documentation written to {output_file}")


if __name__ == "__main__":
    main()
