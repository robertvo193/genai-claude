---
name: git-manager
description: Natural language git control for non-technical managers. Use when managing git repositories including viewing status or history, creating or switching branches, making commits, pushing or pulling changes, merging code, handling pull requests, reverting commits, or summarizing changes. Translates plain English requests into safe git commands with clear explanations.
---

# Git Manager

Natural language git control for non-technical managers. This skill translates plain English requests into safe git commands with clear explanations.

## Quick Start

Simply describe what you want to do in plain English:

- "Show me what's changed" → Shows git status
- "See recent commits" → Shows commit history
- "Create a new branch for the login feature" → Creates feature/login branch
- "Save my changes with message 'Fixed the bug'" → Creates commit
- "Push my changes to the server" → Pushes to remote
- "Review PR #123" → Analyzes pull request
- "Revert to commit abc1234" → Safely reverts changes

## Core Operations

### View Operations

| What You Say | What Happens |
|-------------|--------------|
| "Show me what's changed" | `git status` |
| "Show me the current state" | `git status` |
| "What files are modified?" | `git status` |
| "See recent commits" | `git log --oneline -10` |
| "Show me the last 20 commits" | `git log --oneline -20` |
| "What's in the current branch history?" | `git log --oneline -10` |
| "Show commits from yesterday" | `git log --since="yesterday" --oneline` |
| "See what changed in this commit" | `git show <commit>` |
| "Compare main with my branch" | `git diff main...HEAD` |

### Branch Operations

| What You Say | What Happens |
|-------------|--------------|
| "Create a new branch for login" | `git checkout -b feature/login` |
| "Create branch feature/user-auth" | `git checkout -b feature/user-auth` |
| "Switch to main branch" | `git checkout main` |
| "Go to develop branch" | `git checkout develop` |
| "Show all branches" | `git branch -a` |
| "List my branches" | `git branch -v` |
| "Delete feature branch" | `git branch -d feature/login` |

### Commit Operations

| What You Say | What Happens |
|-------------|--------------|
| "Save my changes" | Stages all and prompts for commit message |
| "Commit my work with message 'Fix login bug'" | `git add -A && git commit -m "Fix login bug"` |
| "Stage the modified files" | `git add -u` |
| "Stage these specific files" | `git add <files>` |
| "Unstage file" | `git restore --staged <file>` |
| "Amend my last commit" | `git commit --amend` |
| "Change the last commit message" | `git commit --amend` |

### Remote Operations

| What You Say | What Happens |
|-------------|--------------|
| "Push my changes" | `git push` |
| "Push to the server" | `git push` |
| "Push this new branch" | `git push -u origin <branch>` |
| "Pull the latest changes" | `git pull` |
| "Get updates from the server" | `git pull` |
| "Fetch all changes" | `git fetch --all` |
| "Sync with the remote" | `git fetch && git pull` |

### Merge Operations

| What You Say | What Happens |
|-------------|--------------|
| "Merge feature into main" | `git checkout main && git merge feature/login` |
| "Combine feature branch with main" | `git checkout main && git merge feature/login` |
| "What will merge?" | Shows potential merge conflicts |
| "I have merge conflicts" | Helps resolve conflicts step-by-step |

## Pull Request Operations

### Review PR with Requirements

When reviewing a PR, you can specify requirements to check:

```
User: "Review PR #123. Check that it has:
       - No breaking changes
       - Tests added
       - Documentation updated
       - Code follows style guidelines"
```

Claude will:
1. Fetch PR details (`gh pr view 123`)
2. Get the diff between branches
3. Analyze for breaking changes (API changes, database migrations, config changes)
4. Check for test files in the changed files list
5. Review documentation changes
6. Check for common style violations
7. Provide a checklist with pass/fail status

Example output:
```
✅ PR Review for #123: "Add user authentication"

Breaking Changes: ✅ None detected
Tests Added: ⚠️  No test files found in changed files
Documentation Updated: ✅ docs/api.md updated
Code Style: ✅ No obvious violations

Overall: Ready with minor concerns
- Recommendation: Add tests before merging
```

### Summarize PR

```
User: "Summarize PR #456"
```

Claude will:
1. Fetch PR details (title, author, description)
2. Get list of changed files
3. Generate a concise summary

Example output:
```
📋 PR #456 Summary: "Fix payment processing timeout"

Author: @developer
Files Changed: 5 (+120, -45 lines)

Key Modifications:
- Increased API timeout from 30s to 60s
- Added retry logic for failed requests
- Updated error messages for better debugging

Risk Level: 🟡 Medium
```

### PR Diff View

