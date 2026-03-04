---
name: proposal-from-excel
description: Global workflow to go from Deal Transfer Excel (S1/S2) to proposal_template.md + reasoning.md + checklist.md using the existing dealtransfer2template skill, with clear state tracking.
argument-hint: "<excel_file.xlsx> [-y|--yes]"
allowed-tools: Task(*), Read(*), Write(*), Skill(*), TodoWrite(*), Bash(*)
---

# Workflow: Proposal From Deal Transfer Excel (/workflow:proposal-from-excel)

## Overview

Single, repeatable workflow to generate proposal markdown files from Deal Transfer Excel with full session tracking and dashboard integration.

**Purpose:**
1. Take a Deal Transfer Excel file (with S1/S2 sheets)
2. Invoke the existing `dealtransfer2template` skill autonomously
3. Produce: `template.md`, `reasoning.md`, `checklist.md`
4. Persist workflow state for progress tracking and resumption

**Important:** This workflow does **not** generate PPTX/PDF. It stops after markdown generation so presales can manually review.

## Usage

```bash
# Standard mode (interactive)
/workflow:proposal-from-excel DT_0109.xlsx

# Auto mode (skip confirmations)
/workflow:proposal-from-excel DT_0109.xlsx --yes
/workflow:proposal-from-excel DT_0109.xlsx -y

# With full path
/workflow:proposal-from-excel /path/to/DT_0109.xlsx
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

1. **State Persistence**: Create and maintain dual state files (`workflow-session.json` + `state.json`)
2. **Dashboard Integration**: Update `workflow-session.json` at each phase for real-time tracking
3. **Auto-Continue**: Execute all phases without user interruption (except on critical errors)
4. **TodoWrite Tracking**: Maintain real-time progress via TodoWrite throughout workflow

## Execution Process

### Phase 0: Initialize

**Step 0.1: Parse arguments**
```javascript
const excelFile = $ARGUMENTS.find(arg => !arg.startsWith('--'))
const autoYes = $ARGUMENTS.includes('--yes') || $ARGUMENTS.includes('-y')

if (!excelFile || excelFile.startsWith('--')) {
  console.log("❌ Usage: /workflow:proposal-from-excel <excel-file> [--yes]")
  console.log("Example: /workflow:proposal-from-excel DT_0109.xlsx")
  return
}
```

**Step 0.2: Create workflow session**
```bash
# Generate session ID from Excel filename
excel_stem=$(basename "$excelFile" .xlsx)
session_id="WFS-proposal-${excel_stem}"
session_dir=".workflow/active/${session_id}"

# Create session directory
mkdir -p "$session_dir"

# Initialize workflow-session.json (for dashboard)
cat > "$session_dir/workflow-session.json" << EOF
{
  "session_id": "$session_id",
  "project": "Generate template from $excelFile",
  "type": "workflow",
  "status": "active",
  "current_phase": "INITIALIZE",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%S.000Z)",
  "updated_at": "$(date -u +%Y-%m-%dT%H:%M:%S.000Z)",
  "workflow_type": "proposal-from-excel",
  "progress": {
    "completed_phases": [],
    "current_tasks": ["Initialize", "Validate Excel", "Run dealtransfer2template", "Summarize"]
  }
}
EOF

