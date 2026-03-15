---
name: api-bootstrapper-init
description: Initialize a Python API project with a single command through api-bootstrapper. Use when the user wants project scaffolding, Python environment setup, Docker files, env template, gitignore updates, and pre-commit hooks in one flow.
---
# API Bootstrapper Init

Use this skill to run the end-to-end `init` command safely.

## Inputs

- `path`: Target project directory. Default to `.`.
- `python_version`: Required Python version (example: `3.12.12`).
- `manager`: `pyenv` or `uv`. Default to `pyenv`.
- `install`: Whether to install dependencies. Default to `true`.

## Execution Contract

1. Validate preconditions before proposing execution:
- Target directory is resolvable.
- `api-bootstrapper` is available in PATH.

2. Build the command:

```bash
api-bootstrapper init --python <python_version> --path <path> --manager <manager>
```

Append `--no-install` when `install=false`.

3. Require explicit confirmation before running any mutating command. Show:
- Planned command.
- Expected artifacts.
- Prompt: `Proceed? (yes/no)`.

4. Run only after explicit `yes`.

5. Report the result in this format:
- `Command executed`: exact command.
- `Artifacts generated/updated`: only observable outputs.
- `Next steps`: short actionable commands.

## Expected Artifacts

- `src/`, `tests/`, `Makefile`
- `.python-version`, `.venv`, `.vscode/settings.json`, `pyproject.toml`
- `Dockerfile`, `docker-compose.yml`
- `.env.example`
- `.pre-commit-config.yaml`

## Command Examples

```bash
api-bootstrapper init --python 3.12.12 --path ./my-api --manager pyenv
api-bootstrapper init --python 3.12.12 --path ./my-api --manager uv
api-bootstrapper init --python 3.12.12 --path ./my-api --manager pyenv --no-install
```
