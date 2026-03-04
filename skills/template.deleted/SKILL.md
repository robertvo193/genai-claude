---
name: template
description: Generate proposal templates from Deal Transfer Excel files. Extracts data from Commercial and Technical sheets, maps pain points to AI modules, and generates 3 files: template (client-facing proposal), reasoning (audit trail), and checklist (placeholders for presale). Use when: Converting Deal Transfer Excel to proposal templates, starting new proposal creation, or extracting data from deal sheets.
---

# Template Skill

## Overview

**Single Purpose**: Convert Deal Transfer Excel files → Proposal templates

Automated extraction and generation system that reads Deal Transfer Excel files and creates professional proposal templates with complete audit trails.

**Input**: Deal Transfer Excel file (.xlsx format)
**Output**: 3 files (template, reasoning, checklist)

## Workflow

```
Deal Transfer Excel (dealA.xlsx)
    ↓
[Step 0] Initialize & Validate
    - Check file exists and is .xlsx format
    - Verify Commercial/S1 sheet exists
    - Verify Technical/S2 sheet exists
    ↓
[Step 1] Extract Deal Transfer Data
    - Parse Commercial sheet (customer, pain points, timeline, budget)
    - Parse Technical sheet (use cases, cameras, deployment)
    - Map pain points → AI modules automatically
    - Identify standard vs custom modules
    ↓
[Step 2] Generate Template File
    - Fill 12 sections from extracted data
    - Create Project Requirement Statement
    - Add placeholders for missing information
    - Output: ./output/[Project]_[Timestamp]/[Project]_template.md
    ↓
[Step 3] Generate Reasoning File
    - Document all data sources (S1/S2 row references)
    - Explain AI module mapping logic
    - Show all calculations and estimates
    - Output: ./output/[Project]_[Timestamp]/[Project]_reasoning.md
    ↓
[Step 4] Generate Checklist File
    - List all placeholders in table format
    - Columns: ID | Section | Item | Estimated | Answer
    - Output: ./output/[Project]_[Timestamp]/[Project]_checklist.md
    ↓
[Complete] 3 files ready for presale review
```

## Output Directory Structure

```
./output/
└── [Project]_[Timestamp]/
    ├── [Project]_template.md       (12 sections, client-facing)
    ├── [Project]_reasoning.md      (complete audit trail)
    └── [Project]_checklist.md      (placeholders to fill)
```

## Usage

### Basic Usage

```bash
/template dealA.xlsx
```

### With Path

```bash
/template /path/to/excel/dealA.xlsx
```

### How It Works

1. **User invokes**: `/template dealA.xlsx`
2. **Skill parses**: Extract Excel file path from arguments
3. **Validate**: Check file format and sheets
4. **Execute**: Run Python generator script
5. **Output**: Show generated files with statistics

## What Gets Extracted

### From Commercial Sheet (S1)

| Row | Field | Example |
|-----|-------|---------|
| 1 | Customer Overview | "Cedo Vietnam - manufacturing arm..." |
| 2 | Customer Type | "End-customer" |
| 5 | Pain Points | "Manual safety monitoring inefficient..." |
| 6 | Project Status | "Real project" |
| 7 | Timeline | "Site survey Jan 2026 → Q1/2026" |
| 8 | Budget | "Not disclosed" |
| 11 | Camera Status | "17 cameras (9 VN1 + 8 VN2)" |

### From Technical Sheet (S2)

| Row | Field | Example |
|-----|-------|---------|
| 1 | Use Cases | "PPE detection, proximity detection" |
| 2 | Alert Method | "Local speaker at site" |
| 5 | Camera Details | "Verkada CD41, 1080p, 10fps" |
| 8 | Deployment | "Cloud-based for PoC" |

### AI Module Mapping (Automatic)

The skill intelligently maps pain point keywords to AI modules:

| Pain Point Keywords | AI Module | Type |
|---------------------|-----------|------|
| helmet, safety | Safety Helmet Detection | Standard |
| vest | Safety Vest Detection | Standard |
| mask | Safety Mask Detection | Standard |
| fire, smoke | Fire & Smoke Detection | Standard |
| intrusion, unauthorized | Intrusion Detection | Standard |
| vehicle | Vehicle Detection | Standard |
| custom patterns | Custom Module | Custom |

## Output Examples

### Template File Structure

```markdown
# Technical Proposal

## 1. Project Requirement Statement
**Project:** AI-Powered Video Analytics for Manufacturing
**Project Owner:** Cedo Vietnam
**Camera Number:** 17 cameras
**AI Modules:**
1. Safety Helmet Detection

## 2. Current Situation & Pain Points
[Customer info + pain points extracted from Excel]

## 3-12. [Other sections with placeholders]
[Value] [PLACEHOLDER_001: Hardware specifications]
[Value] [PLACEHOLDER_002: Storage requirements]
```

### Reasoning File Structure

```markdown
# Reasoning and Audit Trail

## Data Sources
### S1 (Commercial) Sheet
- Customer Name: "Cedo Vietnam" (S1, Row 1)
- Pain Points: "Manual safety..." (S1, Row 5)
- Timeline: "Q1/2026" (S1, Row 7)

### S2 (Technical) Sheet
- Use Cases: "PPE detection..." (S2, Row 1)
- Camera Details: "Verkada CD41..." (S2, Row 5)

## AI Module Mapping
**Pain Points:** Manual safety monitoring...
**Mapping Logic:**
- Pain points → AI modules: Safety Helmet Detection
- Standard modules: 1
- Custom modules: 0
```

