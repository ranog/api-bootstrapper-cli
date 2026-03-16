# Parameters and Errors

## Parameters

- `tool_name` (required): New external tool.
- `capability` (required): Intended behavior provided by the tool.
- `scope` (optional): Affected commands/services.

## Validation Rules

- Prefer existing protocol reuse when possible.
- New manager should have a single responsibility.
- Service should orchestrate managers, not execute tool logic directly.

## Common Errors

- Tool logic added directly in CLI command:
  - Cause: architectural boundary violation.
  - Action: move logic to manager/service layers.

- New protocol created without real polymorphism need:
  - Cause: premature abstraction.
  - Action: use existing protocol or concrete implementation first.
