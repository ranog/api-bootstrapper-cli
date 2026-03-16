# Parameters and Errors

## Parameters

- `target` (optional): `staged`, `branch`, or explicit file-oriented review scope.
- `focus` (optional): `architecture`, `bugs`, `tests`, or `all`.
- `paths` (optional): Explicit file paths to review.

## Validation Rules

- Review output should prioritize behavioral risk over stylistic feedback.
- Every high-severity finding should include concrete impact and file reference.
- Findings should be based on observable code changes, not assumptions.

## Common Errors

- Empty diff for selected scope:
  - Cause: no staged or branch changes to review.
  - Action: ask user to select another scope.

- Missing base branch in branch comparison:
  - Cause: unknown or outdated local reference.
  - Action: ask user for explicit base branch.

- Ambiguous ownership in architectural findings:
  - Cause: insufficient module context.
  - Action: flag as open question instead of asserting a defect.
