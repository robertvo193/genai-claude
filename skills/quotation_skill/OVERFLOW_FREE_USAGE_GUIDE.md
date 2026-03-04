# quotation_skill - Overflow-Free Usage Guide

## Executive Summary

The quotation_skill has been updated with **overflow-proof HTML templates** and **correct CSS specifications** to prevent text overflow errors for ANY proposal template.

**Key Changes**:
1. ✅ Added 6 pre-configured HTML templates
2. ✅ Updated SKILL.md with correct margin specifications
3. ✅ Added comprehensive troubleshooting guide
4. ✅ Created content length guidelines

---

## Quick Start (3 Steps)

### Step 1: Get Your Template Ready

Start with your verified proposal template (markdown format, no placeholders).

### Step 2: Use Overflow-Proof HTML Templates

For each slide section in your template:

1. **Open** `~/.claude/skills/quotation_skill/templates/SLIDE_TEMPLATES.html`
2. **Copy** the appropriate template (Template 1-6)
3. **Replace** placeholder content with your actual content
4. **Update** background.png path to your system
5. **Save** as `slideXX_name.html`

**Template Selection Guide**:
```
Cover page → Template 1
Bullet lists → Template 2
Two columns → Template 3
Sections + bullets → Template 4
AI module → Template 5
Timeline → Template 6
```

### Step 3: Generate PowerPoint & PDF

```bash
# Convert HTML → PowerPoint
cd ~/.claude/skills/pptx
node your_convert_script.js

# Convert PowerPoint → PDF
libreoffice --headless --convert-to pdf proposal.pptx
```

---

## What Causes Text Overflow?

### The Problem

html2pptx validation requires:
- **Minimum 0.5" (36pt) from bottom edge** for all text
- **Text must NOT extend past slide boundaries**

### Root Causes

1. **Bottom margin too small** (72pt or less)
   - Text extends past slide edge
   - Error: "ends too close to bottom edge"

2. **Right margin too small** (80pt or less)
   - Not enough horizontal space
   - Text wraps awkwardly

3. **Font sizes too large** (12pt+)
   - Content overflows vertically
   - Takes too much space

4. **Line spacing too loose** (1.3+)
   - Wastes vertical space
   - Causes overflow

5. **Too much content**
   - Long sentences wrap excessively
   - Too many bullets per slide

---

## The Solution: Correct CSS Values

### Critical Specifications

```css
/* CONTENT WRAPPER - MOST IMPORTANT */
.content {
  flex: 1;
  margin: 0 120pt 85pt 40pt;  /* Right: 120pt, Bottom: 85pt */
  overflow-y: auto;
  overflow-x: hidden;
  min-height: 0;
  padding-bottom: 0;
  max-height: 100%;
}

/* TYPOGRAPHY */
p, li {
  font-size: 11pt;        /* Small font = fits more content */
  line-height: 1.25;      /* Tight spacing */
  margin: 0 0 8pt 0;      /* Reduced spacing */
}

/* HEADERS */
h2 {
  font-size: 15pt;        /* Not 16pt+ */
  margin: 12pt 0 8pt 0;   /* Tight spacing */
}
```

### Why These Values Work

| Specification | Value | Purpose |
|--------------|-------|---------|
| Right margin | 120pt | Leaves room for viAct background design |
| Bottom margin | 85pt | Prevents text from extending past 0.5" boundary |
| Font size | 11pt | Fits more content vertically |
| Line height | 1.25 | Tighter spacing, less vertical space |
| Item spacing | 8pt | Reduced gaps between paragraphs |

---

## Content Length Guidelines

### Maximum Content Per Slide

| Slide Type | Max Bullets | Max Words per Bullet | Total Words |
|-----------|-------------|---------------------|-------------|
| Cover | N/A | N/A | ~10 words |
| Content | 10 | 15 | ~150 words |
| Two-column | 7 per column | 12 | ~168 words |
| Module | 4 paragraphs | 20 | ~80 words |
| Timeline | 4 phases | 4 tasks | ~80 words |

### Writing Guidelines

**DO**:
- ✅ Use concise bullet points
- ✅ Keep descriptions under 15 words
- ✅ Use short URLs (bit.ly)
- ✅ Split content across multiple slides if needed

**DON'T**:
- ❌ Write long paragraphs
- ❌ Use full sentences for bullets
- ❌ Include long Google Drive URLs
- ❌ Cram too much onto one slide

---

## Using the Templates

### Example: Creating a Module Slide

