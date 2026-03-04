---
name: proposal-from-template
description: Global workflow to generate PPTX + PDF from verified proposal template using quotation skill, with session reuse and dashboard integration.
argument-hint: "<template_file.md> [-y|--yes]"
allowed-tools: Task(*), Read(*), Write(*), Skill(*), TodoWrite(*), Bash(*)
---

# Workflow: Proposal From Template (/workflow:proposal-from-template)

## Overview

Single, repeatable workflow to generate final presentation (PowerPoint + PDF) from verified proposal template with full session tracking and dashboard integration.

**Purpose:**
1. Take a verified proposal template (no placeholders)
2. Invoke the existing `quotation` skill autonomously
3. Produce: `presentation.pptx` + `presentation.pdf`
4. **Reuse session** from previous `proposal-from-excel` workflow (if exists)
5. Persist workflow state for progress tracking

**Session Reuse:**
- If workflow session exists from `proposal-from-excel` → Augment existing session
- If no session exists → Create new session
- Always preserve `created_at` timestamp and existing metadata

## Usage

```bash
# Standard mode (interactive)
/workflow:proposal-from-template ./output/DT_0109_20260128_120000/DT_0109_template.md

# Auto mode (skip confirmations)
/workflow:proposal-from-template ./output/DT_0109_*/DT_0109_template.md --yes
/workflow:proposal-from-template ./output/DT_0109_*/DT_0109_template.md -y

# With full path
/workflow:proposal-from-template /full/path/to/template.md
```

## Auto Mode

When `--yes` or `-y` flag is used:
- Auto-confirm all prompts
- Use defaults for any decisions
- Continue without stopping

**Flag Parsing:**
```javascript
const autoYes = $ARGUMENTS.includes('--yes') || $ARGUMENTS.includes('-y')
```

## Core Rules

1. **State Persistence**: Create or reuse session with dual state files
2. **Dashboard Integration**: Update `workflow-session.json` at each phase for real-time tracking
3. **Auto-Continue**: Execute all phases without user interruption (except on critical errors)
4. **TodoWrite Tracking**: Maintain real-time progress via TodoWrite throughout workflow
5. **Session Reuse**: Augment existing session if available (preserve `created_at`, add quotation steps)

## Execution Process

### Phase 0: Initialize or Reuse Session

**Step 0.1: Parse arguments**
```javascript
const templateFile = $ARGUMENTS.find(arg => !arg.startsWith('--'))
const autoYes = $ARGUMENTS.includes('--yes') || $ARGUMENTS.includes('-y')

if (!templateFile || templateFile.startsWith('--')) {
  console.log("❌ Usage: /workflow:proposal-from-template <template-file> [--yes]")
  console.log("Example: /workflow:proposal-from-template ./output/DT_0109_*/DT_0109_template.md")
  return
}
```

**Step 0.2: Extract project identifier**
```bash
# Extract project name from template path
# Path format: ./output/PROJECT_TIMESTAMP/PROJECT_template.md
template_basename=$(basename "$templateFile" .md)
project_name="${template_basename%_template}"

# Generate session ID
session_id="WFS-proposal-${project_name}"
session_dir=".workflow/active/${session_id}"
archive_dir=".workflow/archives/${session_id}"
```

**Step 0.3: Check for existing session**
```bash
# Check if session exists in archives (from proposal-from-excel)
if [ -d "$archive_dir" ]; then
  # Reuse existing session - move back to active
  echo "📂 Reusing existing session: $session_id"
  mv "$archive_dir" "$session_dir"
  existing_session=true
else
  # Create new session
  echo "📂 Creating new session: $session_id"
  mkdir -p "$session_dir"
  existing_session=false
fi
```

