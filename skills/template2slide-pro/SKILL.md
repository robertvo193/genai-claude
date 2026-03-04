---
name: template2slide-pro
description: High-level orchestration skill for converting proposal templates to presentations (PowerPoint + PDF). Processes multiple template files through two-phase pipeline with Slide Agent (generates HTML/PPTX/PDF) and Reviewer Agent (validates outputs). Use when converting verified proposal templates (placeholder-free) from dealtransfer2template to final deliverables, or when users request "generate slides from templates", "create proposal presentations", or "convert templates to PowerPoint/PDF".
---

# Template2Slide Pro - Orchestration Skill

## Overview

Template2Slide Pro is a **high-level orchestration layer** that converts verified proposal templates into final presentation formats (PowerPoint + PDF). It processes **n input templates** through a **two-phase workflow** with specialized subagents:

- **Phase 1**: Slide Agent (Subagent 0) - Generates HTML, PPTX, and PDF from templates
- **Phase 2**: Reviewer Agent (Subagent 1) - Validates outputs and provides feedback

**IMPORTANT**: This skill should be **self-contained** and **independent** of the `/template2slide` reference directory. The `/template2slide` directory is for reference only - to understand existing patterns, NOT to be directly used or referenced during execution.

## When to Use This Skill

Use this skill when:
- Converting **presales-approved proposal templates** (placeholder-free) to presentations
- Templates originate from `dealtransfer2template` after checklist updates
- Processing **multiple templates** in batch (n ≥ 1)
- User requests "generate slides from template", "create proposal presentation", or "convert template to PowerPoint"
- Final deliverables needed in both PPTX and PDF formats

**Pre-flight**: Verify templates have **no unresolved placeholders** (e.g., `[NETWORK_001]`, `[TIMELINE_001]`). If placeholders exist, route back to checklist update before proceeding.

## Quick Start

### Single Template

```bash
# Basic usage
python3 scripts/template2slide.py <template_file.md> [output_dir]

# Example
python3 scripts/template2slide.py AVA_Project_Nas_Ltd_template.md ./output
```

### Multiple Templates (Orchestration Mode)

When processing **n templates**, the orchestration layer:

1. **Phase 1 - Slide Agent** (parallel processing):
   - For each template: Generate HTML → PPTX → PDF
   - Processes all templates concurrently
   - Outputs: `[Project_Name]_proposal.{pptx,pdf,html}` per template

2. **Phase 2 - Reviewer Agent** (sequential validation):
   - For each template set: Validate all outputs
   - Generates validation report
   - Returns: APPROVED/CONDITIONAL/REJECTED per template

### Manual Two-Phase Execution

```bash
# Phase 1: Generate outputs (per template)
python3 scripts/template2slide.py template1.md output1/
python3 scripts/template2slide.py template2.md output2/
# ... (process all templates)

# Phase 2: Validate outputs
python3 scripts/validate_outputs.py template1.md output1/
python3 scripts/validate_outputs.py template2.md output2/
# ... (validate all outputs)
```

## Orchestration Flow

```
Input: n template files (template1.md, template2.md, ..., templaten.md)
    ↓
[Phase 1] Slide Agent (Subagent 0)
    ↓
    ├─→ Template 1 ──→ Parse → Architecture → Mapping → HTML → PPTX → PDF
    ├─→ Template 2 ──→ Parse → Architecture → Mapping → HTML → PPTX → PDF
    ├─→ ...
    └─→ Template n ──→ Parse → Architecture → Mapping → HTML → PPTX → PDF
    ↓
Outputs: {HTML, PPTX, PDF} × n templates
    ↓
[Phase 2] Reviewer Agent (Subagent 1)
    ↓
    ├─→ Template 1 Outputs ──→ Extract → Compare → Validate → Report
    ├─→ Template 2 Outputs ──→ Extract → Compare → Validate → Report
    ├─→ ...
    └─→ Template n Outputs ──→ Extract → Compare → Validate → Report
    ↓
Output: Validation Report × n templates (APPROVED/CONDITIONAL/REJECTED)
```

## Phase 1: Slide Agent (Subagent 0)

**Purpose**: Generate HTML, PPTX, and PDF from proposal template markdown files.

For detailed instructions, see: **[subagent0_slide_agent.md](references/subagent0_slide_agent.md)**

### Actions

1. **Parse Template Markdown**
   - Extract project metadata and all sections
   - Validate template structure
   - Check for unresolved placeholders (reject if found)

2. **Generate Architecture Diagram (Mermaid)**
   - Determine deployment method
   - Generate Mermaid diagram code
   - Output: `[Project_Name]_architecture_diagram.md`

3. **Render Architecture Diagram to PNG**
   - Use mermaid-cli: `mmdc -i [Project_Name]_architecture_diagram.md -o assets/architecture_diagram.png -t dark -b transparent`
   - Verify PNG output is generated correctly
   - Output: `assets/architecture_diagram.png`

4. **Map Content to Slide Structure**
   - Parse all template sections
   - Map to slide types (title, content_bullets, two_column, module_description, diagram, timeline)
   - Extract ALL module information (type, purpose, alert_logic, preconditions, detection_criteria)
   - For module slides: Use "Module X: [Name]" title format, two-column layout (text left, media right)
   - Output: `[Project_Name]_slide_structure.json`

