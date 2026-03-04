# Smart Overflow Detection in quotation_skill

## Overview

As of January 2026, quotation_skill includes **smart overflow detection** that prevents the need for tiny, unreadable fonts.

## The Problem

**Previous approach**:
- Text overflowing? → Make fonts smaller (9pt, 8pt...)
- Result: Unreadable slides 😞

**New approach**:
- Text overflowing? → Use two-column layout or split into 2 slides
- Result: Readable 10pt fonts ✅

## Smart Overflow Detection

### Implementation in html2pptx.js

```javascript
function validateTextBoxPosition(slideData, bodyDimensions) {
  const slideWidthInches = bodyDimensions.width / PX_PER_IN;
  const slideHeightInches = bodyDimensions.height / PX_PER_IN;
  const maxPageCoverage = 0.9; // 90% of page
  const maxArea = slideWidthInches * slideHeightInches * maxPageCoverage;

  for (const el of slideData.elements) {
    if (['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'list'].includes(el.type)) {
      const textBoxArea = el.position.w * el.position.h;

      // CHECK: Text box covers too much of the page
      if (textBoxArea > maxArea) {
        const coveragePercent = (textBoxArea / (slideWidthInches * slideHeightInches)) * 100;
        errors.push(
          `⚠️ Text box covers ${coveragePercent.toFixed(1)}% of slide (>90% limit). ` +
          `Solution: Use two-column layout or split into 2 slides.`
        );
      }
    }
  }
  return errors;
}
```

### How It Works

1. **Calculates text box area**: `width × height` in inches
2. **Calculates slide area**: `slideWidth × slideHeight` in inches
3. **Checks coverage**: `textBoxArea / slideArea`
4. **If > 90%**: Throws error with helpful message

### Example Error Message

```
⚠️ Text box "Phase T1: Hardware Depl..." covers 92.3% of slide (>90% limit). 
Solution: Use two-column layout or split into 2 slides. 
Current size: 8.50" × 3.90"
```

## Decision Tree

```
┌─────────────────────────────────────┐
│  Create slide with 10pt fonts      │
└──────────────┬──────────────────────┘
               │
               ▼
       ┌───────────────┐
       │ Does it fit?  │
       └───┬───────┬───┘
           │       │
          YES      NO
           │       │
           ▼       ▼
    ┌──────────┐  ┌─────────────────────┐
    │ ✅ Done  │  │ Use two-column     │
    └──────────┘  │ (Templates 3 or 7) │
                  └─────────┬───────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Does it fit?  │
                    └───┬───────┬───┘
                        │       │
                       YES      NO
                        │       │
                        ▼       ▼
                 ┌──────────┐ ┌──────────────┐
                 │ ✅ Done  │ │ Split into   │
                 └──────────┘ │ 2 slides     │
                              └──────────────┘
```

## Template Selection Guide

| Template | Layout | Use When | Font Size |
|----------|--------|----------|-----------|
| 1 | Cover | Title page | N/A |
| 2 | Single column | Short lists | 10pt |
| 3 | Two columns | Side-by-side comparison | 10pt |
| 4 | Sections + bullets | Multiple sections | 10pt |
| 5 | Module | AI module description | 10pt |
| 6 | Timeline (1 col) | 1-3 phases | 10pt |
| **7** | **Timeline (2 col)** | **4+ phases** | **10pt** ✅ |

## Bromma Malaysia Example

### Before (Single Column)
- Template 6 (single column)
- 4 phases with tasks
- Overflow with 10pt fonts
- Had to use 9pt → unreadable

### After (Two Columns)
- Template 7 (two columns)
- Same 4 phases
- Fits with 10pt fonts ✅
- Readable and professional

## Implementation Steps

### 1. Create Single-Column Slide First
```bash
# Use Template 2, 4, 5, or 6
# Set font-size: 10pt
# Test conversion
```

### 2. Check for Overflow Error
```bash
cd ~/.claude/skills/pptx
node convert_script.js

# If you see:
# ⚠️ Text box covers XX% of slide
# → Proceed to step 3
```

### 3. Convert to Two-Column Layout
```html
<!-- OLD: Single column -->
<div class="content">
  <h2>Section 1</h2>
  <ul><li>Item 1</li></ul>
  <h2>Section 2</h2>
  <ul><li>Item 2</li></ul>
  <h2>Section 3</h2>
  <ul><li>Item 3</li></ul>
  <h2>Section 4</h2>
  <ul><li>Item 4</li></ul>
</div>

<!-- NEW: Two columns -->
<div class="columns">
  <div class="column">
    <h2>Section 1</h2>
    <ul><li>Item 1</li></ul>
    <h2>Section 2</h2>
    <ul><li>Item 2</li></ul>
  </div>
  <div class="column">
    <h2>Section 3</h2>
    <ul><li>Item 3</li></ul>
    <h2>Section 4</h2>
    <ul><li>Item 4</li></ul>
  </div>
</div>
```

### 4. Update CSS
```css
/* OLD */
.content {
  margin: 0 140pt 110pt 40pt;
}

/* NEW */
.columns {
  display: flex;
  gap: 40pt;
  flex: 1;
  margin: 0 40pt 110pt 40pt;  /* Smaller side margins for columns */
}
.column {
  flex: 1;
  overflow-y: auto;
}
```

### 5. Reconvert and Verify
```bash
node convert_script.js
libreoffice output.pptx  # Open and verify visually
```

## Best Practices

1. **Start with 10pt fonts** - Don't go smaller
2. **Use two columns early** - Don't wait for overflow
3. **Split if needed** - 3 slides better than unreadable
4. **Always verify** - Open PowerPoint and check

## Technical Details

### Why 90% Threshold?

- Slide size: 10" × 5.625" (16:9) = 56.25 in²
- 90% threshold: 50.6 in²
- Leaves 10% buffer for margins and rendering differences
- PowerPoint renders ~5-10% larger than HTML

### Why Not 100%?

- PowerPoint's text engine differs from browser
- Line breaking may create different text heights
- Font metrics differ between browser and PowerPoint
- 90% provides safety margin

### Font Size Guidelines

| Content | Minimum | Recommended | Maximum |
|---------|---------|-------------|---------|
| Body text | 10pt | 10-11pt | 12pt |
| Headers (h2) | 14pt | 14-16pt | 18pt |
| Slide title | 24pt | 28pt | 32pt |

**Never go below 10pt for body text!**

## Files Modified

1. **~/.claude/skills/pptx/scripts/html2pptx.js**
   - Added smart overflow detection (line 88-145)
   - Checks text box area > 90% of slide area

2. **~/.claude/skills/quotation_skill/SKILL.md**
   - Updated overflow prevention section
   - Added decision tree and template guide

3. **~/.claude/skills/quotation_skill/templates/SLIDE_TEMPLATES.html**
   - Added Template 7: Two-Column Timeline
   - Standardized all templates to 140pt/110pt margins

## Summary

✅ **Smart overflow detection** prevents tiny fonts
✅ **Two-column layouts** maintain readability  
✅ **Decision tree** guides template selection
✅ **10pt minimum** ensures legibility
✅ **Visual verification** catches remaining issues

No more 9pt fonts! 🎉
