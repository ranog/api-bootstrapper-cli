---
name: api-bootstrapper-debug-issue
description: Debug issues with a reproduce-first, test-first workflow. Use when the user reports a bug or unexpected behavior and wants a safe fix.
---
# API Bootstrapper Debug Issue

Use this skill to investigate bugs with controlled scope and test-first correction.

## Inputs

- `symptom`: User-visible failure description.
- `path`: Optional module or command scope.
- `test_scope`: Preferred level (`unit`, `integration`, or `auto`). Default to `auto`.

## Execution Contract

1. Clarify reproducibility target:
- Failing command, function call, or scenario.
- Expected behavior versus current behavior.

2. Reproduce the issue using the smallest viable command or test.

3. Create or adjust a test that fails for the current bug.

4. Before mutating production code, require explicit confirmation. Show:
- Failing test evidence.
- Planned fix scope.
- Prompt: `Proceed? (yes/no)`.

5. Implement the smallest fix to satisfy the failing test.

6. Validate:
- Failing test now passes.
- Relevant nearby tests still pass.

7. Report:
- `Root cause`
- `Files changed`
- `Tests added/updated`
- `Validation commands and results`

## Command Examples

```bash
pytest tests/unit/path/to/test_file.py -k bug_keyword
pytest tests/integration/path/to/test_flow.py
pytest -k failing_scenario
```
