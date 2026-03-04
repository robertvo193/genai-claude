# Subagent 0: Slide Agent (v2 - Intelligent Direct Generation)

**Purpose**: Intelligently read template markdown, analyze each section, decide slide types, and generate HTML/PPTX directly with flexible formatting (no JSON intermediate).

## Overview

The Slide Agent intelligently processes proposal templates by:
1. Reading and analyzing each section of the template markdown
2. Deciding appropriate slide types based on content characteristics
3. Creating HTML slides directly that meet html2pptx requirements
4. Leveraging pptx skill for PowerPoint generation and pdf skill for PDF conversion
5. Using flexible, adaptive formatting rather than rigid templates

## Key Principles

- **No JSON intermediate**: Generate HTML directly, then convert to PPTX/PDF
- **Intelligent slide type selection**: Analyze content to determine best slide type
- **Flexible formatting**: Adapt layout to content, not content to fixed layout
- **Reference slide learning**: Study standard slides in `20252410_Proposal_EGA.pptx` for patterns
- **Content-aware decisions**: Combine short sections (e.g., Camera + Network requirements) when appropriate

## Input

- **Template file**: Proposal template markdown (placeholder-free)
- **Reference slides**: `20252410_Proposal_EGA.pptx` for style/formatting reference

## Actions

### 1. Read and Parse Template

For each section in the template:
- Extract section title and content
- Analyze content characteristics:
  - Length (short, medium, long)
  - Type (text, list, table, timeline, modules)
  - Structure (single column, two columns, mixed)
  - Media requirements (images, videos, diagrams)

**Template Sections** (typical structure):
1. Cover Page
2. Project Requirement Statement
3. Scope of Work
4. System Architecture
5. System Requirements
   - Network Requirements
   - Camera Specifications
   - AI Training Workstation
   - AI Inference Workstation
   - Dashboard Workstation
   - Power Requirements
6. Implementation Plan (Timeline)
7. Proposed Modules & Functional Description
8. User Interface & Reporting (optional)

### 2. Intelligently Decide Slide Types

For each section, decide slide type based on content analysis:

#### **Cover Page** → Title Slide
- Always `type: title`
- Centered title + optional date
- Minimal, clean design

#### **Project Requirement Statement** → Content Bullets
- `type: content_bullets`
- Use bullet point hierarchy for all information
- Convert table/list data to nested bullets

#### **Scope of Work** → Two Column Slide
- `type: two_column`
- Left: viAct Responsibilities
- Right: Client Responsibilities
- Balanced layout

#### **System Architecture** → Diagram Slide
- `type: diagram`
- Generate Mermaid diagram from content
- Convert Mermaid to PNG (transparent background)
- Embed as full-width image

#### **System Requirements** → Flexible Multi-Slide
**INTELLIGENT COMBINATION LOGIC**:
- **Short content** (< 3 items each): Combine Network + Camera into single slide
- **Medium content** (3-6 items): Keep separate but use compact format
- **Long content** (> 6 items): Separate slides with full details

**Combination Rules**:
```python
if network_items <= 3 and camera_items <= 3:
    create_combined_slide("Network & Camera Requirements")
else:
    create_separate_slides()
```

**Slide Types for System Requirements**:
- `type: content_bullets` - Workstation specs
- `type: content_bullets` - Network + Camera (if combined)
- `type: content_bullets` - Power (if minimal content)

**Formatting Guidelines**:
- Use key-value highlighting: **Processor**: Intel Xeon
- Group related specifications
- Add icons for visual clarity (camera, network, workstation icons)

#### **Implementation Plan** → Timeline Slide
- `type: timeline`
- Parse timeline milestones from template
- **FIX TIMELINE FORMATTING**:
  - Extract phases: T0, T1, T2, T3...
  - Extract events for each phase
  - Extract dates/durations
  - Apply anti-overlap logic
  - Use horizontal timeline visualization

**Timeline Format Expected**:
```markdown
### Phase T0: Project Award
- Contract finalization
- Project kickoff meeting

### Phase T1: Hardware Deployment (Weeks 1-2)
- Duration: 2 weeks
- Activities:
  - Verification of cameras
  - Installation of workstations
```

