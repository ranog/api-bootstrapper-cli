---
name: api-bootstrapper-prepare-task
description: Structure complex implementation requests into clear context, requirements, plan, tests, and validation steps. Use when the task is broad, ambiguous, or high risk.
---
# API Bootstrapper Prepare Task

Use this skill to transform a raw request into an executable and reviewable task brief.

## Inputs

- `objective`: What needs to be delivered.
- `context`: Current system state and constraints.
- `scope`: Optional in/out boundaries.

## Execution Contract

1. Build a structured task brief with:
- Context and motivation.
- Objective and constraints.
- Functional and non-functional requirements.
- Incremental implementation plan.
- Test strategy (happy path, errors, edges).
- Validation commands.

2. Highlight ambiguities and assumptions that can change implementation.

3. Before applying any implementation changes from the prepared task, require explicit confirmation. Show:
- Planned scope.
- Main risks.
- Prompt: `Proceed? (yes/no)`.

4. Report:
- `Task brief`
- `Open questions`
- `Ready-to-execute checklist`

## Output Template

- Context
- Objective
- Requirements
- Architectural constraints
- Test strategy
- Implementation plan
- Validation
