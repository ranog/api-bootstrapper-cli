---
name: api-bootstrapper-add-alembic
description: Handle Alembic setup requests through api-bootstrapper add-alembic while the command is still a placeholder. Use when users ask for migrations setup and need clear status plus next actions.
---
# API Bootstrapper Add Alembic

Use this skill as a controlled placeholder until the command is fully implemented.

## Current Status

- `api-bootstrapper add-alembic` is currently unavailable as a full implementation.
- The current CLI output is `add-alembic: TODO`.

## Inputs

- No command options are currently supported.

## Execution Contract

1. Validate preconditions:
- `api-bootstrapper` is available in PATH.

2. Build the command:

```bash
api-bootstrapper add-alembic
```

3. Require explicit confirmation before execution because command invocation is still mutating-capable by design. Show:
- Planned command.
- Current placeholder status.
- Prompt: `Proceed? (yes/no)`.

4. Execute only after explicit `yes`.

5. Report:
- `Command executed`
- `Observed output` (expected placeholder: `add-alembic: TODO`)
- `Next steps`

## Expected Behavior After Future Implementation

- Generate Alembic configuration and migration scaffolding.
- Preserve compatibility with existing project layout.
- Provide deterministic next commands for migration lifecycle.
