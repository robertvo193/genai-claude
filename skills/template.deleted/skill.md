# Template Generation Skill

**Generate proposal templates from Deal Transfer Excel files with one simple command**

## Quick Start

```bash
/template dealA.xlsx
```

That's it! No Python, no scripts, just one command.

---

## What It Does

When you run `/template dealA.xlsx`, the skill will:

1. ✅ Validate your Excel file
2. ✅ Extract data from Commercial & Technical sheets
3. ✅ Map pain points to AI modules automatically
4. ✅ Generate 3 files:
   - `dealA_template.md` - Proposal template
   - `dealA_reasoning.md` - Audit trail
   - `dealA_checklist.md` - Placeholders to fill

---

## Usage

### Basic Usage

```bash
/template <your_excel_file.xlsx>

# Examples
/template dealA.xlsx
/template DT_cedo.xlsx
/template /path/to/excel/DT_leda.xlsx
```

### What You Need

- Excel file in `.xlsx` format
- Sheets named "Commercial" (or S1) and "Technical" (or S2)
- That's it!

---

## Output

### Files Generated

```
./output/<project>_<timestamp>/
├── <project>_template.md       ← Your proposal (12 sections)
├── <project>_reasoning.md      ← Complete audit trail
└── <project>_checklist.md      ← Placeholders to fill
```

### Example Output

```
🎯 Template Generation Started
📁 Excel: dealA.xlsx
📊 Project: dealA

[Step 1/5] Validate Excel File [✓ COMPLETED]
✓ File exists: dealA.xlsx
✓ Valid Excel format (.xlsx)
✓ S1 (Commercial) sheet found
✓ S2 (Technical) sheet found

[Step 2/5] Extract Deal Transfer Data [✓ COMPLETED]
✓ Extracted 14 rows from S1 sheet
✓ Extracted 14 rows from S2 sheet
✓ Mapped pain points → 2 AI modules
✓ Identified: 2 standard modules, 0 custom modules

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
  • ./output/dealA_20260126_230000/dealA_template.md
  • ./output/dealA_20260126_230000/dealA_reasoning.md
  • ./output/dealA_20260126_230000/dealA_checklist.md
```

---

## What Gets Extracted Automatically

The skill automatically extracts and maps:

### From Commercial Sheet (S1)
- ✅ Customer name and overview
- ✅ Pain points
- ✅ Project timeline
- ✅ Budget information
- ✅ Stakeholders

### From Technical Sheet (S2)
- ✅ Use cases
- ✅ Camera details
- ✅ Deployment preference
- ✅ Network/hardware requirements

### AI Module Mapping (Automatic)
The skill intelligently maps pain points to AI modules:

| Pain Points | AI Module |
|-------------|-----------|
| helmet, safety | Safety Helmet Detection |
| vest | Safety Vest Detection |
| mask | Safety Mask Detection |
| fire, smoke | Fire & Smoke Detection |
| intrusion | Intrusion Detection |
| vehicle | Vehicle Detection |

---

## Complete Workflow

### From Excel to Final Proposal

```bash
# Step 1: Generate template
/template dealA.xlsx

# Step 2: Review checklist
cat ./output/dealA_*/dealA_checklist.md

# Step 3: Fill placeholders (edit template)
vim ./output/dealA_*/dealA_template.md
# Replace [Value] [PLACEHOLDER_XXX] with actual values

# Step 4: Generate PowerPoint + PDF
/quotation slide ./output/dealA_*/dealA_template.md

# Done! 🎉
```

---

## Common Errors & Solutions

### ❌ "Excel file not found: dealA.xlsx"

**Cause**: File doesn't exist in current directory

**Solution**:
```bash
# Check current directory
pwd

# Find your file
find ~ -name "dealA.xlsx" 2>/dev/null

# Use full path
/template /full/path/to/dealA.xlsx
```

### ❌ "File must be .xlsx format"

**Cause**: File is .xls (old format)

**Solution**:
```bash
# Convert to .xlsx
libreoffice --headless --convert-to xlsx dealA.xls
/template dealA.xlsx
```

### ❌ "S1 sheet not found"

**Cause**: Excel doesn't have required sheets

**Solution**: Ensure your Excel has sheets named:
- "Commercial" or "S1"
- "Technical" or "S2"

```bash
# Check your sheets
python3 -c "import pandas as pd; print(pd.ExcelFile('dealA.xlsx').sheet_names)"
```

---

## Quick Reference

### Command Structure
```bash
/template <excel_file.xlsx>
```

### Expected Excel Structure
- ✅ Commercial sheet (or S1)
- ✅ Technical sheet (or S2)
- ✅ Row-based format (Question/Answer pairs)

### Output Structure
```
./output/
└── <project>_<timestamp>/
    ├── <project>_template.md
    ├── <project>_reasoning.md
    └── <project>_checklist.md
```

---

## Tips

### Tip 1: Check File Before Running
```bash
# Verify file exists and format
file dealA.xlsx  # Should show "Excel 2007+"
```

### Tip 2: Find Latest Output
```bash
# Show most recent output
ls -td ./output/*/ | head -1
```

### Tip 3: Quick Preview
```bash
# Preview template
head -50 ./output/dealA_*/dealA_template.md

# View checklist
cat ./output/dealA_*/dealA_checklist.md
```

---

## Real Example

### Input: `DT_cedo.xlsx`

**Commercial Sheet**:
- Customer: Cedo Vietnam
- Pain Points: Manual safety monitoring inefficient
- Timeline: Q1/2026
- Cameras: 17 cameras (9 + 8)

**Technical Sheet**:
- Use Cases: PPE detection, proximity detection
- Deployment: Cloud-based

### Output: Generated Files

**`DT_cedo_template.md`**:
- Project: AI-Powered Video Analytics for Manufacturing
- Customer: Cedo Vietnam
- Cameras: 17 cameras
- AI Modules: Safety Helmet Detection
- 12 sections, 8 placeholders

**`DT_cedo_reasoning.md`**:
- All sources documented
- AI module mapping explained
- Complete audit trail

**`DT_cedo_checklist.md`**:
- 8 placeholders listed
- Ready for presale to fill

---

## Next Steps After Template Generation

1. **Review Checklist** 📋
   ```bash
   cat ./output/dealA_*/dealA_checklist.md
   ```

2. **Fill Placeholders** ✏️
   - Work with presales team
   - Confirm pricing, hardware, timeline
   - Fill in answers

3. **Update Template** 📝
   - Replace `[Value] [PLACEHOLDER_XXX]` with confirmed values
   - Save verified template

4. **Generate Slides** 🎨
   ```bash
   /quotation slide ./output/dealA_*/dealA_template.md
   ```

---

## Summary

**One command to generate templates**:
```bash
/template dealA.xlsx
```

**That's it!** No Python, no scripts, just one simple command. ✅

The skill handles everything else automatically:
- ✅ Validation
- ✅ Data extraction
- ✅ AI module mapping
- ✅ Template generation
- ✅ Reasoning documentation
- ✅ Checklist creation
