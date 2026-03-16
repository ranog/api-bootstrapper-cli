# Parameters and Errors

## Parameters

- `remote` (optional): Remote repository name, defaults to `origin`.
- `default_branch` (optional): Target default branch name (for example `main`).

## Validation Rules

- Current branch must be resolvable via `git branch --show-current`.
- Remote default branch must be resolvable from `refs/remotes/<remote>/HEAD` when not provided.
- Sync must not proceed automatically when worktree is dirty.

## Common Errors

- `fatal: not a git repository`: Current directory is not inside a git repo.
- `fatal: ref refs/remotes/origin/HEAD is not a symbolic ref`: Remote HEAD not configured.
- `fatal: couldn't find remote ref`: Invalid remote or branch.
- `CONFLICT (content)`: Rebase conflicts requiring manual resolution.

## Recovery Guidance

- Ask the user to clean, stash, or commit local changes before sync.
- If remote HEAD is missing, request explicit `default_branch`.
- On conflicts, stop and ask user whether to continue or abort rebase.
