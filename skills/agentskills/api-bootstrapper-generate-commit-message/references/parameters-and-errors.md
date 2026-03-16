# Parameters and Errors

## Parameters

- `scope_fallback` (optional): Scope used when no task key is found, defaults to `cli`.
- `prefer_staged` (optional): Analyze staged diff first, defaults to `true`.

## Validation Rules

- Branch name should be available to detect a task code when present.
- Commit message must be derived from the observed diff only.
- Commit type should reflect dominant impact in changed files.

## Common Errors

- `fatal: not a git repository`: Current path is outside a git repository.
- Empty staged and unstaged diffs: no changes available for message generation.
- Ambiguous mixed diff (for example docs + refactor + tests): requires user confirmation for split commits.

## Recovery Guidance

- Ask user to stage intended files first for more accurate message generation.
- If no changes are detected, ask user what should be committed.
- When multiple contexts are mixed, recommend splitting into atomic commits.
