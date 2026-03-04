# 🚀 Template Generation - Quick Start Guide

## Super Simple Usage

### Step 1: Navigate to Your Excel File

```bash
cd /path/to/your/excel/files
ls DT_cedo.xlsx  # Verify file exists
```

### Step 2: Run the Command

```bash
~/.claude/skills/template_skill/template.sh DT_cedo.xlsx
```

**That's it!** ✅

---

## What Happens Automatically

The command will:

1. ✅ **Validate** your Excel file
2. ✅ **Extract** data from Commercial & Technical sheets
3. ✅ **Generate** 3 files in `./output/<project>_<timestamp>/`:
   - `<project>_template.md` - Your proposal template
   - `<project>_reasoning.md` - Audit trail
   - `<project>_checklist.md` - Placeholders to fill

---

## Example Output

```
🎯 Generating template from: DT_cedo.xlsx

[Step 1/5] Validate Excel File [✓ COMPLETED]
✓ File exists: DT_cedo.xlsx
✓ Valid Excel format (.xlsx)
✓ S1 (Commercial) sheet found
✓ S2 (Technical) sheet found

[Step 2/5] Extract Deal Transfer Data [✓ COMPLETED]
✓ Extracted 14 rows from S1 sheet
✓ Extracted 14 rows from S2 sheet
✓ Mapped pain points → 1 AI modules

... [more steps]

✅ Template generation complete!

📝 Next steps:
   1. Review the checklist file
   2. Fill in presale answers
   3. Update template with confirmed values
   4. Generate slides: /quotation slide <template.md>
```

---

## Complete Workflow Example

### From Excel to PowerPoint (Full Pipeline)

```bash
# Step 1: Generate template from Excel
~/.claude/skills/template_skill/template.sh DT_cedo.xlsx

# Output: ./output/DT_cedo_20260126_224745/
#   • DT_cedo_template.md
#   • DT_cedo_reasoning.md
#   • DT_cedo_checklist.md

# Step 2: Review and fill checklist
cat ./output/DT_cedo_*/DT_cedo_checklist.md

# Step 3: Edit template and fill placeholders
vim ./output/DT_cedo_*/DT_cedo_template.md
# Replace [Value] [PLACEHOLDER_XXX] with actual values

# Step 4: Generate PowerPoint + PDF
/quotation slide ./output/DT_cedo_*/DT_cedo_template.md

# Output: PowerPoint and PDF files ready for client! 🎉
```

---

## Common Commands

### Check Available Excel Files

```bash
ls *.xlsx
```

### View Generated Files

```bash
# List all outputs
ls -l ./output/DT_cedo_*/

# View template
cat ./output/DT_cedo_*/DT_cedo_template.md

# View checklist
cat ./output/DT_cedo_*/DT_cedo_checklist.md

# View reasoning (audit trail)
cat ./output/DT_cedo_*/DT_cedo_reasoning.md
```

### Find Latest Output

```bash
# List most recent output directory
ls -td ./output/DT_cedo_* | head -1
```

---

## Error Messages & Solutions

### ❌ "Excel file not found"

**Cause**: File doesn't exist in current directory

**Solution**:
```bash
# Check current directory
pwd

# Find your Excel file
find ~ -name "DT_cedo.xlsx" 2>/dev/null

# Navigate to correct directory
cd /path/to/excel/files

# Run command again
~/.claude/skills/template_skill/template.sh DT_cedo.xlsx
```

### ❌ "File must be .xlsx format"

**Cause**: File is .xls (old format) not .xlsx (new format)

**Solution**:
```bash
# Convert .xls to .xlsx
libreoffice --headless --convert-to xlsx DT_cedo.xls

# Then run command
~/.claude/skills/template_skill/template.sh DT_cedo.xlsx
```

### ❌ "S1 sheet not found"

**Cause**: Excel doesn't have "Commercial" or "S1" sheet

**Solution**:
```bash
# Check sheet names
python3 << 'EOF'
import pandas as pd
xls = pd.ExcelFile('DT_cedo.xlsx')
print("Available sheets:", xls.sheet_names)
EOF

# Expected: ['Commercial', 'Technical', ...]
```

