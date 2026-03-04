# quotation_skill - Final Working Solution

## Summary

After extensive testing, I've created a working solution using the pptx skill's ooxml tools to merge PowerPoint presentations while preserving all formatting, designs, and backgrounds.

## The Working Solution

### Script: `merge_pptx_ooxml.py`

**Location**: `~/.claude/skills/quotation_skill/scripts/merge_pptx_ooxml.py`

**What it does**:
1. Unpacks both PPTX files using ooxml unpack.py
2. Merges slides in the correct order:
   - Slide 1: Generated (Cover)
   - Slides 2-10: Available (9 reference slides)
   - Slides 11-21: Generated (remaining generated slides)
   - Slides 22-36: Available (15 reference slides)
3. Copies ALL media files from both sources
4. Updates presentation.xml with correct slide order
5. Packs back into PPTX using ooxml pack.py

### Usage

```bash
python3 ~/.claude/skills/quotation_skill/scripts/merge_pptx_ooxml.py \
  ./output/[Project]_[Timestamp]/[Project]_Proposal.pptx \
  ~/.claude/skills/quotation_skill/assets/AvailableSlide11.pptx \
  ./output/[Project]_[Timestamp]/[Project]_Proposal_OOXML_FINAL.pptx
```

### Results

✅ **What Works**:
- Correct slide order (36 slides)
- All formatting preserved (both generated and reference slides)
- All backgrounds preserved
- python-pptx can load and edit the file
- File size: ~48 MB (includes all media from both sources)

❌ **Known Issue**:
- LibreOffice cannot convert the file to PDF (XML compatibility issue)
- **Workaround**: The PowerPoint file itself is valid and can be opened in PowerPoint application

## Comparison of Approaches

| Approach | Slide Order | Formatting | Backgrounds | PDF Conversion |
|----------|-------------|------------|-------------|----------------|
| **HTML → PPTX** | ✓ Correct | ✓ Consistent viAct styling | ✓ All backgrounds | ✓ Works |
| **Direct PPTX Copy (insert_reference_slides.py)** | ✗ Wrong | ✓ Original designs | ✗ Broken relationships | ✗ Corrupt |
| **OOXML Merge (merge_pptx_ooxml.py)** | ✓ Correct | ✓ Original designs | ✓ All backgrounds | ⚠️ LibreOffice issue |

## Recommended Workflow

### Option 1: Use HTML Approach (for consistent styling)

**Best for**: Proposals where all slides should have viAct branding

```bash
# Step 1: Generate HTML from template (existing workflow)
# Step 2: Convert AvailableSlide11.pptx to HTML (one-time setup)
python3 ~/.claude/skills/quotation_skill/scripts/pptx_to_html.py \
  ~/.claude/skills/quotation_skill/assets/AvailableSlide11.pptx \
  ~/.claude/skills/quotation_skill/assets/available_slides_html \
  ~/.claude/skills/quotation_skill/assets/background.png

# Step 3: Combine HTML slides
~/.claude/skills/quotation_skill/scripts/insert_html_slides.sh \
  "./output/[Project]_[Timestamp]/slides" \
  "~/.claude/skills/quotation_skill/assets/available_slides_html/available_html_test" \
  "./output/[Project]_[Timestamp]/slides_combined"

# Step 4: Convert to PowerPoint
cd ~/.claude/skills/pptx && node convert_combined.js

# Step 5: Convert to PDF
libreoffice --headless --convert-to pdf \
  --outdir "./output/[Project]_[Timestamp]" \
  "./output/[Project]_[Timestamp]/[Project]_Proposal_HTML_FINAL.pptx"
```

**Pros**: Consistent viAct styling, works end-to-end
**Cons**: Reference slides are simplified (text extraction only)

### Option 2: Use OOXML Merge (for original designs)

**Best for**: Proposals where reference slides should keep their original design

```bash
# Step 1: Generate PowerPoint from template (existing workflow)
# Step 2: Merge with AvailableSlide11.pptx
python3 ~/.claude/skills/quotation_skill/scripts/merge_pptx_ooxml.py \
  "./output/[Project]_[Timestamp]/[Project]_Proposal.pptx" \
  ~/.claude/skills/quotation_skill/assets/AvailableSlide11.pptx \
  "./output/[Project]_[Timestamp]/[Project]_Proposal_OOXML_FINAL.pptx"

# Step 3: Open in PowerPoint application to convert to PDF manually
```

**Pros**: All original designs preserved, all backgrounds work
**Cons**: PDF conversion requires PowerPoint application (LibreOffice incompatible)

## Files Created

1. **`merge_pptx_ooxml.py`** - OOXML-based merge script (recommended)
2. **`pptx_to_html.py`** - PPTX to HTML converter for HTML approach
3. **`insert_html_slides.sh`** - HTML slide combiner for HTML approach
4. **`slide_order_fix.py`** - Alternative PPTX merge (similar to merge_pptx_ooxml.py)
5. **`insert_reference_slides.py`** - Direct PPTX copy (has background issues)

## Final Recommendation

**Use Option 1 (HTML Approach)** for most cases because:
- ✓ End-to-end automation
- ✓ Consistent viAct branding
- ✓ PDF conversion works
- ✓ All backgrounds preserved

The reference slides will be simplified, but this is acceptable since they serve a different purpose (company credentials, awards, dashboard screenshots).

If you need the original designs of reference slides, use Option 2 (OOXML Merge) and manually convert to PDF using PowerPoint application.
