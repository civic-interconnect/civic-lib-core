# _ci_release.ps1
# Automate version bump, testing, tagging, and push.

param (
    [Parameter(Mandatory = $true)]
    [string]$Version  # Example: "0.1.0"
)

$Version = $Version.TrimStart("v")

Write-Host "Bumping version to $Version..."

# Update pre-commit hooks
Write-Host "Updating pre-commit hooks..."
pre-commit autoupdate --repo https://github.com/pre-commit/pre-commit-hooks

# Clean build directory if it exists
if (Test-Path "build") {
    Remove-Item -Recurse -Force build
}

# Uninstall civic-lib-*  packages if installed
pip freeze | ForEach-Object {
    if ($_ -match "^civic-lib-" ) {
        $pkg = ($_ -split "==")[0]
        Write-Host "Uninstalling $pkg"
        pip uninstall $pkg -y
    }
}

# Reinstall if pyproject.toml exists
if (Test-Path "pyproject.toml") {
    Write-Host "Installing package from pyproject.toml"
    pip install -e .
} else {
    Write-Host "No pyproject.toml — skipping install."
}

# Run ruff check with fix
Write-Host "Running ruff check..."
ruff check . --fix
if ($LASTEXITCODE -ne 0) {
    Write-Host "ruff check found issues; continuing after fixes."
}

# Run pre-commit (twice)
if (Test-Path ".pre-commit-config.yaml") {
    Write-Host "Running pre-commit hooks..."
    pre-commit run --all-files
    pre-commit run --all-files
}

# Run tests if present
if (Test-Path "tests") {
    Write-Host "Running tests..."
    pytest
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Tests failed."
        exit $LASTEXITCODE
    }
} else {
    Write-Host "No tests folder — skipping tests."
}

# Stage and commit if needed
git add .
git diff --cached --quiet
if ($LASTEXITCODE -eq 1) {
    git commit -m "Release: v$Version"
    git push origin main
    Write-Host "Pushed commit for v$Version."
} else {
    Write-Host "No changes to commit."
}

# ====================================================================================
# EARLY STAGE ONLY: Always delete and recreate local and remote tag (v$Version)
# WARNING: This approach is unsafe for production or team workflows.
# TODO: Replace with tag protection and version increment logic before production.
# ====================================================================================

$tag = "v$Version"
if (git tag --list $tag) {
    Write-Host "Tag $tag already exists — deleting and recreating."

    # Delete local tag
    git tag -d $tag

    # Delete remote tag
    git push --delete origin $tag
}

Write-Host "Creating and pushing tag $tag..."
git tag $tag
git push origin $tag

Write-Host "Release v$Version completed successfully."
