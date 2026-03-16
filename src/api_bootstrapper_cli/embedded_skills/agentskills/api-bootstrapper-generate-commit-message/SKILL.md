---
name: api-bootstrapper-generate-commit-message
description: Generate commit messages following Conventional Commits from staged or unstaged diffs. Use when the user asks for a commit title aligned with branch task code and real change scope.
---
# API Bootstrapper Generate Commit Message

Use this skill to produce accurate, concise commit messages from the actual git diff.

## Inputs

- `scope_fallback`: Scope to use when no task key is found. Default to `cli`.
- `prefer_staged`: Whether to prioritize staged changes. Default to `true`.

## Execution Contract

1. Identify branch:

```bash
git branch --show-current
```

2. Extract task code when present using pattern `[A-Z]+-[0-9]+`.

3. Analyze diff in this order:

```bash
git diff --staged --name-only
git diff --staged
```

If staged diff is empty, then use:

```bash
git diff --name-only
git diff
```

4. Determine dominant change type from observable diff:
- `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `build`, `ci`.

Never force `feat` when the diff indicates another type.

5. Build message format:
- With task code: `<type>(<TASK-CODE>): short message in English`
- Without task code: `<type>(<scope_fallback>): short message in English`

6. Enforce message quality:
- Imperative mood.
- Concise and factual.
- No invented changes.

7. Before running `git commit`, require explicit confirmation and show:
- Selected type and scope.
- Proposed message.
- Prompt: `Proceed? (yes/no)`.

8. Report:
- `Diff analyzed`
- `Proposed commit message`
- `Scope rationale`
- `Next steps`

## Command Examples

```bash
git diff --staged --name-only
git diff --staged
git diff --name-only
git diff
```
