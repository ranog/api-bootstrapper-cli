# Parameters Matrix

| Parameter | Required | Default | Values |
| --- | --- | --- | --- |
| `--path` | No | `.` | Existing project directory |
| `--manager` | No | auto-detect | `pyenv`, `uv` |
| `--with-db` | No | `false` | Flag |
| `--create-initial-items` | No | `false` | Flag |
| `--upgrade-head` | No | `false` | Flag |

# Common Errors

- `pyproject.toml not found`:
  - Cause: command run outside a Python project root.
  - Action: run inside a configured project directory.

- Partial Alembic setup detected:
  - Cause: only `alembic.ini` or only `alembic/` exists.
  - Action: fix or remove partial files, then rerun.

- Docker Compose not found:
  - Cause: migration execution requested with DB startup but compose is unavailable.
  - Action: install Docker Compose or run setup-only mode without DB-dependent flags.

- Database did not become ready:
  - Cause: `db` service failed to pass readiness check (`pg_isready`).
  - Action: inspect `docker compose logs db` and retry.

- Alembic revision/upgrade command fails:
  - Cause: dependency/runtime issues or invalid DB connectivity.
  - Action: verify environment and rerun the Alembic command manually.
