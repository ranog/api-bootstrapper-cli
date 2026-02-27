# api-bootstrapper-cli

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Tests](https://github.com/ranog/api-bootstrapper-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/ranog/api-bootstrapper-cli/actions/workflows/ci.yml)

A modular and extensible CLI for bootstrapping Python projects with opinionated platform defaults.

Automates the setup of **pyenv + Poetry** or **uv**, plus **VSCode** configuration in a single command, following manual setup best practices.

---

## ✨ Features

- 🐍 **Python Version Management** - Automatic installation and configuration via pyenv or uv
- 📦 **Dependency Management** - Poetry or uv setup with in-project virtualenv
- 🔧 **VSCode Integration** - Auto-generated settings for Python interpreter and testing
- 🪝 **Pre-commit Hooks** - Automated setup with Ruff and Commitizen
- 🚀 **Smart Detection** - Skips setup if environment already exists
- 🎯 **Zero Configuration** - Creates minimal `pyproject.toml` if missing
- 🔒 **Environment Isolation** - Clean environment to prevent version conflicts
- 🔄 **Pluggable Backends** - Choose between pyenv/Poetry (default) or uv via `--manager`
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
api-bootstrapper <TAB>           # Shows: init, bootstrap-env, add-alembic, add-pre-commit
api-bootstrapper bootstrap-env --<TAB>  # Shows: --path, --python, --install
```

---

## 🚀 Quick Start

### Option 1: All-in-One (Recommended)

Initialize a complete Python project with a single command:

```bash
# Complete setup with pyenv + Poetry (default)
api-bootstrapper init --python 3.12.12 --path ./my-project

# Complete setup with uv (faster, single tool)
api-bootstrapper init --python 3.12.12 --path ./my-project --manager uv

# Navigate and activate
cd my-project
source .venv/bin/activate

# With pyenv+Poetry backend:
python --version  # Python 3.12.12
poetry --version  # Poetry (version 2.x.x)

# With uv backend:
python --version  # Python 3.12.12
uv --version      # uv 0.x.x
```

### Option 2: Step-by-Step

For more control, run commands individually:

```bash
# Step 1: Setup Python environment (default: pyenv + Poetry)
api-bootstrapper bootstrap-env --python 3.12.12 --path ./my-project

# Step 1 (alternative): Setup with uv
api-bootstrapper bootstrap-env --python 3.12.12 --path ./my-project --manager uv

# Step 2: Add pre-commit hooks (optional)
api-bootstrapper add-pre-commit --path ./my-project

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
- **Backend: pyenv (default)** — [pyenv](https://github.com/pyenv/pyenv) installed  
  **Backend: uv** — [uv](https://github.com/astral-sh/uv) installed (`pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`)

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

This command combines `bootstrap-env` and `add-pre-commit` into a single workflow, giving you a fully configured development environment.

**Basic usage:**

```bash
# Initialize new project (default: pyenv + Poetry)
api-bootstrapper init --python 3.12.12 --path ./my-project

# Initialize new project with uv
api-bootstrapper init --python 3.12.12 --path ./my-project --manager uv

# In current directory
api-bootstrapper init --python 3.13.9

# Skip dependency installation
api-bootstrapper init --python 3.12.12 --no-install
```

**What it does:**

1. ✅ Sets up Python environment (pyenv or uv + VSCode)
2. ✅ Installs pre-commit, ruff, and commitizen dependencies
3. ✅ Configures pre-commit hooks
4. ✅ Shows clear next steps

**This is the recommended command for new projects!**

See [`--manager` option](#-manager-option) below for choosing between pyenv+Poetry and uv.

---

### bootstrap-env

Sets up a complete Python development environment and VSCode configuration.

Supports two backends via `--manager`:
- **`pyenv`** (default) — uses pyenv for Python installation + Poetry for dependencies
- **`uv`** — uses uv for both Python installation and dependency management (faster)

> **💡 Tip:** If you want environment + pre-commit in one command, use `init` instead.

**Basic usage:**

```bash
# Default backend: pyenv + Poetry
api-bootstrapper bootstrap-env --python 3.12.12
api-bootstrapper bootstrap-env --python 3.13.9 --path ./my-api
api-bootstrapper bootstrap-env --python 3.12.12 --no-install

# uv backend (faster, single tool)
api-bootstrapper bootstrap-env --python 3.12.12 --manager uv
api-bootstrapper bootstrap-env --python 3.13.9 --path ./my-api --manager uv
```

**What it does (pyenv + Poetry backend):**

1. ✅ Installs Python version via pyenv (if not installed)
2. ✅ Creates `.python-version` file
3. ✅ Installs `pip`, `setuptools`, `wheel`, and `poetry` in project's Python
4. ✅ Creates minimal `pyproject.toml` if missing (Poetry format, never overwrites)
5. ✅ Configures Poetry with in-project virtualenv (`.venv`)
6. ✅ Creates Poetry environment
7. ✅ Installs dependencies (unless `--no-install`)
8. ✅ Generates VSCode `settings.json` with Python interpreter

**What it does (uv backend):**

1. ✅ Installs Python version via `uv python install` (if not installed)
2. ✅ Creates `.python-version` file via `uv python pin`
3. ✅ Creates minimal `pyproject.toml` if missing (PEP 621 format, never overwrites)
4. ✅ Creates in-project virtualenv (`.venv`) via `uv venv`
5. ✅ Installs/syncs dependencies via `uv sync` (unless `--no-install`)
6. ✅ Generates VSCode `settings.json` with Python interpreter

**Smart detection:**
Running the command a second time on the same project will skip setup if the environment is already configured.

```bash
# First run: Full setup
api-bootstrapper bootstrap-env --python 3.12.12

# Second run: Skips setup
api-bootstrapper bootstrap-env --python 3.12.12
# Output: environment already configured ✓
```

---

### `--manager` option

All commands that bootstrap an environment accept `--manager pyenv` (default) or `--manager uv`.

| Option | Python version tool | Dependency tool | pyproject.toml format |
|---|---|---|---|
| `--manager pyenv` | `pyenv install` | `poetry install` | `[tool.poetry]` (Poetry) |
| `--manager uv` | `uv python install` | `uv sync` | `[project]` (PEP 621) |

> **When to use uv?** uv is significantly faster and requires only one tool to install.
> Choose `pyenv` when the project already uses Poetry or requires a specific pyenv workflow.

### add-pre-commit

Configures pre-commit hooks with Ruff (linter/formatter) and Commitizen (conventional commits).

> **💡 Tip:** If you're starting a new project, use `init` which includes this automatically.

**Basic usage:**

```bash
# In current directory
api-bootstrapper add-pre-commit

# In a specific directory
api-bootstrapper add-pre-commit --path ./my-project
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
# After running add-pre-commit
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
├── .pre-commit-config.yaml  # Pre-commit hooks (if add-pre-commit used)
├── .python-version          # Python version (pyenv or uv)
├── .venv/                   # Virtual environment
├── .vscode/
│   └── settings.json        # VSCode Python configuration
└── pyproject.toml           # Project configuration (format depends on --manager)
```

### Generated pyproject.toml — pyenv + Poetry backend (`--manager pyenv`)

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

### Generated pyproject.toml — uv backend (`--manager uv`)

```toml
[project]
name = "my-project"
version = "0.1.0"
description = ""
readme = "README.md"
requires-python = ">=3.10"  # automatically set from --python version
dependencies = []
```

**Important:**
- Python version constraint automatically matches your specified `--python` version
- Poetry backend uses `[tool.poetry]` section with caret constraint (`^X.Y`)
- uv backend uses `[project]` section (PEP 621) with floor constraint (`>=X.Y`)
- Neither file is ever overwritten if `pyproject.toml` already exists

---

## 🎯 Philosophy

Instead of generating a huge opinionated template, `api-bootstrapper-cli` allows you to:

- ✅ Initialize a minimal working environment
- ✅ Add platform features incrementally
- ✅ Maintain idempotency (safe to run multiple times)
- ✅ Avoid breaking existing setups

Designed for teams that want **consistent environments** and **deterministic setup** without the complexity of cookiecutter templates.

---

## � Troubleshooting

### pyenv not found

**Symptom:** `Error: pyenv not found in PATH. Install pyenv first.`

```bash
# Install pyenv (Linux)
curl https://pyenv.run | bash

# Add to ~/.bashrc or ~/.zshrc:
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Then reload your shell:
source ~/.bashrc  # or ~/.zshrc
```
### uv not found

**Symptom:** `Error: uv not found in PATH. Install uv first.`

```bash
# Install uv (Linux/macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv

# Or with pipx
pipx install uv

# Make sure ~/.cargo/bin or ~/.local/bin is in PATH:
source ~/.bashrc  # or ~/.zshrc
```
### Python build dependencies (Linux)

When `pyenv install` fails with compilation errors, install the required system libraries:

```bash
# Debian / Ubuntu
sudo apt install -y build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev libffi-dev \
  liblzma-dev tk-dev

# Fedora / RHEL / CentOS
sudo dnf install -y gcc zlib-devel bzip2 bzip2-devel readline-devel \
  sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel
```

### Poetry not found

**Symptom:** The CLI can't locate `poetry` after installation.

```bash
# Check if Poetry is installed
poetry --version

# Install Poetry via pipx (recommended)
pipx install poetry

# Or install via the official installer
curl -sSL https://install.python-poetry.org | python3 -

# Make sure $HOME/.local/bin is in PATH:
export PATH="$HOME/.local/bin:$PATH"
```

### Permission error when removing poetry.lock

If you see a warning about `poetry.lock` not being removable:

```bash
rm poetry.lock
api-bootstrapper bootstrap-env --python <version> --path .
```

### SSL errors when installing packages

```bash
# Test connectivity
python -m pip install --upgrade pip

# If behind a corporate proxy, configure pip:
pip config set global.proxy http://proxy.example.com:8080

# Or set pip trusted hosts:
pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org"
```

### bootstrap-env re-runs even though environment exists

This happens when the venv Python major.minor doesn't match `.python-version`. Delete
the venv and let the CLI recreate it:

```bash
# pyenv + Poetry backend
rm -rf .venv poetry.lock
api-bootstrapper bootstrap-env --python <version> --path .

# uv backend
rm -rf .venv uv.lock
api-bootstrapper bootstrap-env --python <version> --path . --manager uv
```

---

## 📋 Compatibility Matrix

| Component | Supported versions | Notes |
|-----------|-------------------|-------|
| **Python (CLI requires)** | 3.12+ | Runtime to run the CLI itself |
| **Python (target project)** | 3.10+ | The version you pass via `--python` |
| **pyenv** | 2.3+ | Earlier versions may lack `pyenv prefix` |
| **Poetry** | 1.8+ | Uses `poetry install --no-root` |
| **uv** | 0.4+ | Uses `uv python install` + `uv sync` |
| **macOS** | 12 Monterey+ | Intel & Apple Silicon tested |
| **Linux** | Ubuntu 22.04+, Fedora 38+ | Any modern distro should work |
| **Windows** | Partial | Activation instructions adapted; pyenv-win needed |

> **Note:** Windows support is experimental. Use [pyenv-win](https://github.com/pyenv-win/pyenv-win) and run commands in PowerShell or Git Bash.

---

## �🗺️ Roadmap
- ✅ `bootstrap-env` - pyenv + Poetry + VSCode- ✅ `bootstrap-env --manager uv` - uv + VSCode- ✅ `add-pre-commit` - Git hooks with Ruff and Commitizen
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
