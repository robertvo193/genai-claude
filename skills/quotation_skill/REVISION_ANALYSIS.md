# Quotation Skill - Revision Analysis

## What Needs to Change

### ❌ Remove (Related to dealtransfer2template)

1. **State 1 Details** (Lines 16-27)
   - Remove: "Extract data from Deal Transfer (S1: Commercial, S2: Technical)"
   - Remove: Details about template, reasoning, checklist generation
   - **Reason**: This is dealtransfer2template's responsibility

2. **State 2 Details** (Lines 29-38)
   - Remove: Placeholder replacement logic
   - Remove: Template update process
   - **Reason**: This is dealtransfer2template's responsibility

3. **Scripts Directory**
   - Remove: `detect_workflow_state.py` (State detection logic)
   - Remove: `validate_template.py` (Template validation)
   - Remove: `update_template_from_checklist.py` (Placeholder replacement)
   - **Reason**: These implement dealtransfer2template logic

4. **Reference Files**
   - Remove: `placeholder_pattern.md` (Placeholder format from dealtransfer2template)
   - Remove: `validation_rules.md` (Template validation from dealtransfer2template)
   - Remove: `workflow.md` (Detailed State 1-2 workflows from dealtransfer2template)
   - **Reason**: These document dealtransfer2template implementation

5. **Quick Start Commands** (Lines 72-81)
   - Remove: State 1 and State 2 commands
   - Keep: State 3 commands (pptx/pdf only)

6. **Intermediate Files** (Lines 83-125)
   - Remove: `workflow_state.md` (State tracking for State 1-2)
   - Remove: `slide_mapping.md` (Template → slides planning)
   - **Reason**: These are dealtransfer2template artifacts

### ✅ Keep (Focus on pptx/pdf skills only)

1. **State 3 Only** (Output Generation)
   - Focus on: Template → PowerPoint → PDF
   - Input: Verified proposal template (no placeholders)
   - Output: PPTX + PDF

2. **pptx Skill Integration**
   - Keep: References to pptx skill
   - Keep: html2pptx workflow guidance
   - Keep: Design principles (viAct branding)

3. **pdf Skill Integration**
   - Keep: References to pdf skill
   - Keep: PPTX → PDF conversion guidance

4. **Assets**
   - Keep: `background.png` (viAct slide background)

5. **Minimal Reference Files**
   - Keep: `pptx_workflow.md` (PowerPoint generation)
   - Keep: `pdf_workflow.md` (PDF generation)

## Revised Scope

### Before (Too Broad)
- State 1: Content generation (dealtransfer2template)
- State 2: Review workflow (dealtransfer2template)
- State 3: Output generation (pptx + pdf)

### After (Focused)
- **Single Purpose**: Convert verified proposal template → PowerPoint → PDF
- **Input**: Verified template (markdown, no placeholders)
- **Output**: PPTX + PDF
- **Leverages**: pptx skill, pdf skill

## High-Level Workflow (Revised)

```
Proposal Template (verified)
    ↓
[Step 1] Generate PowerPoint
    - Use pptx skill (html2pptx workflow)
    - Apply viAct branding
    - Output: .pptx
    ↓
[Step 2] Generate PDF
    - Use pdf skill (PPTX → PDF)
    - Output: .pdf
    ↓
[Complete] Both outputs ready
```

## What quotation_skill Should Be

**High-level orchestration layer** that:
1. Accepts verified proposal template (no implementation details of how it was created)
2. Generates PowerPoint using pptx skill
3. Generates PDF using pdf skill
4. Provides design guidance (viAct branding)

**NOT**:
- Deal Transfer Excel processing
- Template generation
- Placeholder management
- Presale review workflow
- State detection logic

## Files to Delete

```
quotation_skill/
├── scripts/
│   ├── detect_workflow_state.py      ❌ DELETE
│   ├── validate_template.py          ❌ DELETE
│   └── update_template_from_checklist.py  ❌ DELETE
└── references/
    ├── workflow.md                   ❌ DELETE (State 1-2 details)
    ├── placeholder_pattern.md        ❌ DELETE (dealtransfer2template)
    └── validation_rules.md           ❌ DELETE (dealtransfer2template)
```

## Files to Keep and Revise

```
quotation_skill/
├── SKILL.md                          ✅ KEEP (revise to State 3 only)
├── README.md                         ✅ KEEP (update scope)
├── QUICK_START.md                    ✅ KEEP (simplify)
├── assets/
│   ├── background.png                ✅ KEEP
│   └── README.md                     ✅ KEEP (update)
└── references/
    ├── pptx_workflow.md              ✅ KEEP (PowerPoint guidance)
    └── pdf_workflow.md               ✅ KEEP (PDF guidance)
```

## New SKILL.md Structure

```markdown
# Quotation Skill

## Overview
Convert verified proposal templates to final presentations (PDF + PowerPoint)

## Workflow
1. Input: Verified proposal template (markdown, no placeholders)
2. Generate PowerPoint (using pptx skill)
3. Generate PDF (using pdf skill)

## Leveraging Skills
- pptx skill: HTML → PowerPoint conversion
- pdf skill: PPTX → PDF conversion

## Design Principles
- viAct branding: #00AEEF, Arial fonts
- Slide size: 720pt × 405pt (16:9)

## Quick Start
[Commands for pptx/pdf generation]

## Assets
- background.png for viAct branding

## References
- pptx_workflow.md
- pdf_workflow.md
```

## Summary

**Remove**: ~150 lines of dealtransfer2template logic
**Keep**: ~50 lines of pptx/pdf orchestration
**Focus**: High-level template → PPTX → PDF conversion only
