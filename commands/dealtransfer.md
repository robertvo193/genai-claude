---
name: dealtransfer
description: Generate proposal draft from Deal Transfer Excel file. Creates template, reasoning, and checklist markdown files for presales review.
argument-hint: "<excel-file>"
allowed-tools: Skill(*), Read(*), Write(*), Bash(*), Glob(*), Grep(*), AskUserQuestion(*)
---

# Deal Transfer Command

Generate technical proposal draft from Deal Transfer Excel file (Commercial S1 + Technical S2).

## Purpose

Extract data from Deal Transfer Excel and generate three markdown files:
- **Template**: Client-facing proposal draft (with placeholders)
- **Reasoning**: Complete audit trail of all decisions
- **Checklist**: All items requiring presales confirmation

## Execution Flow

### Phase 1: Validate Input

1. Check argument provided (Excel file path)
2. Verify file exists and is .xlsx format
3. Extract filename for project identification

**Error handling:**
- If no argument: Show usage example
- If file not found: Display error with example
- If invalid file: Display required format

### Phase 2: Extract Project Metadata

1. Extract project name from Excel filename or content
2. Generate timestamp for output directory
3. Create output directory: `./output/[ProjectName]_[YYYYMMDD]_[HHMMSS]/`

**Project name extraction priority:**
1. Read Excel "Customer overview" field (S1)
2. Fallback to filename (e.g., DT_0109.xlsx → "DT_0109")
3. Always use alphanumeric + underscore only

### Phase 3: Call dealtransfer2template Skill

**NO confirmation required** - autonomous execution.

Use Skill tool to invoke dealtransfer2template:

```
Skill({
  skill: "dealtransfer2template",
  args: "/path/to/DT_0109.xlsx"
})
```

**What the skill does:**
1. Extracts data from Commercial (S1) and Technical (S2) sheets
2. Analyzes pain points and use cases
3. Determines AI modules automatically
4. Generates three markdown files:
   - `[ProjectName]_template.md`
   - `[ProjectName]_reasoning.md`
   - `[ProjectName]_checklist.md`
5. Validates output with `validate_output.py`

### Phase 4: Validate and Summarize

1. Check all three files created
2. Parse checklist to count placeholders
3. Display summary with file sizes and location
4. Show next steps for presales user

## Output Format

### Success Message

```
✅ Generated proposal draft for: [Project Name]

📁 Output Directory: ./output/[ProjectName]_[timestamp]/

Files Created:
  ✓ [ProjectName]_template.md (X.X KB) - Client-facing proposal
  ✓ [ProjectName]_reasoning.md (XX KB) - Internal audit trail
  ✓ [ProjectName]_checklist.md (X.X KB) - Items to confirm

📋 Placeholders to Confirm: [N]

Next Steps:
  1. Review: ./output/.../[ProjectName]_template.md
  2. Confirm all placeholders in checklist.md
  3. When ready: /quotation ./output/.../[ProjectName]_template.md

💡 Tip: Use /presales-guide for detailed instructions
```

### Error Messages

**File not found:**
```
❌ File not found: [filename]

Please check:
  - File path is correct
  - File extension is .xlsx
  - File exists in specified location

Example: /dealtransfer DT_0109.xlsx
         /dealtransfer /full/path/to/DT_0109.xlsx
```

**Invalid Excel format:**
```
❌ Invalid Deal Transfer Excel file: [filename]

Required sheets:
  - Commercial (S1)
  - Technical (S2)

Please check the file has both sheets with exact names.
```

**Skill execution failed:**
```
❌ Failed to generate proposal: [error reason]

Check:
  - Excel file format is correct
  - Sheets are named "Commercial" and "Technical"
  - File is not corrupted

For help: /presales-guide
```

## Implementation Notes

### Directory Creation

**Pattern:**
```bash
output_dir="./output/${project_name}_$(date +%Y%m%d_%H%M%S)/"
mkdir -p "$output_dir"
```

**Example:**
`./output/Leda_Inio_20260127_200428/`

### Placeholder Counting

**Parse checklist file:**
```bash
# Count unique placeholder IDs
grep -o '\[[A-Z_]*[0-9]\]' checklist.md | sort -u | wc -l
```

### File Size Calculation

```bash
# Get human-readable sizes
ls -lh template.md | awk '{print $5}'
```

## Examples

### Basic Usage

```bash
/dealtransfer DT_0109.xlsx
```

**Output:**
```
✅ Generated proposal draft for: Leda Inio

📁 Output Directory: ./output/Leda_Inio_20260127_200428/

Files Created:
  ✓ Leda_Inio_template.md (7.0 KB)
  ✓ Leda_Inio_reasoning.md (14 KB)
  ✓ Leda_Inio_checklist.md (6.6 KB)

📋 Placeholders to Confirm: 14

Next Steps:
  1. Review: ./output/Leda_Inio_20260127_200428/Leda_Inio_template.md
  2. Confirm all placeholders in checklist.md
  3. When ready: /quotation ./output/Leda_Inio_20260127_200428/Leda_Inio_template.md
```

### With Full Path

```bash
/dealtransfer ~/Documents/Deal_Transfers/DT_0110.xlsx
```

### Multiple Files

```bash
# First deal
/dealtransfer DT_0109.xlsx

# Second deal
/dealtransfer DT_0110.xlsx
```

Each creates separate output directory with timestamp.

## User Experience

### Target Audience

Non-technical presales users who:
- Receive Deal Transfer Excel files from sales team
- Need to generate proposals quickly
- Are not familiar with CLI or skills system
- Want simple, English-only interface

### Key Design Principles

1. **Single command** - No parameters to remember
2. **Clear feedback** - Know exactly what was created and where
3. **Next steps** - Always told what to do next
4. **No jargon** - Plain English, no technical terms
5. **Error recovery** - Clear error messages with solutions

### Workflow Integration

This is **Step 1** of the two-step presales workflow:

```
Step 1: /dealtransfer <excel>  → Draft proposal (manual review)
                ↓
         (Presales reviews and adjusts)
                ↓
Step 2: /quotation <template> → Final slides (PPTX + PDF)
```

## Technical Constraints

### What This Command Does NOT Do

- ❌ Does NOT modify the Excel file
- ❌ Does NOT ask for confirmations (autonomous)
- ❌ Does NOT fill placeholders (presales task)
- ❌ Does NOT generate slides/PDF (next command)
- ❌ Does NOT read from previous runs (always fresh)

### What This Command DOES

- ✅ Extracts data from Excel (S1 + S2)
- ✅ Calls dealtransfer2template skill
- ✅ Creates three markdown files
- ✅ Validates output quality
- ✅ Shows clear next steps

## Related Commands

- `/quotation` - Generate final slides from verified template
- `/presales-guide` - Display user guide

## Aliases

None by default. Can add custom alias:
```bash
/dt <excel-file>  # Alias for /dealtransfer
```

