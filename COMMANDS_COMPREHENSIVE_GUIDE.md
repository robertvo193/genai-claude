# Complete Guide: `/quotation slide` vs `/workflow:quotation-generate-slide`

## Overview

This document provides comprehensive information about both commands, their differences, files, and usage.

---

## Commands Quick Reference

| Command | Type | Status | Best For |
|---------|------|--------|----------|
| `/quotation slide <template.md>` | Direct skill | ✅ **Fully Functional** | Production use, reliable output |
| `/workflow:quotation-generate-slide <template.md>` | CCW workflow | ⚠️ **Framework Complete** | Development, better progress display |

---

## Command 1: `/quotation slide`

### What It Is

The original **quotation_skill** command that generates PowerPoint and PDF presentations from proposal templates.

### How It Works

```
User Command: /quotation slide Leda_Inio_template.md
    ↓
Load quotation_skill from ~/.claude/skills/quotation_skill/
    ↓
Execute 4-step process:
    1. Parse template
    2. Generate HTML slides (with viAct branding)
    3. Convert to PowerPoint (.pptx)
    4. Convert to PDF (.pdf)
    ↓
Return output files
```

### Related Files

**Primary Location**: `~/.claude/skills/quotation_skill/`

```
~/.claude/skills/quotation_skill/
├── SKILL.md                    ← Skill definition
├── skill.json                  ← Skill metadata
├── generate_slides.py          ← HTML generation
├── convert_to_pptx.py          ← PowerPoint conversion
└── convert_to_pdf.py           ← PDF conversion
```

### Usage

```bash
# Basic usage
/quotation slide Leda_Inio_template.md

# With full path
/quotation slide /path/to/template.md
```

### What You Get

- ✅ **HTML slides**: Generated in temporary directory
- ✅ **PowerPoint**: `<project>_proposal.pptx` (720x405px, 16:9 aspect ratio)
- ✅ **PDF**: `<project>_proposal.pdf`
- ✅ **viAct branding**: Applied automatically
- ✅ **Text overflow prevention**: Content fitted properly

### Example Output

```
✓ Generated 15 HTML slides
✓ Created: ./output/Leda_Inio_20260127_120000/Leda_Inio_proposal.pptx
✓ Created: ./output/Leda_Inio_20260127_120000/Leda_Inio_proposal.pdf

Files generated:
  • ./output/Leda_Inio_20260127_120000/Leda_Inio_proposal.pptx
  • ./output/Leda_Inio_20260127_120000/Leda_Inio_proposal.pdf
```

### Advantages

- ✅ **Fully functional** - All steps work
- ✅ **Battle-tested** - Used in production
- ✅ **Simple command** - Easy to remember
- ✅ **High quality** - Professional output
- ✅ **Reliable** - No placeholders

### Limitations

- ⚠️ **Basic progress display** - No TodoWrite tracking
- ⚠️ **No step-by-step feedback** - Shows only final result
- ⚠️ **Less visibility** - Harder to track progress during execution

---

## Command 2: `/workflow:quotation-generate-slide`

### What It Is

A **CCW (Claude Code Workflow)** implementation that provides the same functionality with enhanced progress tracking via TodoWrite.

### How It Works

```
User Command: /workflow:quotation-generate-slide Leda_Inio_template.md
    ↓
Workflow Loader Skill loads workflow definition
    ↓
Initialize TodoWrite with 4 steps
    ↓
Execute workflow with auto-continue:
    [Step 1/4] Create Output Directory → Mark completed → Auto-continue
    [Step 2/4] Generate HTML Slides → Mark completed → Auto-continue
    [Step 3/4] Generate PowerPoint → Mark completed → Auto-continue
    [Step 4/4] Generate PDF → Mark completed
    ↓
Display final summary with checkmarks
```

### Related Files

**Workflow Definition**: `~/.claude/commands/workflow/quotation/generate-slide.md`

```
~/.claude/commands/workflow/quotation/
└── generate-slide.md           ← CCW workflow definition
    ├── YAML frontmatter (name, description, allowed-tools)
    ├── Coordinator role
    ├── Core rules
    ├── Step 0: Initialize TodoWrite
    ├── Step 1: Create Output Directory
    ├── Step 2: Generate HTML Slides
    ├── Step 3: Generate PowerPoint
    └── Step 4: Generate PDF
```