**Step 0.4: Initialize or Update workflow-session.json**
```bash
if [ "$existing_session" = true ]; then
  # UPDATE existing session - preserve created_at
  jq '.status = "active" |
      .current_phase = "INITIALIZE" |
      .workflow_type = "proposal-from-template" |
      .updated_at = "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'" |
      .progress.current_tasks = ["Validate Template", "Run quotation skill", "Summarize"]' \
    "$session_dir/workflow-session.json" > "${session_dir}/workflow-session.json.tmp"
  mv "${session_dir}/workflow-session.json.tmp" "$session_dir/workflow-session.json"
else
  # CREATE new session
  cat > "$session_dir/workflow-session.json" << EOF
{
  "session_id": "$session_id",
  "project": "Generate PPTX + PDF from $templateFile",
  "type": "workflow",
  "status": "active",
  "current_phase": "INITIALIZE",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%S.000Z)",
  "updated_at": "$(date -u +%Y-%m-%dT%H:%M:%S.000Z)",
  "workflow_type": "proposal-from-template",
  "progress": {
    "completed_phases": [],
    "current_tasks": ["Validate Template", "Run quotation skill", "Summarize"]
  }
}
EOF
fi
```

**Step 0.5: Initialize or Update state.json**
```bash
if [ "$existing_session" = true ]; then
  # AUGMENT existing state - add quotation workflow info
  jq '.workflow = "proposal-from-template" |
      .input_template = "'$(basename "$templateFile")'" |
      .template_path = "'$(pwd)/$templateFile'" |
      .status = "initialized" |
      .steps += [
        { "id": 5, "name": "Validate Template", "status": "pending" },
        { "id": 6, "name": "Run quotation skill", "status": "pending" },
        { "id": 7, "name": "Summarize outputs", "status": "pending" }
      ] |
      .output_files.template_path = "'$(pwd)/$templateFile'" |
      del(.placeholder_count)' \
    "$session_dir/state.json" > "${session_dir}/state.json.tmp"
  mv "${session_dir}/state.json.tmp" "$session_dir/state.json"
else
  # CREATE new state
  cat > "$session_dir/state.json" << EOF
{
  "workflow": "proposal-from-template",
  "input_template": "$(basename "$templateFile")",
  "template_path": "$(pwd)/$templateFile",
  "status": "initialized",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%S.000Z)",
  "steps": [
    { "id": 1, "name": "Initialize", "status": "completed" },
    { "id": 2, "name": "Validate Template", "status": "pending" },
    { "id": 3, "name": "Run quotation skill", "status": "pending" },
    { "id": 4, "name": "Summarize outputs", "status": "pending" }
  ],
  "output_files": {
    "template_path": "$(pwd)/$templateFile",
    "pptx": null,
    "pdf": null
  }
}
EOF
fi
```

**Step 0.6: Initialize TodoWrite**
```javascript
TodoWrite({
  todos: [
    { content: "Initialize workflow session", status: "completed", activeForm: "Initializing workflow session" },
    { content: "Validate template file", status: "in_progress", activeForm: "Validating template file" },
    { content: "Run quotation skill", status: "pending", activeForm: "Running quotation skill" },
    { content: "Summarize outputs", status: "pending", activeForm: "Summarizing outputs" }
  ]
})
```

### Phase 1: Validate Template

**Step 1.1: Check file exists**
```bash
# Resolve file path
if [[ "$templateFile" != /* ]]; then
  # Relative path - resolve from current directory
  template_path="$(pwd)/$templateFile"
else
  # Absolute path
  template_path="$templateFile"
fi

# Validate file exists
if [ ! -f "$template_path" ]; then
  echo "❌ Template file not found: $templateFile"
  echo ""
  echo "Please check:"
  echo "  - File path is correct"
  echo "  - File was generated by /workflow:proposal-from-excel"
  echo ""
  echo "Example: /workflow:proposal-from-template ./output/DT_0109_20260128_120000/DT_0109_template.md"

  # Update state as failed
  jq '.steps += [{"id": 5, "name": "Validate Template", "status": "failed"}] |
      .status = "failed"' \
    "$session_dir/state.json" > "${session_dir}/state.json.tmp"
  mv "${session_dir}/state.json.tmp" "$session_dir/state.json"

  exit 1
fi
```

