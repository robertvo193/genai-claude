# Git Commands Reference

Quick reference for git commands used by the git-manager skill.

## Status & Information

| Command | Description | Use When |
|---------|-------------|----------|
| `git status` | Show working directory status | User wants to see what changed |
| `git log --oneline -n` | Show last n commits | User wants commit history |
| `git log --since="date"` | Show commits since date | User wants history by date |
| `git show <commit>` | Show commit details | User wants to see specific commit |
| `git diff` | Show unstaged changes | User wants to see what's modified |
| `git diff --staged` | Show staged changes | User wants to see staged modifications |
| `git diff <branch1> <branch2>` | Compare branches | User wants to see branch differences |

## Branch Operations

| Command | Description | Use When |
|---------|-------------|----------|
| `git branch` | List branches | User wants to see all branches |
| `git branch -a` | List all branches (remote) | User wants to see remote branches |
| `git checkout <branch>` | Switch to branch | User wants to change branches |
| `git checkout -b <branch>` | Create and switch to branch | User wants to start new feature |
| `git branch -d <branch>` | Delete branch | User wants to remove branch (safe) |
| `git branch -D <branch>` | Force delete branch | User wants to remove branch (force - require confirmation) |

## Commit Operations

| Command | Description | Use When |
|---------|-------------|----------|
| `git add <file>` | Stage file | User wants to stage specific file |
| `git add -A` | Stage all changes | User wants to stage everything |
| `git add -u` | Stage modified/deleted | User wants to stage changes only |
| `git commit -m "msg"` | Commit with message | User wants to save changes |
| `git commit --amend` | Edit last commit | User wants to change last commit |
| `git reset HEAD <file>` | Unstage file | User wants to unstage changes |

## Remote Operations

| Command | Description | Use When |
|---------|-------------|----------|
| `git remote -v` | Show remotes | User wants to see configured remotes |
| `git fetch` | Fetch from remote | User wants to get updates |
| `git pull` | Fetch and merge | User wants to sync with remote |
| `git push` | Push to remote | User wants to send changes |
| `git push -u origin <branch>` | Push and set upstream | User wants to push new branch |
| `git push --force` | Force push | DANGEROUS - require confirmation |

## Merge & Rebase

| Command | Description | Use When |
|---------|-------------|----------|
| `git merge <branch>` | Merge branch | User wants to combine branches |
| `git merge --no-ff <branch>` | Merge with commit | User wants to preserve history |
| `git rebase <branch>` | Rebase onto branch | User wants to rebase history |
| `git mergetool` | Open merge tool | User needs help resolving conflicts |

## Reset & Revert

| Command | Description | Use When |
|---------|-------------|----------|
| `git revert <commit>` | Revert commit (safe) | User wants to undo commit, keep history |
| `git reset --soft <commit>` | Soft reset | User wants to keep changes, move HEAD |
| `git reset --mixed <commit>` | Mixed reset (default) | User wants to unstage changes |
| `git reset --hard <commit>` | Hard reset | DANGEROUS - discard all changes |
| `git clean -fd` | Remove untracked files | DANGEROUS - clean workspace |

## Tag Operations

| Command | Description | Use When |
|---------|-------------|----------|
| `git tag` | List tags | User wants to see tags |
| `git tag <name>` | Create tag | User wants to tag current commit |
| `git tag -a <name> -m "msg"` | Annotated tag | User wants to create tag with message |
| `git push origin <tag>` | Push tag | User wants to send tag to remote |
| `git push --tags` | Push all tags | User wants to send all tags |

## Stash Operations

| Command | Description | Use When |
|---------|-------------|----------|
| `git stash` | Stash changes | User wants to save work temporarily |
| `git stash list` | List stashes | User wants to see stashed work |
| `git stash pop` | Apply and remove stash | User wants to restore work |
| `git stash drop` | Remove stash | User wants to discard stash |

## Common Aliases for Users

For non-technical users, explain these as:

| User Request | Real Command | Friendly Explanation |
|--------------|--------------|---------------------|
| "Show changes" | `git status` | Shows which files are modified |
| "Save work" | `git commit` | Takes a snapshot of your work |
| "Send to server" | `git push` | Uploads your work to the shared repository |
| "Get updates" | `git pull` | Downloads latest work from the repository |
| "Go to branch" | `git checkout` | Switches to a different version of the code |
