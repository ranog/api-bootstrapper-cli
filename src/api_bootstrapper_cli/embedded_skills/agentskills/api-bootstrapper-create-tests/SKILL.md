---
name: api-bootstrapper-create-tests
description: Create behavior-focused pytest coverage for existing code. Use when the user asks to improve test coverage for modules, flows, or edge cases.
---
# API Bootstrapper Create Tests

Use this skill to close meaningful testing gaps with behavior-first tests.

## Inputs

- `module_or_path`: Target module, package, or command flow.
- `priority`: Risk priority (`critical` or `normal`). Default to `normal`.
- `include_edge_cases`: Whether to include relevant boundary scenarios. Default to `true`.

## Execution Contract

1. Inspect current behavior and existing tests for the target scope.

2. Propose test matrix before coding:
- Happy path.
- Error handling.
- Relevant edge cases.

3. Before creating new tests, require explicit confirmation. Show:
- Proposed scenarios.
- Target files to create/update.
- Prompt: `Proceed? (yes/no)`.

4. Implement tests using pytest with AAA separation through blank lines.

5. Validate by running targeted test commands.

6. Report:
- `Gaps covered`
- `Tests added/updated`
- `Remaining risks`
- `Validation commands`

## Command Examples

```bash
pytest tests/unit/path/to/test_module.py
pytest tests/integration/path/to/test_flow.py -k edge
pytest -k module_name
```
