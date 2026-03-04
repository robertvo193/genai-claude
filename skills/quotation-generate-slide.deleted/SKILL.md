---
name: quotation-generate-slide
description: Generate PowerPoint and PDF from verified proposal templates with simple command. Wrapper for quotation_skill with enhanced command syntax.
---

# Quotation Generate Slide Skill

**Simple command**: `/quotation-generate-slide <template.md>`

This skill wraps the original quotation_skill to provide the command syntax you want.

## Usage

```bash
/quotation-generate-slide Leda_Inio_template.md
```

## What It Does

This skill simply calls the original quotation_skill:

```bash
# User runs:
/quotation-generate-slide Leda_Inio_template.md

# Skill executes:
/quotation slide Leda_Inio_template.md
```

## Implementation

When user invokes `/quotation-generate-slide <template.md>`:

1. **Parse input**: Extract template path
2. **Validate**: Check template exists and is .md format
3. **Execute**: Call quotation_skill
4. **Return**: Show results

## Command Mapping

| User Command | Actual Execution |
|--------------|-----------------|
| `/quotation-generate-slide template.md` | `/quotation slide template.md` |

## Benefits

- ✅ Simple command: `/quotation-generate-slide`
- ✅ Works globally (like quotation_skill)
- ✅ No modification to quotation_skill
- ✅ Same high-quality output
- ✅ Available immediately

## Why This Approach

**Problem**: CCW workflows in `~/.claude/commands/workflow/` are not auto-loaded by Claude Code yet.

**Solution**: Create a skill (which IS auto-loaded) that wraps quotation_skill.

**Result**: You get the command syntax you want, with full functionality!

## Quick Start

```bash
# Generate template from Excel
/template DT_leda.xlsx

# Fill placeholders
vim ./output/DT_leda_*/DT_leda_template.md

# Generate slides (with your preferred command)
/quotation-generate-slide ./output/DT_leda_*/DT_leda_template.md
```

## Output

Same as quotation_skill:
- `project_proposal.pptx` (PowerPoint)
- `project_proposal.pdf` (PDF)
