---
name: api-bootstrapper-sync-branch
description: Safely synchronize the current branch with the remote default branch before creating new commits. Use when the user requests branch sync or asks to update the branch with latest origin changes.
---
# API Bootstrapper Sync Branch

Use this skill to sync the current branch with the remote default branch using a safe, explicit workflow.

## Inputs

- `remote`: Git remote name. Default to `origin`.
- `default_branch`: Optional explicit default branch. If omitted, detect from remote HEAD.

## Execution Contract

1. Identify current branch:

```bash
git branch --show-current
```

2. Check worktree cleanliness:

```bash
git status --porcelain
```

If there are uncommitted changes, do not auto-sync. Ask how to proceed before continuing.

3. Resolve remote default branch when `default_branch` is missing:

```bash
git symbolic-ref --short refs/remotes/<remote>/HEAD
```

4. Before mutating git state, require explicit confirmation and show:
- Current branch.
- Resolved default branch.
- Planned commands.
- Prompt: `Proceed? (yes/no)`.

5. Execute:

```bash
git fetch <remote> --prune
```

If current branch equals default branch:

```bash
git pull --ff-only <remote> <default_branch>
```

Otherwise:

```bash
git rebase <remote>/<default_branch>
```

6. If conflicts happen during rebase:
- List conflicting files.
- Suggest resolution options.
- Ask confirmation before running `git rebase --continue` or `git rebase --abort`.

Never complete conflicting rebases automatically.

7. Report:
- `Command executed`
- `Branch synchronization status`
- `Conflicts detected/resolved`
- `Next steps`

## Command Examples

```bash
git fetch origin --prune
git pull --ff-only origin main
git rebase origin/main
```
