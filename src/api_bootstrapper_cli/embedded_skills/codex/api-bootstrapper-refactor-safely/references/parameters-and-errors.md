# Parameters and Errors

## Parameters

- `target` (required): Refactor scope.
- `goals` (optional): Desired quality outcomes.

## Validation Rules

- No intentional behavior change without explicit approval.
- Refactor should preserve architecture boundaries.
- Validation must include relevant tests before/after changes.

## Common Errors

- Hidden behavior changes:
  - Cause: refactor coupled with logic alteration.
  - Action: split behavior changes into separate task.

- Missing safety net:
  - Cause: insufficient tests around touched logic.
  - Action: add targeted regression tests first.
