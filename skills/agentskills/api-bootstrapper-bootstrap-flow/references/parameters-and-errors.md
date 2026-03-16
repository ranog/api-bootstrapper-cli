# Decision Matrix

| Scenario | Recommended Command Path |
| --- | --- |
| New project from scratch | `init` |
| Existing project, env only | `bootstrap-env` |
| Existing project, code quality hooks | `add-pre-commit` |
| Existing project, containerization only | `add-docker` |
| Database migrations setup request | `add-alembic` |
| Database migrations setup + execution | `add-alembic --with-db --create-initial-items --upgrade-head` |

# Sequencing Matrix

| Step | Command | Expected Output |
| --- | --- | --- |
| 1 | `bootstrap-env` or `init` | Python environment configured |
| 2 | `add-pre-commit` | Hook config and dependencies updated |
| 3 | `add-docker` (optional) | Dockerfile created (or skip if exists) |
| 4 | `add-alembic` (optional) | Alembic configuration scaffolded |
| 5 | `add-alembic --with-db --create-initial-items --upgrade-head` (optional) | DB ready + initial migration generated/applied |

# Common Errors

- Partial setup after interruption:
  - Cause: command flow stopped after a failed step.
  - Action: report completed steps and suggest safe rerun from next missing step.

- Manager mismatch (`pyenv` vs `uv`):
  - Cause: requested manager differs from project metadata.
  - Action: keep requested manager explicit and report any command-level failure.
