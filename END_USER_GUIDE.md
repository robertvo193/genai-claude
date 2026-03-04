# ✅ Template Generation - Ready to Use!

## 🎯 For You (End User)

### Simple Command

```bash
~/.claude/skills/template_skill/template.sh DT_cedo.xlsx
```

**That's it!** The script handles everything else automatically.

---

## 📁 What You Need

1. **Deal Transfer Excel file** (`.xlsx` format)
2. **Required sheets**:
   - `Commercial` (or S1)
   - `Technical` (or S2)

3. **Python libraries** (install once):
   ```bash
   pip install pandas openpyxl
   ```

---

## 🚀 Step-by-Step Guide

### Step 1: Go to Your Excel File

```bash
cd /path/to/your/project
ls DT_cedo.xlsx  # Make sure file exists
```

### Step 2: Run the Command

```bash
~/.claude/skills/template_skill/template.sh DT_cedo.xlsx
```

### Step 3: Check the Output

```bash
# See generated files
ls -l ./output/DT_cedo_*/

# View template
cat ./output/DT_cedo_*/DT_cedo_template.md

# View checklist
cat ./output/DT_cedo_*/DT_cedo_checklist.md
```

### Step 4: Fill the Placeholders

Open the checklist and fill in the "Presale's Answer" column:

```bash
# Open in your editor
vim ./output/DT_cedo_*/DT_cedo_checklist.md
```

### Step 5: Update Template

Replace `[Value] [PLACEHOLDER_XXX]` with actual values:

```bash
# Edit template
vim ./output/DT_cedo_*/DT_cedo_template.md
```

### Step 6: Generate Slides (When Ready)

```bash
/quotation slide ./output/DT_cedo_*/DT_cedo_template.md
```

This creates PowerPoint + PDF files! 🎉

---

## 📊 What Gets Extracted Automatically

The script automatically extracts:

- ✅ **Customer name** (from Commercial sheet, Row 1)
- ✅ **Pain points** (from Commercial sheet, Row 5)
- ✅ **Timeline** (from Commercial sheet, Row 7)
- ✅ **Budget** (from Commercial sheet, Row 8)
- ✅ **Use cases** (from Technical sheet, Row 1)
- ✅ **Camera count** (from Technical sheet, Row 5)
- ✅ **AI modules** (auto-mapped from pain points)

### AI Module Mapping

The script automatically maps pain points to AI modules:

| Pain Points Detected | AI Module Added |
|---------------------|-----------------|
| "helmet", "safety" | Safety Helmet Detection |
| "vest" | Safety Vest Detection |
| "mask" | Safety Mask Detection |
| "fire", "smoke" | Fire & Smoke Detection |
| "intrusion" | Intrusion Detection |
| "vehicle" | Vehicle Detection |

---

## 📝 Output Files Explained

### 1. Template File (`<project>_template.md`)

**Purpose**: Client-facing proposal document

**Contains**:
- Project Requirement Statement
- Current Situation & Pain Points
- Proposed Solution
- Technical Architecture
- Implementation Plan
- Timeline & Milestones
- Resource Requirements
- Success Criteria
- Pricing & Licensing
- Support & Maintenance
- Terms & Conditions
- Next Steps

**Format**: Clean markdown, no internal references

### 2. Reasoning File (`<project>_reasoning.md`)

**Purpose**: Complete audit trail

**Contains**:
- All data sources (S1 Row X, S2 Row Y)
- AI module mapping logic
- All calculations (bandwidth, storage)
- All estimates explained

**Format**: Internal documentation

### 3. Checklist File (`<project>_checklist.md`)

**Purpose**: Presale task list

**Contains**:
- Table of all placeholders
- Columns: ID | Section | Item | Estimated | Answer

**Format**: Markdown table

---

## 💡 Tips & Tricks

### Tip 1: Quick File Check

Before running, verify your Excel:

