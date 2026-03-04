# Quotation Skill - Quick Start Guide

## Overview

The `quotation` skill provides a unified interface for viAct proposal generation, orchestrating the end-to-end workflow from Deal Transfer Excel to final PowerPoint presentation.

## Location

```
./quotation_skill/
├── SKILL.md                          # Main skill file (load this first)
├── scripts/                          # Helper scripts
│   ├── detect_workflow_state.py      # Detect current workflow state
│   ├── validate_template.py          # Validate template for completeness
│   └── update_template_from_checklist.py  # Update template with confirmed values
├── references/                       # Detailed documentation
│   ├── workflow.md                   # Complete workflow guide
│   ├── placeholder_pattern.md        # Placeholder format and conventions
│   └── validation_rules.md           # Validation checklists
└── assets/                           # Static assets (currently empty)
```

## Three Workflow States

### State 1: Initial Generation (Excel → Template)
**Input**: Deal Transfer Excel file
**Output**: template.md, reasoning.md, checklist.md
**Trigger**: User provides Excel file

### State 2: Template Update (Checklist → Template)
**Input**: template.md + checklist.md (with presale answers)
**Output**: template_updated.md (no placeholders)
**Trigger**: User provides updated checklist

### State 3: Slide Generation (Template → PowerPoint)
**Input**: Clean template.md (no placeholders)
**Output**: proposal.pptx
**Trigger**: User confirms template ready

## Quick Commands

### Detect Workflow State
```bash
python scripts/detect_workflow_state.py [directory]
```

### Validate Template
```bash
python scripts/validate_template.py <template.md>
# Exit codes: 0 = clean, 1 = has placeholders, 2 = has issues
```

### Update Template from Checklist
```bash
python scripts/update_template_from_checklist.py <template.md> <checklist.md> [output.md]
```

### Check for Placeholders
```bash
grep -r "\[.*_.*\]" template_file.md
```

## Leveraging Existing Skills

This skill orchestrates two existing skills:

### dealtransfer2template
**Location**: `../dealtransfer2template/`
**Purpose**: Generate proposal from Deal Transfer Excel
**Use**: State 1 - Initial generation

### template2slide
**Location**: `~/.claude/skills/template2slide/`
**Purpose**: Generate PowerPoint from template
**Use**: State 3 - Slide generation

## Key Features

### Intelligent State Detection
Automatically detects current workflow state from available files

### Placeholder Pattern
Format: `[Estimated Value] [PLACEHOLDER_ID]`
- Shows estimates while flagging confirmation needs
- Example: `30 Mbps [NETWORK_001]`

### Progressive Disclosure
- SKILL.md: Quick overview and state detection
- references/workflow.md: Detailed workflow guide
- references/placeholder_pattern.md: Placeholder conventions
- references/validation_rules.md: Complete validation checklists

### Validation Automation
Scripts to validate templates, detect placeholders, and ensure completeness

## Usage Examples

### Example 1: Start from Excel
```bash
# User provides DT_0109.xlsx
# Skill detects State 1
# Generates: template.md, reasoning.md, checklist.md
```

### Example 2: Update Template
```bash
# User provides template.md + updated checklist.md
# Skill detects State 2
# Runs: update_template_from_checklist.py
# Outputs: template_updated.md (no placeholders)
```

### Example 3: Generate Slides
```bash
# User provides clean template.md
# Skill detects State 3
# Runs: template2slide skill
# Outputs: proposal.pptx
```

## Important Notes

1. **No Code Duplication**: Leverages existing dealtransfer2template and template2slide skills
2. **Orchestration Layer**: Adds workflow intelligence and validation on top
3. **State Management**: Tracks workflow state and routes to appropriate actions
4. **Validation First**: Always validates before proceeding to next state

## Next Steps

1. **Review SKILL.md** - Main entry point with state detection logic
2. **Run detect_workflow_state.py** - See current state
3. **Follow workflow.md** - Detailed step-by-step guide
4. **Validate before proceeding** - Use validation scripts at each transition

## Troubleshooting

### "Which state am I in?"
Run: `python scripts/detect_workflow_state.py`

### "Template has placeholders"
Run: `python scripts/update_template_from_checklist.py`

### "Is template ready for slides?"
Run: `python scripts/validate_template.py <template.md>`

### "Where are the detailed docs?"
See: `references/workflow.md` for complete workflow guide

## Architecture

```
quotation_skill (orchestration layer)
    ├── State detection logic
    ├── Validation scripts
    └── Workflow guidance
        ↓
    ├── dealtransfer2template (existing skill)
    │   └── Excel → Template generation
    └── template2slide (existing skill)
        └── Template → PowerPoint generation
```

## File Locations

- **Current workdir**: `./quotation_skill/`
- **dealtransfer2template**: `../dealtransfer2template/`
- **template2slide**: `~/.claude/skills/template2slide/`

## Summary

The `quotation` skill unifies the proposal generation workflow by:
1. Detecting current state from available files
2. Routing to appropriate existing skills
3. Validating outputs at each transition
4. Providing clear guidance for next steps

**No code duplication** - orchestrates existing skills intelligently.