**Step 1.2: Validate file format**
```bash
# Check file extension
if [[ ! "$templateFile" =~ \.md$ ]]; then
  echo "❌ Invalid file format: $templateFile"
  echo ""
  echo "Expected: .md file"
  echo "Got: ${templateFile##*.}"
  echo ""
  echo "Please provide a valid proposal template file (.md format)"

  # Update state as failed
  jq '.steps += [{"id": 5, "name": "Validate Template", "status": "failed", "message": "Invalid file format"}] |
      .status = "failed"' \
    "$session_dir/state.json" > "${session_dir}/state.json.tmp"
  mv "${session_dir}/state.json.tmp" "$session_dir/state.json"

  exit 1
fi
```

**Step 1.3: Check for placeholders (safety check)**
```bash
# Scan for placeholders
placeholders=$(grep -oE '\[([A-Z_]+[0-9])\]' "$template_path" 2>/dev/null | sort -u | wc -l)

if [ $placeholders -gt 0 ]; then
  echo "❌ Template has $placeholders placeholders that must be confirmed first"
  echo ""
  echo "Please fill in all placeholders in the checklist, then run again"
  echo "💡 Use /workflow:proposal-from-excel to regenerate from original Excel if needed"
  echo ""
  echo "Found placeholders:"
  grep -oE '\[([A-Z_]+[0-9])\]' "$template_path" 2>/dev/null | sort -u | head -10
  if [ $placeholders -gt 10 ]; then
    echo "... and $((placeholders - 10)) more"
  fi

  # Update state as failed
  jq '.steps += [{"id": 5, "name": "Validate Template", "status": "failed", "message": "Template has placeholders"}] |
      .status = "failed" |
      .placeholder_count = '$placeholders'' \
    "$session_dir/state.json" > "${session_dir}/state.json.tmp"
  mv "${session_dir}/state.json.tmp" "$session_dir/state.json"

  exit 1
fi

echo "✅ Template validated successfully (no placeholders)"
```

**Step 1.4: Update state**
```bash
# Mark validation as completed
jq 'if .steps[1] then
      .steps[1].status = "completed"
    else
      .steps += [{"id": 5, "name": "Validate Template", "status": "completed"}]
    end |
    .status = "validated"' \
  "$session_dir/state.json" > "${session_dir}/state.json.tmp"
mv "${session_dir}/state.json.tmp" "$session_dir/state.json"

# Update workflow-session.json for dashboard
jq '.current_phase = "VALIDATED" |
    .progress.completed_phases = ["INITIALIZE", "VALIDATE"] |
    .updated_at = "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'"' \
  "$session_dir/workflow-session.json" > "${session_dir}/workflow-session.json.tmp"
mv "${session_dir}/workflow-session.json.tmp" "$session_dir/workflow-session.json"
```

**Step 1.5: Update TodoWrite**
```javascript
TodoWrite({
  todos: [
    { content: "Initialize workflow session", status: "completed", activeForm: "Initializing workflow session" },
    { content: "Validate template file", status: "completed", activeForm: "Validating template file" },
    { content: "Run quotation skill", status: "in_progress", activeForm: "Running quotation skill" },
    { content: "Summarize outputs", status: "pending", activeForm: "Summarizing outputs" }
  ]
})
```

### Phase 2: Run quotation Skill

**Step 2.1: Update dashboard state**
```bash
jq '.current_phase = "PROCESSING" |
    .updated_at = "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'"' \
  "$session_dir/workflow-session.json" > "${session_dir}/workflow-session.json.tmp"
mv "${session_dir}/workflow-session.json.tmp" "$session_dir/workflow-session.json"
```

**Step 2.2: Execute skill**
```javascript
// Call quotation skill
// In auto mode: skill will auto-confirm without asking user
Skill({
  skill: "quotation",
  args: template_path
})
```