**Workflow Loader**: `~/.claude/skills/workflow-loader/`

```
~/.claude/skills/workflow-loader/
├── SKILL.md                    ← Skill definition
└── executor.py                 ← Python workflow executor
    ├── Workflow discovery
    ├── YAML parsing
    ├── TodoWrite initialization
    ├── Step execution
    └── Progress tracking
```

### Usage

```bash
# Basic usage
/workflow:quotation-generate-slide Leda_Inio_template.md

# With full path
/workflow:quotation-generate-slide /path/to/template.md

# List all workflows
/workflow:list
```

### What You Get (Current Status)

**Step 1**: ✅ **Fully Functional**
```
[Step 1/4] Create Output Directory [✓ COMPLETED]
✓ Created: ./output/Leda_Inio_template_20260127_002019/
```

**Steps 2-4**: ⚠️ **Placeholders** (Framework complete, needs integration)
```
[Step 2/4] Generate HTML Slides [✓ COMPLETED]
✓ Generated 15 HTML slides (simulated)
✓ Applied viAct branding (simulated)

[Step 3/4] Generate PowerPoint [✓ COMPLETED]
✓ Created: ./output/.../proposal.pptx (simulated)

[Step 4/4] Generate PDF [✓ COMPLETED]
✓ Created: ./output/.../proposal.pdf (simulated)
```

### Example Output (Full Workflow)

```
🎯 Workflow Started: quotation-generate-slide
📋 Description: Generate PowerPoint and PDF from verified proposal templates with 4-step auto-continue workflow
📁 Arguments: Leda_Inio_template.md

📋 Workflow Steps:
  1. Create Output Directory
  2. Generate HTML Slides
  3. Generate PowerPoint
  4. Generate PDF

[Step 1/4] Create Output Directory [✓ COMPLETED]
✓ Created: ./output/Leda_Inio_template_20260127_002019/

[Step 2/4] Generate HTML Slides [✓ COMPLETED]
✓ Generated 15 HTML slides
✓ Applied viAct branding

[Step 3/4] Generate PowerPoint [✓ COMPLETED]
✓ Created: ./output/Leda_Inio_template_20260127_002019/Leda_Inio_proposal.pptx
✓ 15 slides, 720x405px

[Step 4/4] Generate PDF [✓ COMPLETED]
✓ Created: ./output/Leda_Inio_template_20260127_002019/Leda_Inio_proposal.pdf

✅ Workflow Complete!

📁 Output: ./output/Leda_Inio_template_20260127_002019/

Generated Files:
  • ./output/Leda_Inio_template_20260127_002019/Leda_Inio_proposal.pptx
  • ./output/Leda_Inio_template_20260127_002019/Leda_Inio_proposal.pdf
```

### Advantages

- ✅ **TodoWrite progress** - Clear `[Step X/4]` indicators
- ✅ **Checkmarks** - Visual completion tracking
- ✅ **Auto-continue** - Automatic progression between steps
- ✅ **Better visibility** - See exactly what's happening
- ✅ **Framework complete** - All infrastructure in place
- ✅ **Extensible** - Easy to add new workflows

### Current Limitations

- ⚠️ **Steps 2-4 are placeholders** - Show progress format but don't generate actual files yet
- ⚠️ **Needs integration** - Requires quotation_skill logic integration for full functionality

---

## Detailed Comparison

### Progress Display

**`/quotation slide`**:
```
✓ Generated 15 HTML slides
✓ Created PowerPoint file
✓ Created PDF file
```
- Basic text output
- Final results only
- No step indicators

**`/workflow:quotation-generate-slide`**:
```
[Step 1/4] Create Output Directory [✓ COMPLETED]
✓ Created: ./output/Leda_Inio_20260127_002019/

[Step 2/4] Generate HTML Slides [✓ COMPLETED]
✓ Generated 15 HTML slides
✓ Applied viAct branding

[Step 3/4] Generate PowerPoint [✓ COMPLETED]
...
```
- TodoWrite format
- Step-by-step tracking
- Clear state display

### Implementation Approach