5. **Generate HTML Slides**
   - Use `scripts/generate_from_json.js`
   - Apply rendering standards (dark theme, overflow handling, typography)
   - **CRITICAL**: Embed architecture diagram in slide_4.html using `<img src="../assets/architecture_diagram.png" />`
   - **CRITICAL**: Use two-column layout for module slides (text left, media right)
   - Output: HTML files (one per slide)

6. **Convert HTML → PPTX**
   - Use `scripts/html2pptx.js` or PPTX skill
   - Verify architecture diagram appears in PPTX (not placeholder)
   - Download and embed images from Google Drive URLs
   - Handle media priority: video_url → image_url → blank
   - Output: `[Project_Name]_proposal.pptx`

7. **Insert Available Slides**
   - Use `scripts/insert_available_slides.py`
   - Combines generated slides with AvailableSlide11.pptx reference slides
   - **Insertion Pattern**:
     - Position 1: Generated Slide 1 (Title Slide)
     - Positions 2-10: Available Slides 2-10 (9 slides)
     - Positions 11+: Remaining Generated Slides (2 onwards)
     - Last positions: Available Slides 11-25 (15 slides)
   - All slides use background.png (same as generated slides)
   - Output: `[Project_Name]_proposal_complete.pptx`

8. **Convert PPTX → PDF**
   - Use PDF skill or LibreOffice
   - Convert the complete presentation (with Available slides)
   - Preserve formatting and layout
   - Verify all images and diagrams are visible
   - Output: `[Project_Name]_proposal_complete.pdf`

### Output Files (Per Template)

- `[Project_Name]_architecture_diagram.md` - Mermaid diagram source
- `assets/architecture_diagram.png` - Rendered architecture diagram (PNG)
- `[Project_Name]_slide_structure.json` - Slide structure
- `html/slide_*.html` - Individual HTML slides (one per slide)
- `[Project_Name]_proposal.pptx` - PowerPoint presentation (generated only)
- `[Project_Name]_proposal_complete.pptx` - Complete PowerPoint with Available slides
- `[Project_Name]_proposal_complete.pdf` - Complete PDF with Available slides

## Phase 2: Reviewer Agent (Subagent 1)

**Purpose**: Validate generated outputs and provide feedback.

For detailed instructions, see: **[subagent1_reviewer_agent.md](references/subagent1_reviewer_agent.md)**

### Actions

1. **Extract Content from Template**
   - Parse original template
   - Extract all sections, modules, metadata

2. **Extract Content from Generated Outputs**
   - Parse architecture_diagram.md, slide_structure.json
   - Extract content from HTML, PPTX, PDF

3. **Compare and Validate**

   **Content Completeness**:
   - All sections from template appear in outputs
   - All modules have corresponding slides
   - No content missing or skipped

   **Field Extraction Accuracy**:
   - Module fields (type, purpose, alert_logic, preconditions) match template exactly
   - NO default/placeholder values in output fields

   **Module Information Completeness**:
   - All required fields present for each module
   - No empty fields (except image_url/video_url)

   **Architecture Diagram Validation**:
   - Deployment method matches template
   - All components and flows correct
   - Minimal, professional layout

   **HTML Validation**:
   - No text overflow
   - Proper typography and styling
   - Media elements embedded correctly

   **PPTX Validation**:
   - File opens correctly
   - All slides present and numbered
   - Images and diagrams visible
   - Consistent formatting

   **PDF Validation**:
   - File opens correctly
   - All pages present
   - Content matches PPTX

   **Design Compliance**:
   - Professional viAct branding
   - Consistent color scheme
   - Proper margins and spacing
   - Readable font sizes

### Output: Validation Report

**Per Template**:
- Summary (pass/fail status)
- Detailed validation results (8 categories)
- Issues found (if any), with severity and recommendations
- Final verdict: ✅ APPROVED / ⚠️ CONDITIONAL / ❌ REJECTED

## Output Structure

For **n input templates**, the skill generates:

```
output/
├── template1/
│   ├── template1_architecture_diagram.md
│   ├── template1_slide_structure.json
│   ├── html/
│   │   ├── slide_1.html
│   │   ├── slide_2.html
│   │   └── ...
│   ├── template1_proposal.pptx
│   ├── template1_proposal.pdf
│   └── validation_report.json
├── template2/
│   ├── ...
│   └── validation_report.json
└── summary_report.json  # Overall summary for all templates
```

## Important Rules

### Template Validation

- Ensure templates are **presales-approved** before processing
- **Reject** if any placeholder tokens remain (e.g., `[NETWORK_001]`, `[TIMELINE_001]`)
- All required sections must be present

### Information Extraction

- **NEVER use default/placeholder values** for module information
- All fields must be extracted from template (purpose, alert_logic, preconditions, detection_criteria)
- Only image_url and video_url can be empty

### Architecture Generation

- Use `deployment_method_selection_logic.md` when deployment method is not explicit
- Match KB architecture examples (minimal, beautiful style)
- Show essential flow only: Camera → Processing → Dashboard & Alert

### Content Mapping

- Map ALL sections from template to slides
- Don't skip any dynamic content
- Use appropriate slide type for each content type

### Quality Assurance

- Apply all rendering standards from `slide_rendering_instructions.md`
- Verify no text overflow in slides
- Ensure all images and diagrams are visible
- Validate all files open correctly