### Checklist File Structure

```markdown
# Placeholder Checklist

| ID | Section | Item | Content Estimated | Presale's Answer |
|----|---------|------|-------------------|------------------|
| 001 | Hardware specifications | | | |
| 002 | Storage requirements | | | |
| 003 | Bandwidth requirements | | | |
```

## Error Handling

| Error | Message | Solution |
|-------|---------|----------|
| File not found | `❌ Excel file not found: dealA.xlsx` | Show current directory and available .xlsx files |
| Invalid format | `❌ File must be .xlsx format (not .xls)` | Suggest conversion with LibreOffice |
| S1 missing | `❌ Commercial sheet not found` | Verify Excel has "Commercial" or "S1" sheet |
| S2 missing | `❌ Technical sheet not found` | Verify Excel has "Technical" or "S2" sheet |
| Python error | `❌ Script execution failed` | Show error + suggest `pip install pandas openpyxl` |

## Integration with Quotation Skill

Complete proposal generation pipeline:

```bash
# Step 1: Generate template from Excel
/template dealA.xlsx

# Step 2: Review and fill checklist
cat ./output/dealA_*/dealA_checklist.md

# Step 3: Edit template (fill placeholders)
vim ./output/dealA_*/dealA_template.md
# Replace [Value] [PLACEHOLDER_XXX] with actual values

# Step 4: Generate PowerPoint + PDF
/quotation slide ./output/dealA_*/dealA_template.md

# Output: dealA_proposal.pptx + dealA_proposal.pdf ✅
```

## Implementation Details

### Python Script Location

`~/.claude/skills/dealtransfer2template/bin/generate_template.py`

### Script Execution

```bash
python3 ~/.claude/skills/dealtransfer2template/bin/generate_template.py <excel_file.xlsx>
```

### Output Format

The script returns:
1. Colored terminal output (step-by-step progress)
2. JSON output (for programmatic use)
3. Exit code (0 = success, 1 = error)

## Requirements

- Python 3.6+
- pandas library: `pip install pandas`
- openpyxl library: `pip install openpyxl`
- Excel file in .xlsx format
- Sheets: "Commercial" (or S1) and "Technical" (or S2)

## Quick Reference Card

### Command
```bash
/template <excel_file.xlsx>
```

### Expected Input
- ✅ .xlsx format (not .xls)
- ✅ Commercial sheet (or S1)
- ✅ Technical sheet (or S2)
- ✅ Row-based structure (Question/Answer pairs)

### Output
- ✅ 3 files in `./output/<project>_<timestamp>/`
- ✅ Template: 12 sections with placeholders
- ✅ Reasoning: Complete audit trail
- ✅ Checklist: Table format for presale

## Next Steps After Template Generation

1. 📋 **Review Checklist**
   ```bash
   cat ./output/dealA_*/dealA_checklist.md
   ```

2. ✏️ **Fill Placeholders**
   - Work with presales team
   - Confirm pricing, hardware, timeline
   - Fill in "Presale's Answer" column

3. 📝 **Update Template**
   - Replace `[Value] [PLACEHOLDER_XXX]` with confirmed values
   - Remove all placeholders
   - Save as verified template

4. 🎨 **Generate Slides**
   ```bash
   /quotation slide ./output/dealA_*/dealA_template.md
   ```

5. 📤 **Deliver to Client**
   - PowerPoint presentation ready
   - PDF document ready

## Example Session

```bash
$template DT_cedo.xlsx

🎯 Template Generation Started
📁 Excel: DT_cedo.xlsx
📊 Project: DT_cedo

[Step 1/5] Validate Excel File [✓ COMPLETED]
✓ File exists: DT_cedo.xlsx
✓ Valid Excel format (.xlsx)
✓ S1 (Commercial) sheet found
✓ S2 (Technical) sheet found

[Step 2/5] Extract Deal Transfer Data [✓ COMPLETED]
✓ Extracted 14 rows from S1 sheet
✓ Extracted 14 rows from S2 sheet
✓ Mapped pain points → 1 AI modules
✓ Identified: 1 standard modules, 0 custom modules

[Step 3/5] Generate Template File [✓ COMPLETED]
✓ Filled 12 sections
✓ Created 8 placeholders for missing info

[Step 4/5] Generate Reasoning File [✓ COMPLETED]
✓ Documented all S1/S2 sources
✓ Complete audit trail

[Step 5/5] Generate Checklist File [✓ COMPLETED]
✓ Listed 8 placeholders
✓ Ready for presale review

✅ Template Generation Complete!

Output Files:
  • ./output/DT_cedo_20260126_230000/DT_cedo_template.md
  • ./output/DT_cedo_20260126_230000/DT_cedo_reasoning.md
  • ./output/DT_cedo_20260126_230000/DT_cedo_checklist.md

📊 Statistics:
  • S1 rows extracted: 14
  • S2 rows extracted: 14
  • AI modules mapped: 1
  • Placeholders created: 8

Next Steps:
  1. Review DT_cedo_checklist.md
  2. Fill presale answers for placeholders
  3. Update template with confirmed values
  4. Generate slides: /quotation slide DT_cedo_template.md
```

## Summary

**Single Command**:
```bash
/template dealA.xlsx
```

**Automatic Processing**:
- ✅ Data extraction (14+ fields)
- ✅ AI module mapping (intelligent)
- ✅ Template generation (12 sections)
- ✅ Audit trail (complete)
- ✅ Checklist creation (presale-ready)

**No Python Required** - Just one simple command! ✅
