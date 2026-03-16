---
name: api-bootstrapper-review-code
description: Perform technical code review focused on risks, regressions, and missing tests. Use when the user asks for a review before commit or pull request.
---
# API Bootstrapper Review Code

Use this skill to run a pragmatic review focused on behavior risk and test gaps.

## Inputs

- `target`: Review scope (`staged`, `branch`, or explicit files). Default to `staged`.
- `focus`: Review focus (`architecture`, `bugs`, `tests`, or `all`). Default to `all`.
- `paths`: Optional explicit file list to narrow the review.

## Execution Contract

1. Collect review context:
- Current branch.
- Effective scope (`staged`, branch diff, or selected files).
- Changed files list.

2. Analyze findings in this priority order:
- Bugs and behavioral regressions.
- Architectural or responsibility violations.
- Missing or weak tests.
- Maintainability risks.

3. Present findings with:
- Severity (`high`, `medium`, `low`).
- File references.
- Observable impact.
- Minimal fix suggestion.

4. Before applying any code changes from the review, require explicit confirmation. Show:
- Proposed changes.
- Expected impact.
- Prompt: `Proceed? (yes/no)`.

5. Report:
- `Findings`
- `Open questions/assumptions`
- `Suggested validation commands`

## Command Examples

```bash
git branch --show-current
git diff --staged --name-only
git diff --name-only
git diff origin/main...HEAD
```