## Progressive Disclosure

This skill uses progressive disclosure to minimize context usage:

- **SKILL.md** (this file): High-level orchestration workflow
- **references/subagent0_slide_agent.md**: Detailed Slide Agent instructions
- **references/subagent1_reviewer_agent.md**: Detailed Reviewer Agent instructions
- **references/SLIDE_TEMPLATE.md**: Slide structure and mapping rules
- **references/slide_rendering_instructions.md**: Slide rendering standards
- **references/deployment_method_selection_logic.md**: Architecture deployment logic
- **references/ARCHITECTURE_TEMPLATES.md**: Architecture patterns

Load reference files only when needed for specific phases.

## Scripts Available

- **generate_diagram.py**: Architecture diagram generation (Mermaid)
- **html2pptx.js**: HTML to PowerPoint conversion
- **insert_available_slides.py**: Insert Available slides into generated presentations
- **convert_*.js**: Conversion scripts for specific projects
- **setup.sh**: Auto-install script for dependencies

## Assets Available

- **background.png**: viAct slide background image (1.3 MB)
  - Used in all HTML slides for consistent branding
  - Dark theme with viAct colors

- **AvailableSlide11.pptx**: Reference slide template (47 MB)
  - Contains 25 standard/reference slides for viAct proposals
  - **Insertion Pattern**: Automatically inserted into generated presentations
  - Slides 2-10 inserted after generated title slide
  - Slides 11-25 inserted after all generated content slides
  - All slides use background.png (consistent with generated slides)

## Dependencies

### Required

- Python 3.8+
- Node.js 20+
- **python-pptx** (for slide insertion): `pip install python-pptx`

**Node.js Dependencies Setup (IMPORTANT)**:
The skill requires specific Node.js packages for HTML → PPTX conversion and diagram rendering.

**Setup Instructions**:

```bash
# Navigate to skill scripts directory
cd ~/.claude/skills/template2slide-pro/scripts

# Install all dependencies (including mermaid-cli)
npm install

# Install Playwright Chromium browser
npx playwright install chromium

# Verify installation
npx playwright --version
npx mmdc --version
```

**Critical Notes**:
- **DO NOT** reference `/template2slide/scripts` from within this skill
- This skill (`template2slide-pro`) is self-contained with its own `node_modules`
- All dependencies are installed locally in `scripts/node_modules` (110 MB total)
- **mermaid-cli is now packaged locally** (not global installation required)
- Use `npx mmdc` to run mermaid-cli from local node_modules
- **node_modules directory is included** in the skill for portability

**Required Packages** (all in package.json):
- pptxgenjs@^4.0.1 - PowerPoint generation
- playwright@^1.48.2 - Browser automation for HTML rendering
- sharp@^0.34.5 - Image processing
- @mermaid-js/mermaid-cli@^10.6.1 - Architecture diagram rendering (LOCAL)
- Chromium browser (install via `npx playwright install chromium`)

**Usage**:
```bash
# Render Mermaid diagram (uses local mermaid-cli)
npx mmdc -i diagram.md -o diagram.png -t dark -b transparent

# With puppeteer config for sandbox issues
npx mmdc -i diagram.md -o diagram.png -t dark -b transparent -p puppeteer-config.json
```

### Dependency Checker

**IMPORTANT**: The skill includes an automatic dependency checker that runs before any conversion. It ensures all required Node.js packages and Playwright browsers are properly installed.

**Check Dependencies**:
```bash
# Run dependency check
cd ~/.claude/skills/template2slide-pro/scripts
node check_dependencies.js

# Auto-fix any issues
node check_dependencies.js --fix
```

**What the Checker Does**:
- ✅ Verifies Node.js version (18+ or 20+ recommended)
- ✅ Checks `node_modules` directory exists in skill scripts folder
- ✅ Validates all required packages: pptxgenjs, playwright, sharp, mermaid-cli
- ✅ Verifies Playwright Chromium browser is installed
- ✅ Checks critical files like `playwright-core/lib/inprocess.js`
- ✅ Provides clear error messages with fix commands

**Automatic Checking**:
The `html2pptx.js` module automatically checks dependencies on load. If dependencies are missing, it will throw an error with instructions to fix:

```
Error: Playwright installation incomplete!
Run: cd /path/to/skill/scripts && npm install
Or run: node check_dependencies.js --fix
```

**Priority**: Always use dependencies from `~/.claude/skills/template2slide-pro/scripts/node_modules`, NOT from project directories or global npm installations.

## Quality Checklist

Before final delivery, verify for each template:

- ✅ All placeholders resolved
- ✅ Architecture diagram generated (Mermaid .md) and rendered to PNG
- ✅ Architecture diagram embedded in slide_4.html (not placeholder)
- ✅ Architecture diagram visible in PPTX and PDF outputs
- ✅ All template sections mapped to slides
- ✅ All module information extracted (no empty fields except image_url/video_url)
- ✅ Module slides use "Module X: [Name]" title format
- ✅ Module slides use two-column layout (text left, media right)
- ✅ Slide numbering is continuous
- ✅ HTML slides render correctly with no overflow
- ✅ All text in proper HTML tags (`<p>`, `<ul>`, `<ol>`, not `<div>`)
- ✅ PPTX file opens and displays properly
- ✅ PDF file opens and displays properly
- ✅ All images and diagrams visible and correctly positioned
- ✅ Validation report shows APPROVED

