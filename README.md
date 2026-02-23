# api-bootstrapper-cli

[![Python Version](https://img.shields.io/pypi/pyversions/api-bootstrapper-cli)](https://pypi.org/project/api-bootstrapper-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Tests](https://github.com/ranog/api-bootstrapper-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/ranog/api-bootstrapper-cli/actions/workflows/ci.yml)

A modular and extensible CLI for bootstrapping Python projects with opinionated platform defaults.

Automates the setup of **pyenv**, **Poetry**, and **VSCode** configuration in a single command, following manual setup best practices.

---

## ✨ Features

- 🐍 **Python Version Management** - Automatic installation and configuration via pyenv
- 📦 **Dependency Management** - Poetry setup with in-project virtualenv
- 🔧 **VSCode Integration** - Auto-generated settings for Python interpreter and testing
- 🪝 **Pre-commit Hooks** - Automated setup with Ruff and Commitizen
- 🚀 **Smart Detection** - Skips setup if environment already exists
- 🎯 **Zero Configuration** - Creates minimal `pyproject.toml` if missing
- 🔒 **Environment Isolation** - Clean environment to prevent version conflicts
- ✅ **Battle-tested** - Comprehensive test suite with high coverage

---

## 📦 Installation

### With pipx (recommended)

First, install pipx if you don't have it:

```bash
# macOS
brew install pipx
pipx ensurepath

# Linux (Debian/Ubuntu)
sudo apt install pipx
pipx ensurepath

# Or using pip
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Then install the CLI:

```bash
pipx install git+https://github.com/ranog/api-bootstrapper-cli.git
```

**After installation, reload your shell:**

```bash
source ~/.bashrc  # or ~/.zshrc if using zsh
```

**Why pipx?** Installs the CLI in an isolated environment, making it available globally regardless of your current Python version.

> **Note:** If you previously installed via `pip`, uninstall it first: `pip uninstall api-bootstrapper-cli`

### From PyPI

```bash
pip install api-bootstrapper-cli
```

### From source (for development)

```bash
git clone https://github.com/ranog/api-bootstrapper-cli
cd api-bootstrapper-cli
poetry install
```

### Updating

To update to the latest version:

**If installed via pipx from git:**

```bash
pipx install git+https://github.com/ranog/api-bootstrapper-cli.git --force
```

**If installed via pipx from PyPI (when available):**

```bash
pipx upgrade api-bootstrapper-cli
```

**If installed via pip:**

```bash
pip install --upgrade api-bootstrapper-cli
```

### Enable shell completion (optional)

Enable tab completion for commands and options:

```bash
# Install completion for your shell
api-bootstrapper --install-completion

# Restart your shell or run:
source ~/.bashrc  # or ~/.zshrc
```

Now you can use tab completion:
```bash
api-bootstrapper <TAB>           # Shows: init, bootstrap-env, add-alembic, add-precommit
api-bootstrapper bootstrap-env --<TAB>  # Shows: --path, --python, --install
```

---

## 🚀 Quick Start

### Option 1: All-in-One (Recommended)

Initialize a complete Python project with a single command:

```bash
# Complete setup: environment + pre-commit hooks
api-bootstrapper init --python 3.12.12 --path ./my-project

# Navigate and activate
cd my-project
source .venv/bin/activate

# Start coding!
python --version  # Python 3.12.12
poetry --version  # Poetry (version 2.3.2)
pre-commit --version  # pre-commit x.x.x
```

### Option 2: Step-by-Step

For more control, run commands individually:

```bash
# Step 1: Setup Python environment
api-bootstrapper bootstrap-env --python 3.12.12 --path ./my-project

# Step 2: Add pre-commit hooks (optional)
api-bootstrapper add-precommit --path ./my-project

# Navigate and activate
cd my-project
source .venv/bin/activate
```

> **Note:** The CLI automatically detects paths with spaces or accents (e.g., `/Área de Trabalho/project`) and shows `source $(poetry env info --path)/bin/activate` which handles special characters reliably.

---

## 📖 Usage

### Two Ways to Use This CLI

**🎯 Use `init` when:**
- Starting a new project from scratch
- You want everything configured in one command
- Recommended for most users

**🔧 Use individual commands when:**
- You already have a project and want to add specific features
- You need more granular control over the setup
- You want to configure environment and hooks separately

### Prerequisites

**For using the CLI:**
- [pipx](https://pipx.pypa.io/) (recommended) or pip
- macOS or Linux  
- [pyenv](https://github.com/pyenv/pyenv) installed

**Target project can be:**
- **Empty directory** - Will create a minimal `pyproject.toml` and setup full environment
- **Existing project** - With `pyproject.toml` already present

### Python Version Support

**Created projects default to Python 3.10+**

When bootstrapping a new project without specifying a Python version, the tool creates a `pyproject.toml` with:
```toml
[tool.poetry.dependencies]
python = "^3.10"
```

**Why Python 3.10 as minimum?**
- ✅ Still under official security support (EOL: October 2026)
- ✅ Compatible with all development tools (ruff, pre-commit, mypy, pytest)
- ✅ Balances compatibility with modern Python features
- ✅ Enterprises focused on security have already migrated from 3.9

**You can use any Python version you want:**
```bash
# Use Python 3.11
api-bootstrapper init --python 3.11.5

# Use Python 3.12
api-bootstrapper init --python 3.12.0

# Use Python 3.13
api-bootstrapper init --python 3.13.2
```

The tool will automatically set the correct Python constraint in `pyproject.toml` based on the version you specify.

> **Note:** The CLI itself requires Python 3.12+ to run, but can bootstrap projects with Python 3.10+.

---
- **Empty directory** - Will create a minimal `pyproject.toml` and setup full environment
- **Existing project** - With `pyproject.toml` already present

---

## 📋 Commands

### init

Initialize a complete Python project with all features in one command.

This command combines `bootstrap-env` and `add-precommit` into a single workflow, giving you a fully configured development environment.

**Basic usage:**

```bash
# Initialize new project
api-bootstrapper init --python 3.12.12 --path ./my-project

# In current directory
api-bootstrapper init --python 3.13.9

# Skip dependency installation
api-bootstrapper init --python 3.12.12 --no-install
```

**What it does:**

1. ✅ Sets up Python environment (pyenv + Poetry + VSCode)
2. ✅ Installs pre-commit, ruff, and commitizen dependencies
3. ✅ Configures pre-commit hooks
4. ✅ Shows clear next steps

**This is the recommended command for new projects!**

---

### bootstrap-env

Sets up a complete Python development environment with pyenv, Poetry, and VSCode configuration.

> **💡 Tip:** If you want environment + pre-commit in one command, use `init` instead.

**Basic usage:**

```bash
# In current directory
api-bootstrapper bootstrap-env --python 3.12.12

# In a specific directory
api-bootstrapper bootstrap-env --python 3.13.9 --path ./my-api

# Skip dependency installation
api-bootstrapper bootstrap-env --python 3.12.12 --no-install

# For an existing project
cd existing-project
api-bootstrapper bootstrap-env --python 3.12.12
```

**What it does:**

1. ✅ Installs Python version via pyenv (if not installed)
2. ✅ Creates `.python-version` file
3. ✅ Installs `pip`, `setuptools`, `wheel`, and `poetry` in project's Python
4. ✅ Creates minimal `pyproject.toml` if missing (never overwrites)
5. ✅ Configures Poetry with in-project virtualenv (`.venv`)
6. ✅ Creates Poetry environment
7. ✅ Installs dependencies (unless `--no-install`)
8. ✅ Generates VSCode `settings.json` with Python interpreter

**Smart detection:**
Running the command a second time on the same project will skip setup if the environment is already configured.

```bash
# First run: Full setup
api-bootstrapper bootstrap-env --python 3.12.12

# Second run: Skips setup
api-bootstrapper bootstrap-env --python 3.12.12
# Output: environment already configured ✓
```

### add-precommit

Configures pre-commit hooks with Ruff (linter/formatter) and Commitizen (conventional commits).

> **💡 Tip:** If you're starting a new project, use `init` which includes this automatically.

**Basic usage:**

```bash
# In current directory
api-bootstrapper add-precommit

# In a specific directory
api-bootstrapper add-precommit --path ./my-project
```

**What it does:**

1. ✅ Creates `.pre-commit-config.yaml` with Ruff and Commitizen hooks
2. ✅ Adds `pre-commit`, `ruff`, and `commitizen` to dev dependencies via Poetry
3. ✅ Updates hook versions in config to match installed packages
4. ✅ Installs pre-commit hooks (pre-commit and commit-msg)

**Generated hooks:**
- **Ruff** - Runs linting with auto-fix on pre-commit
- **Ruff Format** - Formats code automatically
- **Commitizen** - Validates commit messages follow conventional commits

**Example workflow:**

```bash
# After running add-precommit
git add .
git commit -m "fix: correct bug"  # ✓ Valid conventional commit

# Hooks automatically run:
# 1. Ruff checks and fixes code
# 2. Ruff formats code
# 3. Commitizen validates commit message
```

**Requires:**
- Git repository initialized (`.git/` directory)
- Poetry environment configured

---

## 📁 Project Structure

After running `init` or `bootstrap-env`, your project will have:

```
my-project/
├── .git/                    # Git repository
├── .pre-commit-config.yaml  # Pre-commit hooks (if add-precommit used)
├── .python-version          # Python version for pyenv
├── .venv/                   # Poetry virtualenv
├── .vscode/
│   └── settings.json        # VSCode Python configuration
└── pyproject.toml           # Poetry configuration
```

### Generated pyproject.toml

If no `pyproject.toml` exists, a minimal one is created:

```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = ""
authors = []
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.10"  # Default: 3.10+ (automatically set from --python version)

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

**Important:**
- Python version constraint automatically matches your specified `--python` version
- Default is `^3.10` if no version specified
- Uses `[tool.poetry]` section (standard Poetry format)
- The CLI uses `poetry install --no-root` for dependencies only
- Works for both libraries and applications

---

## 🎯 Philosophy

Instead of generating a huge opinionated template, `api-bootstrapper-cli` allows you to:

- ✅ Initialize a minimal working environment
- ✅ Add platform features incrementally
- ✅ Maintain idempotency (safe to run multiple times)
- ✅ Avoid breaking existing setups

Designed for teams that want **consistent environments** and **deterministic setup** without the complexity of cookiecutter templates.

---

## 🗺️ Roadmap

- ✅ `init` - Complete project initialization (environment + pre-commit)
- ✅ `bootstrap-env` - pyenv + Poetry + VSCode
- ✅ `add-precommit` - Git hooks with Ruff and Commitizen
- ⬜ `add-alembic` - Database migrations
- ⬜ `add-docker-postgres` - Local database
- ⬜ `add-mypy` - Type checking
- ⬜ `add-healthcheck` - Basic health endpoints
- ⬜ Profiles - fastapi-postgres-clean-arch

---

## 🧪 Development

### Setup development environment

```bash
# Clone and install
git clone https://github.com/ranog/api-bootstrapper-cli.git
cd api-bootstrapper-cli
poetry install
```

### Running tests

```bash
# All tests
poetry run pytest

# With coverage
poetry run pytest --cov=api_bootstrapper_cli

# By type
poetry run pytest -m unit
poetry run pytest -m integration
poetry run pytest -m e2e
```

### Code quality

```bash
# Linting & formatting (auto-fix)
poetry run ruff check . --fix
poetry run ruff format .
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Install dependencies (`poetry install`)
4. Make your changes with tests
5. Run tests and formatting (`poetry run pytest`, `poetry run ruff format .`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to your fork (`git push origin feature/amazing-feature`)
8. Open a Pull Request

---

## 📄 License

MIT License © 2026 João Paulo Ramos Nogueira

See [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Typer](https://typer.tiangolo.com/) for the CLI framework
- Styled with [Rich](https://rich.readthedocs.io/) for beautiful terminal output
- Tested with [pytest](https://pytest.org/) for reliability

---

**Made with ❤️ for Python developers who value automation and consistency**
