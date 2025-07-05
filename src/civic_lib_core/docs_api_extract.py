"""
civic_lib_core/docs_api_extract.py

Utilities to analyze Python source code and extract public API metadata
for documentation purposes in Civic Interconnect projects.

Features:
- Dynamic import of Python modules from file paths
- AST-based extraction of public classes and functions
- Capture of signatures and docstrings for documentation rendering

This module is backend logic for transforming code into structured
data used by the documentation system.
"""

import ast
import importlib.util
import inspect
import sys
from pathlib import Path
from types import ModuleType

from civic_lib_core import log_utils

__all__ = [
    "dynamic_import_from_path",
    "extract_module_api",
    "extract_public_names",
    "find_public_classes",
    "find_public_functions",
    "get_public_members",
    "parse_python_file",
]

logger = log_utils.logger


def dynamic_import_from_path(file_path: Path, module_name: str) -> ModuleType:
    """
    Dynamically import a Python module from a file path.

    Args:
        file_path (Path): Path to the .py file.
        module_name (str): Name to assign to the imported module.

    Returns:
        ModuleType: Imported Python module object.

    Raises:
        ImportError: If module cannot be loaded.
    """
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {module_name} from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def extract_module_api(package_path: Path) -> dict[str, dict]:
    """
    Recursively extract public functions and classes from Python source files.

    Args:
        package_path (Path): Path to a Python package directory.

    Returns:
        dict[str, dict]: Mapping of module names to their functions and classes.
    """
    api_data = {}

    for py_file in package_path.rglob("*.py"):
        logger.info(f"Processing {py_file}")
        if py_file.name.startswith("_"):
            continue  # skip private modules like __init__.py

        rel_path = py_file.relative_to(package_path)
        module_name = ".".join(rel_path.with_suffix("").parts)

        try:
            module = dynamic_import_from_path(py_file, module_name)
            functions, classes = get_public_members(module)
            api_data[module_name] = {
                "functions": functions,
                "classes": classes,
            }
        except Exception as e:
            logger.warning(f"Skipped {py_file}: {e}")

    return api_data


def extract_public_names(tree: ast.AST) -> set[str]:
    """
    Extract names listed in a module's __all__ variable.

    Args:
        tree (ast.AST): Parsed AST tree.

    Returns:
        set[str]: Public names listed in __all__, if any.
    """
    public_names = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets)
            and isinstance(node.value, ast.List)
        ):
            public_names |= {elt.s for elt in node.value.elts if isinstance(elt, ast.Str)}
    return public_names


def find_public_classes(tree: ast.AST, public_names: set[str]) -> list[dict[str, str]]:
    """
    Find all public classes in a Python module AST.

    Args:
        tree (ast.AST): Parsed AST tree.
        public_names (set[str]): Names explicitly marked public in __all__.

    Returns:
        list[dict[str, str]]: Class info dicts.
    """
    classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and (
            not node.name.startswith("_") or node.name in public_names
        ):
            docstring = ast.get_docstring(node) or "No description available."

            # Get base classes
            bases = [ast.unparse(base) for base in node.bases] if node.bases else []
            inheritance = f"({', '.join(bases)})" if bases else ""

            classes.append({
                "name": node.name,
                "signature": f"{node.name}{inheritance}",
                "docstring": docstring,
            })

    return sorted(classes, key=lambda x: x["name"])


def find_public_functions(tree: ast.AST, public_names: set[str]) -> list[dict[str, str]]:
    """
    Find all public functions in a Python module AST.

    Args:
        tree (ast.AST): Parsed AST tree.
        public_names (set[str]): Names explicitly marked public in __all__.

    Returns:
        list[dict[str, str]]: Function info dicts.
    """
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and (
            not node.name.startswith("_") or node.name in public_names
        ):
            docstring = ast.get_docstring(node) or "No description available."

            # Build signature
            args = [arg.arg for arg in node.args.args]
            defaults = (
                [ast.unparse(default) for default in node.args.defaults]
                if node.args.defaults
                else []
            )

            signature_parts = []
            num_defaults = len(defaults)
            for i, arg in enumerate(args):
                if i >= len(args) - num_defaults:
                    default_idx = i - (len(args) - num_defaults)
                    signature_parts.append(f"{arg}={defaults[default_idx]}")
                else:
                    signature_parts.append(arg)

            signature = f"{node.name}({', '.join(signature_parts)})"

            functions.append({
                "name": node.name,
                "signature": signature,
                "docstring": docstring,
            })

    return sorted(functions, key=lambda x: x["name"])


def get_public_members(module) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """
    Inspect a live imported Python module for public classes and functions.

    Args:
        module (ModuleType): Imported Python module.

    Returns:
        tuple: (functions, classes)
            Each is a list of dicts with name, signature, and docstring.
    """
    functions = []
    classes = []

    for name, member in vars(module).items():
        if name.startswith("_"):
            continue

        if inspect.isfunction(member):
            try:
                sig = str(inspect.signature(member))
            except Exception:
                sig = "()"
            doc = inspect.getdoc(member) or "No description available."
            functions.append({"name": name, "signature": f"{name}{sig}", "docstring": doc})

        elif inspect.isclass(member):
            try:
                sig = str(inspect.signature(member.__init__))
            except Exception:
                sig = "()"
            doc = inspect.getdoc(member) or "No description available."
            classes.append({"name": name, "signature": f"{name}{sig}", "docstring": doc})

    return sorted(functions, key=lambda x: x["name"]), sorted(classes, key=lambda x: x["name"])


def parse_python_file(file_path: Path) -> ast.AST | None:
    """
    Parse a Python file into an AST.

    Args:
        file_path (Path): Path to a Python file.

    Returns:
        ast.AST | None: AST object if parsing succeeds, else None.
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            return ast.parse(f.read(), filename=str(file_path))
    except SyntaxError as e:
        logger.warning(f"Syntax error in {file_path}: {e}")
        return None
