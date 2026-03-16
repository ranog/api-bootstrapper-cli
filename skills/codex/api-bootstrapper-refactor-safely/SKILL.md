---
name: api-bootstrapper-refactor-safely
description: Refactor existing code while preserving behavior and architectural boundaries. Use when the user asks to improve code quality without functional change.
---
# API Bootstrapper Refactor Safely

Use this skill to improve structure, readability, and maintainability with low regression risk.

## Inputs

- `target`: Module or flow to refactor.
- `goals`: Optional refactor goals (clarity, duplication removal, cohesion).

## Execution Contract

1. Define behavior-preservation constraints.

2. Map current responsibilities and identify refactor opportunities.

3. Ensure tests exist or add safety tests before deep refactor.

4. Before applying refactor edits, require explicit confirmation. Show:
- Planned structural changes.
- Behavior-preservation checks.
- Prompt: `Proceed? (yes/no)`.

5. Implement incremental refactor with minimal blast radius.

6. Validate unchanged behavior through targeted tests.

7. Report:
- `Refactor summary`
- `Behavior guarantees`
- `Validation commands`
