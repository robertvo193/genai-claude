# Understanding quotation_skill and dealtransfer2template Skills

## Overview

These two skills form the **proposal generation pipeline** for viAct technical proposals, but they serve **different purposes** and operate at **different stages** of the workflow.

---

## Skill 1: dealtransfer2template

### Purpose
**Generate technical proposal templates from Deal Transfer Excel files and Knowledge Base**

### Location
```
~/.claude/skills/dealtransfer2template/
├── SKILL.md                          # Main skill documentation
├── bin/
│   └── generate_template.py          # Python script (17KB)
├── scripts/
│   └── (extraction and validation scripts)
├── references/
│   ├── TEMPLATE.md                   # Proposal structure template
│   ├── STANDARD_MODULES.md           # Standard AI modules list
│   ├── FIELD_NAMES_REFERENCE.md      # Excel field mappings
│   └── Logic_for_Determining_List_of_AI_Modules_from_VA_usecases_and_Client_Painpoint.md
└── (other reference files)
```

### What It Does

**Input**: Deal Transfer Excel file
- Commercial Sheet (S1): Customer info, pain points, timeline, budget
- Technical Sheet (S2): Use cases, deployment, requirements

**Process** (5 steps):
1. **Extract Data**: Parse Excel S1/S2 sheets
2. **Query Knowledge Base**: Get relevant module information
3. **Map Pain Points**: Auto-map to AI modules (helmet → Safety Helmet Detection)
4. **Generate 3 Files**:
   - `{project}_template.md` - Clean proposal
   - `{project}_reasoning.md` - Audit trail
   - `{project}_checklist.md` - Placeholders

**Output**: `./output/{project}_{timestamp}/`
- `dealA_template.md` - **Client-facing proposal** (12 sections)
- `dealA_reasoning.md` - **Complete audit trail**
- `dealA_checklist.md` - **Placeholders to fill**

### Key Characteristics

**Template File Rules** (CRITICAL):
- ✅ **ONLY client-facing content**
- ✅ Pure markdown (NO HTML: `<br>`, `<table>`, etc.)
- ✅ Professional language (no meta-commentary)
- ✅ Estimated values: `[Value] [PLACEHOLDER_ID]`
- ❌ NO source references ("S1 -", "from S2")
- ❌ NO reasoning ("because", "based on")
- ❌ NO calculations shown (just final result)
- ❌ NO meta-comments ("Note:", "Reminder:")

**Project Requirement Format** (Section 2):
```
## 2. PROJECT REQUIREMENT STATEMENT

**Project:** AI-Powered Video Analytics for [Short Description]

**Project Owner:** [Client Name]

**Work Scope:** [Deployment method] AI system to [objective]

**Project Duration:** [X months/years]

**Camera Number:** [X cameras]

**AI Modules per Camera:** [X modules per camera]

**AI Modules:**
1. [Module Name 1]
2. [Module Name 2]
...
```

**AI Module Mapping** (automatic):
| Pain Points | AI Module |
|-------------|-----------|
| helmet, safety | Safety Helmet Detection |
| vest | Safety Vest Detection |
| mask | Safety Mask Detection |
| fire, smoke | Fire & Smoke Detection |
| intrusion | Intrusion Detection |
| vehicle | Vehicle Detection |

### Execution Method

**Option 1: Direct Script**
```bash
python ~/.claude/skills/dealtransfer2template/bin/generate_template.py <excel_file>
```

**Option 2: Through Skill Invocation**
```
User provides: "Generate proposal from dealA.xlsx"
Invokes: dealtransfer2template skill
Runs: generate_template.py script
```

### Knowledge Base Integration

Queries KB for:
- Standard AI modules specifications
- Similar project references
- Industry standards
- Best practices

---

## Skill 2: quotation_skill

### Purpose
**Convert verified proposal templates to final presentations (PowerPoint + PDF)**

