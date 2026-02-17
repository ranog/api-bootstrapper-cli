# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-02-17

### Added
- Initial release of api-bootstrapper-cli
- Bootstrap Python development environments with a single command
- Automatic Python version management via pyenv
- Poetry integration for dependency management
- VSCode configuration with Python interpreter and testing setup
- Auto-creation of minimal `pyproject.toml` if missing
- Smart environment detection - skips setup if already configured
- Clean environment isolation to prevent version conflicts
- Support for any Python version available in pyenv
- Comprehensive test suite with 53 passing tests

### Features
- `bootstrap-env` command to setup complete Python development environment
- Installs pip, setuptools, wheel, and poetry in project's Python version
- Creates `.python-version` file for pyenv
- Configures Poetry with in-project virtualenv (`.venv`)
- Generates VSCode `settings.json` with Python interpreter and pytest configuration
- Direct venv activation path (no dependency on Poetry command)
- Protocol-based architecture for better maintainability

### Documentation
- Comprehensive README with usage examples
- Command help with detailed descriptions
- MIT License

[Unreleased]: https://github.com/joaopnogueira/api-bootstrapper-cli/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/joaopnogueira/api-bootstrapper-cli/releases/tag/v0.1.0
