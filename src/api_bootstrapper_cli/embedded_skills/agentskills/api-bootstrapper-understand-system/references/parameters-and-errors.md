# Parameters and Errors

## Parameters

- `target` (required): Command, module, or feature to map.
- `depth` (optional): `high-level` or `detailed`.

## Validation Rules

- Flow should include all relevant layers, not only one file.
- IO points must be explicit when present.
- Impact map should separate direct and indirect effects.

## Common Errors

- Partial flow mapping:
  - Cause: analysis stopped at command layer.
  - Action: continue through services/managers and IO.

- Confusing implementation details with contracts:
  - Cause: no protocol boundary separation.
  - Action: name protocol and concrete implementation explicitly.
