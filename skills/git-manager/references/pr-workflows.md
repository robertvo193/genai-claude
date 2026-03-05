# Pull Request Workflows

Guide for reviewing, summarizing, and managing pull requests.

## PR Review Checklist Patterns

### General Review Requirements

Common requirements to check when reviewing a PR:

| Requirement | How to Check | CLI Commands |
|-------------|---------------|---------------|
| No breaking changes | Look for API changes, database migrations, config changes | `gh pr diff <pr#>`, `git diff` |
| Tests added | Check for test files in changed list | `gh pr view <pr#> --json files` |
| Documentation updated | Look for docs/README changes | `gh pr diff <pr#>` |
| Code style follows guidelines | Check common style violations | Review diff manually |
| No security issues | Check for hardcoded secrets, unsafe operations | Review diff |
| Performance impact | Look for query changes, loops, heavy operations | Review diff |

### Breaking Change Detection

Look for these patterns in the diff:

- **API Changes**:
  - Changed function signatures
  - Modified request/response formats
  - Added/removed endpoints
  - Changed authentication requirements

- **Database Changes**:
  - Schema modifications (`ALTER TABLE`, `DROP COLUMN`)
  - Migration files added/modified
  - Model field changes

- **Configuration Changes**:
  - Modified environment variables
  - Changed config files
  - Updated settings structure

### Test Coverage Check

When checking if tests were added:

```bash
# Get list of changed files
gh pr view <pr#> --json files --jq '.files[].path'

# Look for test files (patterns vary by language)
# JavaScript/TypeScript: *.test.js, *.test.ts, *.spec.js
# Python: test_*.py, tests/test_*.py
# Java: *Test.java, *Tests.java
# Go: *_test.go
```

### Documentation Review

Documentation patterns to verify:

- README.md updated with new features
- API docs updated for API changes
- CHANGELOG.md noted (if applicable)
- Inline code comments for complex logic
- Migration guides if breaking changes exist

## PR Summary Templates

### Summary Structure

```
📋 PR #<number>: "[Title]"

Author: @username
Status: [Open/Closed/Merged]
Created: [date]

📁 Files Changed: X (+Y, -Z lines)

📝 Key Modifications:
- [Change 1]
- [Change 2]
- [Change 3]

🎯 Purpose: [What this PR does]

🚦 Risk Level: [Low/Medium/High]

⚠️  Notes: [Any concerns or special attention needed]
```

### Risk Assessment Guidelines

| Risk Level | Criteria | Example |
|------------|-----------|---------|
| 🟢 Low | Small changes, isolated scope | Typo fix, minor UI tweak |
| 🟡 Medium | Moderate changes, some complexity | Feature addition, refactor |
| 🔴 High | Large changes, affects core | API change, database migration |

## GitHub CLI (gh) Commands Reference

### PR Viewing

| Command | Description | Example |
|---------|-------------|----------|
| `gh pr list` | List all PRs | `gh pr list` |
| `gh pr view <n>` | View PR details | `gh pr view 123` |
| `gh pr diff <n>` | Show PR diff | `gh pr diff 123` |
| `gh pr checks <n>` | Show CI status | `gh pr checks 123` |
| `gh pr files <n>` | List changed files | `gh pr files 123` |

### PR Comments & Reviews

| Command | Description | Example |
|---------|-------------|----------|
| `gh pr comment <n> -m "text"` | Add comment | `gh pr comment 123 -m "LGTM!"` |
| `gh pr review <n>` | Create review | `gh pr review 123` |
| `gh pr merge <n>` | Merge PR | `gh pr merge 123` |
| `gh pr close <n>` | Close PR | `gh pr close 123` |

### PR Filtering

| Filter | Description | Example |
|--------|-------------|----------|
| `--state <state>` | Filter by state | `gh pr list --state open` |
| `--author <user>` | Filter by author | `gh pr list --author @john` |
| `--label <label>` | Filter by label | `gh pr list --label bug` |
| `--base <branch>` | Filter by base branch | `gh pr list --base main` |

