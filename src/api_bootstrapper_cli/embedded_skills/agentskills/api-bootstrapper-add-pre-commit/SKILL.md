---
name: api-bootstrapper-add-pre-commit
description: Configure pre-commit hooks through api-bootstrapper add-pre-commit. Use when the user needs Ruff and Commitizen hooks configured and installed for an existing project.
---
# API Bootstrapper Add Pre Commit

Use this skill to configure `.pre-commit-config.yaml`, dev dependencies, and git hooks.

## Inputs

- `path`: Target project directory. Default to `.`.

## Execution Contract

1. Validate preconditions:
- Target directory is resolvable.
- `api-bootstrapper` is available in PATH.
- `pyproject.toml` exists in target project.

2. Build the command:

```bash
api-bootstrapper add-pre-commit --path <path>
```

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

- `.pre-commit-config.yaml` (create or preserve and update dependencies)
- `pyproject.toml` (dev dependencies)
- lock file updates (`poetry.lock` or `uv.lock`)
- `.git/hooks/` entries when in a git repository

## Command Examples

```bash
api-bootstrapper add-pre-commit --path ./my-api
api-bootstrapper add-pre-commit --path .
```
