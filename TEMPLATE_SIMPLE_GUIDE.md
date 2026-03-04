# ✅ Template Generation - Super Simple Guide

## 🎯 For End Users - One Command Only!

```bash
/template dealA.xlsx
```

**That's it!** ✅

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

## 🚀 Complete Workflow (Excel → PowerPoint)

### Step 1: Generate Template

```bash
/template dealA.xlsx
```

**Output**: 3 files created in `./output/dealA_<timestamp>/`
- `dealA_template.md` - Your proposal template
- `dealA_reasoning.md` - Audit trail
- `dealA_checklist.md` - Placeholders to fill

### Step 2: Review Checklist

```bash
cat ./output/dealA_*/dealA_checklist.md
```

### Step 3: Fill Placeholders

```bash
# Edit template
vim ./output/dealA_*/dealA_template.md

# Replace [Value] [PLACEHOLDER_XXX] with actual values
```

### Step 4: Generate Slides

```bash
/quotation slide ./output/dealA_*/dealA_template.md
```

**Output**: PowerPoint + PDF ready for client! 🎉

---

## 📊 What Happens Automatically

When you run `/template dealA.xlsx`:

✅ **Validates** Excel file
✅ **Extracts** 14+ fields from Commercial & Technical sheets
✅ **Maps** pain points to AI modules
✅ **Generates** 12-section template
✅ **Creates** audit trail
✅ **Lists** all placeholders

---

## 💡 Quick Examples

### Example 1: Basic Usage

```bash
# Navigate to your Excel file
cd /path/to/project

# Run template generation
/template dealA.xlsx

# View output
ls -l ./output/dealA_*/
```

### Example 2: Full Pipeline

```bash
# 1. Generate template
/template dealA.xlsx

# 2. Review checklist
cat ./output/dealA_*/dealA_checklist.md

# 3. Edit template (fill placeholders)
vim ./output/dealA_*/dealA_template.md

# 4. Generate PowerPoint + PDF
/quotation slide ./output/dealA_*/dealA_template.md
```

### Example 3: Multiple Deals

```bash
# Generate templates for all deals
for file in *.xlsx; do
    /template "$file"
done
```

---

## 🐛 Common Errors & Quick Fixes

### ❌ "Excel file not found"

**Fix**: Check you're in the right directory
```bash
pwd  # Show current directory
ls *.xlsx  # List Excel files
cd /path/to/excel/files  # Go to correct directory
```

### ❌ "File must be .xlsx format"

**Fix**: Convert .xls to .xlsx
```bash
libreoffice --headless --convert-to xlsx dealA.xls
/template dealA.xlsx
```

### ❌ "S1 sheet not found"

**Fix**: Check your Excel sheets
```bash
python3 -c "import pandas as pd; print(pd.ExcelFile('dealA.xlsx').sheet_names)"
# Expected: ['Commercial', 'Technical', ...]
```

### ❌ "pandas library not found"

**Fix**: Install Python libraries
```bash
pip install pandas openpyxl
```

---

## 📋 What Gets Extracted

### From Commercial Sheet

| Field | Row | Example |
|-------|-----|---------|
| Customer | 1 | "Cedo Vietnam" |
| Pain Points | 5 | "Manual safety monitoring" |
| Timeline | 7 | "Q1/2026" |
| Budget | 8 | "Not disclosed" |
| Cameras | 11 | "17 cameras" |

### From Technical Sheet

| Field | Row | Example |
|-------|-----|---------|
| Use Cases | 1 | "PPE detection" |
| Camera Details | 5 | "Verkada CD41" |
| Deployment | 8 | "Cloud-based" |

### AI Modules (Auto-Mapped)

| Pain Points | AI Module |
|-------------|-----------|
| helmet, safety | Safety Helmet Detection |
| vest | Safety Vest Detection |
| mask | Safety Mask Detection |
| fire, smoke | Fire & Smoke Detection |
| intrusion | Intrusion Detection |
| vehicle | Vehicle Detection |

---

## 📁 Output Structure

```
./output/dealA_20260126_230000/
├── dealA_template.md       ← Your proposal (12 sections)
├── dealA_reasoning.md      ← Complete audit trail
└── dealA_checklist.md      ← Placeholders to fill
```

---

## 🎯 Quick Reference

| Command | Purpose |
|---------|---------|
| `/template dealA.xlsx` | Generate template |
| `cat ./output/dealA_*/dealA_checklist.md` | Review placeholders |
| `vim ./output/dealA_*/dealA_template.md` | Edit template |
| `/quotation slide dealA_template.md` | Generate slides |

---

## ✨ Real Example: Cedo Vietnam

### Input: `DT_cedo.xlsx`

**Commercial**:
- Customer: Cedo Vietnam
- Pain Points: Manual safety monitoring
- Timeline: Q1/2026
- Cameras: 17 cameras

**Technical**:
- Use Cases: PPE detection
- Deployment: Cloud-based

### Output: Generated Files

**`DT_cedo_template.md`**:
- Project: AI-Powered Video Analytics
- Customer: Cedo Vietnam
- Cameras: 17 cameras
- AI Modules: Safety Helmet Detection
- 12 sections, 8 placeholders

**Statistics**:
- ✅ 14 rows from S1
- ✅ 14 rows from S2
- ✅ 1 AI module mapped
- ✅ 8 placeholders created

---

## 🎉 Summary

**One command to generate templates**:

```bash
/template dealA.xlsx
```

**Complete workflow**:

```bash
/template dealA.xlsx           # Generate template
# [fill placeholders]
/quotation slide dealA_template.md  # Generate slides
```

**That's everything!** ✅

No Python scripts, no complex commands, just `/template <file.xlsx>`!
