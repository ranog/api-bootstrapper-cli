# Parameters and Errors

## Parameters

- `base_branch` (optional): Reference branch for comparison.
- `include_risks` (optional): Include risk section in PR draft.

## Validation Rules

- PR content must be derived from observable diff.
- Do not claim tests or impacts not present in artifacts.
- Include validation commands when available.

## Common Errors

- Empty or wrong branch diff:
  - Cause: incorrect base branch.
  - Action: set explicit `base_branch`.

- Overstated impact:
  - Cause: assumptions beyond changed files.
  - Action: state unknowns as open risks.
