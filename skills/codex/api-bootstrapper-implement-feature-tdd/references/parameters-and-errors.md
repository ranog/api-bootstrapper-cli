# Parameters and Errors

## Parameters

- `objective` (required): Feature behavior to deliver.
- `scope` (required): Modules/files in scope.
- `test_level` (optional): `unit`, `integration`, or mixed.

## Validation Rules

- Tests must be written before implementation changes.
- At least one failing test must demonstrate missing behavior.
- Final output must confirm tests passing after implementation.

## Common Errors

- Test-after-code workflow:
  - Cause: implementation started before failing test.
  - Action: revert to test-first sequence.

- Oversized implementation step:
  - Cause: multiple behavioral changes in one pass.
  - Action: split into smaller TDD iterations.
