"""Generate and update application interface documentation using pdoc.

This script:
- Locates the project root
- Discovers local Python packages to document
- Generates standalone HTML API documentation
- Writes HTML files into the docs/api/ folder (or configured docs_api_dir)

File cli/build_api.py

"""

import subprocess
import sys

from civic_lib_core import log_utils, project_layout

logger = log_utils.logger


def main() -> int:
    """Generate standalone HTML API documentation using pdoc.

    Returns:
        int: exit code (0 if successful, nonzero otherwise)
    """
    logger.info("Generating API documentation with pdoc...")

    # Discover the project layout (includes paths and package info)
    layout = project_layout.discover_project_layout()

    output_dir = layout.docs_api_dir
    if not output_dir:
        logger.error("No output directory configured for API documentation.")
        return 1
    output_dir.mkdir(parents=True, exist_ok=True)

    # Convert list of package Paths → dotted module names
    packages = _packages_as_module_names(layout.packages, layout.src_dir)

    if not packages:
        logger.warning("No Python packages found to document.")
        return 0

    logger.info(f"Packages discovered for API docs: {', '.join(packages)}")

    # Validate packages before building command
    validation_error = _validate_packages(packages)
    if validation_error:
        return validation_error

    # Build and validate pdoc command
    cmd = _build_pdoc_command(packages, output_dir)
    validation_error = _validate_command(cmd, output_dir)
    if validation_error:
        return validation_error

    # Execute pdoc command
    return _execute_pdoc_command(cmd, output_dir)


def _validate_packages(packages):
    """Validate that packages only contain safe module names.

    Returns:
        int: error code if validation fails, 0 if successful
    """
    for package in packages:
        if not package.replace("_", "").replace(".", "").isalnum():
            logger.error(f"Invalid package name detected: {package}")
            return 1
    return 0


def _build_pdoc_command(packages, output_dir):
    """Build the pdoc command with all arguments."""
    return [
        sys.executable,
        "-m",
        "pdoc",
        *packages,
        "--output-dir",
        str(output_dir),
    ]


def _validate_command(cmd, output_dir):
    """Validate the pdoc command for security and correctness.

    Returns:
        int: error code if validation fails, 0 if successful
    """
    # Final safety check: only allow trusted executable and known safe arguments
    if cmd[0] != sys.executable or cmd[1] != "-m" or cmd[2] != "pdoc":
        logger.error("Command validation failed: untrusted executable or module")
        return 1

    # Additional validation: ensure cmd is properly constructed
    if len(cmd) < 4 or not all(isinstance(arg, str) for arg in cmd):
        logger.error("Command structure validation failed")
        return 1

    # Additional validation: ensure all arguments are safe
    for i, arg in enumerate(cmd):
        if i < 3 or arg == "--output-dir":  # sys.executable, "-m", "pdoc" are trusted
            continue
        if i == len(cmd) - 1:  # Last argument should be output_dir
            if str(output_dir) != arg:
                logger.error(f"Output directory mismatch: expected {output_dir}, got {arg}")
                return 1
        else:  # Package names
            if not arg.replace("_", "").replace(".", "").isalnum():
                logger.error(f"Unsafe package name detected: {arg}")
                return 1
    return 0


def _execute_pdoc_command(cmd, output_dir):
    """Execute the pdoc command and handle errors.

    Returns:
        int: exit code from pdoc execution
    """
    try:
        # Perform comprehensive validation
        validation_error = _perform_comprehensive_validation(cmd, output_dir)
        if validation_error:
            return validation_error

        # Build and validate trusted command
        trusted_cmd = _build_and_validate_trusted_command(cmd, output_dir)
        if not trusted_cmd:
            logger.error("Failed to build trusted command")
            return 1

        logger.info(f"Running command: {' '.join(trusted_cmd)}")

        # Execute with subprocess after all validations
        # Command has been thoroughly validated through multiple layers
        result = subprocess.run(trusted_cmd, check=True, shell=False)  # noqa: S603
        logger.info(f"API documentation successfully generated in {output_dir}")
        return result.returncode
    except subprocess.CalledProcessError as e:
        logger.error(f"pdoc build failed with exit code {e.returncode}")
        return e.returncode
    except Exception as e:
        logger.error(f"Unexpected error during API generation: {e}", exc_info=True)
        return 1


def _perform_comprehensive_validation(cmd, output_dir):
    """Perform all validation checks on the command.

    Returns:
        int: error code if validation fails, 0 if successful
    """
    # Validate command structure
    if not _validate_command_structure(cmd):
        return 1

    # Validate command arguments
    return _validate_command_arguments(cmd, output_dir)