| What You Say | What Happens |
|-------------|--------------|
| "Show me what changed in PR #123" | `gh pr view 123 --json files,body` |
| "Compare PR #123 to main" | `gh pr diff 123` |
| "What files are in PR #456?" | `gh pr view 456 --json files` |
| "Check PR status" | `gh pr view --json state,mergeable` |

## Commit Revert Operations

### Revert to Specific Commit

**WARNING**: Revert operations are destructive. Always show what will be lost before executing.

```
User: "Revert to commit abc1234"
```

Claude will:
1. Show commit details (`git show abc1234`)
2. Show what commits will be removed
3. Calculate files affected
4. Ask for explicit confirmation

Example output:
```
⚠️  REVERT OPERATION

Commit to revert: abc1234 - "Fix authentication bug"
Author: John Doe (2 days ago)

This will remove:
- 3 commits after abc1234
- Changes to 12 files
- ~150 lines of code

Files that will be affected:
  src/auth/login.js (revert to previous version)
  src/auth/session.js (revert to previous version)
  tests/auth.test.js (will be removed)

Continue? (yes/no)
```

### Safe Revert Methods

| Method | When to Use | Command |
|--------|------------|---------|
| **Revert (undo)** | Keep history, create new commit to undo | `git revert <commit>` |
| **Reset (hard)** | Discard everything after commit | `git reset --hard <commit>` |
| **Reset (soft)** | Keep changes, move HEAD back | `git reset --soft <commit>` |

### Common Revert Scenarios

| What You Say | Recommended Action |
|-------------|-------------------|
| "Undo the last commit" | `git revert HEAD` (safe) or `git reset --soft HEAD~1` |
| "Go back to yesterday's version" | `git log --since="2 days ago"` to find commit, then `git revert` |
| "Discard all recent changes" | Warning: Use `git reset --hard` only if certain |
| "I made a mistake, take me back" | Show options, ask which method to use |

## Safety Checks

### Always Confirm Before Destructive Operations

Ask for explicit confirmation before:

- ✗ Force push (`git push --force`)
- ✗ Delete branches (`git branch -D`)
- ✗ Hard reset (`git reset --hard`)
- ✗ Discard uncommitted changes
- ✗ Revert commits (shows what will be lost)
- ✗ Remove remote branches (`git push origin --delete`)

### Current State Awareness

Before any operation, always show:
- Current branch
- Current commit
- Working directory status (clean/dirty)
- Remote status (ahead/behind)

Example:
```
📍 Current State:
Branch: feature/login (3 commits ahead of origin)
Last commit: abc1234 "Fix authentication bug"
Status: 2 files modified, 5 files staged
```

## Common Workflows

### Start a New Feature

```
1. Update from main: "Pull the latest changes"
2. Create branch: "Create a branch feature/user-profile"
3. Work on changes
4. Save changes: "Commit my work with message 'Add user profile page'"
5. Push: "Push my new branch"
6. Create PR on GitHub
```

### Merge to Main

```
1. Switch to main: "Switch to main branch"
2. Update: "Pull the latest changes"
3. Merge: "Merge feature/user-profile into main"
4. Push: "Push to main"
```

### Release a Version

```
1. Switch to main: "Switch to main"
2. Update: "Pull latest changes"
3. Tag: "Create tag v1.2.3 with message 'Release version 1.2.3'"
4. Push tag: "Push tags to remote"
```

### Fix a Mistake

```
1. Undo last commit: "Revert the last commit"
2. Discard changes: "Discard my uncommitted changes"
3. Reset to safe point: "Reset to commit abc1234"
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "I see 'detached HEAD'" | "Switch to a branch" |
| "Merge conflicts occurred" | "Show me the conflicts" → help resolve |
| "Remote rejected my push" | "Pull first, then push" |
| "File is locked" | "Check if file is open in another program" |
| "Commit is not found" | "Check the commit hash, or show recent commits" |

### Error Messages Explained

| Git Error | Plain English |
|-----------|--------------|
| "fatal: not a git repository" | "This folder is not a git project" |
| "error: failed to push" | "Cannot send changes - try pulling first" |
| "CONFLICT (content)" | "Two versions have different content - needs manual fix" |
| "Your branch is ahead of 'origin/main'" | "You have changes not yet pushed to the server" |

## Resources

### Git Command Reference

For detailed git command information, see [references/commands.md](references/commands.md)

### Git Workflows

For common git workflow patterns, see [references/workflows.md](references/workflows.md)

### PR Operations

For detailed PR review patterns, see [references/pr-workflows.md](references/pr-workflows.md)