### Location
```
~/.claude/skills/quotation_skill/
├── SKILL.md                          # Orchestration documentation
├── README.md                         # Summary and usage
├── QUICK_START.md                    # Quick reference
├── WORKFLOW_GUIDE.md                 # Complete workflow guide
├── SLIDE_TEMPLATES.md                # Standardized HTML templates
├── OVERFLOW_FREE_USAGE_GUIDE.md      # Prevent text overflow
├── DIAGRAM_GENERATION_GUIDE.md       # Architecture diagrams
├── scripts/
│   └── generate_architecture_diagram.py  # Mermaid → PNG
├── assets/
│   └── background.png                # viAct branded background
└── references/
    ├── pptx_workflow.md             # PowerPoint generation guide
    └── pdf_workflow.md              # PDF generation guide
```

### What It Does

**Input**: Verified proposal template (markdown, no placeholders)
- `{project}_template.md` (from dealtransfer2template)
- All placeholders filled and verified

**Process** (3 steps):
1. **Create Output Directory**: `./output/{project}_{timestamp}/`
2. **Generate PowerPoint**:
   - Read template sections
   - Create HTML slides (using SLIDE_TEMPLATES.html)
   - Convert to PPTX (via pptx skill html2pptx workflow)
   - Apply viAct branding
3. **Generate PDF**:
   - Convert PPTX to PDF (via pdf skill)
   - Using LibreOffice or pypdf

**Output**: `./output/{project}_{timestamp}/`
- `{project}_proposal.pptx` - PowerPoint presentation (13 slides)
- `{project}_proposal.pdf` - PDF document (13 pages)
- `slides/` - HTML source files (optional)

### Key Characteristics

**High-Level Orchestration**:
- Does NOT generate content
- Does NOT process Excel
- Does NOT validate templates
- ONLY converts verified templates → PPTX + PDF

**Design Specifications**:
- **Primary Color**: #00AEEF (viAct Blue)
- **Text Color**: #FFFFFF (White)
- **Font**: Arial, Helvetica, Verdana (web-safe)
- **Size**: 720pt × 405pt (16:9)
- **Margins**:
  - Title: `30pt 120pt 20pt 40pt` (top right bottom left)
  - Content: `0 120pt 85pt 40pt` (bottom 85pt prevents overflow)

**Template Selection** (from SLIDE_TEMPLATES.html):
- Template 1: Cover page
- Template 2: Bullet lists
- Template 3: Two columns
- Template 4: Sections + bullets
- Template 5: AI module detail
- Template 6: Timeline/phases

