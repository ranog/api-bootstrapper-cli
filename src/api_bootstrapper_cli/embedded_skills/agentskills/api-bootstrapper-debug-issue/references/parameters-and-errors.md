# Parameters and Errors

## Parameters

- `symptom` (required): Observable bug or failure description.
- `path` (optional): Module, package, or file path to narrow investigation.
- `test_scope` (optional): `unit`, `integration`, or `auto`.

## Validation Rules

- Do not claim the bug is fixed without a failing-then-passing test trail.
- Keep fix scope minimal and directly connected to reproduced behavior.
- Prefer deterministic reproduction over flaky environment-dependent checks.

## Common Errors

- Bug not reproducible locally:
  - Cause: missing setup, environment mismatch, or unclear symptom.
  - Action: request reproducible steps and environment details.

- No test layer available for reported behavior:
  - Cause: gap in current test suite architecture.
  - Action: create the smallest realistic test harness in closest layer.

- False fix by over-mocking:
  - Cause: test isolates away real failing path.
  - Action: reduce mocks and assert observable behavior.
