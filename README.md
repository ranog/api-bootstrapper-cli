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

### Bootstrap development environment

Sets up a complete Python development environment with pyenv, Poetry, and VSCode configuration.

```bash
# In an existing project with pyproject.toml
api-bootstrapper bootstrap-env --python 3.12.12

# In a new/empty directory
api-bootstrapper bootstrap-env --python 3.12.12 --path ./my-project

# Skip dependency installation
api-bootstrapper bootstrap-env --python 3.12.12 --no-install
```

This will:

- Install and configure the specified Python version via pyenv
- Set local Python version (`.python-version`)
- Configure Poetry with in-project virtualenv (if `pyproject.toml` exists)
- Create/install Poetry environment
- Generate VSCode settings with Python interpreter (relative paths)
- Enable pytest by default

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