## HTML Structure Requirements for PPTX Conversion

**CRITICAL**: The `html2pptx.js` converter enforces strict HTML validation. Failing to follow these rules will cause conversion errors.

### Text Wrapping Rules

**Why text must be in `<p>` tags, not `<div>`**:
- The html2pptx converter treats `<div>` as **layout containers** (for backgrounds, borders, positioning)
- The converter treats `<p>`, `<h1>-<h6>`, `<ul>`, `<ol>` as **text elements** (content that appears in PowerPoint)
- Text directly inside `<div>` elements will NOT appear in the generated PowerPoint

**Correct Structure**:
```html
<div class="content">  <!-- Layout container -->
  <p class="section">  <!-- Text element - WILL appear in PPTX -->
    <span class="label">Purpose:</span> Text content here
  </p>
  <ul style="list-style-type: none; padding: 0; margin: 0;">
    <li>List item 1</li>
    <li>List item 2</li>
  </ul>
</div>
```

**Incorrect Structure**:
```html
<div class="content">
  <div class="section">  <!-- WRONG - Text won't appear in PPTX -->
    Purpose: Text content here
  </div>
</div>
```

### HTML Validation Rules

The `html2pptx.js` converter enforces these validation rules:

1. **All text must be wrapped**: Text content MUST be in `<p>`, `<h1>-<h6>`, `<ul>`, or `<ol>` tags
2. **No manual bullets**: Do NOT use bullet symbols (•, -, *) in text. Use `<ul>` or `<ol>` lists instead
3. **Divs for layout only**: `<div>` elements with backgrounds, borders, or shadows must NOT contain text directly
4. **Proper nesting**: Text elements must be inside layout containers, not vice versa

**Example Timeline Slide Fix**:
```html
<!-- BEFORE (ERROR - unwrapped text in divs) -->
<div class="phase">
  <div class="phase-title">Phase T0: Project Award</div>
  <div class="phase-date">Project Start</div>
  <div class="phase-activities">• Contract finalization<br/>• Project kickoff</div>
</div>

<!-- AFTER (CORRECT - text in p tags) -->
<div class="phase">
  <p class="phase-title">Phase T0: Project Award</p>
  <p class="phase-date">Project Start</p>
  <ul class="phase-activities" style="list-style-type: none; padding: 0; margin: 0;">
    <li>Contract finalization</li>
    <li>Project kickoff meeting</li>
  </ul>
</div>
```

### Common Conversion Errors

**Error 1**: "DIV element contains unwrapped text"
- **Cause**: Text directly inside `<div>` without `<p>` wrapper
- **Fix**: Wrap text in `<p>`, `<h1>-<h6>`, `<ul>`, or `<ol>` tags

**Error 2**: "Text element starts with bullet symbol"
- **Cause**: Using manual bullets (•, -, *) in `<p>` tags
- **Fix**: Use `<ul>` or `<ol>` lists instead (can hide bullets with `list-style-type: none`)

**Error 3**: "Text element has background"
- **Cause**: `<p>` tag with `background` or `border` styles
- **Fix**: Use `<div>` for styled containers, put text inside `<p>` within the div

### Overflow Handling

When content overflows slide boundaries:
1. **Reduce font sizes**: Decrease by 1-2pt increments
2. **Adjust margins**: Reduce top/bottom margins to fit content
3. **Reduce padding**: Shrink container padding
4. **Consolidate content**: Merge related points where appropriate

**Example Fix** (from slide_4.html - System Architecture):
```css
/* BEFORE - Overflow by 18pt */
.title {
  margin: 30pt 120pt 20pt 40pt;
}
.content {
  padding: 20pt 40pt 80pt 40pt;
}

/* AFTER - No overflow */
.title {
  margin: 20pt 120pt 10pt 40pt;  /* Reduced margins */
}
.content {
  padding: 10pt 40pt 100pt 40pt;  /* Increased bottom padding */
}
```

## Module Slide Layout

**CRITICAL**: Module slides (AI module descriptions) **MUST** use a specific two-column layout with text on the left and media on the right.

**Required Structure**:

### Title Format
- **Use**: "Module X: [Module Name]"
- Example: "Module 1: Safety Helmet Detection"
- Place at top of slide as H1 title

### Layout: Two-Column Split

```
┌─────────────────────────────────────────────────┐
│  Module 1: Safety Helmet Detection              │
├──────────────────────┬──────────────────────────┤
│                      │                          │
│  Text Content        │    Media                 │
│  (Left Column)       │    (Right Column)        │
│                      │                          │
│  • Purpose           │    [Video or Image]      │
│  • Alert Logic       │                          │
│  • Preconditions     │    • Embed video_url     │
│  • Detection         │      (iframe/video tag)  │
│    Criteria          │    • OR embed image_url  │
│                      │      (img tag)           │
│                      │    • 16:9 aspect ratio   │
│                      │                          │
└──────────────────────┴──────────────────────────┘
```

### HTML Implementation

