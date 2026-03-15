# Parameters Matrix

| Parameter | Required | Default | Values |
| --- | --- | --- | --- |
| `--path` | No | `.` | Existing project directory |
| `--python` | No | `3.13` | Major/minor Python version (`3.13`, `3.12`) |

# Common Errors

- Dockerfile already exists:
  - Cause: target already contains `Dockerfile`.
  - Action: command skips overwrite and returns informational message.

- Invalid path:
  - Cause: non-existent or non-directory target.
  - Action: resolve path issues before rerun.
