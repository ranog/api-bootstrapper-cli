# Parameters and Errors

## Parameters

- `objective` (required): Desired delivery outcome.
- `context` (required): Existing behavior, architecture, and constraints.
- `scope` (optional): Explicit boundaries for what should not be changed.

## Validation Rules

- The brief must be actionable and testable.
- Requirements should be observable and verifiable.
- Ambiguities must be listed as open questions.

## Common Errors

- Under-specified objective:
  - Cause: vague request without acceptance criteria.
  - Action: define observable outcomes before coding.

- Hidden scope expansion:
  - Cause: inferred requirements not confirmed.
  - Action: isolate assumptions and request confirmation.
