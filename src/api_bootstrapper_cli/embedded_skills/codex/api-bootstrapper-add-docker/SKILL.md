---
name: api-bootstrapper-add-docker
description: Add Docker support with api-bootstrapper add-docker. Use when the user wants a Dockerfile configured for a Python API project without running full initialization.
---
# API Bootstrapper Add Docker

Use this skill to create a project Dockerfile with a selected Python image version.

## Inputs

- `path`: Target project directory. Default to `.`.
- `python_version`: Python version used by Docker image. Default to `3.13`.

## Execution Contract

1. Validate preconditions:
- Target directory is resolvable.
- `api-bootstrapper` is available in PATH.

2. Build the command:

```bash
api-bootstrapper add-docker --path <path> --python <python_version>
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

- `Dockerfile`

## Command Examples

```bash
api-bootstrapper add-docker --path ./my-api --python 3.13
api-bootstrapper add-docker --path ./my-api --python 3.12
```