def _validate_command_structure(cmd):
    """Validate the basic structure of the command.

    Returns:
        bool: True if valid, False otherwise
    """
    if len(cmd) < 4:
        logger.error("Command too short")
        return False

    if cmd[0] != sys.executable:
        logger.error("Untrusted executable")
        return False

    if cmd[1] != "-m":
        logger.error("Invalid module flag")
        return False

    if cmd[2] != "pdoc":
        logger.error("Invalid module name")
        return False

    if not all(isinstance(arg, str) for arg in cmd):
        logger.error("Command contains non-string arguments")
        return False

    return True


def _validate_command_arguments(cmd, output_dir):
    """Validate each command argument.

    Returns:
        int: error code if validation fails, 0 if successful
    """
    for i, arg in enumerate(cmd):
        validation_error = _validate_single_argument(i, arg, cmd, output_dir)
        if validation_error:
            return validation_error
    return 0


def _validate_single_argument(index, arg, cmd, output_dir):
    """Validate a single command argument based on its position.

    Returns:
        int: error code if validation fails, 0 if successful
    """
    if index == 0:
        return _validate_executable(arg)
    if index == 1:
        return _validate_module_flag(arg)
    if index == 2:
        return _validate_module_name(arg)
    if arg == "--output-dir":
        return 0  # Known safe flag
    if index == len(cmd) - 1:
        return _validate_output_directory(arg, output_dir)
    return _validate_package_name(arg)


def _validate_executable(arg):
    """Validate the executable argument."""
    if arg != sys.executable:
        logger.error("Untrusted executable")
        return 1
    return 0


def _validate_module_flag(arg):
    """Validate the module flag argument."""
    if arg != "-m":
        logger.error("Invalid module flag")
        return 1
    return 0


def _validate_module_name(arg):
    """Validate the module name argument."""
    if arg != "pdoc":
        logger.error("Invalid module name")
        return 1
    return 0


def _validate_output_directory(arg, output_dir):
    """Validate the output directory argument."""
    if str(output_dir) != arg:
        logger.error("Output directory validation failed")
        return 1
    return 0


def _validate_package_name(arg):
    """Validate a package name argument."""
    if not arg.replace("_", "").replace(".", "").isalnum():
        logger.error(f"Unsafe package name: {arg}")
        return 1
    return 0


def _build_and_validate_trusted_command(cmd, output_dir):
    """Build and validate a trusted command from validated input.

    Returns:
        list: trusted command arguments, or None if validation fails
    """
    # Build trusted command
    trusted_cmd = _build_trusted_command(cmd, output_dir)

    # Perform final validation
    if not _validate_trusted_command_final(trusted_cmd, output_dir):
        return None

    return trusted_cmd


def _build_trusted_command(cmd, output_dir):
    """Build a trusted command from validated input.

    Returns:
        list: trusted command arguments
    """
    trusted_cmd = [sys.executable, "-m", "pdoc"]

    # Add validated package names
    for i in range(3, len(cmd)):
        if cmd[i] == "--output-dir":
            trusted_cmd.extend(["--output-dir", str(output_dir)])
            break
        # Already validated as safe package name
        trusted_cmd.append(cmd[i])

    # Add output dir if not already added
    if "--output-dir" not in trusted_cmd:
        trusted_cmd.extend(["--output-dir", str(output_dir)])

    return trusted_cmd


def _validate_trusted_command_final(trusted_cmd, output_dir):
    """Perform final validation on the trusted command.

    Returns:
        bool: True if valid, False otherwise
    """
    # Check basic structure
    if not (
        len(trusted_cmd) >= 5
        and trusted_cmd[0] == sys.executable
        and trusted_cmd[1] == "-m"
        and trusted_cmd[2] == "pdoc"
        and "--output-dir" in trusted_cmd
    ):
        logger.error("Trusted command structure invalid")
        return False

    # Validate all arguments are strings
    if not all(isinstance(arg, str) for arg in trusted_cmd):
        logger.error("Trusted command contains non-string arguments")
        return False

    # Validate each argument
    for arg in trusted_cmd[3:]:
        if arg in ["--output-dir", str(output_dir)]:
            continue
        if not arg.replace("_", "").replace(".", "").isalnum():
            logger.error(f"Unsafe argument in trusted command: {arg}")
            return False

    return True


def _packages_as_module_names(packages, src_dir):
    """Convert a list of Path objects under src_dir into dotted Python module names.

    Args:
        packages (list[Path]): package directories under src_dir
        src_dir (Path): path to the source directory

    Returns:
        list[str]: e.g. ["civic_lib_core", "civic_lib_core.cli"]
    """
    return sorted(
        ".".join(p.parts) for p in (pkg.relative_to(src_dir) for pkg in packages) if p.parts
    )


if __name__ == "__main__":
    sys.exit(main())
