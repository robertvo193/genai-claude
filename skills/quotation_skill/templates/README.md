# quotation_skill HTML Templates

## Overview

This directory contains **overflow-proof HTML templates** that prevent text overflow issues when generating PowerPoint presentations.

## Problem These Templates Solve

**Text Overflow Error**:
```
Text box "Title" ends too close to bottom edge (-1.30" from bottom, minimum 0.5" required)
```

**Root Cause**: Incorrect margins, fonts, or spacing in HTML slides

**Solution**: Use these pre-configured templates with **correct CSS values**

## Templates Included

| Template File | Use Case | Slide Type |
|--------------|----------|------------|
| Template 1 | Cover page | Title slide |
| Template 2 | Bullet lists | Single column content |
| Template 3 | Two columns | Side-by-side comparison |
| Template 4 | Sections + bullets | Structured content |
| Template 5 | AI module | Module description slide |
| Template 6 | Timeline/phases | Implementation plan |

## How to Use

### Option 1: Copy Template (Recommended)

1. **Open** `SLIDE_TEMPLATES.html`
2. **Find** the template you need (e.g., "Template 2: Content Slide")
3. **Copy** the entire HTML code block
4. **Paste** into new file: `slides/slideXX_name.html`
5. **Replace** placeholder content with your actual content
6. **Update** background.png path (see below)
7. **Save** the file

### Option 2: Modify Existing Slide

If you have an existing slide with overflow issues, apply these fixes:

```css
/* Fix content margins */
.content {
  margin: 0 120pt 85pt 40pt;  /* Change to this */
}

/* Fix font sizes */
p, li {
  font-size: 11pt;        /* Change to this */
  line-height: 1.25;      /* Change to this */
}
```

## Critical CSS Values

These values are **calculated to prevent overflow**:

```css
/* Most Important - Prevents Overflow */
margin: 0 120pt 85pt 40pt;
  /* Right: 120pt - Leaves room for background design */
  /* Bottom: 85pt - Prevents text from extending past slide edge */

/* Typography */
font-size: 11pt;        /* Body text */
font-size: 15pt;        /* Section headers */
line-height: 1.25;     /* Tight spacing */
```

## Background Image Path

**IMPORTANT**: Update the background image path in each template:

```bash
# Get your absolute path
echo "file://$(realpath ~/.claude/skills/quotation_skill/assets/background.png)"

# Output example:
# file:////home/username/.claude/skills/quotation_skill/assets/background.png
```

Then replace in template:
```html
<!-- Replace this line -->
background-image: url('file:///absolute/path/to/quotation_skill/assets/background.png');

<!-- With your actual path -->
background-image: url('file:////home/YOUR_USERNAME/.claude/skills/quotation_skill/assets/background.png');
```

## Content Guidelines

To prevent overflow, **keep content concise**:

- **Bullets**: 10-15 words per bullet max
- **Purpose descriptions**: 1 sentence max
- **Lists**: 5-7 bullets per section
- **URLs**: Use short URLs (bit.ly) instead of long Google Drive links

## Troubleshooting

### Still Getting Overflow Errors?

1. **Increase bottom margin** by 5pt increments:
   - Try: `margin: 0 120pt 90pt 40pt;`
   - Then: `margin: 0 120pt 95pt 40pt;`

2. **Reduce content length**:
   - Shorten sentences
   - Remove unnecessary details
   - Split into 2 slides if needed

3. **Reduce font size** (last resort):
   - Try: `font-size: 10pt;` (minimum recommended)

## Quick Reference

| Content Type | Template | Max Bullets | Font Size |
|--------------|----------|-------------|-----------|
| Cover | Template 1 | N/A | 40pt/28pt |
| Bullets | Template 2 | 7-10 | 11pt |
| Two columns | Template 3 | 5-7 per column | 11pt |
| Sections | Template 4 | 5-7 per section | 11pt |
| Module | Template 5 | 4 paragraphs | 11pt |
| Timeline | Template 6 | 3-4 per phase | 10pt |

## Examples

See `output/Leda_Inio_20260121_002812/slides/` for real examples of slides created using these templates (no overflow errors).

## Support

For more details:
- See `SKILL.md` - Complete workflow guide
- See `TEXT_OVERFLOW_FIX.md` - Root cause analysis
- See `references/pptx_workflow.md` - PowerPoint generation details
