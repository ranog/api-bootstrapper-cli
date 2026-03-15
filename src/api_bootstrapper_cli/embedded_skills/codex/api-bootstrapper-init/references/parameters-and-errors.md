# Parameters Matrix

| Parameter | Required | Default | Values |
| --- | --- | --- | --- |
| `--python` | Yes | n/a | Full Python version (`3.12.12`) |
| `--path` | No | `.` | Existing or new directory |
| `--manager` | No | `pyenv` | `pyenv`, `uv` |
| `--install/--no-install` | No | `--install` | Boolean flag |

# Common Errors

- `pyenv not found in PATH`:
  - Cause: `--manager pyenv` without pyenv installed.
  - Action: install pyenv or switch to `--manager uv`.

- `uv not found in PATH`:
  - Cause: `--manager uv` without uv installed.
  - Action: install uv or switch to `--manager pyenv`.

- Dependency manager not found (`poetry` or `uv`):
  - Cause: environment manager is available but dependency manager is missing.
  - Action: install required dependency manager and rerun.

- Command exits non-zero during setup:
  - Cause: filesystem permission issues or project misconfiguration.
  - Action: report stderr summary and stop without retry loops.
