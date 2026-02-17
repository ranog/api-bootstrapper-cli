# api-bootstrapper-cli

A modular and extensible CLI for bootstrapping Python API projects with opinionated platform defaults.

Designed for teams that want:

- Consistent project structure
- Deterministic environments
- Incremental feature adoption
- Clean architecture foundations

---

## Philosophy

Instead of generating a huge opinionated template, `api-bootstrapper-cli` allows you to:

- Initialize a minimal project
- Add platform features incrementally
- Keep idempotency
- Avoid breaking existing setups

It follows a feature-based extensible architecture.

---

## Installation (local development)

```bash
git clone https://github.com/ranog/api-bootstrapper-cli
cd api-bootstrapper-cli
poetry install
```

Run:

```bash
poetry run api-bootstrapper --help
```

---

## Usage

### Minimum Requirements

The target directory needs:
- **Nothing** - Can be completely empty (will setup pyenv + VSCode only)
- **Or** `pyproject.toml` - For full Poetry environment setup

### pyproject.toml Format (if using Poetry)

For projects using Poetry, ensure your `pyproject.toml` follows the correct format:

```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = ""
authors = ["Your Name <your.email@example.com>"]
package-mode = false  # Required for application projects (not libraries)

[tool.poetry.dependencies]
python = "^3.12"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

**Important:**
- Use `[tool.poetry]` section (not `[project]`)
- Set `package-mode = false` for API/application projects that aren't installable packages
- Without these settings, `poetry install` will fail

### Bootstrap development environment

Sets up a complete Python development environment with pyenv, Poetry, and VSCode configuration.

```bash
# In an existing project with pyproject.toml
api-bootstrapper bootstrap-env --python 3.12.12

# In a new/empty directory (will skip Poetry setup)
api-bootstrapper bootstrap-env --python 3.12.12 --path ./my-project

# Skip dependency installation
api-bootstrapper bootstrap-env --python 3.12.12 --no-install
```

**What it does:**

With `pyproject.toml`:
- Install and configure the specified Python version via pyenv
- Set local Python version (`.python-version`)
- Configure Poetry with in-project virtualenv
- Create/install Poetry environment (`.venv`)
- Install dependencies from `pyproject.toml`
- Generate VSCode settings with Python interpreter (relative paths: `.venv/bin/python`)
- Enable pytest by default

Without `pyproject.toml`:
- Install and configure the specified Python version via pyenv
- Set local Python version (`.python-version`)
- Generate VSCode settings with Python interpreter
- Skip Poetry setup (you can run `poetry init` later)

### Add Alembic support (planned)

```bash
api-bootstrapper add-alembic --path .
```

_Note: This command is currently a placeholder for future implementation._

---

## Roadmap

- ✅ bootstrap-env (pyenv + poetry + vscode)
- ⬜ add-alembic
- ⬜ add-docker-postgres
- ⬜ add-ruff
- ⬜ add-mypy
- ⬜ add-pre-commit
- ⬜ add-healthcheck
- ⬜ profiles (fastapi-postgres-clean-arch)

---

## Contributing

Contributions are welcome.

Please:

- Keep features modular
- Ensure idempotency
- Add tests when possible

---

## License

MIT License © 2026 João Paulo Ramos Nogueira

---
