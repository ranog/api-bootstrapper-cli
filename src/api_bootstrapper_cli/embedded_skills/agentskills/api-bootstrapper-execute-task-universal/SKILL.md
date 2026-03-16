---
name: api-bootstrapper-execute-task-universal
description: Execute a universal workflow for planning, tests, implementation, and validation in one guided sequence. Use when no specialized skill is clearly better.
---
# API Bootstrapper Execute Task Universal

Use this skill as the default end-to-end workflow for generic development tasks.

## Inputs

- `objective`: Task objective.
- `constraints`: Optional architectural or delivery constraints.

## Execution Contract

1. Plan quickly:
- Clarify objective.
- Map impacted modules.
- Define acceptance criteria.

2. Define tests first:
- Happy path.
- Error path.
- Relevant edge cases.

3. Implement minimum viable change.

4. Validate with lint/type/tests as applicable.

5. Before mutating files, require explicit confirmation. Show:
- Planned implementation scope.
- Test plan.
- Prompt: `Proceed? (yes/no)`.

6. Report:
- `Plan executed`
- `Files changed`
- `Tests added/updated`
- `Validation commands/results`
