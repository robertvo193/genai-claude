# Text Overflow Problem: Root Cause Analysis & Fix

## Problem Summary

The quotation_skill was generating HTML slides with **text overflow** - content extending beyond the slide boundaries, causing html2pptx validation errors like:

```
Text box "System Requirements" ends too close to bottom edge (-1.30" from bottom, minimum 0.5" required)
```

## Root Cause

### 1. **Incorrect Margin Specifications in SKILL.md**

The original quotation_skill SKILL.md had **incorrect/insufficient margin specifications**:

```markdown
### Slide Specifications
- **Size**: 720pt × 405pt (16:9 aspect ratio)
- **Margins**: 0.5" (36pt) on all sides  ❌ WRONG
- **Body Text**: 18-20px  ❌ TOO LARGE
```

**Problems**:
- **Bottom margin 72pt** → Text extends past slide edge (html2pptx requires minimum 0.5"/36pt from edge)
- **Right margin 80pt** → Not enough horizontal space for text
- **Font size 12pt+** → Content overflows vertically
- **Line height 1.3+** → Takes too much vertical space

### 2. **Missing Detailed Guidance**

The SKILL.md did NOT provide:
- ❌ Exact CSS values for margins
- ❌ Font size recommendations for different content types
- ❌ Line height specifications
- ❌ Step-by-step instructions for fixing overflow
- ❌ Example CSS that prevents overflow

### 3. **No Overflow Prevention Strategy**

The skill had **no proactive overflow prevention**:
- ❌ No warnings about common overflow causes
- ❌ No pre-flight checklist before generating slides
- ❌ No validation guidelines
- ❌ No troubleshooting section for overflow issues

## The Fix

### Updated SKILL.md Specifications

```markdown
### Typography (FIXED)
- **Font**: Arial, Helvetica, Verdana (web-safe)
- **Slide Title**: 28pt (uppercased, bold)
- **Section Headers**: 15pt (bold)
- **Body Text**: 11pt (regular)  ← REDUCED from 12pt
- **Line Height**: 1.2-1.25 (tight spacing)  ← TIGHTENED from 1.3

### Slide Specifications (CRITICAL - Prevents Text Overflow)
- **Size**: 720pt × 405pt (16:9 aspect ratio)
- **Title Margins**: `30pt 120pt 20pt 40pt` (top right bottom left)
- **Content Margins**: `0 120pt 85pt 40pt`  ← FIXED
  - **Right margin 120pt**: Leaves room for viAct logo/background
  - **Bottom margin 85pt**: Prevents text overflow (min 0.5" required)
```

### Safe CSS Template

```css
/* Content wrapper - CRITICAL MARGINS */
.content {
  flex: 1;
  margin: 0 120pt 85pt 40pt;  /* right=120pt, bottom=85pt */
  overflow-y: auto;
  overflow-x: hidden;
  min-height: 0;
  padding-bottom: 0;
  max-height: 100%;
}

/* Typography - smaller fonts */
p {
  margin: 0 0 8pt 0;      /* reduced spacing */
  font-size: 11pt;        /* smaller font */
  line-height: 1.25;      /* tighter spacing */
}

/* Headers */
h2 {
  font-size: 15pt;        /* not 16pt+ */
  margin: 12pt 0 8pt 0;   /* tighter spacing */
}
```

### Troubleshooting Section Added

Added comprehensive troubleshooting to SKILL.md:

| Issue | Solution |
|-------|----------|
| **Text overflow on slides** | **CRITICAL**: Increase bottom margin to 85pt minimum, reduce font size to 11pt |
| **"Text box ends too close to bottom edge"** | **Fix**: Change `margin: 0 80pt 72pt 40pt` to `margin: 0 120pt 85pt 40pt` |
| **Content extends past slide bottom** | **Fix**: Reduce content length or increase bottom margin in 5pt increments |

## Why quotation_skill Had This Problem

### Design Philosophy Gap

The quotation_skill was designed as a **high-level orchestration layer** that:
1. **Assumes** HTML slides are created correctly
2. **Delegates** actual HTML generation to AI/humans
3. **Provides** guidelines but NOT enforcement
4. **Lacks** automatic validation or pre-flight checks

### Missing Components

```
quotation_skill
├── ❌ NO HTML template generator
├── ❌ NO automatic overflow detection
├── ❌ NO CSS validation tool
├── ❌ NO content length checker
├── ✅ Has design guidelines
├── ✅ Has example HTML
└── ✅ Has troubleshooting (NOW ADDED)
```

### Manual Process Required

The current workflow **requires manual HTML creation**:

```
template.md
    ↓
[MANUAL PROCESS]  ← Where overflow happens
    ↓
AI reads template
    ↓
AI manually writes HTML  ← Must know correct margins/fonts
    ↓
html2pptx validates  ← Catches overflow AFTER creation
    ↓
Error!  ← Too late, must go back and fix HTML
```

## Best Practices Going Forward

### For quotation_skill Users

1. **Always use the safe CSS values** from SKILL.md
2. **Test incrementally** - Generate 1-2 slides first, validate, then continue
3. **Run html2pptx early** - Don't wait until all 12 slides are created
4. **Use shorter text** - Condense verbose descriptions
5. **Follow the troubleshooting guide** - Check SKILL.md first when errors occur

### For Future quotation_skill Improvements

**Recommended Additions**:
1. **HTML Template Generator** - Auto-generate HTML with correct CSS
2. **Pre-flight Validator** - Check HTML before running html2pptx
3. **Content Length Calculator** - Estimate if content fits in slide space
4. **Automatic Shortening** - AI assistance to condense long text
5. **CSS Template Library** - Ready-to-use CSS for different slide types

## Summary

**Root Cause**: quotation_skill SKILL.md had **insufficient/incorrect specifications** for margins, fonts, and spacing, leading to text overflow.

**Fix Applied**: Updated SKILL.md with:
- ✅ Correct margin specifications (120pt right, 85pt bottom)
- ✅ Smaller font sizes (11pt body, 15pt headers)
- ✅ Tighter line spacing (1.25)
- ✅ Comprehensive troubleshooting section
- ✅ Safe CSS template examples
- ✅ Step-by-step overflow prevention guide

**Result**: Future quotation_skill users will have **clear, correct specifications** to prevent text overflow before it happens.