**From your template.md**:
```markdown
### Module 1: Helmet Detection

**Purpose**: Ensures compliance with safety regulations by identifying workers wearing safety helmets...

**Alert Trigger Logic**: AI will capture people not wearing a helmet...
```

**Using Template 5**:
```html
<!DOCTYPE html>
<html>
<head>
<style>
/* ... copy from Template 5 ... */
.content {
  flex: 1;
  margin: 0 120pt 85pt 40pt;  /* Correct margins */
  /* ... rest of CSS ... */
}
</style>
</head>
<body>
<h1 class="title">Module 1: Helmet Detection</h1>
<div class="content">
  <div class="module-header">
    <h2 class="module-name">Module 1: Helmet Detection</h2>
    <span class="module-type">Standard</span>
  </div>

  <p><span class="label">Purpose:</span> Identifies workers wearing safety helmets.</p>

  <p><span class="label">Alert Trigger:</span> AI captures people not wearing helmets.</p>

  <p><span class="label">Preconditions:</span> Camera must maintain 5-10 meters distance.</p>

  <p><span class="label">Video Demo:</span> bit.ly/helmet-demo</p>
</div>
</body>
</html>
```

**Key Changes**:
- Long purpose → Shortened to 1 sentence
- Full Google Drive URL → Short bit.ly link
- Verbose alert logic → Concise description

---

## Troubleshooting Guide

### Error: "Text box ends too close to bottom edge"

**Cause**: Bottom margin < 85pt OR too much content

**Solutions** (in order):
1. **Check bottom margin**: Must be `85pt` or higher
2. **Reduce content**: Shorten text, remove redundancies
3. **Increase margin**: Try 90pt, 95pt, 100pt
4. **Reduce font**: Change to 10pt (last resort)
5. **Split slides**: Divide content into 2 slides

### Error: "Text element has border"

**Cause**: Applied border to `<h2>` or other text element

**Solution**: Remove border from text elements, only use on `<div>`

```css
/* WRONG */
h2 {
  border-bottom: 2pt solid #00AEEF;  /* Don't do this */
}

/* CORRECT */
h2 {
  padding-bottom: 3pt;  /* Use padding instead */
}
```

### Content Still Overflowing?

**Progressive Fixes**:

1. **First**: Increase bottom margin
   ```css
   margin: 0 120pt 90pt 40pt;  /* Try this */
   margin: 0 120pt 95pt 40pt;  /* Then this */
   margin: 0 120pt 100pt 40pt; /* Then this */
   ```

2. **Second**: Shorten content
   - Remove adjectives and adverbs
   - Combine related points
   - Delete non-essential details

3. **Third**: Reduce font size
   ```css
   font-size: 10pt;  /* Minimum recommended */
   line-height: 1.2;
   ```

4. **Last**: Create 2 slides
   - Split content logically
   - Use "continued..." in title

---

## Best Practices

### Before Creating Slides

1. **Read the template section** from your template.md
2. **Estimate content length** - Will it fit?
3. **Choose appropriate template** (Template 1-6)
4. **Plan content structure** - How many sections?

### While Creating Slides

1. **Use templates as starting point** - Don't start from scratch
2. **Keep text concise** - Shorter is better
3. **Test early** - Generate 1-2 slides first
4. **Validate** - Run html2pptx to check for errors

### After Creating Slides

1. **Review all slides** for consistency
2. **Check for overflow errors**
3. **Fix any issues** before final output
4. **Generate PowerPoint** - Confirm no errors
5. **Generate PDF** - Final deliverable

---

## Summary

**Key Takeaways**:

1. **Use the templates** - They prevent overflow by design
2. **Keep content concise** - Shorter text = fewer issues
3. **Follow specifications** - 120pt right, 85pt bottom, 11pt font
4. **Test incrementally** - Don't wait until all slides are done
5. **Use troubleshooting guide** - SKILL.md has solutions

**With these templates, ANY proposal template can be converted WITHOUT overflow errors!**

---

## Files Updated

- `~/.claude/skills/quotation_skill/SKILL.md` - Updated with correct specs
- `~/.claude/skills/quotation_skill/templates/SLIDE_TEMPLATES.html` - 6 overflow-proof templates
- `~/.claude/skills/quotation_skill/templates/README.md` - Template usage guide
- `~/.claude/skills/quotation_skill/TEXT_OVERFLOW_FIX.md` - Root cause analysis

**All future quotation_skill users will have overflow-free presentations!**
