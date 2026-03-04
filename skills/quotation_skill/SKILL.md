---
name: quotation
description: Convert verified proposal templates to final presentations (PDF + PowerPoint). High-level orchestration that invokes pptx and pdf skills for output generation. Use when: (1) Converting approved proposal templates to PowerPoint, (2) Generating PDF from proposal templates, (3) Creating final proposal presentations, or (4) Any proposal-to-presentation conversion task.
---

# Quotation Skill

## Overview

**Single Purpose**: Convert verified proposal templates → PowerPoint → PDF

High-level orchestration layer that leverages `pptx` and `pdf` skills for final output generation.

**Input**: Verified proposal template (markdown, no placeholders)
**Output**: PowerPoint presentation + PDF document

## Workflow

```
Verified Proposal Template (markdown)
    ↓
[Step 0] Create Output Directory
    - Create folder: ./output/[Project]_[Timestamp]/
    - Example: ./output/Leda_Inio_20250115_143022/
    ↓
[Step 1] Generate PowerPoint (from template.md)
    - Create HTML slides from template
    - Use pptx skill (html2pptx workflow)
    - Apply viAct branding
    - Output: ./output/[Project]_[Timestamp]/[Project]_proposal.pptx
    ↓
[Step 2] Generate PDF
    - Use pdf skill (PPTX → PDF)
    - Output: ./output/[Project]_[Timestamp]/[Project]_proposal.pdf
    ↓
[Complete] Both outputs ready for delivery
```

**Output Directory Structure**:
```
./output/
└── [Project]_[Timestamp]/
    ├── [Project]_proposal.pptx           (Step 1: Generated from template)
    ├── [Project]_proposal.pdf            (Step 2: Final PDF)
    └── slides/                           (optional: HTML source files)
        ├── slide01_cover.html
        ├── slide02_requirements.html
        └── ...
```

## Leveraging Existing Skills

### pptx Skill
**Location**: `~/.claude/skills/pptx/`
**Purpose**: HTML → PowerPoint conversion
**Method**: html2pptx workflow
**See**: `references/pptx_workflow.md` for complete guide

**Key features**:
- Convert HTML slides to PowerPoint with accurate positioning
- Design principles (colors, typography, layouts)
- Image and diagram handling
- Professional formatting

### pdf Skill
**Location**: `~/.claude/skills/pdf/`
**Purpose**: PPTX → PDF conversion
**Method**: LibreOffice or pypdf
**See**: `references/pdf_workflow.md` for complete guide

**Key features**:
- High-quality PDF conversion
- Metadata preservation
- Text selection and accessibility

## Quick Start

### Prerequisites
- Verified proposal template (markdown format)
- No placeholders in template
- pptx skill available
- pdf skill available

### Step 0: Create Output Directory
```bash
# Create timestamped output directory
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="./output/${PROJECT_NAME}_${TIMESTAMP}"
mkdir -p "$OUTPUT_DIR/slides"
```

### Step 1: Generate HTML Slides (OVERFLOW-PROOF)
**IMPORTANT**: Use the pre-configured HTML templates to prevent text overflow.

```bash
# Templates location: templates/SLIDE_TEMPLATES.html
# These templates have CORRECT margins, fonts, and spacing

# For each slide:
# 1. Copy the appropriate template from templates/SLIDE_TEMPLATES.html
# 2. Replace placeholder content with your actual content
# 3. Update background.png path to your absolute path
# 4. Save as: $OUTPUT_DIR/slides/slideXX_name.html
```

**Quick Template Selection**:
- Cover page → Template 1
- Bullet lists → Template 2
- Two columns → Template 3
- Sections + bullets → Template 4
- AI module → Template 5
- Timeline/phases → Template 6

### Step 2: Generate PDF
```bash
# Use pdf skill PPTX → PDF conversion
# See references/pdf_workflow.md for detailed guide

# Using LibreOffice (recommended):
libreoffice --headless --convert-to pdf \
  --outdir "$OUTPUT_DIR" \
  "$OUTPUT_DIR/${PROJECT_NAME}_proposal.pptx"
```

## Design Principles