```html
<!DOCTYPE html>
<html>
<head>
<style>
html { background: #000000; }
body {
  width: 720pt;
  height: 405pt;
  margin: 0;
  padding: 0;
  background-image: url('../../template2slide-pro/scripts/background.png');
  background-size: cover;
  font-family: Arial, Helvetica, sans-serif;
  display: flex;
  flex-direction: column;
}
.title {
  color: #00AEEF;
  font-size: 24pt;
  font-weight: bold;
  margin: 20pt 40pt 15pt 40pt;
}
.content {
  flex: 1;
  display: flex;
  gap: 30pt;
  margin: 0 40pt 40pt 40pt;
}
.text-column {
  flex: 1;
  font-size: 10pt;
  line-height: 1.6;
  color: #FFFFFF;
}
.media-column {
  flex: 1.2;
  display: flex;
  align-items: center;
  justify-content: center;
}
.video-wrapper {
  width: 100%;
  aspect-ratio: 16 / 9;
  background: #000;
  border: 2px solid #00AEEF;
}
.section {
  margin-bottom: 15pt;
}
.section-label {
  color: #00AEEF;
  font-weight: bold;
  margin-bottom: 3pt;
}
.section-text {
  color: #FFFFFF;
  line-height: 1.5;
}
ul {
  list-style-type: none;
  padding-left: 0;
  margin: 5pt 0 0 0;
}
li {
  margin-bottom: 5pt;
  padding-left: 15pt;
  position: relative;
}
li:before {
  content: "•";
  color: #00AEEF;
  position: absolute;
  left: 0;
  font-weight: bold;
}
</style>
</head>
<body>
<h1 class="title">Module 1: Safety Helmet Detection</h1>
<div class="content">
  <div class="text-column">
    <div class="section">
      <p class="section-label">Purpose:</p>
      <p class="section-text">Detect whether workers are wearing safety helmets in designated areas.</p>
    </div>
    <div class="section">
      <p class="section-label">Alert Logic:</p>
      <p class="section-text">Alert triggered when:</p>
      <ul>
        <li>Person detected without helmet in monitored area</li>
        <li>Confidence score > 85%</li>
      </ul>
    </div>
    <div class="section">
      <p class="section-label">Preconditions:</p>
      <p class="section-text">Camera installed, area marked as helmet-required zone.</p>
    </div>
    <div class="section">
      <p class="section-label">Detection Criteria:</p>
      <p class="section-text">Real-time detection with 95% accuracy target.</p>
    </div>
  </div>
  <div class="media-column">
    <div class="video-wrapper">
      <iframe src="[video_url]" frameborder="0" allowfullscreen
              style="width: 100%; height: 100%;"></iframe>
    </div>
  </div>
</div>
</body>
</html>
```

### Media Embedding Rules

**Priority Order**:
1. **video_url** (highest priority) - Embed as iframe or video tag
2. **image_url** - Embed as img tag
3. **Placeholder** - If neither URL available, show "[Video/Image Placeholder]"

**Video URL Auto-Detection**:
The renderer automatically detects and converts video URLs to embed format:
- **Google Drive**: `https://drive.google.com/file/d/FILE_ID/view` → `https://drive.google.com/file/d/FILE_ID/preview`
- **YouTube**: `https://youtube.com/watch?v=VIDEO_ID` → `https://www.youtube.com/embed/VIDEO_ID`
- **Direct URLs**: Used as-is for iframe embedding

**Video Embedding** (Google Drive/YouTube):
```html
<div class="video-wrapper">
  <iframe src="https://drive.google.com/file/d/VIDEO_ID/preview"
          frameborder="0" allowfullscreen
          style="width: 100%; height: 100%;"></iframe>
</div>
```

**Image Embedding**:
```html
<div class="media-column">
  <img src="[image_url]" alt="Module demo"
       style="max-width: 100%; max-height: 100%; object-fit: contain;" />
</div>
```

### Module Numbering

- Number modules sequentially: Module 1, Module 2, Module 3, etc.
- Use module order from template (preserve original order)
- Update numbering if modules are added/removed

### Common Mistakes to Avoid

❌ **WRONG**: Media on left, text on right
❌ **WRONG**: Stacked layout (media above/below text)
❌ **WRONG**: Missing "Module X:" prefix in title
❌ **WRONG**: Using `<div>` for text content instead of `<p>` tags
✅ **CORRECT**: Text left (60%), Media right (40%)
✅ **CORRECT**: "Module 1: Safety Helmet Detection" as title
✅ **CORRECT**: All text in `<p>`, `<ul>`, `<ol>` tags

## Architecture Diagram Embedding

**CRITICAL**: Architecture diagrams **MUST** be embedded in the System Architecture slide (slide_4.html), not shown as placeholders.

**Required Workflow**:
1. Generate Mermaid diagram code from template (see Phase 1, Step 2)
2. **Render Mermaid to PNG** using mermaid-cli
3. **Embed PNG image** in the diagram slide HTML
4. Verify image appears in PPTX and PDF outputs

**Implementation**:

```bash
# Step 1: Render Mermaid diagram to PNG (using local mermaid-cli)
cd output/[Project_Name]/
npx mmdc -i [Project_Name]_architecture_diagram.md -o assets/architecture_diagram.png -t dark -b transparent

# OR with puppeteer config (for sandbox issues):
npx mmdc -i [Project_Name]_architecture_diagram.md -o assets/architecture_diagram.png -t dark -b transparent -p puppeteer-config.json

# Step 2: Update slide_4.html to embed the diagram
# Replace placeholder div with:
<img src="../assets/architecture_diagram.png" style="width: 100%; max-width: 600pt; height: auto;" />

# Step 3: Verify diagram appears in PPTX conversion
node scripts/convert.js  # Diagram should be visible in slide_4
```

