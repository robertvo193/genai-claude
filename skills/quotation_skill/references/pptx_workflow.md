# PowerPoint Generation Workflow (using pptx skill)

## Overview

This guide explains how to generate PowerPoint presentations from verified proposal templates using the `pptx` skill.

## Prerequisites

- Template verified (no placeholders)
- `pptx` skill available at `~/.claude/skills/pptx/`
- Node.js and required packages installed (pptxgenjs, playwright, sharp)

## html2pptx Workflow

The `pptx` skill provides the **html2pptx** workflow for converting HTML slides to PowerPoint with accurate positioning.

### Step 1: Design Your Slides

**Before writing code**, analyze content and choose design elements:

1. **Consider subject matter**: Video analytics for safety/compliance
2. **Check branding**: viAct blue (#00AEEF), professional styling
3. **Match palette to content**: Select colors reflecting the topic
4. **State your approach**: Explain design choices before implementation

**Design Principles** (from pptx skill):
- ✅ State content-informed design approach BEFORE writing code
- ✅ Use web-safe fonts only: Arial, Helvetica, Verdana, Tahoma
- ✅ Create visual hierarchy through size, weight, color
- ✅ Ensure readability: strong contrast, appropriate sizing
- ✅ Be consistent: patterns, spacing, visual language

### Step 2: Create HTML Slides

For each proposal section, create an HTML slide:

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      margin: 0;
      padding: 0;
      width: 720px;
      height: 405px;
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #00AEEF 0%, #0080B0 100%);
      color: #FFFFFF;
    }
    .slide-content {
      padding: 40px;
    }
    h1 {
      font-size: 36px;
      margin-bottom: 20px;
    }
    ul {
      font-size: 18px;
      line-height: 1.6;
    }
  </style>
</head>
<body>
  <div class="slide-content">
    <h1>Project Requirement Statement</h1>
    <ul>
      <li>Project: AI-Powered Video Analytics for Workplace Safety</li>
      <li>Project Owner: Client Name</li>
      <li>Project Duration: 6 months</li>
      <li>Camera Number: 9 cameras</li>
    </ul>
  </div>
</body>
</html>
```

### Step 3: Convert HTML to PowerPoint

Use the html2pptx workflow from pptx skill:

```javascript
// From pptx skill - html2pptx.js
const pptxgen = require('pptxgenjs');
const html2pptx = require('./html2pptx.js');

// Create presentation
let pres = new pptxgen();

// Add slide from HTML
pres.addSlide();
pres.importContent(htmlSlideContent);

// Save
pres.writeFile({ fileName: 'proposal.pptx' });
```

### Step 4: Add Architecture Diagram

Convert Mermaid diagram to image, then add to slide:

```bash
# Using mermaid-cli
mmdc -i architecture_diagram.md -o architecture_diagram.png
```

```javascript
// Add to PowerPoint
let slide = pres.addSlide();
slide.addImage({ path: 'architecture_diagram.png', x: 0, y: 0, w: 10, h: 5.6 });
```

## Slide Structure Mapping

Map template sections to slide types (from `~/.claude/skills/template2slide/SLIDE_TEMPLATE.md`):

| Template Section | Slide Type | Layout |
|-----------------|------------|--------|
| 1. Cover Page | Title slide | Centered title + date |
| 2. Project Requirements | Content slide | Bullet points |
| 3. Scope of Work | Two-column | viAct / Client responsibilities |
| 4. System Architecture | Diagram slide | Architecture diagram |
| 5. System Requirements | Content slides | Bullet points, may span multiple slides |
| 6. Implementation Plan | Timeline slide | Visual timeline |
| 7. Proposed Modules | Module slides | One slide per module |
| 8. User Interface | Content slides | Custom features only |

## Color Palette

For viAct proposals, use this palette:

```css
/* Primary Colors */
--viact-blue: #00AEEF;
--dark-navy: #1C2833;
--light-gray: #AAB7B8;
--white: #FFFFFF;

