# Parameters and Errors

## Parameters

- `module_or_path` (required): Target code area to receive tests.
- `priority` (optional): `critical` or `normal` to guide depth.
- `include_edge_cases` (optional): Whether to explicitly include boundary scenarios.

## Validation Rules

- Cover at least happy path and one failure path.
- Prefer behavior assertions over implementation detail assertions.
- Keep tests deterministic and readable.

## Common Errors

- Over-mocked tests:
  - Cause: tests assert internals and become brittle.
  - Action: assert externally observable behavior.

- Missing negative scenarios:
  - Cause: only happy path was implemented.
  - Action: add explicit error-path tests.

- Unclear test intent:
  - Cause: ambiguous naming or mixed assertions.
  - Action: split test cases and rename to expected behavior.