**Timeline HTML Structure**:
- Horizontal timeline axis
- Staggered label heights (positions 1-4) to prevent overlap
- Event text above/below line alternating
- Phase and date information
- Visual milestone markers

#### **Proposed Modules** → Module Description Slides
- One slide per module (don't group)
- `type: module_description`
- Left: Text content (purpose, alert_logic, preconditions, detection_criteria)
- Right: Media (video → image → blank)
- 50/50 or 60/40 split depending on content length

**Module Slide Structure**:
```html
<div class="module-slide">
  <div class="content-left">
    <h2>Module Name</h2>
    <p><strong>Purpose:</strong> Description</p>
    <p><strong>Alert Logic:</strong> Logic</p>
    <p><strong>Preconditions:</strong> Conditions</p>
    <p><strong>Detection Criteria:</strong> Criteria (if custom)</p>
  </div>
  <div class="media-right">
    <video src="module_video.mp4" />
  </div>
</div>
```

#### **User Interface & Reporting** → Content Bullets
- `type: content_bullets`
- Multiple slides if needed
- Group by: Alerts, Dashboard, Reports

### 3. Generate HTML Slides Directly

For each decided slide type, create HTML that meets html2pptx requirements:

#### **HTML Requirements for html2pptx**:

**Page Setup**:
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    @page {
      size: 10in 7.5in;  /* Standard slide ratio 4:3 */
      margin: 0;
    }
    body {
      width: 10in;
      height: 7.5in;
      margin: 0;
      padding: 0;
      background: #000;
      color: #fff;
      font-family: Arial, sans-serif;
      overflow: hidden;
    }
  </style>
</head>
<body>
  <!-- Slide content here -->
</body>
</html>
```

**Critical Requirements**:
1. **Fixed dimensions**: 10in × 7.5in (4:3 ratio)
2. **Overflow handling**: `overflow: hidden` on all containers
3. **Min-height**: `min-height: 0` on flex containers
4. **Bottom margin**: Minimum 0.5in from bottom edge
5. **Word wrap**: `word-wrap: break-word` and `overflow-wrap: break-word` on text
6. **Media sizing**: Specify width/height explicitly

**Background**:
```html
<div style="
  position: absolute;
  top: 0;
  left: 0;
  width: 10in;
  height: 7.5in;
  background-image: url('background.png');
  background-size: cover;
  background-position: center;
  z-index: 0;
"></div>
```

#### **Slide Type Implementations**:

**Title Slide**:
```html
<div style="
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  width: 90%;
  z-index: 1;
">
  <h1 style="
    font-size: 48pt;
    color: #00AEEF;
    margin-bottom: 20pt;
    text-transform: uppercase;
  ">Video Analytics Solution Proposal for Client</h1>
  <p style="font-size: 24pt; color: #fff;">January 2026</p>
</div>
```

**Content Bullets Slide**:
```html
<div style="
  position: absolute;
  top: 0.5in;
  left: 0.5in;
  right: 0.5in;
  bottom: 0.5in;
  z-index: 1;
">
  <h2 style="color: #00AEEF; font-size: 36pt; margin-bottom: 20pt;">
    Slide Title
  </h2>
  <div style="font-size: 18pt; line-height: 1.6;">
    <p style="margin-bottom: 12pt;">• Level 0 bullet</p>
    <p style="margin-left: 30pt; margin-bottom: 12pt;">  • Level 1 bullet</p>
    <p style="margin-left: 60pt; margin-bottom: 12pt;">    • Level 2 bullet</p>
  </div>
</div>
```

**Two Column Slide**:
```html
<div style="
  position: absolute;
  top: 0.5in;
  left: 0.5in;
  right: 0.5in;
  bottom: 0.5in;
  display: flex;
  gap: 40pt;
  z-index: 1;
">
  <div style="flex: 1; min-width: 0;">
    <h3 style="color: #00AEEF; font-size: 28pt; margin-bottom: 16pt;">
      Column 1 Title
    </h3>
    <div style="font-size: 16pt; line-height: 1.5;">
      <!-- Content here -->
    </div>
  </div>
  <div style="flex: 1; min-width: 0;">
    <h3 style="color: #00AEEF; font-size: 28pt; margin-bottom: 16pt;">
      Column 2 Title
    </h3>
    <div style="font-size: 16pt; line-height: 1.5;">
      <!-- Content here -->
    </div>
  </div>
</div>
```

**Timeline Slide (Fixed)**:
```html
<div style="
  position: absolute;
  top: 0.5in;
  left: 0.5in;
  right: 0.5in;
  bottom: 0.5in;
  z-index: 1;
">
  <h2 style="color: #00AEEF; font-size: 36pt; margin-bottom: 30pt;">
    Implementation Plan
  </h2>

  <!-- Timeline container -->
  <div style="position: relative; height: 400pt;">
    <!-- Timeline axis -->
    <div style="
      position: absolute;
      top: 200pt;
      left: 50pt;
      right: 50pt;
      height: 4pt;
      background: #00AEEF;
    "></div>

    <!-- Milestones with staggered heights -->
    <!-- Position 1 (far-top): Event at -80pt, Phase/Date at -40pt -->
    <!-- Position 2 (near-top): Event at -80pt, Phase/Date at -40pt -->
    <!-- Position 3 (near-bottom): Event at +30pt, Phase/Date at +60pt -->
    <!-- Position 4 (far-bottom): Event at +30pt, Phase/Date at +60pt -->

    <!-- Example milestone -->
    <div style="position: absolute; left: 100pt;">
      <!-- Event text -->
      <div style="
        position: absolute;
        bottom: 230pt;  /* Above line */
        width: 150pt;
        text-align: center;
        font-size: 14pt;
        word-wrap: break-word;
      ">Project Award</div>

      <!-- Phase/Date -->
      <div style="
        position: absolute;
        bottom: 270pt;
        width: 150pt;
        text-align: center;
        font-size: 12pt;
        color: #00AEEF;
      ">T0</div>

      <!-- Marker -->
      <div style="
        position: absolute;
        top: 198pt;
        width: 8pt;
        height: 8pt;
        background: #fff;
        border-radius: 50%;
      "></div>
    </div>
  </div>
</div>
```

**Module Description Slide**:
```html
<div style="
  position: absolute;
  top: 0.5in;
  left: 0.5in;
  right: 0.5in;
  bottom: 0.5in;
  display: flex;
  gap: 30pt;
  z-index: 1;
">
  <!-- Left: Content -->
  <div style="flex: 1; min-width: 0;">
    <h2 style="color: #00AEEF; font-size: 32pt; margin-bottom: 20pt;">
      Module Name
    </h2>
    <div style="font-size: 16pt; line-height: 1.6;">
      <p style="margin-bottom: 16pt;">
        <strong>Purpose:</strong> Module purpose description here.
      </p>
      <p style="margin-bottom: 16pt;">
        <strong>Alert Logic:</strong> Alert trigger logic here.
      </p>
      <p style="margin-bottom: 16pt;">
        <strong>Preconditions:</strong> Preconditions here.
      </p>
      <p style="margin-bottom: 16pt;">
        <strong>Detection Criteria:</strong> Criteria (if custom).
      </p>
    </div>
  </div>

  <!-- Right: Media -->
  <div style="flex: 1; min-width: 0; display: flex; align-items: center;">
    <video style="
      width: 100%;
      height: auto;
      max-height: 400pt;
      object-fit: contain;
    " src="module_video.mp4" controls />
  </div>
</div>
```

**Diagram Slide**:
```html
<div style="
  position: absolute;
  top: 0.5in;
  left: 0.5in;
  right: 0.5in;
  bottom: 0.5in;
  z-index: 1;
">
  <h2 style="color: #00AEEF; font-size: 36pt; margin-bottom: 20pt;">
    Proposed System Architecture
  </h2>
  <img style="
    width: 100%;
    height: auto;
    max-height: 500pt;
    object-fit: contain;
  " src="architecture_diagram.png" />
</div>
```

### 4. Process Media

**Architecture Diagram**:
1. Generate Mermaid code from template content
2. Convert Mermaid to PNG:
   ```bash
   mmdc -i diagram.mmd -o diagram.png -t dark -b transparent
   ```
3. Verify PNG dimensions (should fit within slide boundaries)

**Module Media** (for each module):
1. Check video_url first
2. If video_url provided:
   - Download from Google Drive using Playwright
   - Verify file is valid video (MP4/MOV)
   - Save as `module_X.mp4`
3. If video_url empty or download fails:
   - Fallback to image_url
   - Download image
   - Save as `module_X.png`
4. If both fail: Leave media area blank

### 5. Generate PPTX Using pptx Skill

**Invoke pptx skill**:
```bash
# Use pptx skill to convert HTML slides to PowerPoint
skill pptx --html-dir ./html_slides --output presentation.pptx
```

Or direct HTML-to-PPTX conversion using html2pptx library:
```javascript
const { HTMLtoPPTX } = require('html2pptx');
await HTMLtoPPTX('./html_slides', './presentation.pptx');
```

### 6. Generate PDF Using pdf Skill

**Invoke pdf skill**:
```bash
# Use pdf skill to convert PPTX to PDF
skill pdf --input presentation.pptx --output presentation.pdf
```

## Output Files

- `html/` - Directory of HTML slide files
- `assets/` - Downloaded media files (videos, images, diagrams)
- `presentation.pptx` - Final PowerPoint presentation
- `presentation.pdf` - Final PDF presentation

## Intelligent Decision Logic

### Content Length Classification

```python
def classify_content_length(items):
    if items <= 3:
        return "short"
    elif items <= 6:
        return "medium"
    else:
        return "long"
```

### Section Combination Logic

```python
def should_combine_sections(section1_items, section2_content):
    # Network + Camera combination
    if (section1_items <= 3 and section2_items <= 3):
        return True

    # Workstation combination (if specs are minimal)
    if (all_workstations_short and total_items <= 6):
        return True

    return False
```

### Slide Type Selection

```python
def select_slide_type(section_name, content_analysis):
    if section_name == "Cover Page":
        return "title"
    elif section_name == "Scope of Work":
        return "two_column"
    elif section_name == "System Architecture":
        return "diagram"
    elif section_name == "Implementation Plan":
        return "timeline"
    elif "Module" in section_name:
        return "module_description"
    elif content_analysis.has_columns:
        return "two_column"
    else:
        return "content_bullets"
```

## Quality Checks

Before passing outputs to Reviewer Agent:
- ✅ All HTML files have proper dimensions (10in × 7.5in)
- ✅ All slides meet bottom margin requirement (0.5in minimum)
- ✅ No text overflow (overflow: hidden applied)
- ✅ Timeline slides have anti-overlap logic
- ✅ Media files downloaded and embedded
- ✅ Architecture diagram converted to PNG
- ✅ PPTX file opens correctly
- ✅ PDF file opens correctly

## Common Issues and Solutions

### Timeline Not Displaying Correctly
- **Issue**: Milestone labels overlapping
- **Solution**: Apply staggered heights (positions 1-4)
- **Solution**: Wrap long text to narrow width (140pt)

### Text Cut Off at Bottom
- **Issue**: Content exceeds slide boundaries
- **Solution**: Verify bottom margin of 0.5in
- **Solution**: Apply `overflow: hidden` and `min-height: 0`
- **Solution**: Reduce font size or split into multiple slides

### Media Not Embedding
- **Issue**: Videos/images not showing in PPTX
- **Solution**: Verify file paths are relative
- **Solution**: Check file formats (MP4/MOV for video, PNG/JPEG for images)
- **Solution**: Ensure media files are in assets/ directory

### HTML Conversion Fails
- **Issue**: html2pptx cannot convert HTML
- **Solution**: Verify all HTML files have proper DOCTYPE
- **Solution**: Check dimensions are exactly 10in × 7.5in
- **Solution**: Ensure all CSS is inline (no external stylesheets)

## Reference Standards

Study `20252410_Proposal_EGA.pptx` for:
- Slide layout patterns
- Typography hierarchy
- Color scheme usage
- Spacing and margins
- Media placement
- Timeline visualization
- Module slide formatting

Apply similar patterns but adapt to content rather than forcing content into rigid structure.