**Mermaid Rendering Options**:
- **Theme**: `-t dark` for dark background (matches viAct slides)
- **Background**: `-b transparent` or `-b #1a1a1a` for dark theme
- **Output**: PNG format for PPTX/PDF compatibility
- **Scale**: Use default scale (1.0) or `-s 2` for higher resolution
- **Command**: Use `npx mmdc` (local installation, not global)

**Puppeteer Config** (for sandbox issues):
Create `puppeteer-config.json`:
```json
{
  "args": ["--no-sandbox", "--disable-setuid-sandbox"]
}
```

**Troubleshooting mermaid-cli**:
- **Error: "No usable sandbox"**: Use puppeteer config: `-p puppeteer-config.json`
- **Error: "Cannot find module"**: Reinstall from skill dir: `cd ~/.claude/skills/template2slide-pro/scripts && npm install`
- **Diagram not rendering**: Check Mermaid syntax in .md file, verify all nodes and edges properly formatted

## Available Slides Insertion

**Purpose**: Automatically insert reference slides from `AvailableSlide11.pptx` into generated presentations.

**What Are Available Slides?**
- 25 standard/reference slides provided by viAct
- Contain company information, terms, conditions, and standard content
- Used across all proposals for consistency
- File: `scripts/AvailableSlide11.pptx` (47 MB)

**Insertion Pattern**:
```
Generated Presentation (12 slides) + Available Slides (25 slides) = Complete Presentation (37 slides)

Structure:
  Slide 1:           Generated Title Slide
  Slides 2-10:       Available Slides 2-10 (9 slides)
  Slides 11-22:      Generated Content Slides (12 slides)
  Slides 23-37:      Available Slides 11-25 (15 slides)

Total: 37 slides
```

**Usage**:

```bash
# Step 1: Install python-pptx (first time only)
pip install python-pptx

# Step 2: Run insertion script
cd ~/.claude/skills/template2slide-pro/scripts
python insert_available_slides.py <generated.pptx> AvailableSlide11.pptx <output.pptx>

# Example:
python insert_available_slides.py \
  ../../output_bromma/presentation.pptx \
  AvailableSlide11.pptx \
  ../../output_bromma/presentation_complete.pptx
```

**Output**:
- `presentation_complete.pptx`: Complete presentation with Available slides inserted
- All slides maintain background.png (consistent theming)
- Generated slides keep their content, videos, and diagrams
- Available slides inserted at correct positions

**Verification**:
```bash
# Count slides in output (should be 37 for 12 generated slides + 25 available slides)
python -c "from pptx import Presentation; p = Presentation('output_bromma/presentation_complete.pptx'); print(f'Total slides: {len(p.slides)}')"
```

**Integration into Workflow**:
After generating presentation.pptx, automatically run insertion:
```bash
# Generate slides from template
node convert_bromma.js

# Insert Available slides
python insert_available_slides.py \
  ../../output_bromma/presentation.pptx \
  AvailableSlide11.pptx \
  ../../output_bromma/presentation_complete.pptx

# Convert to PDF
soffice --headless --convert-to pdf \
  ../../output_bromma/presentation_complete.pptx \
  --outdir ../../output_bromma/
```

**Troubleshooting**:
- **ModuleNotFoundError: No module named 'pptx'**: Install python-pptx: `pip install python-pptx`
- **FileNotFoundError**: Check paths to generated.pptx and AvailableSlide11.pptx
- **Slide count incorrect**: Verify AvailableSlide11.pptx has 25 slides
- **Background missing**: Ensure background.png is in scripts directory

## Troubleshooting

### Dependency Issues

**FIRST STEP**: Always run the dependency checker for any module-related errors:

```bash
cd ~/.claude/skills/template2slide-pro/scripts
node check_dependencies.js --fix
```

This will automatically detect and fix:
- Missing node_modules directory
- Incomplete package installations
- Missing Playwright browser
- Broken symlinks or corrupted files

**Error: "Cannot find module 'pptxgenjs'" or similar**:
- **Cause**: Node.js packages not installed in skill directory
- **Auto-fix**: Run `node check_dependencies.js --fix`
- **Manual fix**:
  1. Install packages locally: `cd scripts && npm install`
  2. Do NOT reference `/template2slide/scripts/node_modules`
  3. Use `~/.claude/skills/template2slide-pro/scripts/node_modules` only

**Error: "Executable doesn't exist at .../chromium"**:
- **Cause**: Playwright browser not installed
- **Auto-fix**: Run `node check_dependencies.js --fix`
- **Manual fix**: `cd scripts && npx playwright install chromium`