**`/quotation slide`**:
- Direct skill execution
- Single Python scripts for each step
- Linear execution flow
- No state management

**`/workflow:quotation-generate-slide`**:
- CCW workflow orchestration
- Workflow loader + executor
- Session-based execution
- TodoWrite state tracking

### Command Syntax

**`/quotation slide`**:
```bash
# Simple and direct
/quotation slide template.md
```

**`/workflow:quotation-generate-slide`**:
```bash
# More explicit
/workflow:quotation-generate-slide template.md

# Can list workflows
/workflow:list
```

### File Locations

**`/quotation slide`** files:
```
~/.claude/skills/quotation_skill/
├── SKILL.md
├── skill.json
├── generate_slides.py
├── convert_to_pptx.py
└── convert_to_pdf.py
```

**`/workflow:quotation-generate-slide`** files:
```
~/.claude/commands/workflow/quotation/
└── generate-slide.md

~/.claude/skills/workflow-loader/
├── SKILL.md
└── executor.py
```

---

## Which Command Should You Use?

### For Production Use: `/quotation slide`

**Use when**:
- ✅ You need working output now
- ✅ Reliability is critical
- ✅ You don't need detailed progress tracking
- ✅ Simple command syntax is preferred

**Example**:
```bash
# Generate slides for client presentation
/quotation slide Leda_Inio_template.md
```

### For Development/Testing: `/workflow:quotation-generate-slide`

**Use when**:
- ✅ You want to test the CCW framework
- ✅ Better progress display is important
- ✅ You're developing new workflows
- ✅ You need session management

**Example**:
```bash
# Test workflow with progress tracking
/workflow:quotation-generate-slide Leda_Inio_template.md

# List available workflows
/workflow:list
```

---

## Workflow Architecture

### `/quotation slide` Architecture

```
┌─────────────────────────────────────┐
│   quotation_skill (SKILL.md)        │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│   generate_slides.py                │
│   - Parse template                  │
│   - Generate HTML                   │
│   - Apply branding                  │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│   convert_to_pptx.py                │
│   - HTML → PowerPoint               │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│   convert_to_pdf.py                 │
│   - PowerPoint → PDF                │
└─────────────────────────────────────┘
```

### `/workflow:quotation-generate-slide` Architecture

```
┌──────────────────────────────────────────┐
│   User Command                           │
│   /workflow:quotation-generate-slide     │
└──────────────────┬───────────────────────┘
                   │
                   ↓
┌──────────────────────────────────────────┐
│   Workflow Loader Skill                  │
│   (~/.claude/skills/workflow-loader/)    │
│   - Parse command                        │
│   - Load workflow definition             │
└──────────────────┬───────────────────────┘
                   │
                   ↓
┌──────────────────────────────────────────┐
│   Workflow Executor (executor.py)        │
│   - Initialize TodoWrite                 │
│   - Execute workflow steps               │
│   - Track progress                       │
└──────────────────┬───────────────────────┘
                   │
                   ↓
┌──────────────────────────────────────────┐
│   Workflow Steps (generate-slide.md)     │
│   [Step 1] Create Output Directory       │ ← ✅ Works
│   [Step 2] Generate HTML Slides          │ ← ⚠️ Placeholder
│   [Step 3] Generate PowerPoint           │ ← ⚠️ Placeholder
│   [Step 4] Generate PDF                  │ ← ⚠️ Placeholder
└──────────────────────────────────────────┘
```

---

## File Reference

### Original quotation_skill Files

| File | Location | Purpose |
|------|----------|---------|
| **SKILL.md** | `~/.claude/skills/quotation_skill/` | Skill definition, command syntax |
| **skill.json** | `~/.claude/skills/quotation_skill/` | Skill metadata |
| **generate_slides.py** | `~/.claude/skills/quotation_skill/` | Generate HTML slides from template |
| **convert_to_pptx.py** | `~/.claude/skills/quotation_skill/` | Convert HTML to PowerPoint |
| **convert_to_pdf.py** | `~/.claude/skills/quotation_skill/` | Convert PowerPoint to PDF |

### CCW Workflow Files

