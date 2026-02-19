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
api-bootstrapper <TAB>           # Shows: bootstrap-env, add-alembic
api-bootstrapper bootstrap-env --<TAB>  # Shows: --path, --python, --install
```

---

## 🚀 Quick Start

Bootstrap a new Python project in seconds:

```bash
# Create and setup a new project
api-bootstrapper bootstrap-env --python 3.12.12 --path ./my-project

# Navigate to project and activate environment
cd my-project
source .venv/bin/activate

# Start coding!
python --version  # Python 3.12.12
poetry --version  # Poetry (version 2.3.2)
```

> **Note:** The CLI automatically detects paths with spaces or accents (e.g., `/Área de Trabalho/project`) and shows `source $(poetry env info --path)/bin/activate` which handles special characters reliably.

---

## 📖 Usage

### Prerequisites

**For using the CLI:**
- [pipx](https://pipx.pypa.io/) (recommended) or pip
- macOS or Linux  
- [pyenv](https://github.com/pyenv/pyenv) installed

**Target project can be:**
- **Empty directory** - Will create a minimal `pyproject.toml` and setup full environment
- **Existing project** - With `pyproject.toml` already present

### bootstrap-env

Sets up a complete Python development environment with pyenv, Poetry, and VSCode configuration.

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

---

## 📁 Project Structure

After running `bootstrap-env`, your project will have:

```
my-project/
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
python = "^3.12"  # Matches your --python version

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

**Important:**
- Python version constraint automatically matches your specified version
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

- ✅ `bootstrap-env` - pyenv + Poetry + VSCode
- ⬜ `add-alembic` - Database migrations
- ⬜ `add-docker-postgres` - Local database
- ⬜ `add-ruff` - Linting configuration
- ⬜ `add-mypy` - Type checking
- ⬜ `add-pre-commit` - Git hooks
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