**Step 2.3: Detect output files**
```bash
# Output files are in same directory as template
template_dir=$(dirname "$template_path")

# Detect generated files
pptx_file=$(find "$template_dir" -maxdepth 1 -name "*.pptx" -type f | head -1)
pdf_file=$(find "$template_dir" -maxdepth 1 -name "*.pdf" -type f | head -1)

if [ -z "$pptx_file" ] && [ -z "$pdf_file" ]; then
  echo "❌ No output files found. Skill may have failed."

  # Update state as failed
  jq 'if .steps[2] then
        .steps[2].status = "failed"
      else
        .steps += [{"id": 6, "name": "Run quotation skill", "status": "failed"}]
      end |
      .status = "failed"' \
    "$session_dir/state.json" > "${session_dir}/state.json.tmp"
  mv "${session_dir}/state.json.tmp" "$session_dir/state.json"

  exit 1
fi

echo "✅ Output files generated"
```

**Step 2.4: Update state**
```bash
# Record output files
jq 'if .steps[2] then
      .steps[2].status = "completed"
    else
      .steps += [{"id": 6, "name": "Run quotation skill", "status": "completed"}]
    end |
    .output_files.pptx = "'$(basename "$pptx_file" 2>/dev/null || echo "")'" |
    .output_files.pdf = "'$(basename "$pdf_file" 2>/dev/null || echo "")'" |
    .status = "processing"' \
  "$session_dir/state.json" > "${session_dir}/state.json.tmp"
mv "${session_dir}/state.json.tmp" "$session_dir/state.json"

# Update workflow-session.json for dashboard
jq '.current_phase = "PROCESSED" |
    .progress.completed_phases = ["INITIALIZE", "VALIDATE", "PROCESSING"] |
    .updated_at = "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'"' \
  "$session_dir/workflow-session.json" > "${session_dir}/workflow-session.json.tmp"
mv "${session_dir}/workflow-session.json.tmp" "$session_dir/workflow-session.json"
```

**Step 2.5: Update TodoWrite**
```javascript
TodoWrite({
  todos: [
    { content: "Initialize workflow session", status: "completed", activeForm: "Initializing workflow session" },
    { content: "Validate template file", status: "completed", activeForm: "Validating template file" },
    { content: "Run quotation skill", status: "completed", activeForm: "Running quotation skill" },
    { content: "Summarize outputs", status: "in_progress", activeForm: "Summarizing outputs" }
  ]
})
```

### Phase 3: Summarize & Complete

**Step 3.1: Update state as completed**
```bash
jq 'if .steps[3] then
      .steps[3].status = "completed"
    else
      .steps += [{"id": 7, "name": "Summarize outputs", "status": "completed"}]
    end |
    .status = "completed"' \
  "$session_dir/state.json" > "${session_dir}/state.json.tmp"
mv "${session_dir}/state.json.tmp" "$session_dir/state.json"

# Update workflow-session.json for dashboard
jq '.status = "completed" |
    .current_phase = "COMPLETED" |
    .progress.completed_phases = ["INITIALIZE", "VALIDATE", "PROCESSING", "COMPLETED"] |
    .updated_at = "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'"' \
  "$session_dir/workflow-session.json" > "${session_dir}/workflow-session.json.tmp"
mv "${session_dir}/workflow-session.json.tmp" "$session_dir/workflow-session.json"
```

**Step 3.2: Archive session**
```bash
# Move to archives
mv ".workflow/active/${session_id}" ".workflow/archives/${session_id}"
```

**Step 3.3: Display summary**
```bash
echo ""
echo "📊 Proposal From Template – Workflow Summary"
echo ""
echo "Input Template: $templateFile"
echo "Status: ✅ completed"
echo ""
echo "Steps:"
echo "  - ✅ Validate Template"
echo "  - ✅ Run quotation skill"
echo "  - ✅ Summarize outputs"
echo ""
echo "Generated files:"
if [ -n "$pptx_file" ]; then
  echo "  - PowerPoint: $(basename "$pptx_file")"
fi
if [ -n "$pdf_file" ]; then
  echo "  - PDF:        $(basename "$pdf_file")"
fi
echo ""
echo "Output directory: $template_dir"
echo ""
echo "📂 Session archived: $session_id"
echo ""
```

**Step 3.4: Update TodoWrite**
```javascript
TodoWrite({
  todos: [
    { content: "Initialize workflow session", status: "completed", activeForm: "Initializing workflow session" },
    { content: "Validate template file", status: "completed", activeForm: "Validating template file" },
    { content: "Run quotation skill", status: "completed", activeForm: "Running quotation skill" },
    { content: "Summarize outputs", status: "completed", activeForm: "Summarizing outputs" }
  ]
})
```

