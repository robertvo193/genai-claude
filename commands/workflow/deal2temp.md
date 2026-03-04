---
name: deal2temp
description: Simple alias for /workflow:proposal-from-excel. Generate proposal draft from Deal Transfer Excel file.
argument-hint: "<excel-file> [--yes|-y]"
allowed-tools: SlashCommand(*)
---

# Deal2Temp Command

Simple alias for `/workflow:proposal-from-excel`. Calls the full workflow with session tracking and dashboard integration.

## Overview

**This command is a lightweight alias** that invokes `/workflow:proposal-from-excel` to generate proposal draft from Deal Transfer Excel file.

**Command delegates to workflow:**
- All execution logic is in workflow file
- Workflow creates session and tracks progress
- Command parses arguments and invokes workflow

## Usage

```bash
# Standard mode
/deal2temp DT_0109.xlsx

# Auto mode (skip confirmations)
/deal2temp DT_0109.xlsx --yes
/deal2temp DT_0109.xlsx -y

# With full path
/deal2temp /path/to/DT_0109.xlsx
```

## Auto Mode

When `--yes` or `-y` flag is used:
- Auto-confirm all prompts
- Use defaults for any decisions
- Continue without stopping

## Execution

**Parse arguments and invoke workflow:**
```javascript
const excelFile = $ARGUMENTS.find(arg => !arg.startsWith('--'))
const flags = $ARGUMENTS.filter(arg => arg.startsWith('--'))

// Build workflow command
const workflowCommand = `/workflow:proposal-from-excel ${excelFile} ${flags.join(' ')}`

// Execute workflow via SlashCommand
SlashCommand({
  command: workflowCommand
})
```

## Error Handling

### File Not Found
```bash
❌ File not found: DT_0109.xlsx

Please check:
  - File path is correct
  - File extension is .xlsx
  - File exists in specified location

Example: /deal2temp DT_0109.xlsx
         /deal2temp /full/path/to/DT_0109.xlsx
```

### Workflow Execution Failed
```bash
❌ Workflow execution failed

Please check:
  - Excel file format is correct (.xlsx)
  - Required sheets exist (Commercial, Technical)
  - File is not corrupted

For help: /presales-guide
```

## Integration

### Followed By
- **`/quotation`** command - Generate final slides from verified template

### Related Commands
- **`/workflow:proposal-from-excel`** - Full workflow with session tracking
- **`/quotation`** - Generate PowerPoint and PDF
- **`/presales-guide`** - Display user guide

## See Also

- `/workflow:proposal-from-excel` - Full workflow (this command calls it)
- `/quotation` - Generate final slides
- `dealtransfer2template` skill documentation
