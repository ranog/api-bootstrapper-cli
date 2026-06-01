# GitHub Copilot Instructions

## Project Context

This repository is a CLI tool for bootstrapping Python API projects with support for:
- Python runtime setup (`pyenv` or `uv`)
- Dependency management (`Poetry` or `uv`)
- VSCode settings
- Pre-commit hooks
- Docker
- Alembic migrations

Main stack:
- Python 3.12
- Typer
- Rich
- Pytest
- Ruff

## Mandatory Source of Truth

- Always read and follow `AGENTS.md` first.
- Use `docs/` as complementary guidance (`ai-prompts.md`, `ai-workflows.md`, templates).

## Architectural Rules

- Keep CLI commands thin: orchestration only.
- Put business logic in `core/` (managers/services), never inside CLI handlers.
- `commands/` can depend on `core/`; `core/` must not depend on `commands/`.
- Keep shell execution and filesystem IO isolated (`core/shell.py`, `core/files.py`).
- Prefer extending existing managers/services/protocols before creating new abstractions.
- Create new managers/services/protocols only with clear cohesion/testability gains.

### When to create new components

- **New Manager**: only for a new external tool (git, docker, npm...) or a clearly isolated responsibility that does not fit an existing manager.
- **New Service**: only when orchestrating multiple managers in a complex flow that is reusable across commands.
- **New Protocol**: only when there are multiple possible implementations of the same behavior (e.g. pyenv/uv) or to enable testability.
- **Do NOT create** new managers/services/protocols when the feature fits naturally into an existing one or when extraction has no clear cohesion/testability gain.

## What to avoid

- Business logic inside CLI commands.
- Duplication between managers or commands.
- Unnecessary dependencies.
- Premature abstractions.
- Unnecessary complexity or cleverness.
- Renaming public interfaces without explicit warning.
- Removing existing tests without justification.

## Design Principles

- Prefer simplicity over cleverness (KISS/YAGNI).
- Keep high cohesion and low coupling.
- Preserve public contracts unless explicitly requested.
- Prefer composition and dependency injection.
- Prefer `pathlib.Path` over string paths.
- Avoid unnecessary dependencies and overengineering.

## Development Workflow (Expected)

1. Understand the problem and impacted layers.
2. Propose a simple and safe approach before large changes.
3. Define expected behavior and test scenarios.
4. Write or update tests first when applicable (TDD).
5. Implement the smallest change to satisfy tests.
6. Refactor while preserving behavior.
7. Verify if docs must be updated (`README.md`, `AGENTS.md`, relevant docs).
8. Run validation commands (`make format`, `make test`, `make check`).
9. Summarize impact clearly.

## Testing Guidelines

- Use `pytest`. Follow TDD when adding or changing business rules.
- Prefer behavior-focused tests over implementation-detail assertions.
- Name tests as `test_should_*` (e.g. `test_should_create_venv_when_missing`).
- Use AAA (Arrange, Act, Assert) structure, separating steps with **blank lines** instead of comments:

```python
manager = SomeManager()
data = {"key": "value"}

result = manager.process(data)

assert result.success is True
```

- Prioritize unit tests for managers, pure functions and business rules.
- Use integration tests for flows depending on filesystem, shell or external tools.
- CLI commands should be tested for orchestration, not business logic.
- Mirror the structure of `src/` under `tests/` whenever possible.
- Avoid unnecessary mocks; prefer real libs (pytest-mock, pytest-asyncio, testcontainers) for realistic scenarios.

## Response and Change Style

- Respond in Portuguese, concise and didactic.
- Code, identifiers, comments and commit messages must be in **English**.
- Before major edits, explain the plan briefly.
- After changes, always report:
  - files changed
  - tests added/updated
  - suggested validation commands
- Do not rename public interfaces without explicit warning.
- Do not remove existing tests without justification.

## Commit & PR Conventions

- Follow **Conventional Commits** in English, concise, preferably single-sentence.
- Commits must be **atomic and complete**: group related code with its dependencies and tests.
- Integrate frequently (XP/Agile): small, cadenced commits over large batches; keep the codebase always runnable.

## Validation Before Proposing Changes

Before concluding a change, ensure the following commands pass:

```bash
make format     # format with ruff
make test       # run all tests with coverage
make check      # lint + type-check
```

## Useful Paths

- `src/api_bootstrapper_cli/cli.py`
- `src/api_bootstrapper_cli/commands/`
- `src/api_bootstrapper_cli/core/`
- `src/api_bootstrapper_cli/core/protocols.py`
- `src/api_bootstrapper_cli/core/environment_service.py`
- `pyproject.toml`
- `Makefile`