**Error: "Cannot find module './lib/inprocess'"**:
- **Cause**: Playwright package corrupted or incomplete installation
- **Auto-fix**: Run `node check_dependencies.js --fix`
- **Manual fix**: Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`

**Error: "Playwright installation incomplete!"** (automatic check):
- **Cause**: html2pptx.js detected missing dependencies on load
- **Auto-fix**: Run `node check_dependencies.js --fix`
- **Prevention**: The checker runs automatically, preventing runtime errors

### Phase 1 Failures

**Placeholders Found**:
- Reject template and request presales verification

**Module Information Missing**:
- Check template format
- Verify extraction logic in `scripts/map_to_slides.py`

**Architecture Not Generated**:
- Review `deployment_method_selection_logic.md`
- Verify template has System Architecture section

**HTML Overflow**:
- Apply overflow handling from `slide_rendering_instructions.md`
- Check content aggregation logic

**Media Download Failed**:
- Verify Google Drive URL format
- Check Playwright handling
- Fallback to alternative URL

### Phase 2 Failures

**Validation Fails - No Issues Found**:
- Check validation logic thresholds
- Adjust criteria if too strict

**Cannot Extract Content from PPTX/PDF**:
- Verify file format
- Try alternative parsing library

**Module Fields Show as Empty**:
- Check slide_structure.json extraction in Slide Agent

**Architecture Diagram Validation Fails**:
- Verify Mermaid syntax
- Check rendering service availability

## Example Usage

### Single Template (Quick)

```bash
python3 scripts/template2slide.py AVA_Project_Nas_Ltd_template.md ./output
```

### Multiple Templates (Batch)

```bash
# Process all templates in a directory
for template in templates/*.md; do
  python3 scripts/template2slide.py "$template" ./output/$(basename "$template" .md)
done

# Validate all outputs
for dir in output/*/; do
  python3 scripts/validate_outputs.py "$dir"
done
```

## Next Steps

After generating and validating presentations:

1. **Review Validation Reports**: Check summary_report.json and individual validation reports
2. **Address Issues**: Fix any CONDITIONAL or REJECTED items
3. **Final Review**: Manually review PPTX/PDF files for quality
4. **Delivery**: Share approved presentations with presales/client

## Available Slides Workflow

### Overview

When a proposal requires **Available slides** (reference slides from a standard deck), use the **HTML merge workflow** instead of direct PPTX manipulation. This approach converts Available slides to HTML, merges them with generated slides, then converts back to PPTX.

### When to Use

- User requests inserting AvailableSlide11.pptx (or similar) into generated presentation
- Need to insert reference slides at specific positions (e.g., after title slide, at end)
- Want to preserve layout and formatting from original Available slides

### Workflow Steps

#### Step 1: Convert Available Slides to HTML

```bash
# Extract Available slides from PPTX and convert to HTML
node scripts/pptx_to_html.js <AvailableSlide11.pptx> <output_dir>/available_html

# Example
node scripts/pptx_to_html.js template2slide-pro/scripts/AvailableSlide11.pptx output_bromma_v2/available_html
```

**Output**:
- `available_slide_1.html` through `available_slide_N.html`
- `media/` folder with all extracted images
- `background.png` (if present in original)

#### Step 2: Merge Generated and Available HTML

```bash
# Merge generated slides with Available slides
# Insertion pattern: Generated #1, Available #2-10, Generated #2+, Available #11-25
node scripts/merge_html_slides.js <generated_html_dir> <available_html_dir> <merged_html_dir>

# Example
node scripts/merge_html_slides.js output_bromma_v2/html output_bromma_v2/available_html output_bromma_v2/html_merged
```

**Output Structure** (for 12 generated + 25 available slides):
- Slide 1: Generated slide 1 (title)
- Slides 2-10: Available slides 2-10 (9 slides)
- Slides 11-22: Generated slides 2-12 (12 slides)
- Slides 23-36: Available slides 11-25 (15 slides)
- **Total: 36 slides**

#### Step 3: Convert Merged HTML to PPTX

```bash
# Convert merged HTML slides to final PPTX
node convert_merged.js  # (or create custom conversion script)

# Example conversion script:
node -e "
const html2pptx = require('./template2slide-pro/scripts/html2pptx.js');
const PptxGenJS = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

