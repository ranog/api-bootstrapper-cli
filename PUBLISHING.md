# Publishing Guide

This document describes how to publish `api-bootstrapper-cli` to PyPI.

## Prerequisites

1. PyPI account: https://pypi.org/account/register/
2. TestPyPI account (optional but recommended): https://test.pypi.org/account/register/
3. Poetry installed and configured

## Configure PyPI Credentials

### Option 1: Using Poetry (recommended)

```bash
# Configure PyPI token
poetry config pypi-token.pypi <your-token>

# Or for TestPyPI
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi <your-testpypi-token>
```

### Option 2: Using environment variables

```bash
export POETRY_PYPI_TOKEN_PYPI=<your-token>
export POETRY_PYPI_TOKEN_TESTPYPI=<your-testpypi-token>
```

## Pre-publication Checklist

- [ ] All tests pass: `poetry run pytest`
- [ ] Version updated in `pyproject.toml`
- [ ] Version updated in `src/api_bootstrapper_cli/__init__.py`
- [ ] `CHANGELOG.md` updated with release notes
- [ ] `README.md` reviewed and up to date
- [ ] Git repository clean (no uncommitted changes)
- [ ] New version tagged: `git tag v0.1.0` and `git push --tags`

## Build the Package

```bash
# Clean any previous builds
rm -rf dist/

# Build the package
poetry build
```

This creates:
- `dist/api_bootstrapper_cli-0.1.0.tar.gz` (source distribution)
- `dist/api_bootstrapper_cli-0.1.0-py3-none-any.whl` (wheel)

## Test on TestPyPI (Optional but Recommended)

```bash
# Publish to TestPyPI
poetry publish -r testpypi

# Test installation
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ api-bootstrapper-cli

# Test the CLI
api-bootstrapper --help
api-bootstrapper bootstrap-env --help

# Uninstall test version
pip uninstall api-bootstrapper-cli
```

**Note:** The `--extra-index-url` is needed because TestPyPI might not have all dependencies.

## Publish to PyPI

```bash
# Publish to production PyPI
poetry publish
```

Or if you want to build and publish in one step:

```bash
poetry publish --build
```

## Verify Publication

1. Check PyPI: https://pypi.org/project/api-bootstrapper-cli/
2. Test installation:
   ```bash
   pip install api-bootstrapper-cli
   api-bootstrapper --version
   ```

## Post-publication Steps

- [ ] Create GitHub release with changelog
- [ ] Update documentation if needed
- [ ] Announce on relevant channels (team Slack, etc.)

## Version Bumping

Use semantic versioning (MAJOR.MINOR.PATCH):

- **PATCH** (0.1.1): Bug fixes, no new features
- **MINOR** (0.2.0): New features, backward compatible
- **MAJOR** (1.0.0): Breaking changes

Update versions in:
1. `pyproject.toml` - `version = "0.1.0"`
2. `src/api_bootstrapper_cli/__init__.py` - `__version__ = "0.1.0"`
3. `CHANGELOG.md` - Add new version section

```bash
# Quick version bump with Poetry
poetry version patch  # 0.1.0 -> 0.1.1
poetry version minor  # 0.1.0 -> 0.2.0
poetry version major  # 0.1.0 -> 1.0.0

# Don't forget to update __init__.py manually after!
```

## Troubleshooting

### "File already exists" error

This means the version already exists on PyPI. You need to bump the version number.

### Authentication errors

Make sure your PyPI token is correctly configured:
```bash
poetry config pypi-token.pypi <your-token>
```

### Missing dependencies in built package

Check `pyproject.toml` to ensure all dependencies are listed correctly.

### Import errors after installation

Verify the package structure:
```bash
tar -tzf dist/api_bootstrapper_cli-0.1.0.tar.gz
```

Should include `api_bootstrapper_cli/` directory with all Python files.

## Rolling Back

If you need to remove a release (only works for <72 hours):

1. Go to PyPI project page
2. Manage → Releases
3. Delete the problematic release
4. Fix the issue, bump version, and republish

**Note:** You cannot reuse the same version number, even after deletion.