# Initialize state.json (for workflow logic)
cat > "$session_dir/state.json" << EOF
{
  "workflow": "proposal-from-excel",
  "input_excel": "$excelFile",
  "excel_path": "$(pwd)/$excelFile",
  "status": "initialized",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%S.000Z)",
  "steps": [
    { "id": 1, "name": "Initialize", "status": "completed" },
    { "id": 2, "name": "Validate Excel", "status": "pending" },
    { "id": 3, "name": "Run dealtransfer2template skill", "status": "pending" },
    { "id": 4, "name": "Summarize outputs", "status": "pending" }
  ],
  "output_files": {
    "template": null,
    "reasoning": null,
    "checklist": null
  }
}
EOF
```

**Step 0.3: Initialize TodoWrite**
```javascript
TodoWrite({
  todos: [
    { content: "Initialize workflow session", status: "completed", activeForm: "Initializing workflow session" },
    { content: "Validate Excel file", status: "in_progress", activeForm: "Validating Excel file" },
    { content: "Run dealtransfer2template skill", status: "pending", activeForm: "Running dealtransfer2template skill" },
    { content: "Summarize outputs", status: "pending", activeForm: "Summarizing outputs" }
  ]
})
```

### Phase 1: Validate Excel

**Step 1.1: Check file exists**
```bash
# Resolve file path
if [[ "$excelFile" != /* ]]; then
  # Relative path - resolve from current directory
  excel_path="$(pwd)/$excelFile"
else
  # Absolute path
  excel_path="$excelFile"
fi

# Validate file exists
if [ ! -f "$excel_path" ]; then
  echo "❌ File not found: $excelFile"
  echo ""
  echo "Please check:"
  echo "  - File path is correct"
  echo "  - File exists in specified location"
  echo ""
  echo "Example: /workflow:proposal-from-excel DT_0109.xlsx"
  echo "         /workflow:proposal-from-excel /full/path/to/DT_0109.xlsx"

  # Update state as failed
  jq '.steps[1].status = "failed" |
      .steps[1].message = "File not found" |
      .status = "failed' \
    "$session_dir/state.json" > "${session_dir}/state.json.tmp"
  mv "${session_dir}/state.json.tmp" "${session_dir}/state.json"

  exit 1
fi
```

**Step 1.2: Validate file format**
```bash
# Check file extension
if [[ ! "$excelFile" =~ \.xlsx$ ]]; then
  echo "❌ Invalid file format: $excelFile"
  echo ""
  echo "Expected: .xlsx file"
  echo "Got: ${excelFile##*.}"
  echo ""
  echo "Please provide a valid Deal Transfer Excel file (.xlsx format)"

  # Update state as failed
  jq '.steps[1].status = "failed" |
      .steps[1].message = "Invalid file format" |
      .status = "failed' \
    "$session_dir/state.json" > "${session_dir}/state.json.tmp"
  mv "${session_dir}/state.json.tmp" "${session_dir}/state.json"

  exit 1
fi
```

**Step 1.3: Update state**
```bash
# Mark validation as completed
jq '.steps[1].status = "completed" |
    .status = "validated"' \
  "$session_dir/state.json" > "${session_dir}/state.json.tmp"
mv "${session_dir}/state.json.tmp" "${session_dir}/state.json"

# Update workflow-session.json for dashboard
jq '.current_phase = "VALIDATED" |
    .progress.completed_phases = ["INITIALIZE", "VALIDATE"] |
    .updated_at = "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'"' \
  "$session_dir/workflow-session.json" > "${session_dir}/workflow-session.json.tmp"
mv "${session_dir}/workflow-session.json.tmp" "$session_dir/workflow-session.json"
```

**Step 1.4: Update TodoWrite**
```javascript
TodoWrite({
  todos: [
    { content: "Initialize workflow session", status: "completed", activeForm: "Initializing workflow session" },
    { content: "Validate Excel file", status: "completed", activeForm: "Validating Excel file" },
    { content: "Run dealtransfer2template skill", status: "in_progress", activeForm: "Running dealtransfer2template skill" },
    { content: "Summarize outputs", status: "pending", activeForm: "Summarizing outputs" }
  ]
})
```

### Phase 2: Run dealtransfer2template Skill

**Step 2.1: Update dashboard state**
```bash
jq '.current_phase = "PROCESSING" |
    .updated_at = "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'"' \
  "$session_dir/workflow-session.json" > "${session_dir}/workflow-session.json.tmp"
mv "${session_dir}/workflow-session.json.tmp" "$session_dir/workflow-session.json"
```

**Step 2.2: Execute skill**
```javascript
// Call dealtransfer2template skill
// In auto mode: skill will auto-confirm without asking user
Skill({
  skill: "dealtransfer2template",
  args: excel_path
})
```

**Step 2.3: Detect output files**
```bash
# Find most recent output directory
output_dir=$(find ./output -type d -name "*_*" -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)

if [ -z "$output_dir" ]; then
  echo "❌ No output directory found. Skill may have failed."

  # Update state as failed
  jq '.steps[2].status = "failed" |
      .steps[2].message = "No output directory found" |
      .status = "failed' \
    "$session_dir/state.json" > "${session_dir}/state.json.tmp"
  mv "${session_dir}/state.json.tmp" "${session_dir}/state.json"

  exit 1
fi

# Detect generated files
template_file=$(find "$output_dir" -name "*_template.md" -type f | head -1)
reasoning_file=$(find "$output_dir" -name "*_reasoning.md" -type f | head -1)
checklist_file=$(find "$output_dir" -name "*_checklist.md" -type f | head -1)

if [ -z "$template_file" ] || [ -z "$reasoning_file" ] || [ -z "$checklist_file" ]; then
  echo "❌ Some output files missing:"
  echo "  Template: ${template_file:-NOT FOUND}"
  echo "  Reasoning: ${reasoning_file:-NOT FOUND}"
  echo "  Checklist: ${checklist_file:-NOT FOUND}"

  # Update state as partial
  jq '.steps[2].status = "completed" |
      .status = "partial" |
      .output_files.template = "'$(basename "$template_file" 2>/dev/null || echo "")'" |
      .output_files.reasoning = "'$(basename "$reasoning_file" 2>/dev/null || echo "")'" |
      .output_files.checklist = "'$(basename "$checklist_file" 2>/dev/null || echo "")'"' \
    "$session_dir/state.json" > "${session_dir}/state.json.tmp"
  mv "${session_dir}/state.json.tmp" "${session_dir}/state.json"

  exit 1
fi
```

**Step 2.4: Update state**
```bash
# Record output files
jq '.steps[2].status = "completed" |
    .output_files.template = "'$(basename "$template_file")'" |
    .output_files.reasoning = "'$(basename "$reasoning_file")'" |
    .output_files.checklist = "'$(basename "$checklist_file")'" |
    .status = "processing"' \
  "$session_dir/state.json" > "${session_dir}/state.json.tmp"
mv "${session_dir}/state.json.tmp" "${session_dir}/state.json"

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
    { content: "Validate Excel file", status: "completed", activeForm: "Validating Excel file" },
    { content: "Run dealtransfer2template skill", status: "completed", activeForm: "Running dealtransfer2template skill" },
    { content: "Summarize outputs", status: "in_progress", activeForm: "Summarizing outputs" }
  ]
})
```

### Phase 3: Summarize & Complete

**Step 3.1: Count placeholders**
```bash
# Count unique placeholders in checklist
placeholder_count=$(grep -o '\[[A-Z_]*[0-9]\]' "$checklist_file" 2>/dev/null | sort -u | wc -l)
```

**Step 3.2: Update state as completed**
```bash
jq '.steps[3].status = "completed" |
    .status = "completed" |
    .placeholder_count = '$placeholder_count'' \
  "$session_dir/state.json" > "${session_dir}/state.json.tmp"
mv "${session_dir}/state.json.tmp" "${session_dir}/state.json"

# Update workflow-session.json for dashboard
jq '.status = "completed" |
    .current_phase = "COMPLETED" |
    .progress.completed_phases = ["INITIALIZE", "VALIDATE", "PROCESSING", "COMPLETED"] |
    .updated_at = "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'"' \
  "$session_dir/workflow-session.json" > "${session_dir}/workflow-session.json.tmp"
mv "${session_dir}/workflow-session.json.tmp" "$session_dir/workflow-session.json"
```

**Step 3.3: Archive session**
```bash
# Move to archives
mv ".workflow/active/${session_id}" ".workflow/archives/${session_id}"
```

**Step 3.4: Display summary**
```bash
echo ""
echo "📊 Proposal From Excel – Workflow Summary"
echo ""
echo "Input Excel: $excelFile"
echo "Status: ✅ completed"
echo ""
echo "Steps:"
echo "  - ✅ Initialize"
echo "  - ✅ Validate Excel"
echo "  - ✅ Run dealtransfer2template skill"
echo "  - ✅ Summarize outputs"
echo ""
echo "Generated files:"
echo "  - Template:  $(basename "$template_file")"
echo "  - Reasoning: $(basename "$reasoning_file")"
echo "  - Checklist: $(basename "$checklist_file")"
echo ""
echo "Placeholders to confirm: $placeholder_count"
echo ""
echo "Next steps (for presales):"
echo "  1) Review the template file for content and wording."
echo "  2) Use the checklist to confirm or adjust assumptions."
echo "  3) When finalized, run: /quotation $(basename "$template_file")"
echo ""
```

**Step 3.5: Update TodoWrite**
```javascript
TodoWrite({
  todos: [
    { content: "Initialize workflow session", status: "completed", activeForm: "Initializing workflow session" },
    { content: "Validate Excel file", status: "completed", activeForm: "Validating Excel file" },
    { content: "Run dealtransfer2template skill", status: "completed", activeForm: "Running dealtransfer2template skill" },
    { content: "Summarize outputs", status: "completed", activeForm: "Summarizing outputs" }
  ]
})
```

## Error Handling

### File Not Found
```bash
❌ File not found: DT_0109.xlsx

Please check:
  - File path is correct
  - File exists in specified location

Example: /workflow:proposal-from-excel DT_0109.xlsx
         /workflow:proposal-from-excel /full/path/to/DT_0109.xlsx
```

### Invalid File Format
```bash
❌ Invalid file format: file.txt

Expected: .xlsx file
Got: .txt

Please provide a valid Deal Transfer Excel file (.xlsx format)
```

### Skill Execution Failed
```bash
❌ No output directory found. Skill may have failed.

Please check:
  - Excel file format is correct (.xlsx)
  - Required sheets exist (Commercial, Technical)
  - File is not corrupted

For help: Check skill output above for detailed error
```

## State & Dashboard

### Dual State System

**1. workflow-session.json** (dashboard metadata):
- Location: `.workflow/active/WFS-proposal-*/workflow-session.json`
- Purpose: Dashboard reads this via `session-scanner.ts`
- Fields: `session_id`, `project`, `type`, `status`, `current_phase`, `created_at`, `updated_at`, `workflow_type`, `progress`
- **Must be updated** at each phase change

**2. state.json** (workflow-specific state):
- Location: `.workflow/active/WFS-proposal-*/state.json`
- Purpose: Detailed workflow state (steps, output files, etc.)
- Used by workflow logic and debugging

### Dashboard Real-Time Tracking

- Dashboard calls `scanSessions()` → reads all `workflow-session.json` files
- Each update to `workflow-session.json` is immediately visible in dashboard
- Status flow: `active` → `active` (with phase updates) → `completed` → archived

### Session Lifecycle

- **Created:** `.workflow/active/WFS-proposal-*/` with both JSON files
- **Active:** Dashboard shows as "active" with current phase
- **Completed:** `status: "completed"` in both files
- **Archived:** Move directory to `.workflow/archives/` (dashboard shows in archived list)

## Integration

### Followed By
- **`/quotation`** command - Generate final slides from verified template

### Related Workflows
- **`/quotation`** - Generate PowerPoint and PDF (should also have workflow version)

## See Also

- `dealtransfer2template` skill documentation
- CCW workflow architecture: `.claude/workflows/workflow-architecture.md`
- Dashboard integration: `session-scanner.ts`
