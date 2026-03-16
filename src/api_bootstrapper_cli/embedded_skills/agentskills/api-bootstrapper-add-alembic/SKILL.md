---
name: api-bootstrapper-add-alembic
description: Configure Alembic migrations with api-bootstrapper add-alembic. Use when the user wants migration scaffolding, optional automatic DB startup, optional initial Item migration generation, and optional upgrade to head.
---
# API Bootstrapper Add Alembic

Use this skill to initialize and configure Alembic for the target project.

## Inputs

- `path`: Target project directory. Default to `.`.
- `manager`: Optional manager backend (`pyenv` or `uv`). Auto-detected when omitted.
- `with_db`: Start PostgreSQL `db` service via docker compose before running migrations.
- `create_initial_items`: Generate `create items table` revision with autogenerate.
- `upgrade_head`: Apply migrations with `alembic upgrade head`.

## Execution Contract

1. Validate preconditions:
- Target directory is resolvable.
- `api-bootstrapper` is available in PATH.
- `pyproject.toml` exists in target project.

2. Build the command:

```bash
api-bootstrapper add-alembic --path <path>
```

Append optional flags when requested:
- `--manager <manager>`
- `--with-db`
- `--create-initial-items`
- `--upgrade-head`

3. Require explicit confirmation before mutating files. Show:
- Planned command.
- Expected artifacts.
- Prompt: `Proceed? (yes/no)`.

4. Execute only after explicit `yes`.

5. Report:
- `Command executed`
- `Artifacts generated/updated`
- `Next steps`

## Expected Artifacts

- `alembic.ini`
- `alembic/env.py`
- `alembic/versions/`
- revision script under `alembic/versions/` when `--create-initial-items` is used

## Command Examples

```bash
api-bootstrapper add-alembic --path ./my-api
api-bootstrapper add-alembic --path ./my-api --with-db --create-initial-items --upgrade-head
api-bootstrapper add-alembic --path ./my-api --manager uv --with-db --upgrade-head
```