/* Usage */
background: linear-gradient(135deg, var(--viact-blue) 0%, #0080B0 100%);
color: var(--white);
```

## Typography

**Web-safe fonts only** (required by pptx skill):
- Headings: Arial, Helvetica (bold, 32-40px)
- Body: Arial, Helvetica (regular, 16-20px)
- Captions: Verdana (12-14px)

**Font sizes**:
- Slide title: 36-40px
- Section headings: 28-32px
- Body text: 18-20px
- Fine print: 12-14px

## Example Slide Code

### Cover Page Slide

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      margin: 0;
      padding: 0;
      width: 720px;
      height: 405px;
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #00AEEF 0%, #0080B0 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #FFFFFF;
    }
    .cover {
      text-align: center;
    }
    h1 {
      font-size: 40px;
      margin-bottom: 20px;
      font-weight: bold;
    }
    h2 {
      font-size: 28px;
      margin-bottom: 40px;
      font-weight: normal;
    }
    .date {
      font-size: 18px;
      margin-top: 60px;
    }
  </style>
</head>
<body>
  <div class="cover">
    <h1>Video Analytics Solution Proposal</h1>
    <h2>for Client Name</h2>
    <div class="date">January 2025</div>
  </div>
</body>
</html>
```

### Content Slide (Project Requirements)

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      margin: 0;
      padding: 0;
      width: 720px;
      height: 405px;
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #00AEEF 0%, #0080B0 100%);
      color: #FFFFFF;
    }
    .slide-content {
      padding: 40px;
    }
    h2 {
      font-size: 36px;
      margin-bottom: 30px;
      border-bottom: 2px solid #FFFFFF;
      padding-bottom: 10px;
    }
    .info-item {
      font-size: 20px;
      margin-bottom: 15px;
      line-height: 1.5;
    }
    .label {
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="slide-content">
    <h2>Project Requirement Statement</h2>
    <div class="info-item">
      <span class="label">Project:</span> AI-Powered Video Analytics for Workplace Safety
    </div>
    <div class="info-item">
      <span class="label">Project Owner:</span> Client Name
    </div>
    <div class="info-item">
      <span class="label">Project Duration:</span> 6 months
    </div>
    <div class="info-item">
      <span class="label">Camera Number:</span> 9 cameras
    </div>
    <div class="info-item">
      <span class="label">AI Modules:</span> 6 modules
    </div>
  </div>
</body>
</html>
```

### Two-Column Slide (Scope of Work)

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      margin: 0;
      padding: 0;
      width: 720px;
      height: 405px;
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #00AEEF 0%, #0080B0 100%);
      color: #FFFFFF;
    }
    .slide-content {
      padding: 40px;
    }
    h2 {
      font-size: 36px;
      margin-bottom: 30px;
      text-align: center;
    }
    .columns {
      display: flex;
      gap: 40px;
    }
    .column {
      flex: 1;
    }
    h3 {
      font-size: 24px;
      margin-bottom: 20px;
      border-bottom: 1px solid #FFFFFF;
      padding-bottom: 5px;
    }
    ul {
      font-size: 16px;
      line-height: 1.6;
      padding-left: 20px;
    }
  </style>
</head>
<body>
  <div class="slide-content">
    <h2>Scope of Work</h2>
    <div class="columns">
      <div class="column">
        <h3>viAct Responsibilities</h3>
        <ul>
          <li>Software license and maintenance</li>
          <li>Camera integration via RTSP</li>
          <li>AI model optimization</li>
          <li>System testing and training</li>
          <li>Technical support</li>
        </ul>
      </div>
      <div class="column">
        <h3>Client Responsibilities</h3>
        <ul>
          <li>Hardware procurement</li>
          <li>AI Inference Workstation</li>
          <li>Network infrastructure</li>
          <li>Camera installation and maintenance</li>
          <li>Power and internet connection</li>
        </ul>
      </div>
    </div>
  </div>
</body>
</html>
```

## Module Description Slides

Each AI module gets its own slide:

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      margin: 0;
      padding: 0;
      width: 720px;
      height: 405px;
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #00AEEF 0%, #0080B0 100%);
      color: #FFFFFF;
    }
    .slide-content {
      padding: 30px;
    }
    .module-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }
    h2 {
      font-size: 32px;
      margin: 0;
    }
    .module-type {
      font-size: 16px;
      background: rgba(255,255,255,0.2);
      padding: 5px 15px;
      border-radius: 15px;
    }
    .info-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 15px;
      font-size: 18px;
    }
    .info-item {
      margin-bottom: 10px;
    }
    .label {
      font-weight: bold;
      color: #E8F4F8;
    }
  </style>
</head>
<body>
  <div class="slide-content">
    <div class="module-header">
      <h2>Module 1: Helmet Detection</h2>
      <span class="module-type">Standard</span>
    </div>
    <div class="info-grid">
      <div class="info-item">
        <span class="label">Purpose:</span> Detect whether workers are wearing safety helmets
      </div>
      <div class="info-item">
        <span class="label">Alert Trigger Logic:</span> Alert when worker detected without helmet for >5 seconds
      </div>
      <div class="info-item">
        <span class="label">Preconditions:</span> Camera positioned to capture worker head area
      </div>
      <div class="info-item">
        <span class="label">Detection Criteria:</span> Helmet present on worker's head
      </div>
    </div>
  </div>
</body>
</html>
```

## Quality Checks

Before finalizing PowerPoint:

- ✅ All template sections mapped to slides
- ✅ Consistent design across all slides
- ✅ Typography follows guidelines (web-safe fonts, correct sizes)
- ✅ Color palette matches viAct branding
- ✅ Architecture diagram visible and clear
- ✅ Text readable (strong contrast, appropriate sizing)
- ✅ No overflow issues
- ✅ All images and diagrams render correctly

## Troubleshooting

### "Slides look different than HTML"
- Check pptxgenjs positioning
- Verify CSS is supported by html2pptx
- Test with simple HTML first

### "Text overflow on slide"
- Reduce font size
- Split content across multiple slides
- Reduce padding/margins

### "Colors don't match viAct brand"
- Ensure using viAct blue (#00AEEF)
- Check gradient directions
- Verify contrast ratios

### "Architecture diagram not visible"
- Convert Mermaid to PNG first
- Check image path in code
- Verify image dimensions fit slide

## Integration with quotation_skill

In State 3 (Output Generation), use this workflow:

1. **Validate template** - Ensure no placeholders
2. **Create HTML slides** - One HTML file per slide section
3. **Convert to PowerPoint** - Use pptx skill's html2pptx workflow
4. **Add diagrams** - Convert Mermaid, add to slides
5. **Review and save** - Quality checks, output proposal.pptx

See: `~/.claude/skills/pptx/SKILL.md` for complete pptx skill documentation.
