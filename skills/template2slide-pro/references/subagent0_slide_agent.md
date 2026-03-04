# Subagent 0: Slide Agent

**Purpose**: Generate HTML, PPTX, and PDF from proposal template markdown files.

## Overview

The Slide Agent is responsible for the complete conversion of proposal template markdown files into final presentation formats (HTML, PPTX, PDF). This agent processes one or more template files and orchestrates the full generation pipeline.

## Input

- **Template files**: One or more proposal template markdown files (e.g., `AVA_Project_Nas_Ltd_template.md`)
- **Templates must be**: Pre-verified, placeholder-free (no `[NETWORK_001]`, `[TIMELINE_001]`, etc.)

## Actions

### 1. Parse Template Markdown

For each input template:
- Extract project metadata (name, client, date, etc.)
- Identify all sections (Cover Page, Requirements, Scope, Architecture, etc.)
- Validate template structure and completeness
- Check for unresolved placeholders (reject if found)

### 2. Generate Architecture Diagram (Mermaid)

- Determine deployment method from template content
- Generate Mermaid diagram code following architecture patterns
- Use `deployment_method_selection_logic.md` for deployment determination
- Use `ARCHITECTURE_TEMPLATES.md` for diagram patterns
- Output: `[Project_Name]_architecture_diagram.md`

### 3. Map Content to Slide Structure

- Parse all template sections
- Map each section to appropriate slide type following `SLIDE_TEMPLATE.md`
- Extract all module information (type, purpose, alert_logic, preconditions, etc.)
- Create structured JSON with slide-by-slide content
- Output: `[Project_Name]_slide_structure.json`

**Critical**: Extract ALL module fields correctly:
- Module Type (Standard/Custom)
- Purpose Description
- Alert Trigger Logic
- Preconditions
- Detection Criteria (if applicable)
- Image URL (optional, can be empty)
- Video URL (optional, can be empty)

### 4. Generate HTML Slides

- Use `scripts/generate_from_json.js` to generate HTML from slide structure JSON
- Apply slide rendering standards from `slide_rendering_instructions.md`
- Handle different slide types: title, content_bullets, two_column, module_description, diagram, timeline
- Output: Individual HTML files for each slide (saved to html_dir for debugging)

**Key rendering rules**:
- Use minimalist dark theme (background.png, white text, viAct blue accent)
- Ensure proper overflow handling (overflow: hidden, min-height: 0)
- Apply proper typography sizing (title large, body readable, min 11pt)
- Handle smart content aggregation (merge short System Requirements slides)
- Implement anti-overlap logic for timeline slides

### 5. Convert HTML → PPTX

- Use `scripts/html2pptx.js` or PPTX skill to convert HTML slides to PowerPoint
- Apply consistent styling and formatting
- Embed architecture diagram (convert Mermaid to PNG with transparent background)
- Download and embed images from Google Drive URLs
- Handle media priority (video_url → image_url → blank)
- Output: `[Project_Name]_proposal.pptx`

**Media handling**:
- Google Drive URLs: Use Playwright to handle download confirmation pages
- Validate downloaded files (check magic bytes: MP4/MOV for video, PNG/JPEG/GIF for image)
- If video download fails: fallback to image_url
- If both fail: leave media area blank for manual insertion

### 6. Convert PPTX → PDF

- Use PDF skill to convert PowerPoint to PDF
- Preserve formatting and layout
- Output: `[Project_Name]_proposal.pdf`

## Output Files (Per Template)

For each input template, the Slide Agent generates:

1. **`[Project_Name]_architecture_diagram.md`**: Mermaid architecture diagram code
2. **`[Project_Name]_project_info.json`**: Extracted project information and deployment method
3. **`[Project_Name]_slide_structure.json`**: Complete slide structure in JSON format
4. **`[Project_Name]_proposal.html`**: HTML slides (individual files in html_dir)
5. **`[Project_Name]_proposal.pptx`**: Final PowerPoint presentation
6. **`[Project_Name]_proposal.pdf`**: Final PDF presentation

## Workflow

```
For each input template.md:
  1. Parse template → Extract metadata and sections
  2. Generate architecture diagram → Create Mermaid diagram
  3. Map content to slides → Create slide_structure.json
  4. Generate HTML slides → Create HTML files
  5. Convert HTML to PPTX → Create .pptx file
  6. Convert PPTX to PDF → Create .pdf file
  7. Return all output file paths
```

## Dependencies

- **Python 3.8+**: For Python scripts (template2slide.py, map_to_slides.py, etc.)
- **Node.js**: For HTML → PPTX conversion
- **pptxgenjs**: npm package for PowerPoint generation
- **playwright**: For Google Drive URL handling
- **sharp**: For image processing
- **mermaid-cli**: For diagram rendering (or use online service)

## Quality Checks

Before passing outputs to Reviewer Agent, verify:
- ✅ All placeholders resolved (no `[NETWORK_001]` tokens remain)
- ✅ Architecture diagram matches deployment method
- ✅ All template sections mapped to slides
- ✅ All module information extracted (no empty fields except image_url/video_url)
- ✅ Slide numbering is continuous
- ✅ HTML slides render correctly
- ✅ PPTX file opens and displays properly
- ✅ PDF file opens and displays properly
- ✅ All images and diagrams visible
- ✅ No text overflow in slides

## Troubleshooting

### Placeholders Found
- **Issue**: Template contains unresolved placeholders like `[NETWORK_001]`
- **Solution**: Reject template and request presales verification

### Module Information Missing
- **Issue**: Empty fields in module data (purpose, alert_logic, etc.)
- **Solution**: Check template format and extraction logic in `map_to_slides.py`

### Architecture Not Generated
- **Issue**: Cannot determine deployment method
- **Solution**: Review `deployment_method_selection_logic.md` and template content

### HTML Overflow
- **Issue**: Content exceeds slide boundaries
- **Solution**: Apply overflow handling rules from `slide_rendering_instructions.md`

### Media Download Failed
- **Issue**: Google Drive URL cannot be downloaded
- **Solution**: Verify URL format, check Playwright handling, fallback to alternative URL

## Integration

This agent is invoked by the main orchestration layer (template2slide-pro SKILL.md) and passes its outputs to Subagent 1 (Reviewer Agent) for validation.
