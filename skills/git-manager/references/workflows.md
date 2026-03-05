# Git Workflows Guide

Common git workflows for different development scenarios.

## Feature Branch Workflow

The most common workflow for team development.

```
main (production)
  ↓
  develop (integration)
    ↓
    feature/xxx (new feature)
```

### Step-by-Step for Non-Technical Users

1. **Start New Feature**
   - User: "Update from develop branch"
   - Git: `git checkout develop && git pull`
   - User: "Create a new branch for [feature name]"
   - Git: `git checkout -b feature/[name]`

2. **Work on Feature**
   - Make changes to files
   - User: "Save my work with message '[description]'"
   - Git: `git add -A && git commit -m "[description]"`

3. **Share Work**
   - User: "Push my changes"
   - Git: `git push -u origin feature/[name]`
   - Create Pull Request on GitHub

4. **Merge Back**
   - User: "Switch to develop branch"
   - Git: `git checkout develop`
   - User: "Pull latest changes"
   - Git: `git pull`
   - User: "Merge feature/[name] into develop"
   - Git: `git merge feature/[name]`
   - User: "Push to develop"
   - Git: `git push`

5. **Cleanup** (Optional)
   - User: "Delete feature branch"
   - Git: `git branch -d feature/[name]`

## Release Workflow

For preparing and deploying releases.

```
main (production)
  ↑
  release/v1.2.0 (release branch)
```

### Step-by-Step

1. **Prepare Release**
   - User: "Create release branch v1.2.0"
   - Git: `git checkout -b release/v1.2.0`

2. **Release Actions**
   - Update version numbers
   - Update changelog
   - User: "Save release changes"
   - Git: `git commit -m "Prepare release v1.2.0"`

3. **Merge to Main**
   - User: "Switch to main"
   - Git: `git checkout main`
   - User: "Merge release/v1.2.0"
   - Git: `git merge release/v1.2.0`
   - User: "Create tag v1.2.0"
   - Git: `git tag -a v1.2.0 -m "Release version 1.2.0"`
   - User: "Push to main with tags"
   - Git: `git push && git push --tags`

4. **Back to Develop**
   - User: "Switch to develop"
   - Git: `git checkout develop`
   - User: "Merge release branch back"
   - Git: `git merge release/v1.2.0`

## Hotfix Workflow

For urgent fixes to production.

```
main (production)
  ↓
  hotfix/xxx (urgent fix)
```

### Step-by-Step

1. **Start Hotfix**
   - User: "Switch to main"
   - Git: `git checkout main`
   - User: "Create hotfix branch for [issue]"
   - Git: `git checkout -b hotfix/[issue]`

2. **Fix and Test**
   - Make urgent fix
   - Test thoroughly
   - User: "Save hotfix with message '[description]'"
   - Git: `git commit -m "Hotfix: [description]"`

3. **Deploy**
   - User: "Push hotfix"
   - Git: `git push -u origin hotfix/[issue]`
   - Merge to main, create PR, test, deploy

4. **Back to Develop**
   - User: "Switch to develop"
   - Git: `git checkout develop`
   - User: "Merge hotfix back to develop"
   - Git: `git merge hotfix/[issue]`

## Fork & Clone Workflow

For contributing to open source or external repositories.

```
Original Repository
  ↓
Your Fork (on GitHub)
  ↓
Your Clone (local machine)
```

### Step-by-Step

1. **Fork Repository**
   - Go to GitHub repository
   - Click "Fork" button
   - Creates copy under your account

2. **Clone Your Fork**
   - User: "Clone the repository from [your fork URL]"
   - Git: `git clone [your-fork-url]`
   - User: "Navigate into project"
   - Git: `cd [project-name]`

3. **Add Upstream**
   - User: "Add original repository as upstream"
   - Git: `git remote add upstream [original-repo-url]`

4. **Keep Updated**
   - User: "Fetch from upstream"
   - Git: `git fetch upstream`
   - User: "Merge upstream changes to your branch"
   - Git: `git merge upstream/main`

5. **Push Your Changes**
   - User: "Push to your fork"
   - Git: `git push origin [your-branch]`
   - Create Pull Request to original repository

## Undo/Recovery Workflows

### Undo Last Commit (Keep Changes)
```
User: "Undo the last commit but keep my changes"
Git: `git reset --soft HEAD~1`
```

### Undo Last Commit (Discard Changes)
```
User: "Discard the last commit completely"
Git: `git reset --hard HEAD~1`
→ DANGEROUS - require confirmation
```

### Undo Multiple Commits
```
User: "Undo the last 3 commits"
Git: `git reset --soft HEAD~3` (keep changes)
Git: `git reset --hard HEAD~3` (discard - dangerous)
```

### Revert Specific Commit
```
User: "Revert commit abc1234"
Git: `git revert abc1234`
→ Creates new commit that undoes changes
```

### Discard Uncommitted Changes
```
User: "Discard all my uncommitted changes"
Git: `git reset --hard HEAD`
→ DANGEROUS - require confirmation
```

### Discard Specific File Changes
```
User: "Discard changes to file.txt"
Git: `git restore file.txt`
```

## Conflict Resolution Workflow

### When Merge Conflicts Happen

1. **Identify Conflicts**
   ```
   User: "Show me the conflicts"
   Git: `git status`
   Output shows: "both modified" files
   ```

2. **View Conflicts**
   ```
   User: "Show conflicts in this file"
   Git: Open the file and look for:
   <<<<<<< HEAD
   Your changes
   =======
   Their changes
   >>>>>>> other-branch
   ```

3. **Resolve Conflicts**
   ```
   - Edit the file to choose which version to keep
   - Or merge both versions
   - Remove the conflict markers (<<<<<<<, =======, >>>>>>>)
   ```

4. **Mark Resolved**
   ```
   User: "Mark conflicts as resolved"
   Git: `git add <file>`
   ```

5. **Complete Merge**
   ```
   User: "Complete the merge"
   Git: `git commit`
   ```

### Common Conflict Scenarios

| Scenario | Resolution |
|----------|------------|
| Same line changed differently | Choose correct version or combine |
| Same file, different lines | Usually auto-resolved by git |
| Delete vs Modify | Decide whether to keep file or deletion |
| Rename vs Modify | Choose between renamed or modified version |

## Clean Working Directory

### Remove Untracked Files
```
User: "Remove untracked files"
Git: `git clean -fd`
→ DANGEROUS - require confirmation
```

### Stash Current Work
```
User: "Save my work temporarily"
Git: `git stash`

User: "Restore my saved work"
Git: `git stash pop`
```

### See Stashed Work
```
User: "Show my saved work"
Git: `git stash list`
```
