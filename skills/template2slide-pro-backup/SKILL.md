---
name: template2slide-pro
description: High-level orchestration skill for converting proposal templates to presentations (PowerPoint + PDF). Direct MD → HTML → PPTX/PDF pipeline with intelligent slide type selection. Leverages pptx and pdf skills for conversion. No JSON intermediate. Use when converting verified proposal templates (placeholder-free) from dealtransfer2template to final deliverables.
---

# Template2Slide Pro - Streamlined Orchestration Skill

## Overview

Template2Slide Pro is a **high-level orchestration layer** that converts verified proposal templates into final presentation formats (PowerPoint + PDF).

**Key Characteristics**:
- ✅ **Direct pipeline**: `.md → mermaid diagram → .html → .pptx → .pdf`
- ✅ **No JSON intermediate**: Agent intelligently selects slide types directly from markdown
- ✅ **Leverages existing skills**: Uses `pptx` skill and `pdf` skill for conversions
- ✅ **Regex-free parsing**: Agent reads and understands markdown structure naturally
- ✅ **Skip reference slides**: Focus on generated content only

## When to Use This Skill

Use this skill when:
- Converting **presales-approved proposal templates** (placeholder-free) to presentations
- Templates originate from `dealtransfer2template` after checklist updates
- User requests "generate slides from template", "create proposal presentation", or "convert template to PowerPoint"
- Final deliverables needed in both PPTX and PDF formats

**Pre-flight**: Verify templates have **no unresolved placeholders** (e.g., `[NETWORK_001]`, `[TIMELINE_001]`). If placeholders exist, route back to checklist update before proceeding.

## Quick Start

```bash
# Basic usage
template2slide <template_file.md> [output_dir]

# Example
template2slide AVA_Project_Nas_Ltd_template.md ./output
```

## Pipeline Architecture

```
Input: template.md (verified, placeholder-free)
    ↓
Step 1: Parse Template
    ├─ Extract project info (client, deployment, modules)
    ├─ Identify sections (Cover, Requirements, Scope, Architecture, etc.)
    ├─ Parse AI modules with metadata
    └─ Extract timeline milestones if present
    ↓
Step 2: Generate Architecture Diagram
    ├─ Create Mermaid diagram based on deployment method
    ├─ Render to PNG with transparent background
    └─ Save as architecture_diagram.md and diagram.png
    ↓
Step 3: Generate HTML Slides
    ├─ Agent reads each section
    ├─ Intelligently selects slide type:
    │   ├─ Cover Page → Title Slide
    │   ├─ Project Requirements → Content Bullets
    │   ├─ Scope of Work → Two Column Slide
    │   ├─ System Architecture → Diagram Slide (use mermaid diagram)
    │   ├─ System Requirements → Content Bullets (combine if short)
    │   ├─ Implementation Plan → Timeline Slide
    │   └─ Proposed Modules → Module Description Slides
    ├─ Generate HTML files directly (no JSON)
    └─ Apply dark theme styling
    ↓
Step 4: Convert HTML → PPTX
    ├─ Use **pptx skill** for conversion
    ├─ Embed all media (diagrams, images, videos)
    └─ Apply consistent formatting
    ↓
Step 5: Convert PPTX → PDF
    ├─ Use **pdf skill** for conversion
    └─ Preserve formatting and layout
    ↓
Output: {presentation.pptx, presentation.pdf, html/, assets/}
```

## Detailed Workflow

### Step 1: Parse Template (Agent-Guided)

**Agent Actions**:
1. Read template.md file completely
2. Extract structured information using natural reading:
   - Project name, client, deployment method
   - Number of cameras, AI modules
   - Section headers and content
   - Module definitions (name, type, purpose, alert_logic, preconditions)
   - Timeline milestones (T0, T1, T2, T3, etc.)

**No Regex Required**:
- Agent reads markdown naturally using heading structure
- Identifies sections by `##` or `###` headers
- Extracts content by reading between headers
- Parses modules from bulleted lists or tables

### Step 2: Generate Architecture Diagram