async function convert() {
  const pres = new PptxGenJS();
  pres.layout = 'LAYOUT_16x9';
  
  const slides = fs.readdirSync('output_bromma_v2/html_merged')
    .filter(f => f.match(/^slide_\d+\.html$/))
    .sort();
  
  for (const slideFile of slides) {
    try {
      await html2pptx(\`output_bromma_v2/html_merged/\${slideFile}\`, pres);
    } catch (err) {
      console.log(\`Skipped \${slideFile}: \${err.message.split('\n')[0]}\`);
    }
  }
  
  await pres.writeFile({ fileName: 'output_bromma_v2/presentation_complete.pptx' });
  console.log('Created presentation_complete.pptx');
}
convert();
"
```

#### Step 4: Convert to PDF (Optional)

```bash
# Convert PPTX to PDF
soffice --headless --convert-to pdf output_bromma_v2/presentation_complete.pptx --outdir output_bromma_v2
```

### Scripts

1. **pptx_to_html.js** - Convert PPTX slides to HTML
   - Extracts text, images, and media from PPTX
   - Generates simple HTML with background support
   - Preserves basic layout structure

2. **merge_html_slides.js** - Merge generated and Available HTML
   - Implements standard insertion pattern
   - Handles asset path rewriting
   - Generates sequential slide numbers

3. **insert_available_slides_ooxml.py** - Direct PPTX insertion (alternative)
   - Uses OOXML unpack/pack approach
   - Handles complex slide copying
   - More reliable for maintaining formatting
   - Use when HTML conversion has issues

### Validation Notes

- **Available slides may have validation errors** (layout issues, text overflow)
- Generated slides are validated normally
- Skipped slides are logged but don't stop conversion
- Final presentation may have 25-36 slides depending on validation

### Troubleshooting

**Issue**: Background images not loading
**Fix**: Use absolute paths in HTML:
```html
<!-- Instead of -->
<img src="../background.png">

<!-- Use -->
<img src="/absolute/path/to/background.png">
```

**Issue**: Media files not found
**Fix**: Update merge script to copy media to correct location and update paths:
```javascript
content = content.replace(/src="media\//g, 'src="../available_html/media/');
```

**Issue**: Slides skipped due to validation
**Fix**: Disable validation for Available slides or adjust layout in HTML:
```javascript
// Skip validation errors
try {
  await html2pptx(slidePath, pres);
} catch (err) {
  console.log(`Skipped: ${err.message}`);
}
```


## Available Slides Insertion (Improved Method)

### Recommended Approach: python-pptx Direct Copying

**Based on pptx skill's proven rearrange.py approach**

When inserting Available slides, use **`insert_available_slides_pro.py`** which directly copies slides between presentations using python-pptx's proven slide duplication technique.

### Why This Approach?

✅ **100% slide success rate** - All 36 slides created successfully  
✅ **python-pptx compatible** - Opens and reads correctly  
✅ **Preserves formatting** - Uses deepcopy for exact copying  
✅ **Handles media** - Proven image/media relationship handling  
✅ **Clean API** - Works at python-pptx level, no OOXML complexity  

### Workflow

```bash
# Step 1: Generate slides from template (as usual)
node template2slide-pro/scripts/html2pptx_wrapper.js <template.md> output_dir

# Step 2: Insert Available slides using improved script
python3 template2slide-pro/scripts/insert_available_slides_pro.py \
  <generated.pptx> \
  <AvailableSlide11.pptx> \
  <output_complete.pptx>

# Example
python3 template2slide-pro/scripts/insert_available_slides_pro.py \
  output_bromma_v2/presentation.pptx \
  template2slide-pro/scripts/AvailableSlide11.pptx \
  output_bromma_v2/presentation_complete.pptx
```

### Output Structure

For 12 generated + 25 available slides:
- Slide 1: Generated slide 1 (Title)
- Slides 2-10: Available slides 2-10 (9 slides)
- Slides 11-22: Generated slides 2-12 (12 slides)
- Slides 23-36: Available slides 11-25 (15 slides)
- **Total: 36 slides**

### Comparison of Approaches

| Aspect | insert_available_slides_pro.py | OOXML Approach | HTML Workflow |
|--------|-------------------------------|----------------|---------------|
| **Success Rate** | ✅ 36/36 (100%) | 36/36 (100%) | 25/36 (69%) |
| **python-pptx** | ✅ Compatible | ✅ Compatible | ✅ Compatible |
| **Complexity** | Low | High (XML) | Medium |
| **Formatting** | ✅ Preserved | ✅ Preserved | ⚠️ May vary |
| **Dependencies** | python-pptx | xml.etree | JSZip, Node |
| **Validation** | None | None | Built-in |
| **PDF Conversion** | ⚠️ LibreOffice issues | ⚠️ LibreOffice issues | ⚠️ Partial |
| **Recommended** | ✅ YES | Alternative | Alternative |

### Known Limitations

**LibreOffice PDF Conversion**: Due to duplicate slide masters/themes from merging two presentations, LibreOffice may fail to convert to PDF. 

**Workarounds**:
1. Use Microsoft PowerPoint/Office 365 (full compatibility)
2. Use online converters (Smallpdf, CloudConvert, etc.)
3. Accept PPTX format only (python-pptx compatible)

**The PPTX file itself is valid and opens correctly** in PowerPoint and can be read by python-pptx.

### Technical Details

The script uses the proven technique from pptx skill's `rearrange.py`:

1. **Deep copy shapes**: Preserves all formatting and layout
2. **Handles relationships**: Updates image/media references correctly
3. **Uses layout**: Preserves slide layout from source
4. **Clears placeholders**: Avoids duplicate placeholder issues

```python
# Key technique from rearrange.py
for shape in source_slide.shapes:
    el = shape.element
    new_el = deepcopy(el)
    new_slide.shapes._spTree.insert_element_before(new_el, "p:extLst")
    
    # Update media relationships
    blips = new_el.xpath(".//a:blip[@r:embed]")
    for blip in blips:
        old_rId = blip.get("{...}embed")
        if old_rId in image_rels:
            new_rId = new_slide.part.rels.get_or_add(...)
            blip.set("{...}embed", new_rId)
```

### When to Use Other Approaches

**Use OOXML approach** (`insert_available_slides_ooxml.py`) when:
- Need to avoid duplicate slide masters
- LibreOffice PDF conversion is critical
- Want complete control over XML structure

**Use HTML workflow** when:
- Need to customize Available slide content
- Want to validate slides before conversion
- Prefer working with HTML/XML

### Script Location

`~/.claude/skills/template2slide-pro/scripts/insert_available_slides_pro.py`

