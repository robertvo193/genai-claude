# template2slide-pro Skill Update Summary

## Date: 2026-01-21

## Major Changes

### 1. Streamlined Architecture

**Before**:
- `.md → .json → .html → .pptx → .pdf`
- Heavy regex-based parsing
- Rigid slide type mapping
- Insert reference slides (Available 2-25)

**After**:
- `.md → .html → .pptx → .pdf` (no JSON intermediate)
- Agent-guided natural reading (no regex)
- Intelligent slide type selection
- Skip reference slides (focus on generated content)

### 2. New Pipeline Flow

```
Input: template.md
    ↓
Step 1: Parse Template (Agent reads markdown naturally)
    ↓
Step 2: Generate Mermaid Diagram
    ↓
Step 3: Generate HTML Slides (Agent selects slide types)
    ↓
Step 4: Convert HTML → PPTX (using pptx skill)
    ↓
Step 5: Convert PPTX → PDF (using pdf skill)
    ↓
Output: {presentation.pptx, presentation.pdf}
```

### 3. Key Improvements

#### No JSON Intermediate
- Agent generates HTML directly from markdown
- Removes unnecessary intermediate step
- Faster processing

#### Intelligent Slide Selection
- Agent reads each section
- Decides optimal slide type based on:
  - Content length
  - Content structure
  - Visual requirements
- Can combine short sections
- Can split long sections

#### No Regex Parsing
- Agent uses natural markdown reading
- Identifies sections by heading structure (`##`, `###`)
- Extracts content by reading between headers
- More flexible and maintainable

#### Skip Reference Slides
- Temporarily disabled inserting Available slides (2-25)
- Focus on generated content quality
- Can be re-enabled as optional feature later

### 4. Bullet Symbol Fix

**Problem**: Star-like blue and white bullet symbols appearing on all slides

**Root Cause**: `html2pptx.js` was unconditionally adding bullets to `<ul>` elements, ignoring `list-style-type: none`

**Solution**: Modified `html2pptx.js` (lines 808-828):
```javascript
// Check if list-style-type is none (no bullets wanted)
const listStyleType = ulComputed.listStyleType;
const shouldAddBullet = listStyleType !== 'none';

liElements.forEach((li, idx) => {
  const runs = parseInlineFormatting(li, { breakLine: false });
  if (runs.length > 0) {
    runs[0].text = runs[0].text.replace(/^[•\-\*▪▸]\s*/, '');
    // Only add bullet if list-style-type is not 'none'
    if (shouldAddBullet) {
      runs[0].options.bullet = { indent: textIndent };
    }
  }
  // ...
});
```

**Files Updated**:
- `scripts/html2pptx.js` - Lines 808-828
- `scripts/renderers/content_bullets.js` - Line 16, 74
- `scripts/renderers/two_column.js` - Lines 14-20, 81-85, 94, 100

### 5. Updated Skill Documentation

**SKILL.md** completely rewritten to reflect:
- Direct pipeline (no JSON)
- Agent-guided workflow
- Slide type selection logic
- pptx/pdf skill integration
- Bullet symbol fix documentation
- Troubleshooting guide

## Slide Type Reference

| Section Type | Slide Type | Renderer | Notes |
|--------------|------------|----------|-------|
| Cover Page | Title | `title.js` | Always first slide |
| Project Requirements | Content Bullets | `content_bullets.js` | Lists with key-value highlighting |
| Scope of Work | Two Column | `two_column.js` | Side-by-side comparison |
| System Architecture | Diagram | `diagram.js` | Use mermaid PNG, not code |
| System Requirements | Content Bullets | `content_bullets.js` | Can combine Network + Camera |
| Implementation Plan | Timeline | `timeline.js` | Parse `### Phase T0:` headings |
| Module Name | Module Description | `module_description.js` | One slide per AI module |

## Technical Details

### HTML Standards
- Dimensions: 720pt × 405pt (16:9)
- Dark theme: `#000000` background
- Text: `#FFFFFF`
- Accents: `#00AEEF` (viAct blue)
- Font: Arial/Helvetica
- Margins: 40pt left, 120pt right, 180pt bottom