```bash
# Check file exists and format
file DT_cedo.xlsx  # Should show "Excel 2007+"

# Check sheets
python3 -c "import pandas as pd; print(pd.ExcelFile('DT_cedo.xlsx').sheet_names)"
# Should show: ['Commercial', 'Technical', ...]
```

### Tip 2: Find Latest Output

```bash
# Show most recent directory
ls -td ./output/*/ | head -1
```

### Tip 3: Count Placeholders

```bash
# Count placeholders in template
grep -c "PLACEHOLDER" ./output/DT_cedo_*/DT_cedo_template.md
```

### Tip 4: Quick Preview

```bash
# Preview template (first 50 lines)
head -50 ./output/DT_cedo_*/DT_cedo_template.md
```

---

## 🐛 Troubleshooting

### Problem: Command not found

**Solution**: Use full path
```bash
~/.claude/skills/template_skill/template.sh DT_cedo.xlsx
```

### Problem: Excel file not found

**Solution**: Check you're in right directory
```bash
pwd  # Show current directory
ls *.xlsx  # List Excel files
cd /path/to/excel/files  # Go to correct directory
```

### Problem: "pandas not found"

**Solution**: Install libraries
```bash
pip install pandas openpyxl
```

### Problem: Wrong data extracted

**Solution**: Check reasoning file
```bash
cat ./output/DT_cedo_*/DT_cedo_reasoning.md
# This shows exactly what was extracted from where
```

---

## 📚 Reference Files

Created for you:

1. **`~/.claude/TEMPLATE_USER_QUICK_START.md`**
   - Complete user guide with examples
   - Common errors and solutions
   - Real example from Cedo Vietnam

2. **`~/.claude/skills/template_skill/SKILL.md`**
   - Technical documentation
   - AI module mapping details
   - Excel structure requirements

3. **`~/.claude/WORKFLOW_FIX_SUMMARY.md`**
   - Technical details of the fix
   - How it works
   - For developers/admins

---

## ✨ Complete Example

```bash
# 1. Navigate to project
cd ~/projects/cedo

# 2. Run template generation
~/.claude/skills/template_skill/template.sh DT_cedo.xlsx

# Output:
# ✅ Template generation complete!
# 📝 Next steps:
#    1. Review the checklist file
#    2. Fill in presale answers
#    3. Update template with confirmed values
#    4. Generate slides: /quotation slide <template.md>

# 3. View generated files
ls -l ./output/DT_cedo_*/
# total 3
# -rw-r--r-- 1 user user 8.2K DT_cedo_template.md
# -rw-r--r-- 1 user user  14K DT_cedo_reasoning.md
# -rw-r--r-- 1 user user 7.9K DT_cedo_checklist.md

# 4. Review checklist
cat ./output/DT_cedo_*/DT_cedo_checklist.md

# 5. Fill placeholders (edit files)
vim ./output/DT_cedo_*/DT_cedo_checklist.md
vim ./output/DT_cedo_*/DT_cedo_template.md

# 6. Generate slides (when template is ready)
/quotation slide ./output/DT_cedo_*/DT_cedo_template.md

# Output:
# ✅ Slide generation complete!
# Files: DT_cedo_proposal.pptx, DT_cedo_proposal.pdf
```

---

## 🎉 Success Checklist

- [ ] Python 3 installed
- [ ] pandas and openpyxl installed
- [ ] Excel file in `.xlsx` format
- [ ] Excel has "Commercial" and "Technical" sheets
- [ ] Run `~/.claude/skills/template_skill/template.sh <file.xlsx>`
- [ ] Check output in `./output/<project>_<timestamp>/`
- [ ] Review checklist file
- [ ] Fill presale answers
- [ ] Update template
- [ ] Generate slides with `/quotation slide`

**All done! Your proposal is ready for the client!** 🚀

---

## Quick Command Summary

```bash
# Generate template
~/.claude/skills/template_skill/template.sh <file.xlsx>

# View output
ls -l ./output/*/

# Generate slides
/quotation slide ./output/*/<file>_template.md
```

**That's everything you need!** ✅