**Agent Actions**:
1. Determine deployment method from template (cloud/on-premise/hybrid)
2. Create appropriate Mermaid diagram:
   - Cloud: Cameras → Internet → Cloud Inference → Dashboard/Alert
   - On-Premise: Cameras → NVR → On-Premise Inference → Dashboard/Alert
   - Hybrid: Cameras → NVR → Cloud + On-Premise → Dashboard/Alert
3. Use **generate_architecture.py** or create Mermaid directly
4. Render Mermaid to PNG with transparent background:
   - Option 1: Use mermaid-cli (`mmdc -i diagram.mmd -o diagram.png -b transparent`)
   - Option 2: Use online service (https://mermaid.live)
5. Save both:
   - `{project}_architecture_diagram.md` (source)
   - `assets/diagram.png` (rendered)

**Architecture Templates**: Reference `ARCHITECTURE_TEMPLATES.md` for patterns.

### Step 3: Generate HTML Slides (Agent-Guided)

**Agent Actions**:

For each section in template:
1. **Read section content**
2. **Intelligently select slide type** based on:
   - Content length
   - Content structure
   - Visual requirements
   - Best presentation practices

3. **Generate appropriate HTML** using renderer templates:

**Slide Type Selection Logic**:

| Section Type | Slide Type | Renderer | When to Use |
|--------------|------------|----------|-------------|
| Cover Page | Title Slide | `title.js` | Always first slide |
| Project Requirements | Content Bullets | `content_bullets.js` | Lists of requirements |
| Scope of Work | Two Column | `two_column.js` | Responsibilities split (viAct vs Client) |
| System Architecture | Diagram | `diagram.js` | Replace with mermaid diagram |
| System Requirements | Content Bullets | `content_bullets.js` | Network + Camera requirements (can combine if short) |
| Implementation Plan | Timeline | `timeline.js` | Phases T0, T1, T2, T3... |
| Module Name | Module Description | `module_description.js` | One slide per AI module |

4. **Apply HTML standards**:
   - Dimensions: 720pt × 405pt (16:9)
   - Dark theme: `#000000` background, `#FFFFFF` text, `#00AEEF` accents
   - Background image: `../assets/background.png`
   - Font: Arial/Helvetica, readable sizes (12-28pt)
   - Margins: 40pt left, 120pt right, 180pt bottom
   - Overflow handling: Scrollable content area, max-height calculations

**HTML File Structure**:
```html
<!DOCTYPE html>
<html>
<head>
<style>
/* Dark theme, dimensions, positioning */
</style>
</head>
<body>
<!-- Slide content -->
</body>
</html>
```

### Step 4: Convert HTML → PPTX (Using pptx skill)

**Agent Actions**:
1. Invoke **pptx skill** with HTML files
2. Specify conversion options:
   - Input: `html/` directory with slide_1.html, slide_2.html, ...
   - Output: `presentation.pptx`
   - Layout: 16:9 (10in × 5.625in)
   - Background: Use `assets/background.png`
   - Fonts: Embed Arial, ensure consistency
3. Embed media files:
   - Architecture diagram: `assets/diagram.png`
   - Module videos/images: `assets/module_1.mp4`, etc.
4. Apply viAct branding:
   - Blue accent color: `#00AEEF`
   - White text on dark background
   - Consistent spacing and margins

**Conversion Command** (via pptx skill):
```bash
pptx convert-html \
  --input html/ \
  --output presentation.pptx \
  --layout 16:9 \
  --background assets/background.png \
  --embed-assets assets/
```

### Step 5: Convert PPTX → PDF (Using pdf skill)

**Agent Actions**:
1. Invoke **pdf skill** with PPTX file
2. Specify conversion options:
   - Input: `presentation.pptx`
   - Output: `presentation.pdf`
   - Quality: High (for presentations)
   - Embed fonts: Yes
   - Preserve links: Yes
3. Verify output:
   - All pages present
   - Formatting preserved
   - Text searchable
   - Images and diagrams visible

**Conversion Command** (via pdf skill):
```bash
pdf convert-pptx \
  --input presentation.pptx \
  --output presentation.pdf \
  --quality high \
  --embed-fonts
```

## Slide Type Reference

### 1. Title Slide (Cover Page)

**Template**: `renderers/title.js`

**Content**:
- Project name (large, bold)
- Client name
- Date (if present)
- No bullets

### 2. Content Bullets

**Template**: `renderers/content_bullets.js`

**Content**:
- Lists of requirements, specifications, features
- Supports indentation levels
- Key-value highlighting (e.g., "Project: AI-Powered...")
- Icons for System Requirements sections

**HTML Structure**:
```html
<ul style="list-style-type: none; padding: 0; margin: 0;">
  <li style="margin-left: 0pt; ...">Item 1</li>
  <li style="margin-left: 18pt; ...">Item 1.1 (indented)</li>
  ...
</ul>
```

**Important**: Use `<ul>` with `list-style-type: none` to prevent html2pptx from adding unwanted bullets.

### 3. Two Column Slide

**Template**: `renderers/two_column.js`

**Content**:
- Side-by-side comparison
- Left column: viAct responsibilities
- Right column: Client responsibilities
- Or any comparative content

**HTML Structure**:
```html
<div class="columns">
  <div class="column">
    <h2>Left Title</h2>
    <ul><li>Item 1</li>...</ul>
  </div>
  <div class="column">
    <h2>Right Title</h2>
    <ul><li>Item 1</li>...</ul>
  </div>
</div>
```

### 4. Diagram Slide (System Architecture)

**Template**: `renderers/diagram.js`

**Content**:
- **DO NOT** render HTML with mermaid code
- **DO** use the generated PNG diagram from Step 2
- Embed `assets/diagram.png` as centered image
- Add caption if needed

**HTML Structure**:
```html
<img src="diagram.png" alt="System Architecture" style="width: 100%; max-width: 600pt;" />
```

### 5. Timeline Slide (Implementation Plan)

**Template**: `renderers/timeline.js`

**Content**:
- Phases T0, T1, T2, T3...
- Event names
- Dates or durations
- Activities per phase

**Parsing**: Extract from markdown headings like `### Phase T0: Event Name`

### 6. Module Description Slide

**Template**: `renderers/module_description.js`

**Content**:
- Module name (title)
- Module type (Standard/Advanced/Premium)
- Purpose (what it detects)
- Alert Logic (when it triggers)
- Preconditions (camera setup requirements)
- Video/image demonstration

**Media Priority**:
1. `_video_url` (Google Drive link) → Download and embed
2. `_image_url` (Image link) → Download and embed
3. Blank (no media)

## Important Rules

### No JSON Intermediate

- **OLD**: `.md → .json → .html → .pptx → .pdf`
- **NEW**: `.md → .html → .pptx → .pdf`
- Agent generates HTML directly from markdown
- No intermediate JSON structure needed

### Intelligent Slide Selection

- Agent reads content and decides slide type
- No rigid mapping rules
- Adapt to content length and structure
- Combine short sections (e.g., Network + Camera on one slide)
- Split long sections across multiple slides

### No Regex Parsing

- Agent reads markdown naturally
- Use heading structure (`##`, `###`)
- Identify sections by context
- Extract content by reading between headers
- Parse modules from list/table structure

### Reference Slides

- **Temporarily skip**: Do not insert Available slides (2-25)
- **Focus on generated content only**
- Future: Can add back as optional step

### Bullet Symbol Fix

**Critical**: Always use `<ul style="list-style-type: none; ...">` for lists to prevent html2pptx from adding unwanted bullet characters.

## Output Structure

```
output/
├── {project}_architecture_diagram.md  # Mermaid source
├── html/
│   ├── slide_1.html
│   ├── slide_2.html
│   └── ...
├── assets/
│   ├── background.png
│   ├── diagram.png  # Rendered mermaid diagram
│   ├── module_1_video.mp4  # Downloaded media
│   └── ...
├── presentation.pptx  # Final PowerPoint
└── presentation.pdf  # Final PDF
```

## Progressive Disclosure

Load reference documentation only when needed:

- **SKILL.md** (this file): High-level workflow
- **references/SLIDE_TEMPLATE.md**: Detailed slide structure patterns
- **references/slide_rendering_instructions.md**: HTML rendering standards
- **references/deployment_method_selection_logic.md**: Architecture patterns
- **references/ARCHITECTURE_TEMPLATES.md**: Mermaid diagram examples
- **renderers/**: HTML template files for each slide type

## Dependencies

### Required Skills

- **pptx skill**: For HTML → PPTX conversion
- **pdf skill**: For PPTX → PDF conversion

### Required Tools

- Python 3.8+
- Node.js 16+
- pptxgenjs: `npm install pptxgenjs`
- playwright: `npm install playwright`
- sharp: `npm install sharp`

### Optional Tools

- mermaid-cli: `npm install -g @mermaid-js/mermaid-cli`

## Quality Checklist

Before final delivery, verify:

- ✅ All placeholders resolved in template
- ✅ Architecture diagram matches deployment method
- ✅ All template sections have corresponding slides
- ✅ All module information extracted (purpose, alert_logic, preconditions)
- ✅ HTML slides use `<ul style="list-style-type: none;">` for lists
- ✅ No unwanted bullet characters in PPTX
- ✅ All images and videos embedded correctly
- ✅ PPTX file opens and displays properly
- ✅ PDF file opens and displays properly
- ✅ Formatting consistent across all slides

## Troubleshooting

### HTML Generation Issues

**Wrong slide type selected**:
- Agent should re-read section content
- Consider content length and structure
- Choose more appropriate slide type

**Text overflow in HTML**:
- Reduce font size
- Split content across multiple slides
- Use scrollable content area

### PPTX Conversion Issues

**Unwanted bullet symbols**:
- Verify `<ul style="list-style-type: none;">` in HTML
- Check html2pptx.js respects list-style-type
- Use updated html2pptx.js (with bullet fix)

**Media not embedded**:
- Check file paths in HTML
- Verify media files downloaded to assets/
- Ensure relative paths correct

### PDF Conversion Issues

**Formatting not preserved**:
- Check pdf skill options
- Try higher quality setting
- Verify font embedding

**Text not searchable**:
- Ensure text rendered as text (not images)
- Check pdf skill OCR options

## Example Session

```
User: Generate slides from Bromma_template.md

Agent:
1. Reading Bromma_template.md...
   - Found: 7 sections, 6 AI modules
   - Deployment: Cloud
   - Timeline: 4 milestones (T0-T3)

2. Generating architecture diagram...
   - Created cloud deployment diagram
   - Rendered to PNG (transparent background)
   - Saved: assets/diagram.png

3. Generating HTML slides...
   - Slide 1: Title (Video Analytics Solution Proposal)
   - Slide 2: Content Bullets (Project Requirements)
   - Slide 3: Two Column (Scope of Work)
   - Slide 4: Diagram (System Architecture) - using diagram.png
   - Slide 5: Content Bullets (System Requirements - Network + Camera combined)
   - Slide 6: Timeline (Implementation Plan)
   - Slides 7-12: Module Descriptions (Safety Helmet, Safety Vest, etc.)
   - Total: 12 HTML slides

4. Converting HTML → PPTX...
   - Using pptx skill
   - Embedding assets/diagram.png
   - Downloading 6 module videos
   - Created: presentation.pptx (61MB)

5. Converting PPTX → PDF...
   - Using pdf skill
   - Quality: High
   - Created: presentation.pdf

✅ Complete! Output: presentation.pptx, presentation.pdf
```

## Next Steps

After generating presentations:

1. **Review PPTX**: Open in PowerPoint/LibreOffice, check all slides
2. **Review PDF**: Open in PDF viewer, verify formatting
3. **Check for issues**: Bullet symbols, text overflow, missing content
4. **Fix if needed**: Regenerate specific slides or entire presentation
5. **Deliver**: Share with presales/client