**Text Overflow Prevention** (CRITICAL):
- Use pre-configured HTML templates
- Right margin 120pt (room for logo)
- Bottom margin 85pt (minimum 0.5" required)
- If overflow, increase bottom margin in 5pt increments
- Test with html2pptx validation

### Architecture

```
quotation_skill (orchestration layer)
│
├── Input: Verified Template (markdown)
│
├── Step 1: Generate PowerPoint
│   ├── Create HTML slides (SLIDE_TEMPLATES.html)
│   ├── Apply viAct branding (background.png)
│   └── Convert via pptx skill → proposal.pptx
│
└── Step 2: Generate PDF
    └── Convert via pdf skill → proposal.pdf
```

**Leverages**:
- **pptx skill**: HTML → PowerPoint conversion
- **pdf skill**: PPTX → PDF conversion

### What It Does NOT Do

❌ Does NOT process Deal Transfer Excel
❌ Does NOT generate templates from scratch
❌ Does NOT handle placeholders
❌ Does NOT validate templates
❌ Does NOT manage presale review

---

## Complete Workflow Pipeline

### Full Proposal Generation Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  STAGE 1: Data Extraction & Template Generation              │
│  (dealtransfer2template skill)                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
        Input: Deal Transfer Excel (dealA.xlsx)
        - Commercial Sheet (S1)
        - Technical Sheet (S2)
                            ↓
        ┌──────────────────────────────────────┐
        │ 1. Extract Data from Excel           │
        │ 2. Query Knowledge Base              │
        │ 3. Map Pain Points → AI Modules      │
        │ 4. Generate Template (clean content) │
        │ 5. Generate Reasoning (audit trail)  │
        │ 6. Generate Checklist (placeholders) │
        └──────────────────────────────────────┘
                            ↓
        Output: ./output/dealA_[timestamp]/
        - dealA_template.md (with placeholders)
        - dealA_reasoning.md
        - dealA_checklist.md
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STAGE 2: Presale Review (Manual Process)                    │
│  - Review checklist.md                                        │
│  - Confirm pricing, hardware, timeline                       │
│  - Fill placeholders in template.md                          │
│  - Verify final template                                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
        Verified Template (no placeholders)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STAGE 3: Final Output Generation                            │
│  (quotation_skill)                                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
        Input: dealA_template.md (verified)
                            ↓
        ┌──────────────────────────────────────┐
        │ 1. Create Output Directory           │
        │ 2. Generate HTML Slides              │
        │ 3. Convert to PowerPoint (pptx skill)│
        │ 4. Convert to PDF (pdf skill)        │
        └──────────────────────────────────────┘
                            ↓
        Output: ./output/dealA_[timestamp]/
        - dealA_proposal.pptx
        - dealA_proposal.pdf
        - slides/ (HTML source)
                            ↓
        ✅ Ready for Client Delivery
```

---

## Key Differences

| Aspect | dealtransfer2template | quotation_skill |
|--------|----------------------|-----------------|
| **Purpose** | Generate templates from Excel | Convert templates to PPTX/PDF |
| **Input** | Deal Transfer Excel | Verified template (markdown) |
| **Output** | 3 MD files (template, reasoning, checklist) | 2 files (PPTX, PDF) |
| **Stage** | Early (data extraction) | Late (final output) |
| **Knowledge Base** | Queries KB for modules | Does not query KB |
| **Placeholders** | Creates placeholders | Requires no placeholders |
| **HTML Generation** | No | Yes (for slides) |
| **Design Work** | No | Yes (viAct branding) |
| **Orchestration** | Standalone script | Orchestrates pptx/pdf skills |
| **Validation** | Validates Excel format | Validates template (no placeholders) |

---

## Integration Points

### dealtransfer2template → quotation_skill

**Connection Point**: Template file
- dealtransfer2template creates: `dealA_template.md` (with placeholders)
- User fills placeholders
- quotation_skill reads: `dealA_template.md` (verified, no placeholders)

**Data Flow**:
```
Excel → Data Extraction → Template (with placeholders) →
User Review → Template (verified) → HTML Generation →
PowerPoint → PDF
```

### Shared Dependencies

**pptx skill**:
- Used by quotation_skill
- Provides html2pptx workflow
- Location: `~/.claude/skills/pptx/`

**pdf skill**:
- Used by quotation_skill
- Provides PPTX → PDF conversion
- Location: `~/.claude/skills/pdf/`

---

## Usage Examples

### Example 1: Complete Workflow

```bash
# Stage 1: Generate template from Excel
cd /path/to/project
python ~/.claude/skills/dealtransfer2template/bin/generate_template.py dealA.xlsx

# Output: ./output/dealA_20250127_143000/
#   - dealA_template.md (with placeholders)
#   - dealA_reasoning.md
#   - dealA_checklist.md

# Stage 2: Presale fills placeholders
vim ./output/dealA_*/dealA_template.md
# Replace [Value] [PLACEHOLDER_XXX] with actual values

# Stage 3: Generate final outputs
# (Invokes quotation_skill through CLI or skill system)
# Output: ./output/dealA_*/
#   - dealA_proposal.pptx
#   - dealA_proposal.pdf
```

### Example 2: quotation_skill Only (Template Already Exists)

```bash
# Input: dealA_template.md (already verified)
# quotation_skill generates PPTX and PDF

# Output: ./output/dealA_*/
#   - dealA_proposal.pptx
#   - dealA_proposal.pdf
```

---

## Technical Details

### dealtransfer2template Script

**File**: `bin/generate_template.py` (17,280 bytes)

**Key Functions**:
- `validate_excel()`: Check file format and sheets
- `extract_deal_transfer_data()`: Parse S1/S2 sheets
- `map_pain_points_to_modules()`: Auto-map to AI modules
- `generate_template()`: Create clean template file
- `generate_reasoning()`: Document audit trail
- `generate_checklist()`: List placeholders

**Dependencies**:
- pandas (Excel parsing)
- json, pathlib, datetime (Python stdlib)

### quotation_skill Orchestration

**File**: `SKILL.md` (23,562 bytes)

**Key Sections**:
1. Prerequisites (verified template, no placeholders)
2. Step 0: Create output directory
3. Step 1: Generate PowerPoint (html2pptx workflow)
4. Step 2: Generate PDF (PPTX → PDF)

**Dependencies**:
- pptx skill (html2pptx workflow)
- pdf skill (PPTX → PDF conversion)
- LibreOffice (PDF generation)

---

## Best Practices

### dealtransfer2template

**DO**:
✅ Follow TEMPLATE.md structure exactly
✅ Use markdown formatting (NO HTML)
✅ Map pain points to standard modules when possible
✅ Document reasoning in separate file
✅ Create placeholders for missing info
✅ Estimate reasonable values based on standards

**DON'T**:
❌ Mix reasoning into template file
❌ Use HTML tags in template
❌ Show calculations in template
❌ Add source references in template
❌ Skip checklist for placeholders

### quotation_skill

**DO**:
✅ Verify template has no placeholders
✅ Use pre-configured HTML templates
✅ Apply viAct branding consistently
✅ Test for text overflow
✅ Use correct margins (85pt bottom)
✅ Generate both PPTX and PDF

**DON'T**:
❌ Process templates with placeholders
❌ Skip validation step
❌ Use incorrect margins (causes overflow)
❌ Forget background.png
❌ Generate only one format

---

## Troubleshooting

### dealtransfer2template Issues

**Issue**: Excel file not found
- **Solution**: Check file path and .xlsx format

**Issue**: S1 sheet not found
- **Solution**: Ensure Excel has "Commercial" or "S1" sheet

**Issue**: AI module mapping fails
- **Solution**: Check STANDARD_MODULES.md for valid modules

### quotation_skill Issues

**Issue**: Text overflow in slides
- **Solution**: Increase bottom margin to 85pt or higher

**Issue**: Placeholders still in template
- **Solution**: Fill all placeholders before running quotation_skill

**Issue**: HTML conversion fails
- **Solution**: Use SLIDE_TEMPLATES.html (correct formatting)

**Issue**: PDF generation fails
- **Solution**: Ensure LibreOffice is installed

---

## Summary

### dealtransfer2template
- **Role**: Data extraction and template generation
- **Input**: Deal Transfer Excel
- **Output**: 3 markdown files (template, reasoning, checklist)
- **Stage**: Early workflow
- **Automation**: High (Python script)

### quotation_skill
- **Role**: Final output generation
- **Input**: Verified template (no placeholders)
- **Output**: PowerPoint + PDF
- **Stage**: Late workflow
- **Automation**: Medium (orchestrates pptx/pdf skills)

### Complete Pipeline
```
Excel → (dealtransfer2template) → Template + Reasoning + Checklist
→ (Presale Review) → Verified Template
→ (quotation_skill) → PowerPoint + PDF
→ (Client Delivery)
```

These two skills work together but at different stages:
- **dealtransfer2template**: Creates the content
- **quotation_skill**: Formats the content for delivery

They are **separate, focused skills** that can be used independently or as part of the complete proposal generation pipeline.
