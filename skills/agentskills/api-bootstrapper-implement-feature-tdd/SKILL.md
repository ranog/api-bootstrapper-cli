---
name: api-bootstrapper-implement-feature-tdd
description: Implement new functionality through a test-first workflow with small, safe changes. Use when the user asks for feature delivery with TDD.
---
# API Bootstrapper Implement Feature TDD

Use this skill to deliver features with incremental, behavior-driven steps.

## Inputs

- `objective`: Feature to implement.
- `scope`: Target modules and boundaries.
- `test_level`: Preferred level (`unit`, `integration`, or mixed). Default to mixed.

## Execution Contract

1. Define expected behavior and acceptance criteria.

2. Propose test scenarios first:
- Happy path.
- Error path.
- Relevant edge cases.

3. Write failing tests before implementation.

4. Before mutating production code, require explicit confirmation. Show:
- Failing tests summary.
- Planned minimal implementation.
- Prompt: `Proceed? (yes/no)`.

5. Implement the smallest change to make tests pass.

6. Refactor safely without changing behavior.

7. Report:
- `Files changed`
- `Tests added/updated`
- `Validation commands and results`
