# Parameters Matrix

| Parameter | Required | Default | Values |
| --- | --- | --- | --- |
| `--path` | No | `.` | Existing or new directory |
| `--python` | No | `3.12.12` | Full Python version (`3.12.12`) |
| `--manager` | No | `pyenv` | `pyenv`, `uv` |
| `--install/--no-install` | No | `--install` | Boolean flag |

# Common Errors

- `pyenv not found in PATH`:
  - Cause: manager is `pyenv` and tool is unavailable.
  - Action: install pyenv or use manager `uv`.

- `uv not found in PATH`:
  - Cause: manager is `uv` and tool is unavailable.
  - Action: install uv or use manager `pyenv`.

- `poetry not found in PATH`:
  - Cause: manager `pyenv` path selected but Poetry missing.
  - Action: install Poetry and rerun.

- Existing environment mismatch:
  - Cause: current `.python-version` or `.venv` targets a different version.
  - Action: rerun with expected version and inspect the reported paths.
