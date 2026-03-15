---
name: api-bootstrapper-bootstrap-env
description: Configure Python runtime, dependency manager environment, and VSCode settings using api-bootstrapper bootstrap-env. Use when a project needs environment setup without full project initialization.
---
# API Bootstrapper Bootstrap Env

Use this skill to configure `.python-version`, `.venv`, `pyproject.toml`, and `.vscode/settings.json`.

## Inputs

- `path`: Target project directory. Default to `.`.
- `python_version`: Python version. Default to `3.12.12`.
- `manager`: `pyenv` or `uv`. Default to `pyenv`.
- `install`: Whether to add/install dependencies. Default to `true`.

## Execution Contract

1. Validate preconditions:
- Target directory is resolvable.
- `api-bootstrapper` is available in PATH.
- Selected manager tool is available.

2. Build one command:

```bash
api-bootstrapper bootstrap-env --path <path> --python <python_version> --manager <manager>
```

Append `--no-install` when `install=false`.

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

- `.python-version`
- `.venv`
- `pyproject.toml` (created or updated)
- `.vscode/settings.json`

## Command Examples

```bash
api-bootstrapper bootstrap-env --path ./my-api --python 3.12.12 --manager pyenv
api-bootstrapper bootstrap-env --path ./my-api --python 3.12.12 --manager uv
api-bootstrapper bootstrap-env --path ./my-api --python 3.12.12 --manager pyenv --no-install
```
