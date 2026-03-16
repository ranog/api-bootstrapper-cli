---
name: api-bootstrapper-prepare-pr
description: Prepare a pull request summary from branch changes with objective, approach, impact, and validation evidence. Use when finalizing a feature branch.
---
# API Bootstrapper Prepare PR

Use this skill to generate a factual PR description from real branch changes.

## Inputs

- `base_branch`: Base for diff comparison. Default to project default branch.
- `include_risks`: Include explicit risk section. Default to `true`.

## Execution Contract

1. Collect diff context:
- Branch name.
- Changed files.
- Main change groups.

2. Build PR summary sections:
- Objective.
- Approach.
- Modules changed.
- Architectural impact.
- Tests added/updated.
- Validation commands/results.

3. Before creating commit or PR side effects, require explicit confirmation. Show:
- Proposed summary.
- Next command suggestions.
- Prompt: `Proceed? (yes/no)`.

4. Report:
- `PR draft`
- `Open risks`
- `Checklist`

## Command Examples

```bash
git branch --show-current
git diff --name-only origin/main...HEAD
git log --oneline origin/main..HEAD
```