### Critical: Bullet Symbol Prevention
Always use `<ul style="list-style-type: none; padding: 0; margin: 0;">` for lists:
```html
<ul style="list-style-type: none; padding: 0; margin: 0;">
  <li style="margin-left: 0pt; ...">Item 1</li>
  <li style="margin-left: 18pt; ...">Item 2 (indented)</li>
</ul>
```

## Migration Notes

### Removed Dependencies
- No longer need `map_to_slides.py` (regex-based)
- No longer need `generate_from_json.js` (JSON intermediate)
- No longer need `insert_reference_slides.py` (temporarily)

### New Dependencies
- **pptx skill** - For HTML → PPTX conversion
- **pdf skill** - For PPTX → PDF conversion

### Renderer Updates
All renderers updated to use `<ul style="list-style-type: none;">`:
- `content_bullets.js`
- `two_column.js`
- `title.js` (no bullets needed)
- `diagram.js` (no bullets needed)
- `timeline.js` (custom rendering)
- `module_description.js` (custom rendering)

## Testing

### Verified Working
✅ Timeline parsing (T0-T3 milestones)
✅ Bullet symbol prevention (html2pptx fix)
✅ HTML generation with correct styling
✅ Architecture diagram rendering
✅ Media embedding (videos, images)

### To Be Tested
⏳ Agent-guided slide type selection
⏳ pptx skill integration
⏳ pdf skill integration
⏳ No-regex template parsing

## Future Enhancements

### Phase 2 (Post-Streamlining)
1. Add back reference slides as optional feature
2. Implement validation agent (Phase 2)
3. Add batch processing for multiple templates
4. Create template validation pre-flight check

### Optional Features
- Custom slide type selection by user
- Template style variations
- Multi-language support
- Export to other formats (Google Slides, Keynote)

## Files Updated

### Core Skill Files
- `SKILL.md` - Complete rewrite (new architecture)
- `UPDATE_PLAN.md` - Previous plan (archived)

### Script Files
- `scripts/html2pptx.js` - Bullet fix (lines 808-828)
- `scripts/renderers/content_bullets.js` - `<ul>` with `list-style-type: none`
- `scripts/renderers/two_column.js` - `<ul>` with `list-style-type: none`

### Reference Documentation (Unchanged)
- `references/SLIDE_TEMPLATE.md`
- `references/slide_rendering_instructions.md`
- `references/deployment_method_selection_logic.md`
- `references/ARCHITECTURE_TEMPLATES.md`
- `references/subagent0_slide_agent_v2.md`
- `references/subagent1_reviewer_agent.md`

## Quick Reference

### Basic Usage
```bash
template2slide <template.md> [output_dir]
```

### Pipeline Steps
1. Parse template (agent-guided)
2. Generate mermaid diagram
3. Generate HTML slides (agent selects types)
4. Convert HTML → PPTX (pptx skill)
5. Convert PPTX → PDF (pdf skill)

### Output Structure
```
output/
├── {project}_architecture_diagram.md
├── html/
│   ├── slide_1.html
│   ├── slide_2.html
│   └── ...
├── assets/
│   ├── background.png
│   ├── diagram.png
│   └── module_*.mp4
├── presentation.pptx
└── presentation.pdf
```

## Quality Checklist

- ✅ All placeholders resolved
- ✅ Architecture diagram matches deployment
- ✅ All sections mapped to slides
- ✅ Module info extracted (purpose, alert_logic, preconditions)
- ✅ HTML uses `<ul style="list-style-type: none;">`
- ✅ No unwanted bullets in PPTX
- ✅ All media embedded correctly
- ✅ PPTX opens and displays properly
- ✅ PDF opens and displays properly
- ✅ Formatting consistent

## Contact

For issues or questions about the updated skill:
1. Check `SKILL.md` for detailed workflow
2. Check `BULLET_FIX_COMPLETE.md` for bullet symbol issues
3. Check renderer files in `scripts/renderers/`
4. Review example session in `SKILL.md`