## Error Handling

### File Not Found
```bash
❌ Template file not found: ./output/.../template.md

Please check:
  - File path is correct
  - File was generated by /workflow:proposal-from-excel
  - File has .md extension

Example: /workflow:proposal-from-template ./output/DT_0109_20260128_120000/DT_0109_template.md
         /workflow:proposal-from-template /full/path/to/template.md
```

### Invalid File Format
```bash
❌ Invalid file format: file.txt

Expected: .md file
Got: .txt

Please provide a valid proposal template file (.md format)
```

### Template Has Placeholders
```bash
❌ Template has 5 placeholders that must be confirmed first

Please fill in all placeholders in the checklist, then run again
💡 Use /workflow:proposal-from-excel to regenerate from original Excel if needed

Found placeholders:
[CLIENT_NAME1]
[PROJECT_VALUE2]
[DEADLINE3]
... and 2 more
```

### Skill Execution Failed
```bash
❌ No output files found. Skill may have failed.

Please check:
  - Template format is correct (.md)
  - Template was generated by /workflow:proposal-from-excel
  - quotation_skill is properly installed

For help: /presales-guide
```

## State & Dashboard

### Dual State System

**1. workflow-session.json** (dashboard metadata):
- Location: `.workflow/active/WFS-proposal-*/workflow-session.json`
- Purpose: Dashboard reads this via `session-scanner.ts`
- Fields: `session_id`, `project`, `type`, `status`, `current_phase`, `created_at`, `updated_at`, `workflow_type`, `progress`
- **Must be updated** at each phase change
- **Session reuse**: Preserves `created_at` when augmenting existing session

**2. state.json** (workflow-specific state):
- Location: `.workflow/active/WFS-proposal-*/state.json`
- Purpose: Detailed workflow state (steps, output files, template info)
- Used by workflow logic and debugging
- **Session reuse**: Augments existing state with quotation workflow info

### Dashboard Real-Time Tracking

- Dashboard calls `scanSessions()` → reads all `workflow-session.json` files
- Each update to `workflow-session.json` is immediately visible in dashboard
- Status flow: `active` → `active` (with phase updates) → `completed` → archived

### Session Lifecycle

- **Created**: `.workflow/active/WFS-proposal-*/` with both JSON files
- **Active**: Dashboard shows as "active" with current phase
- **Completed**: `status: "completed"` in both files
- **Archived**: Move directory to `.workflow/archives/` (dashboard shows in archived list)

### Session Reuse Pattern

**Scenario 1: Running after proposal-from-excel**
```bash
# Step 1: Run proposal-from-excel
/workflow:proposal-from-excel DT_0109.xlsx
# Creates: .workflow/active/WFS-proposal-DT_0109/
# Archives: .workflow/archives/WFS-proposal-DT_0109/

# Step 2: Run proposal-from-template
/workflow:proposal-from-template ./output/DT_0109_*/DT_0109_template.md
# Reuses: Moves .workflow/archives/WFS-proposal-DT_0109/ → .workflow/active/
# Augments: Adds quotation steps to existing state
# Preserves: created_at timestamp from original session
```

**Scenario 2: Running standalone**
```bash
# No existing session
/workflow:proposal-from-template ./output/DT_0109_*/DT_0109_template.md
# Creates: .workflow/active/WFS-proposal-DT_0109/
# New state with quotation workflow only
```

## Integration

### Requires
- **Verified template** - Must have no placeholders
- **Template generated by** `/workflow:proposal-from-excel` (recommended)

### Followed By
- None (this is the final step in the presales workflow)

### Related Workflows
- **`/workflow:proposal-from-excel`** - Generate template from Excel (preceding step)

## See Also

- `quotation` skill documentation
- CCW workflow architecture: `.claude/workflows/workflow-architecture.md`
- Dashboard integration: `session-scanner.ts`
- `/workflow:proposal-from-excel` - Preceding workflow
