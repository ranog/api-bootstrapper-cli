---
name: api-bootstrapper-add-tool-support
description: Add support for a new external tool using manager/service architecture boundaries. Use when integrating new tooling into bootstrap workflows.
---
# API Bootstrapper Add Tool Support

Use this skill to integrate new tools without breaking architectural contracts.

## Inputs

- `tool_name`: External tool to integrate.
- `capability`: What behavior this tool should provide.
- `scope`: Commands/services affected.

## Execution Contract

1. Evaluate reuse before creation:
- Check existing protocols.
- Decide whether new manager is required.
- Keep CLI thin and orchestration-focused.

2. Define integration design:
- Manager responsibilities.
- Service orchestration updates.
- IO boundaries.

3. Propose test plan:
- Manager unit tests.
- Service orchestration tests.
- Edge/error cases.

4. Before mutating implementation, require explicit confirmation. Show:
- Proposed architecture changes.
- Modules to be created/updated.
- Prompt: `Proceed? (yes/no)`.

5. Implement minimal integration and tests.

6. Report:
- `Architecture decision`
- `Files changed`
- `Tests added/updated`
- `Validation commands`
