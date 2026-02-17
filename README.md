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

### Add Alembic support to an existing API project

```bash
api-bootstrapper add-alembic --path .
```

This will:

- Add Alembic dependency
- Create migrations folder
- Inject Makefile targets
- Wire Alembic to your project config

---

## Roadmap

- ✅ add-alembic
- ⬜ bootstrap-env (pyenv + poetry)
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
