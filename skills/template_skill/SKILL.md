# Template Generation Skill

**Simple command to generate proposal templates from Deal Transfer Excel files**

## Quick Start

```bash
/template DT_cedo.xlsx
```

That's it! The skill will:
1. ✅ Validate your Excel file
2. ✅ Extract data from Commercial & Technical sheets
3. ✅ Generate 3 files:
   - `DT_cedo_template.md` (proposal template)
   - `DT_cedo_reasoning.md` (audit trail)
   - `DT_cedo_checklist.md` (placeholders to fill)

## Usage

### Basic Usage

```bash
# Generate template from Excel
/template <your_excel_file.xlsx>

# Example
/template DT_cedo.xlsx
```

### Advanced Usage

```bash
# Specify custom output directory
/template DT_cedo.xlsx --output ./my_output/

# Show detailed progress
/template DT_cedo.xlsx --verbose
```

## What It Does

1. **Validates Excel File**
   - Checks file exists and is .xlsx format
   - Verifies Commercial (S1) sheet exists
   - Verifies Technical (S2) sheet exists

2. **Extracts Data**
   - Customer information
   - Pain points
   - Use cases
   - Camera details
   - Timeline and budget
   - Maps pain points → AI modules

3. **Generates 3 Files**

   **Template File** (`<project>_template.md`)
   - 12 sections
   - Client-facing proposal content
   - Placeholders for missing info

   **Reasoning File** (`<project>_reasoning.md`)
   - Complete audit trail
   - All data sources (S1/S2 references)
   - All calculations explained
   - AI module mapping logic

   **Checklist File** (`<project>_checklist.md`)
   - List of all placeholders
   - Table format for presale to fill
   - Sorted by section

## Output Location

```
./output/<project>_<timestamp>/
├── <project>_template.md
├── <project>_reasoning.md
└── <project>_checklist.md
```

## Example Output

```
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
✓ Filled 12 sections from TEMPLATE.md
✓ Created 48 placeholders for missing info
✓ Clean proposal content (no source references)

[Step 4/5] Generate Reasoning File [✓ COMPLETED]
✓ Documented all S1/S2 sources
✓ Complete audit trail

[Step 5/5] Generate Checklist File [✓ COMPLETED]
✓ Listed 48 placeholders
✓ Ready for presale review

✅ Template Generation Complete!

Output Files:
  • ./output/DT_cedo_20260126_224655/DT_cedo_template.md
  • ./output/DT_cedo_20260126_224655/DT_cedo_reasoning.md
  • ./output/DT_cedo_20260126_224655/DT_cedo_checklist.md

📊 Statistics:
  • S1 rows extracted: 14
  • S2 rows extracted: 14
  • AI modules mapped: 1
  • Placeholders created: 48

Next Steps:
  1. Review DT_cedo_checklist.md
  2. Fill presale answers for placeholders
  3. Update template with confirmed values
  4. Generate slides: /quotation slide DT_cedo_template.md
```

## Next Steps After Template Generation

1. **Review Checklist**
   ```bash
   cat ./output/DT_cedo_*/DT_cedo_checklist.md
   ```

2. **Fill Placeholders**
   - Work with presales team
   - Confirm pricing, hardware, timeline
   - Fill in "Presale's Answer" column

3. **Update Template**
   - Replace `[Value] [PLACEHOLDER_XXX]` with confirmed values
   - Remove all placeholders
   - Save as verified template

4. **Generate Slides**
   ```bash
   /quotation slide DT_cedo_template.md
   ```

## Common Issues

### Issue: "Excel file not found"
**Solution**: Make sure you're in the same directory as the Excel file
```bash
ls DT_cedo.xlsx  # Check file exists
/template DT_cedo.xlsx
```

### Issue: "S1 sheet not found"
**Solution**: Ensure your Excel has sheets named "Commercial" or "S1"
```python
import pandas as pd
xls = pd.ExcelFile('DT_cedo.xlsx')
print(xls.sheet_names)  # Should show ['Commercial', 'Technical', ...]
```

### Issue: "pandas library not found"
**Solution**: Install required Python libraries
```bash
pip install pandas openpyxl
```

## Requirements

- Python 3.6+
- pandas library
- openpyxl library

Install requirements:
```bash
pip install pandas openpyxl
```

## Technical Details

### Excel Structure Expected

**Commercial Sheet (S1)**
- Row 0: Header
- Row 1: Customer overview
- Row 5: Pain points
- Row 7: Timeline
- Row 8: Budget
- Row 11: Camera status

**Technical Sheet (S2)**
- Row 0: Header
- Row 1: Use cases
- Row 5: Camera details
- Row 8: Deployment preference

### AI Module Mapping

The skill automatically maps pain points to AI modules:

| Pain Point Keywords | AI Module |
|---------------------|-----------|
| helmet, safety | Safety Helmet Detection |
| mask | Safety Mask Detection |
| vest | Safety Vest Detection |
| fire, smoke | Fire & Smoke Detection |
| intrusion, unauthorized | Intrusion Detection |
| vehicle | Vehicle Detection |

## Integration with Quotation Workflow

After template generation and presale confirmation:

```bash
# Generate PowerPoint + PDF from verified template
/quotation slide DT_cedo_template.md
```

This creates:
- `DT_cedo_proposal.pptx` (PowerPoint presentation)
- `DT_cedo_proposal.pdf` (PDF document)

## Support

For issues or questions:
1. Check the generated `reasoning.md` file for audit trail
2. Review the `checklist.md` for placeholder details
3. Verify Excel structure matches expected format