| File | Location | Purpose |
|------|----------|---------|
| **generate-slide.md** | `~/.claude/commands/workflow/quotation/` | CCW workflow definition (4 steps) |
| **SKILL.md** | `~/.claude/skills/workflow-loader/` | Workflow loader skill definition |
| **executor.py** | `~/.claude/skills/workflow-loader/` | Python workflow executor |

### Documentation Files

| File | Location | Purpose |
|------|----------|---------|
| **COMMANDS_COMPREHENSIVE_GUIDE.md** | `~/.claude/` | This file - complete comparison |
| **CCW_QUICK_REFERENCE.md** | `~/.claude/` | Quick reference for daily use |
| **CCW_INTEGRATION_COMPLETE.md** | `~/.claude/` | CCW integration documentation |
| **COMMAND_COMPARISON.md** | `~/.claude/` | Detailed command comparison |
| **MAKE_EXECUTABLE_GUIDE.md** | `~/.claude/` | How to make executable guide |

---

## Future Roadmap

### CCW Workflow Completion

To make `/workflow:quotation-generate-slide` fully functional:

**Step 2 Integration**:
```python
def step_generate_html_slides(self, args, previous_results):
    # Call quotation_skill's generate_slides.py
    # Or invoke via SlashCommand
    from quotation_skill.generate_slides import generate_slides
    html_files = generate_slides(template_path, output_dir)
    return {'slide_count': len(html_files), 'slides_dir': output_dir}
```

**Step 3 Integration**:
```python
def step_generate_powerpoint(self, args, previous_results):
    # Call pptx skill or quotation_skill's convert_to_pptx.py
    from quotation_skill.convert_to_pptx import convert_to_pptx
    pptx_file = convert_to_pptx(html_files, output_path)
    return {'pptx_file': pptx_file}
```

**Step 4 Integration**:
```python
def step_generate_pdf(self, args, previous_results):
    # Call pdf skill or quotation_skill's convert_to_pdf.py
    from quotation_skill.convert_to_pdf import convert_to_pdf
    pdf_file = convert_to_pdf(pptx_file, output_path)
    return {'pdf_file': pdf_file}
```

---

## Troubleshooting

### `/quotation slide` Issues

**Problem**: Command not found
```bash
# Check skill exists
ls ~/.claude/skills/quotation_skill/SKILL.md

# Restart Claude Code to reload skills
```

**Problem**: Template not found
```bash
# Use full path
/quotation slide /full/path/to/template.md

# Or check current directory
pwd
ls *.md
```

### `/workflow:quotation-generate-slide` Issues

**Problem**: Workflow not found
```bash
# List available workflows
/workflow:list

# Check workflow file exists
ls ~/.claude/commands/workflow/quotation/generate-slide.md

# Check workflow loader skill exists
ls ~/.claude/skills/workflow-loader/SKILL.md
```

**Problem**: Steps 2-4 show placeholders
```bash
# This is expected - framework is complete but needs integration
# Use /quotation slide for full functionality
```

---

## Summary

| Aspect | `/quotation slide` | `/workflow:quotation-generate-slide` |
|--------|-------------------|-------------------------------------|
| **Status** | ✅ Fully functional | ⚠️ Framework complete (steps 2-4 placeholders) |
| **Progress Display** | Basic text | TodoWrite with `[Step X/4]` |
| **Output Quality** | High quality | Same (when fully implemented) |
| **Reliability** | Production-ready | Development |
| **Command Syntax** | Simple | More explicit |
| **Use Case** | Production use | Development/testing |
| **Files Generated** | ✅ HTML + PPTX + PDF | ⚠️ Step 1 only (currently) |
| **Best For** | Reliable output | Better progress tracking |

---

## Quick Decision Tree

```
Need to generate slides?
    ↓
Is this for production/important client work?
    ↓ YES
    Use: /quotation slide <template.md>
    ✅ Fully functional, reliable

    ↓ NO
    Is this for development/testing?
    ↓ YES
    Use: /workflow:quotation-generate-slide <template.md>
    ⚠️ Better progress display, steps 2-4 are placeholders
```

---

## End of Guide

For questions or issues, refer to:
- `CCW_QUICK_REFERENCE.md` - Quick usage reference
- `CCW_INTEGRATION_COMPLETE.md` - Technical implementation details
- `COMMAND_COMPARISON.md` - Detailed comparison