### viAct Branding
- **Primary Color**: #00AEEF (viAct Blue)
- **Text Color**: #FFFFFF (White for contrast on blue)
- **Background**: Use `assets/background.png` (pre-sized viAct background)

### Typography
- **Font**: Arial, Helvetica, Verdana (web-safe required by pptx skill)
- **Slide Title**: 28pt (uppercased, bold)
- **Section Headers**: 15pt (bold)
- **Body Text**: 11pt (regular)
- **Line Height**: 1.2-1.25 (tight spacing to prevent overflow)

### Slide Specifications (CRITICAL - Prevents Text Overflow)
- **Size**: 720pt × 405pt (16:9 aspect ratio)
- **Title Margins**: `30pt 120pt 20pt 40pt` (top right bottom left)
- **Content Margins**: `0 120pt 85pt 40pt` (top right bottom left)
  - **Right margin 120pt**: Leaves room for viAct logo/background design
  - **Bottom margin 85pt**: Prevents text from extending past slide edge (minimum 0.5" required)
- **Text Overflow Prevention**:
  - Maximum bottom margin: **85pt** (not 72pt)
  - If content overflows, increase bottom margin in 5pt increments
  - Test with html2pptx validation before final output
- **Spacing**: Consistent throughout
- **Alignment**: Left-aligned text, centered titles

## Template Structure Mapping

Proposals should follow this structure (mapped to slides):

| Template Section | Slide Type | Content |
|-----------------|------------|---------|
| 1. Cover Page | Title | Project name, date |
| 2. Project Requirements | Content | Project details, scope |
| 3. Scope of Work | Two-column | Responsibilities |
| 4. Client Requirements | Content | Client needs, assumptions |
| 5. System Architecture | Diagram | System architecture |
| 6. System Design | Content | Design approach |
| 7. Solutions | Content | Proposed solutions |
| 8. System Requirements | Content | Hardware, network |
| 9. Implementation Plan | Timeline | Phases, durations |
| 10. AI Modules | Module slides | One slide per module |
| 11. Limitations | Content | System limitations |

**Estimated slides**: 12-18 slides depending on module count

## Technical Proposal Template

All technical proposals MUST follow this 12-section structure:

### 1. COVER PAGE
**Required Fields:**
- Project Name (from S1: Project Name)
- Client/Company Name (from S1: Client Name)
- Date (from S1: Submission Date)
- Version (default: v1.0)
- Prepared by: viAct

### 2. PROJECT REQUIREMENT STATEMENT
**Required Fields:**
- **Project Overview** (from S2: Project Overview)
- **Business Context** (from S1: Industry + S2: Use Case)
- **Key Objectives** (from S2: Objectives)
- **Success Criteria** (from S2: KPIs)

**Logic:**
- Extract project description from S2 "Project Overview"
- Combine S1 "Industry" with S2 "Use Case" for business context
- List 3-5 bullet points from S2 "Objectives"
- Map S2 "KPIs" to measurable success criteria

### 3. SCOPE OF WORK
**Required Fields:**
- **In Scope** (from S2: Scope/Responsibilities)
- **Out of Scope** (explicitly state exclusions)
- **viAct Responsibilities** (from S2: Deliverables)
- **Client Responsibilities** (from S2: Client Requirements)

**Logic:**
- Parse S2 "Scope" section into bullet points
- Add standard exclusions (hardware maintenance, network changes)
- Extract viAct deliverables from S2
- List client prerequisites (site access, data, approvals)

### 4. CLIENT REQUIREMENTS & ASSUMPTIONS
**Required Fields:**
- **Client Needs** (from S1: Requirements + S2: Use Case)
- **Assumptions** (from S2: Assumptions/Constraints)
- **Infrastructure Provided** (from S2: Client Infrastructure)
- **Client Responsibilities** (from S2: Client Requirements)

**Logic:**
- Extract client's stated needs and pain points from S1/S2
- List all assumptions made (network stability, site access, etc.)
- Document what client must provide (power, network, mounting points)
- Clarify client responsibilities (approvals, coordination, access)

### 5. SYSTEM ARCHITECTURE
**Required Fields:**
- **Architecture Diagram** (generate based on S2 components)
- **System Components** (from S2: AI Modules + Hardware)
- **Data Flow** (from S2: Workflow)
- **Integration Points** (from S2: Integration)

**Logic:**
- Create visual diagram showing camera → AI server → dashboard flow
- List all components from S2 sections
- Map data pipeline: capture → inference → storage → reporting
- Identify external system integrations (API, database, etc.)

### 6. SYSTEM DESIGN
**Required Fields:**
- **Design Approach** (from S2: Design Philosophy)
- **Technology Stack** (from S2: Technology Choices)
- **Scalability Considerations** (from S2: Scalability)
- **Redundancy & Reliability** (from S2: Reliability)

**Logic:**
- Explain overall design philosophy (modular, scalable, etc.)
- List key technologies (AI frameworks, databases, etc.)
- Address how system scales (add cameras, add modules)
- Describe redundancy (backup servers, failover mechanisms)

### 7. SOLUTIONS
**Required Fields:**
- **Primary Solution** (from S2: Proposed Solution)
- **Alternative Options** (from S2: Alternatives)
- **Justification** (from S2: Solution Justification)
- **Competitive Advantages** (from S2: Advantages)

**Logic:**
- Present main recommended solution approach
- List alternative approaches considered (if any)
- Explain why this solution is optimal
- Highlight unique viAct advantages vs competitors

### 8. SYSTEM REQUIREMENTS

#### 8.1 Network Requirements
**Source:** S2: Network Requirements
- Bandwidth per camera
- Total bandwidth calculation
- Network switch specifications
- Cable requirements (Cat6/Fiber)

**Logic:**
`Bandwidth = Camera Count × Bandwidth per Camera × 1.2 (buffer)`

#### 8.2 Camera Requirements
**Source:** S1: Camera Quantity + S2: Camera Specifications
- Total camera count
- Resolution per camera (1080p/4K)
- Field of View requirements
- Mounting type (pole/wall)

**Logic:**
- Extract count from S1 "Quantity" column
- Map camera specs from S2 requirements
- Specify mounting based on use case

#### 8.3 AI Inference Workstation
**Source:** S2: Hardware Requirements
- CPU/GPU specifications
- RAM requirements
- Storage (SSD) capacity
- Operating system

**Logic:**
`Storage = Camera Count × Retention Days × Daily Storage per Camera`

#### 8.4 AI Training Workstation (Optional)
**Source:** S2: Custom AI Model Development
- GPU specifications (if training required)
- Training dataset size
- Training frequency

#### 8.5 Dashboard Workstation
**Source:** S2: User Access Requirements
- Number of concurrent users
- Browser requirements
- Display specifications

#### 8.6 Additional Equipment
**Source:** S1 & S2: Additional Items
- UPS (uninterruptible power supply)
- Network racks/cabinets
- Cabling and accessories

#### 8.7 Power Requirements
**Source:** S2: Infrastructure Requirements
- Power consumption (Watts)
- Electrical outlet type
- Backup power recommendations

### 9. IMPLEMENTATION PLAN (TIMELINE)
**Required Phases:**

#### T0: Pre-Installation (1-2 weeks)
- Site survey and final assessment
- Network infrastructure validation
- Hardware procurement
- Project kick-off meeting

#### T1: Installation (1-2 weeks)
- Camera mounting and cabling
- Server and network equipment setup
- Power and connectivity testing
- On-site hardware validation

#### T2: Configuration & Testing (1-2 weeks)
- AI model deployment
- System configuration (zones, rules)
- Integration testing
- User acceptance testing (UAT)

#### T3: Training & Handover (1 week)
- User training sessions
- Documentation handover
- Go-live support
- Project sign-off

**Logic:**
- Calculate duration based on project complexity
- Add buffer for change requests
- Include weekly progress reporting

### 10. PROPOSED MODULES & FUNCTIONAL DESCRIPTION
**Structure:** One slide per AI module

**For each module (from S2: AI Modules):**
- **Module Name** (e.g., PPE Detection)
- **Functionality** (what it detects)
- **Business Value** (benefit to client)
- **Key Features** (3-5 bullet points)
- **Technical Approach** (algorithm/accuracy)

**Logic:**
- Extract each module from S2 "AI Modules" section
- Create dedicated slide for each module
- Include detection examples if available
- Link to business objectives from Section 2

### 11. USER INTERFACE & REPORTING
**Required Fields:**
- **Dashboard Features** (from S2: Dashboard Requirements)
- **Real-time Alerts** (from S2: Alert Configuration)
- **Reporting Capabilities** (from S2: Reports)
- **Mobile Access** (if specified)

**Logic:**
- List key dashboard widgets/charts
- Describe alert channels (email/SMS/app)
- Specify report types (daily/weekly/monthly)
- Include screenshots if available

### 12. LIMITATIONS
**Required Fields:**
- **Technical Limitations** (from S2: Technical Constraints)
- **Environmental Limitations** (from S2: Environmental Factors)
- **Accuracy Limitations** (from S2: Accuracy Constraints)
- **Scope Limitations** (from S2: Scope Boundaries)

**Logic:**
- List technical constraints (lighting, weather, angles)
- Document environmental limitations (indoor/outdoor, distance)
- Specify accuracy limitations (false positive/negative rates)
- Clarify scope boundaries (what system cannot do)
- Be transparent to set realistic expectations

**Template Mappings Summary:**
- S1 (Commercial) → Project metadata, quantities, commercial terms
- S2 (Technical) → All technical content, requirements, modules
- Each S2 section maps to specific proposal sections
- Use logic to derive calculated fields (bandwidth, storage, timeline)

## Output Files

### Final Outputs (in timestamped directory)
- `./output/[Project]_[Timestamp]/[Project]_proposal.pptx` - Generated PowerPoint presentation
- `./output/[Project]_[Timestamp]/[Project]_proposal.pdf` - Final PDF document

### Optional (for reference)
- `./output/[Project]_[Timestamp]/slides/` - HTML source files
- `./output/[Project]_[Timestamp]/[Project]_slide_mapping.md` - Template sections → slide mapping

### Output Directory Naming Convention
```
./output/[ProjectName]_[YYYYMMDD]_[HHMMSS]/

Examples:
./output/Leda_Inio_20250115_143022/
./output/Construction_Safety_20250116_091545/
./output/PPE_Detection_20250117_163030/
```

**Benefits of timestamped directories:**
- Each run creates a new unique folder
- No risk of overwriting previous outputs
- Easy to track generation history
- Simple to compare different versions

## Assets

### background.png
**Location**: `assets/background.png`
**Purpose**: viAct slide background for consistent branding
**Size**: 154KB
**Dimensions**: 720px × 405px (16:9 aspect ratio)
**Format**: PNG image

**Usage in HTML slides** (WORKING METHOD):
```html
<style>
  body {
    background-image: url('file:///absolute/path/to/quotation_skill/assets/background.png');
    background-size: cover;
    background-position: center;
  }
</style>
```

**Critical Note**: Background MUST use absolute `file://` URLs for html2pptx compatibility. Relative paths and base64 data URIs do not work reliably.

**How to reference background:**
```python
import os

# Get absolute path to background
skill_dir = os.path.dirname(os.path.abspath(__file__))
background_path = os.path.join(skill_dir, 'assets', 'background.png')
background_url = f'file://{background_path}'

# Use in HTML
background_style = f"background-image: url('{background_url}');"
```

## References

- **SLIDE_TEMPLATES.md** - Standardized HTML slide templates (UPDATED)
  - Template 1: Simplified Cover Page
  - Template 2: Standard Content Slide
  - Template 3: Two-Column Layout
  - Template 4: AI Modules Overview
  - Template 5: AI Module Detail (two-column with video/image placeholder)
  - Template 6: Timeline (two-column)
  - Complete usage guidelines and validation checklist
  - **Use this for any proposal generation task**

- `references/pptx_workflow.md` - Complete PowerPoint generation guide
  - HTML slide creation
  - html2pptx workflow
  - Design principles
  - Example slides

- `references/pdf_workflow.md` - Complete PDF generation guide
  - PPTX → PDF conversion
  - LibreOffice usage
  - Quality verification

## Example Usage

### Basic Usage
**User**: "Generate PowerPoint and PDF from Leda_Inio_template.md"
**Action**:
1. Extract project name from template: "Leda_Inio"
2. Create timestamped output directory: `./output/Leda_Inio_20250115_143022/`
3. Read template to extract sections
4. Create HTML slides in `./output/Leda_Inio_20250115_143022/slides/`
5. Convert to PowerPoint using pptx skill
6. Convert PowerPoint to PDF using pdf skill
**Output**:
- `./output/Leda_Inio_20250115_143022/Leda_Inio_proposal.pptx` - PowerPoint presentation
- `./output/Leda_Inio_20250115_143022/Leda_Inio_proposal.pdf` - PDF document

### Advanced Usage
**User**: "Create presentation with custom colors"
**Action**:
1. Create timestamped output directory
2. Override default viAct branding if specified
3. Follow pptx skill design principles
4. Ensure consistent styling throughout
5. Save outputs to timestamped directory

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Template has placeholders | Template must be verified first (no `[PLACEHOLDER_ID]`) |
| PowerPoint generation failed | Check pptx skill installation, see `pptx_workflow.md` |
| PDF conversion failed | Install LibreOffice, see `pdf_workflow.md` |
| Slides missing content | Verify template completeness, check section mapping |
| Layout issues | Adjust HTML/CSS spacing, follow pptx skill guidelines |
| **Text overflow on slides** | **CRITICAL**: Increase bottom margin to 85pt minimum, reduce font size to 11pt |
| **"Text box ends too close to bottom edge"** | **Fix**: Change `margin: 0 80pt 72pt 40pt` to `margin: 0 120pt 85pt 40pt` |
| **Content extends past slide bottom** | **Fix**: Reduce content length or increase bottom margin in 5pt increments |
| **Background not showing** | Background MUST use absolute `file://` URL |
| Background shows white/blank | Verify path is absolute and starts with `file://` |
| Background distorted | Verify image dimensions are 720×405px |
| "Unable to read media" error | Check that URL uses `file://` not `data:` scheme |

### Text Overflow Prevention (CRITICAL)

**⚠️ SMART OVERFLOW DETECTION**: html2pptx now detects when text box bounding box > 0.9 * page size and suggests using two-column layout or splitting into 2 slides.

**Problem Solved**:
- **OLD**: Make fonts tiny (9pt) → Hard to read ❌
- **NEW**: Use two-column layout → Readable 10pt fonts ✅

**Smart Overflow Detection** (in html2pptx.js):
```javascript
// Detects when text box covers > 90% of slide
if (textBoxArea > (slideWidth * slideHeight * 0.9)) {
  errors.push(`⚠️ Text covers ${coverage}% of slide. Use two-column layout or split.`);
}
```

**Solution - Two Approaches**:

### Approach 1: Use Two-Column Layout (Recommended for content-heavy slides)
```html
<!-- Template 7: Two-Column Timeline -->
<div class="columns">
  <div class="column">
    <!-- Left content -->
  </div>
  <div class="column">
    <!-- Right content -->
  </div>
</div>
```

**Benefits**:
- Reduces vertical space by ~50%
- Maintains readable 10pt fonts
- Perfect for timelines, requirements, scope

### Approach 2: Increase Margins (For simple slides)
```css
.content {
  margin: 0 140pt 110pt 40pt;  /* Standard safe margins */
}
p, li {
  font-size: 10pt;        /* Readable, not tiny */
  line-height: 1.15;
}
h2 {
  font-size: 14pt;
}
```

**When to use each approach**:

| Situation | Use | Template |
|-----------|-----|----------|
| Timeline with 4+ phases | Two-column | Template 7 |
| Long requirements list | Two-column | Template 3 |
| AI module (short) | Single column | Template 5 |
| Cover page | Special layout | Template 1 |

**Step-by-Step Decision Tree**:
1. **Content fits in one column with 10pt fonts?** → Use single column (Templates 2, 4, 5, 6)
2. **Content overflows even with 10pt fonts?** → Use two columns (Templates 3, 7)
3. **Still overflows with two columns?** → Split into 2 slides

**⚠️ ALWAYS VERIFY**: Open PowerPoint and visually check NO TEXT OVERFLOWS!

### Background Issues - Common Causes

1. **Wrong URL scheme**
   - ❌ `background-image: url('data:image/png;base64,...')` - html2pptx doesn't support base64 in path property
   - ❌ `background-image: url('assets/background.png')` - Relative paths don't work
   - ✅ `background-image: url('file:///absolute/path/to/background.png')` - CORRECT
   - **Reason**: html2pptx requires absolute file:// URLs for external images

2. **Path must be absolute**
   - ❌ `file://background.png` - Not absolute
   - ❌ `file://./assets/background.png` - Relative
   - ✅ `file:///home/user/skills/quotation_skill/assets/background.png` - Absolute

3. **Wrong image dimensions**
   - Background must be 720×405px for 16:9 slides
   - Larger images will be cropped/scaled incorrectly
   - Pre-size image before using

4. **File not accessible**
   - Verify file exists at specified path
   - Check file permissions (readable)
   - Use absolute paths to avoid path resolution issues

## Important Notes

### This Skill Does NOT
- ❌ Process Deal Transfer Excel files
- ❌ Generate proposal templates from scratch
- ❌ Handle placeholders or presale review
- ❌ Validate template content
- ❌ Extract data from Deal Transfer

### This Skill DOES
- ✅ Convert verified templates to PowerPoint
- ✅ Generate PDF from PowerPoint
- ✅ Apply viAct branding consistently
- ✅ Orchestrate pptx and pdf skills

### Prerequisites
- Template must already be verified (no placeholders)
- Template must follow standard proposal structure
- pptx skill must be available
- pdf skill must be available

## Architecture

```
quotation_skill (high-level orchestration)
│
└── Template (verified)
    ├── [Step 1] → pptx skill → proposal.pptx
    └── [Step 2] → pdf skill → proposal.pdf
```

**Key Points**:
- ✅ **Simple workflow**: Template → PowerPoint → PDF
- ✅ **No reference slides**: Only generates slides from template content
- ✅ **Focused**: Single purpose output generation
- ✅ **High-level**: Orchestrates pptx and pdf skills only
- ✅ **Leverages**: pptx skill, pdf skill
- ✅ **Delivers**: PDF + PowerPoint final outputs

---

## System Architecture Diagram Generation

**NEW FEATURE**: Automatically generate system architecture diagrams from template.md

### High-Level Workflow (No JSON, No Regex)

```
template.md (SYSTEM ARCHITECTURE section)
    ↓
Extract: deployment method, cameras, AI modules
    ↓
Generate Mermaid code (Python)
    ↓
Convert to PNG (mmdc / mermaid-cli)
    ↓
Insert into HTML slide (diagram template)
    ↓
PowerPoint with embedded diagram
```

### Quick Start: Generate Architecture Diagram

#### Step 1: Extract Data from template.md

From the "SYSTEM ARCHITECTURE" section:

```markdown
## 4. SYSTEM ARCHITECTURE

**Deployment Method:** On-Premise

**System Components:**
- IP Cameras: 9 existing cameras
- AI Modules: 5 modules
  1. Helmet Detection
  2. Safety Mask Detection
  3. Hi-vis vest detection
  4. Fire & Smoke Detection
  5. Human Down Detection
```

#### Step 2: Generate Mermaid Code

```python
from scripts.generate_architecture_diagram import SimpleArchitectureGenerator

generator = SimpleArchitectureGenerator(
    deployment_method='on-prem',
    num_cameras=9,
    ai_modules=[
        'Helmet Detection',
        'Safety Mask Detection',
        'Hi-vis vest detection',
        'Fire & Smoke Detection',
        'Human Down Detection'
    ],
    deployment_details={
        'alert_methods': ['Dashboard', 'Email', 'Telegram'],
        'include_nvr': False,
        'compact_mode': True
    }
)

mermaid_code = generator.generate()
```

#### Step 3: Save Mermaid Code

```bash
# Save to .mmd file
cat > architecture.mmd << 'EOF'
<mermaid_code_from_step_2>
