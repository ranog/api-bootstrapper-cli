---
name: api-bootstrapper-bootstrap-flow
description: Orchestrate the complete api-bootstrapper workflow across init, bootstrap-env, add-pre-commit, add-docker, and add-alembic placeholder handling. Use when the user asks for a full project bootstrap strategy or sequenced execution.
---
# API Bootstrapper Bootstrap Flow

Use this skill to coordinate a full bootstrap plan across command-level skills.

## Inputs

- `path`: Target project directory.
- `python_version`: Desired Python version.
- `manager`: `pyenv` or `uv`.
- `install`: Whether to install dependencies.
- `include_docker`: Whether Docker setup should be applied (for existing projects).
- `include_alembic`: Whether placeholder command should be invoked for tracking.

## Orchestration Rules

1. Prefer one-command setup for new projects:

```bash
api-bootstrapper init --python <python_version> --path <path> --manager <manager>
```

Append `--no-install` when `install=false`.

2. For existing projects, run step-by-step:

```bash
api-bootstrapper bootstrap-env --path <path> --python <python_version> --manager <manager>
api-bootstrapper add-pre-commit --path <path>
api-bootstrapper add-docker --path <path> --python <docker_python_version>
api-bootstrapper add-alembic
```

Run Docker and Alembic commands only when requested.

## Execution Contract

1. Validate preconditions before each step:
- Target directory is resolvable.
- `api-bootstrapper` is available in PATH.
- Selected manager dependencies are installed.

2. Before every mutating command, require explicit confirmation. Show:
- Step number and purpose.
- Planned command.
- Expected artifacts for that step.
- Prompt: `Proceed? (yes/no)`.

3. Execute only after explicit `yes` at each step.

4. Report a consolidated summary:
- `Commands executed`
- `Artifacts generated/updated`
- `Deferred/blocked steps`
- `Next steps`

## Notes

- `add-alembic` is currently placeholder-only and should be reported as unavailable after execution.
- Keep command output factual; do not claim features that are not implemented.
