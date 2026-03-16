---
name: api-bootstrapper-understand-system
description: Explain architecture and execution flow of an existing feature before changes. Use when the user needs system understanding or impact mapping.
---
# API Bootstrapper Understand System

Use this skill to map how a behavior flows through project layers.

## Inputs

- `target`: Command, module, or feature to analyze.
- `depth`: Optional depth (`high-level` or `detailed`). Default to `detailed`.

## Execution Contract

1. Map execution flow across layers:
- CLI entry point.
- Command orchestration.
- Service coordination.
- Manager responsibilities.
- IO boundaries (filesystem/shell).

2. List contracts/protocols involved and extension points.

3. Identify coupling and likely change impact zones.

4. Before applying any change based on this mapping, require explicit confirmation. Show:
- Impacted modules.
- Main risks.
- Prompt: `Proceed? (yes/no)`.

5. Report:
- `Flow summary`
- `Key files`
- `Impact map`
- `Open questions`