### ❌ "pandas library not found"

**Cause**: Python libraries not installed

**Solution**:
```bash
pip install pandas openpyxl
```

---

## Quick Reference Card

### Command Structure

```bash
~/.claude/skills/template_skill/template.sh <excel_file.xlsx>
```

### Expected Excel Sheets

- ✅ **Commercial** (or S1)
- ✅ **Technical** (or S2)

### Output Structure

```
./output/
└── <project>_<timestamp>/
    ├── <project>_template.md       (12 sections)
    ├── <project>_reasoning.md      (audit trail)
    └── <project>_checklist.md      (placeholders)
```

### Next Steps After Generation

1. 📋 Review checklist
2. ✏️ Fill placeholders
3. 📄 Update template
4. 🎨 Generate slides: `/quotation slide <template.md>`

---

## Advanced Usage

### Create an Alias (Optional)

For even simpler commands, add this to your `~/.bashrc`:

```bash
alias template='~/.claude/skills/template_skill/template.sh'
```

Then you can use:

```bash
template DT_cedo.xlsx
```

### Batch Processing

```bash
# Generate templates for all Excel files
for file in *.xlsx; do
    ~/.claude/skills/template_skill/template.sh "$file"
done
```

---

## Real Example: Cedo Vietnam

### Input

**Excel File**: `DT_cedo.xlsx`

**Commercial Sheet**:
- Customer: Cedo Vietnam (manufacturing arm of European Cedo Group)
- Pain Points: Manual safety monitoring inefficient
- Timeline: Site survey Jan 2026 → Implementation Q1/2026
- Cameras: 17 cameras (9 in Workshop VN1, 8 in Workshop VN2)

**Technical Sheet**:
- Use Cases: PPE detection, proximity detection
- Deployment: Cloud-based for PoC
- Camera: Verkada CD41 and CD41-E

### Output

**Generated Files** (in `./output/DT_cedo_20260126_224745/`):

1. **DT_cedo_template.md**
   - Project: AI-Powered Video Analytics for Manufacturing
   - Customer: Cedo Vietnam
   - Cameras: 9 cameras (auto-detected)
   - AI Modules: Safety Helmet Detection (auto-mapped from pain points)
   - 12 sections, 48 placeholders

2. **DT_cedo_reasoning.md**
   - All data sources documented (S1 Row 5, S2 Row 1, etc.)
   - AI module mapping logic explained
   - Complete audit trail

3. **DT_cedo_checklist.md**
   - 48 placeholders listed
   - Table format: ID | Section | Item | Estimated | Answer
   - Ready for presale review

### Statistics

```
📊 Statistics:
  • S1 rows extracted: 14
  • S2 rows extracted: 14
  • AI modules mapped: 1
  • Placeholders created: 48
  • Sections filled: 12/12
```

---

## Need Help?

### Check Generated Files

If something looks wrong, check the reasoning file:

```bash
cat ./output/DT_cedo_*/DT_cedo_reasoning.md
```

This shows:
- All data sources
- Extraction logic
- AI module mapping
- Calculations

### Verify Excel Structure

```bash
python3 << 'EOF'
import pandas as pd

excel_file = 'DT_cedo.xlsx'
xls = pd.ExcelFile(excel_file)

print(f"File: {excel_file}")
print(f"Sheets: {xls.sheet_names}")

for sheet in xls.sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet, header=None)
    print(f"\n{sheet}: {df.shape[0]} rows x {df.shape[1]} columns")
    print("First 5 rows:")
    print(df.head())
EOF
```

---

## Summary

**For End Users - Just Remember This**:

```bash
# Navigate to Excel files
cd /path/to/project

# Run template generation
~/.claude/skills/template_skill/template.sh YourFile.xlsx

# Find output
ls -l ./output/YourFile_*/

# Review and fill checklist
cat ./output/YourFile_*/YourFile_checklist.md

# Generate slides when ready
/quotation slide ./output/YourFile_*/YourFile_template.md
```

**That's the complete workflow!** 🎉