## PR Review Workflow

### Step-by-Step Review Process

1. **Fetch PR Information**
   ```
   gh pr view <pr#>
   gh pr diff <pr#>
   ```

2. **Check Requirements**
   ```
   # Get changed files
   gh pr view <pr#> --json files --jq '.files[].path'

   # Analyze for breaking changes (manual review of diff)
   gh pr diff <pr#>

   # Check test coverage (look for test files)
   gh pr view <pr#> --json files | grep "test"
   ```

3. **Generate Review Report**
   ```
   Present checklist with pass/fail status for each requirement
   ```

4. **Provide Feedback**
   ```
   - Add comments via `gh pr comment`
   - Or create formal review via `gh pr review`
   ```

### Common PR Review Scenarios

#### Scenario: Code Quality Review
```
User: "Review PR #123 for code quality"

Check:
- Code readability
- Variable naming
- Function complexity
- Error handling
- Security issues
```

#### Scenario: Feature Completeness Review
```
User: "Review PR #123 for feature completeness"

Check:
- All requirements implemented
- Edge cases handled
- Documentation updated
- Tests cover scenarios
- Configuration options available
```

#### Scenario: Security Review
```
User: "Review PR #123 for security issues"

Check:
- No hardcoded secrets
- Input validation
- SQL injection protection
- XSS prevention
- Authentication/authorization
- Dependency vulnerabilities
```

## PR Summary Generation

### Automated Summary Generation Steps

1. **Get PR Metadata**
   ```bash
   gh pr view <pr#> --json title,author,state,createdAt,body
   ```

2. **Get Changed Files Stats**
   ```bash
   gh pr view <pr#> --json additions,deletions,changedFiles
   ```

3. **Get File List**
   ```bash
   gh pr view <pr#> --json files --jq '.files[].path'
   ```

4. **Analyze Diff for Key Changes** (manual inspection of relevant files)

5. **Generate Summary** using the template above

### Quick Summary Command

```bash
# One-line summary
gh pr view <pr#> --json title,author,state | jq -r '"PR #" + (.number|tostring) + ": " + .title + " by " + .author.login + " (" + .state + ")"'

# File count summary
gh pr view <pr#> --json changedFiles,additions,deletions | jq -r '"Files: " + (.changedFiles|tostring) + ", +" + (.additions|tostring) + ", -" + (.deletions|tostring)'
```

## PR Management for Non-Technical Users

### Common User Requests & Actions

| User Request | Action to Take |
|--------------|----------------|
| "Show me open PRs" | `gh pr list --state open` |
| "What's the status of PR #123?" | `gh pr view 123 --json state,mergeable` |
| "Can I merge PR #123?" | Check `gh pr checks 123` and review status |
| "Who created PR #123?" | `gh pr view 123 --json author` |
| "What files changed in PR #123?" | `gh pr files 123` |
| "Close PR #123" | `gh pr close 123` (require confirmation) |
| "Merge PR #123" | `gh pr merge 123` (require confirmation) |

### PR Status Indicators

| Indicator | Meaning | Action |
|-----------|----------|--------|
| ✅ All checks passing | Ready for review | Proceed with review |
| ⚠️ Checks failing | Issues found | Address before merge |
| 🟡 Draft PR | Work in progress | Don't merge yet |
| 🔴 Merge conflicts | Cannot merge | Resolve conflicts first |

## PR Merge Strategies

| Strategy | When to Use | Command |
|----------|-------------|---------|
| **Merge Commit** | Preserve history, always merge | `gh pr merge <n> --merge` |
| **Squash and Merge** | Clean history, single commit | `gh pr merge <n> --squash` |
| **Rebase and Merge** | Linear history, preserve commits | `gh pr merge <n> --rebase` |
