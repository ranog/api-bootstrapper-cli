# Parameters and Errors

## Parameters

- `objective` (required): Goal to be delivered.
- `constraints` (optional): Architecture, toolchain, or scope constraints.

## Validation Rules

- Plan should precede implementation.
- Testing strategy should be explicit before coding.
- Delivery report should include concrete validation evidence.

## Common Errors

- Jumping straight to implementation:
  - Cause: skipped planning/testing steps.
  - Action: restore workflow order.

- Validation gaps:
  - Cause: no commands run after changes.
  - Action: run and report targeted checks.
