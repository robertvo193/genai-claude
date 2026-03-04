# quotation_skill Workflow Guide

## Overview

This guide explains the complete workflow for generating proposal presentations with reference slides from AvailableSlide11.pptx.

## High-Level Workflow

```
template.md (verified proposal)
    ↓
Step 1: Generate HTML slides from template
    ↓
Step 2: Convert AvailableSlide11.pptx to HTML (one-time setup)
    ↓
Step 3: Combine HTML slides in correct order
    ↓
Step 4: Convert combined HTML to PowerPoint (with html2pptx)
    ↓
Step 5: Convert PowerPoint to PDF
    ↓
Output: PowerPoint + PDF with all backgrounds preserved!
```

## Step-by-Step Instructions

### Step 1: Generate HTML Slides from Template

Use the quotation_skill or manually create HTML slides from your template.md.

**Output**: `./output/[Project]_[Timestamp]/slides/` with slide*.html files

### Step 2: Convert AvailableSlide11.pptx to HTML (One-Time Setup)

**This only needs to be done once** - the HTML slides are cached in the skill assets.

```bash
python3 ~/.claude/skills/quotation_skill/scripts/pptx_to_html.py \
  ~/.claude/skills/quotation_skill/assets/AvailableSlide11.pptx \
  ~/.claude/skills/quotation_skill/assets/available_slides_html \
  ~/.claude/skills/quotation_skill/assets/background.png
```

**Output**:
- `~/.claude/skills/quotation_skill/assets/available_slides_html/available_slide*.html` (25 files)
- `~/.claude/skills/quotation_skill/assets/available_slides_html/images/` (extracted images)

### Step 3: Combine HTML Slides

Use the insert_html_slides.sh script to combine generated and available slides in the correct order:

```bash
~/.claude/skills/quotation_skill/scripts/insert_html_slides.sh \
  "./output/[Project]_[Timestamp]/slides" \
  "~/.claude/skills/quotation_skill/assets/available_slides_html/available_html_test" \
  "./output/[Project]_[Timestamp]/slides_combined"
```

**What this does**:
1. Copies slide01_cover.html (generated)
2. Copies available_slide02-10.html (9 reference slides)
3. Copies slide02-12.html (remaining generated slides)
4. Copies available_slide11-25.html (15 reference slides)
5. Copies images/ directory

**Output**: `./output/[Project]_[Timestamp]/slides_combined/` with 36 HTML files

### Step 4: Convert Combined HTML to PowerPoint

Use html2pptx (via pptx skill) to convert all HTML slides to PowerPoint:

```bash
# Create conversion script
cat > ~/.claude/skills/pptx/convert_combined.js << 'EOF'
const html2pptx = require('/home/philiptran/.claude/skills/pptx/scripts/html2pptx.js');
const pptxgenjs = require('pptxgenjs');
const path = require('path');
const fs = require('fs');

const slidesDir = '/absolute/path/to/slides_combined';
const outputFile = '/absolute/path/to/Output_FINAL.pptx';

const htmlFiles = fs.readdirSync(slidesDir)
  .filter(f => f.endsWith('.html'))
  .sort()
  .map(f => path.join(slidesDir, f));

(async () => {
  try {
    const pptx = new pptxgenjs();
    pptx.layout = 'LAYOUT_16x9';

    for (const htmlFile of htmlFiles) {
      await html2pptx(htmlFile, pptx);
    }

    await pptx.writeFile({ fileName: outputFile });
    console.log('✓ PowerPoint created!');
  } catch (error) {
    console.error('✗ Error:', error.message);
    process.exit(1);
  }
})();
EOF

# Run conversion
cd ~/.claude/skills/pptx
node convert_combined.js
```

**Output**: `./output/[Project]_[Timestamp]/[Project]_Proposal_HTML_FINAL.pptx`

### Step 5: Convert PowerPoint to PDF

```bash
libreoffice --headless --convert-to pdf \
  --outdir ./output/[Project]_[Timestamp] \
  ./output/[Project]_[Timestamp]/[Project]_Proposal_HTML_FINAL.pptx
```

**Output**: `./output/[Project]_[Timestamp]/[Project]_Proposal_HTML_FINAL.pdf`

## Why This Approach Works

### Problem with Direct PPTX Copying

When copying slides directly from one PowerPoint to another using python-pptx:
- ✗ XML shapes are copied
- ✗ Media files are copied
- ✗ **BUT relationship entries are NOT copied**
- Result: Slides reference images via rId, but rId mappings are broken → White backgrounds

### Solution: HTML Approach

By converting to HTML first:
1. ✓ AvailableSlide11.pptx → HTML (with background.png references)
2. ✓ Combine HTML files (simple file copy)
3. ✓ HTML → PowerPoint via html2pptx
4. ✓ html2pptx correctly embeds background.png for EACH slide
5. ✓ All relationships are created correctly
6. ✓ **All backgrounds preserved!**

## File Structure

### Input Files
- `template.md` - Verified proposal template
- `AvailableSlide11.pptx` - Reference slides (47 MB, 25 slides)
- `background.png` - viAct background (154 KB)

### Output Files
```
./output/[Project]_[Timestamp]/
├── slides/                          # Generated HTML only
│   ├── slide01_cover.html
│   ├── slide02_requirements.html
│   └── ...
├── slides_combined/                 # Combined HTML (generated + reference)
│   ├── slide01_cover.html
│   ├── available_slide02.html
│   ├── ...
│   ├── available_slide25.html
│   ├── bromma_architecture.png      # Architecture diagram
│   └── images/                      # Images from available slides
│       ├── slide2_image1.png
│       └── ...
├── [Project]_Proposal.pptx          # Generated only (before reference)
├── [Project]_Proposal_HTML_FINAL.pptx   # Final with reference slides ✓
└── [Project]_Proposal_HTML_FINAL.pdf    # Final PDF ✓
```

## Key Points

1. **Background.png is embedded per-slide** - Each slide gets its own copy of background.png embedded as `Slide-N-image-1.png`

2. **Media count**: ~195 media files (12 generated backgrounds + 25 available backgrounds + other images)

3. **File size**: ~40-50 MB PowerPoint (larger due to embedded backgrounds)

4. **All backgrounds work**: Both generated slides AND reference slides have correct viAct backgrounds

5. **Relationships preserved**: html2pptx creates correct rId mappings for all images

## One-Time Setup

**Converting AvailableSlide11.pptx to HTML only needs to be done once.**

After that, the HTML files are permanently stored in:
- `~/.claude/skills/quotation_skill/assets/available_slides_html/`

You can reuse them for all future proposals.
