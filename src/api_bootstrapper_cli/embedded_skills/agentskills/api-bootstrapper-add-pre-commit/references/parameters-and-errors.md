# Parameters Matrix

| Parameter | Required | Default | Values |
| --- | --- | --- | --- |
| `--path` | No | `.` | Existing project directory |

# Common Errors

- `pyproject.toml not found`:
  - Cause: command run outside a Python project root.
  - Action: run in the project folder or create `pyproject.toml` first.

- Dependency install fails (`poetry install` or `uv sync`):
  - Cause: invalid pyproject metadata or dependency conflicts.
  - Action: report command stderr and stop.

- Not a git repository:
  - Cause: `.git/` missing in target path.
  - Action: keep config changes and report manual hook install guidance.
