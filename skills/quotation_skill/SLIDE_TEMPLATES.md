# Slide Layout Templates

This document provides standardized HTML slide templates for generating consistent viAct proposals.

## Overview

All slides follow viAct branding with:
- **Background**: viAct blue background (#00AEEF)
- **Font**: Arial, Helvetica, Verdana (web-safe)
- **Size**: 720pt × 405pt (16:9)
- **Margins**: Title `30pt 120pt 20pt 40pt`, Content `0 120pt 85pt 40pt`

## Template Library

### Template 1: Simplified Cover Page

**Use Case**: Title slide for proposal
**Features**: Title and client name on same line, date below

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {
            size: 720pt 405pt;
            margin: 0;
        }
        body {
            margin: 0;
            padding: 0;
            width: 720pt;
            height: 405pt;
            background-image: url('file:///home/philiptran/.claude/skills/quotation_skill/assets/background.png');
            background-size: cover;
            background-position: center;
            font-family: Arial, Helvetica, Verdana, sans-serif;
        }
        .content {
            padding: 100pt 80pt 120pt 80pt;
            height: 185pt;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .title-line {
            font-size: 32pt;
            font-weight: bold;
            margin: 0 0 60pt 0;
            text-transform: uppercase;
            line-height: 1.2;
        }
        .title-text {
            color: #FFFFFF;
            padding-right: 10pt;
        }
        .client-name {
            color: #FF9900;
            padding-left: 10pt;
        }
        .date {
            font-size: 14pt;
            color: #FFFFFF;
            margin: 0;
            line-height: 1.3;
        }
    </style>
</head>
<body>
    <div class="content">
        <p class="title-line">
            <span class="title-text">Video Analytics Solution Proposal</span>
            <span class="client-name">[Client Name]</span>
        </p>
        <p class="date">[Date]</p>
    </div>
</body>
</html>
```

**Key Features**:
- "Video Analytics Solution Proposal" (white) and "[Client Name]" (orange) on SAME LINE
- Both are same size (32pt), bold, uppercase
- Client name has 10pt left padding for spacing (use padding, not margin on inline elements)
- Date below in white (14pt)
- Clean, single-line title layout

---

### Template 2: Standard Content Slide

**Use Case**: General content with bullets, sections
**Features**: Single column with section headers

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {
            size: 720pt 405pt;
            margin: 0;
        }
        body {
            margin: 0;
            padding: 0;
            width: 720pt;
            height: 405pt;
            background-image: url('file:///home/philiptran/.claude/skills/quotation_skill/assets/background.png');
            background-size: cover;
            background-position: center;
            font-family: Arial, Helvetica, Verdana, sans-serif;
        }
        .title {
            margin: 30pt 120pt 20pt 40pt;
            font-size: 28pt;
            font-weight: bold;
            color: #FFFFFF;
            text-transform: uppercase;
        }
        .content {
            margin: 0 120pt 85pt 40pt;
            font-size: 11pt;
            color: #FFFFFF;
            line-height: 1.25;
        }
        h2 {
            font-size: 15pt;
            font-weight: bold;
            margin: 15pt 0 10pt 0;
            color: #00AEEF;
        }
        p, li {
            margin: 5pt 0;
            line-height: 1.25;
        }
        ul {
            margin: 5pt 0;
            padding-left: 20pt;
        }
    </style>
</head>
<body>
    <div class="title"><p>[SLIDE TITLE]</p></div>
    <div class="content">
        <h2>[Section Header]</h2>
        <p>[Content paragraph]</p>
        <ul>
            <li>[Bullet point 1]</li>
            <li>[Bullet point 2]</li>
        </ul>
    </div>
</body>
</html>
```

---

### Template 3: Two-Column Layout

**Use Case**: Side-by-side content comparison
**Features**: Equal-width columns

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {
            size: 720pt 405pt;
            margin: 0;
        }
        body {
            margin: 0;
            padding: 0;
            width: 720pt;
            height: 405pt;
            background-image: url('file:///home/philiptran/.claude/skills/quotation_skill/assets/background.png');
            background-size: cover;
            background-position: center;
            font-family: Arial, Helvetica, Verdana, sans-serif;
        }
        .title {
            margin: 30pt 120pt 20pt 40pt;
            font-size: 28pt;
            font-weight: bold;
            color: #FFFFFF;
            text-transform: uppercase;
        }
        .content {
            margin: 0 120pt 85pt 40pt;
            font-size: 11pt;
            color: #FFFFFF;
            line-height: 1.25;
        }
        .columns {
            display: flex;
            gap: 30pt;
        }
        .column {
            flex: 1;
        }
        h2 {
            font-size: 15pt;
            font-weight: bold;
            margin: 15pt 0 10pt 0;
            color: #00AEEF;
        }
        p, li {
            margin: 5pt 0;
            line-height: 1.25;
        }
        ul {
            margin: 5pt 0;
            padding-left: 20pt;
        }
    </style>
</head>
<body>
    <div class="title"><p>[SLIDE TITLE]</p></div>
    <div class="content">
        <div class="columns">
            <div class="column">
                <h2>[Left Section Header]</h2>
                <ul>
                    <li>[Left content 1]</li>
                    <li>[Left content 2]</li>
                </ul>
            </div>
            <div class="column">
                <h2>[Right Section Header]</h2>
                <ul>
                    <li>[Right content 1]</li>
                    <li>[Right content 2]</li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
```

---

### Template 4: AI Modules Overview ⚠️ DEPRECATED

**Status**: DO NOT USE - This template has been deprecated
**Reason**: AI Modules overview slide is no longer needed in proposals
**Action**: Proceed directly to individual module slides (Template 5)

---

### Template 5: AI Module Detail (Two-Column)

**Use Case**: Individual AI module slides
**Features**: Text on left, video/image placeholder on right with URL

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {
            size: 720pt 405pt;
            margin: 0;
        }
        body {
            margin: 0;
            padding: 0;
            width: 720pt;
            height: 405pt;
            background-image: url('file:///home/philiptran/.claude/skills/quotation_skill/assets/background.png');
            background-size: cover;
            background-position: center;
            font-family: Arial, Helvetica, Verdana, sans-serif;
        }
        .title {
            margin: 30pt 120pt 20pt 40pt;
            font-size: 28pt;
            font-weight: bold;
            color: #FFFFFF;
            text-transform: uppercase;
        }
        .content {
            margin: 0 120pt 85pt 40pt;
            font-size: 11pt;
            color: #FFFFFF;
            line-height: 1.25;
        }
        .columns {
            display: flex;
            gap: 30pt;
        }
        .column-left {
            flex: 1.2;
        }
        .column-right {
            flex: 0.8;
        }
        h2 {
            font-size: 13pt;
            font-weight: bold;
            margin: 12pt 0 8pt 0;
            color: #00AEEF;
        }
        p {
            margin: 5pt 0;
            line-height: 1.25;
        }
        .video-link {
            font-size: 9pt;
            color: #FFFFFF;
            margin: 10pt 0;
            line-height: 1.2;
        }
        .placeholder {
            background: rgba(255,255,255,0.1);
            border: 2pt dashed #00AEEF;
            padding: 20pt;
            text-align: center;
            min-height: 120pt;
            display: flex;
            align-items: center;
            justify-content: center;
        }
    </style>
</head>
<body>
    <div class="title"><p>Module X: [Module Name]</p></div>
    <div class="content">
        <div class="columns">
            <div class="column-left">
                <h2>Purpose</h2>
                <p>[Module purpose description]</p>

                <h2>Alert Trigger Logic</h2>
                <p>[Alert trigger description]</p>

                <h2>Preconditions</h2>
                <p>[Preconditions description]</p>
            </div>
            <div class="column-right">
                <div class="placeholder">
                    <p style="font-size: 10pt; color: #00AEEF;">[Video/Image]</p>
                </div>
                <p class="video-link"><strong>Video URL:</strong></p>
                <p class="video-link" style="word-break: break-all;">[Google Drive URL]</p>
            </div>
        </div>
    </div>
</body>
</html>
```

**Key Features**:
- **Left column (60%)**: Text content (Purpose, Alert Trigger Logic, Preconditions)
- **Right column (40%)**:
  - Placeholder box for video/image
  - Video URL link below
- **Title format**: "Module X: [Module Name]" (not "MODULES & FUNCTIONAL DESCRIPTION")

---

### Template 6: Timeline (Two-Column)

**Use Case**: Implementation phases and timelines
**Features**: Phases split across two columns

> **NOTE**: Previously labeled as Template 6, now Template 5 after deprecating AI Modules Overview

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {
            size: 720pt 405pt;
            margin: 0;
        }
        body {
            margin: 0;
            padding: 0;
            width: 720pt;
            height: 405pt;
            background-image: url('file:///home/philiptran/.claude/skills/quotation_skill/assets/background.png');
            background-size: cover;
            background-position: center;
            font-family: Arial, Helvetica, Verdana, sans-serif;
        }
        .title {
            margin: 30pt 120pt 20pt 40pt;
            font-size: 28pt;
            font-weight: bold;
            color: #FFFFFF;
            text-transform: uppercase;
        }
        .content {
            margin: 0 120pt 85pt 40pt;
            font-size: 10pt;
            color: #FFFFFF;
            line-height: 1.2;
        }
        .columns {
            display: flex;
            gap: 25pt;
        }
        .column {
            flex: 1;
        }
        h2 {
            font-size: 13pt;
            font-weight: bold;
            margin: 12pt 0 8pt 0;
            color: #00AEEF;
        }
        p, li {
            margin: 4pt 0;
            line-height: 1.2;
        }
        ul {
            margin: 5pt 0;
            padding-left: 18pt;
        }
        .phase {
            font-size: 11pt;
            font-weight: bold;
            color: #FFFFFF;
            margin-bottom: 5pt;
        }
        .duration {
            font-style: italic;
            color: #00AEEF;
        }
    </style>
</head>
<body>
    <div class="title"><p>[TITLE]</p></div>
    <div class="content">
        <div class="columns">
            <div class="column">
                <p class="phase">Phase T0: [Phase Name]</p>
                <p class="duration">Duration: [Duration]</p>
                <ul>
                    <li>[Task 1]</li>
                    <li>[Task 2]</li>
                </ul>

                <p class="phase">Phase T1: [Phase Name]</p>
                <p class="duration">Duration: [Duration]</p>
                <ul>
                    <li>[Task 1]</li>
                    <li>[Task 2]</li>
                </ul>
            </div>
            <div class="column">
                <p class="phase">Phase T2: [Phase Name]</p>
                <p class="duration">Duration: [Duration]</p>
                <ul>
                    <li>[Task 1]</li>
                    <li>[Task 2]</li>
                </ul>

                <p class="phase">Phase T3: [Phase Name]</p>
                <p class="duration">Duration: [Duration]</p>
                <ul>
                    <li>[Task 1]</li>
                    <li>[Task 2]</li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
```

---

## Usage Guidelines

### Text Wrapping Rules (CRITICAL)

**ALL text MUST be wrapped in proper tags**:
- ✅ Correct: `<div><p>Text here</p></div>`
- ❌ Wrong: `<div>Text here</div>` - Text will NOT appear in PowerPoint
- ❌ Wrong: `<span>Text</span>` - Text will NOT appear in PowerPoint

**Valid text containers**: `<p>`, `<h1>`-`<h6>`, `<ul>`, `<ol>`

### Overflow Prevention

1. **Use two-column layouts** for content-heavy slides
2. **Maximum bottom margin**: 85pt (not 72pt)
3. **Font size**: Minimum 10pt for readability
4. **Test validation**: Run html2pptx to check for overflow

### Background Path

Always use absolute `file://` URLs:
```html
background-image: url('file:///home/philiptran/.claude/skills/quotation_skill/assets/background.png');
```

### Common Patterns

| Slide Type | Template | Columns |
|------------|----------|---------|
| Cover Page | Template 1 | N/A |
| General Content | Template 2 | 1 |
| Responsibilities | Template 3 | 2 |
| AI Module Detail | Template 5 | 2 (text/image) |
| Timeline | Template 6 | 2 |

> **Note**: Template 4 (AI Modules Overview) is deprecated and should not be used.

---

## Slide Naming Convention

Use descriptive names with sequential numbering:
- `slide01_cover.html`
- `slide02_requirements.html`
- `slide03_scope.html`
- `slide04_architecture.html`
- `slide05_requirements.html`
- `slide06_timeline.html`
- `slide07_module1_helmet.html`
- `slide08_module2_vest.html`
- `slide09_module3_fire.html`
- `slide10_module4_collision.html`
- `slide11_module5_intrusion.html`
- `slide12_module6_human_down.html`

> **Total**: 12 slides (no AI Modules Overview slide)

---

## Quick Reference: Color Palette

```css
/* viAct Branding */
--primary: #00AEEF;      /* viAct Blue - Headers, accents */
--text: #FFFFFF;          /* White - Body text on blue */
--text-dark: #1C2833;     /* Dark Navy - Body text on light */
--orange: #FF9900;        /* Orange - Client name accent on cover */

/* Module Slide Specifics */
--placeholder-bg: rgba(255,255,255,0.1);
--placeholder-border: 2pt dashed #00AEEF;
```

---

## Validation Checklist

Before generating PowerPoint:
- [ ] All text wrapped in `<p>`, `<h1>`-`<h6>`, `<ul>`, or `<ol>` tags
- [ ] Background uses absolute `file://` URL
- [ ] Content margins: `0 120pt 85pt 40pt` (bottom ≥85pt)
- [ ] Font size ≥10pt for body text
- [ ] No manual bullets (•, -, *) - use `<ul>`/`<ol>`
- [ ] Web-safe fonts only: Arial, Helvetica, Verdana
- [ ] Slide dimensions: 720pt × 405pt
- [ ] File naming: slideXX_name.html

---

**Generated**: 2026-01-23
**Skill**: quotation_skill
**Version**: 2.1

**Changes in v2.1**:
- Updated Template 1: Title and client name on same line
- Deprecated Template 4: AI Modules Overview (removed)
- Updated slide numbering: 12 slides total (was 13)
