---
name: quotation-generate-slide
description: Generate PowerPoint and PDF from verified proposal templates with 4-step auto-continue workflow and clear state display
argument-hint: "<template.md>"
allowed-tools: SlashCommand(*), TodoWrite(*), Bash(*), Read(*), Write(*)
---

# Quotation Generate Slide Workflow Command

## Coordinator Role

**This command is a pure orchestrator**: Execute 4 steps in sequence to convert verified proposal templates into PowerPoint presentations and PDF documents. Runs **fully autonomously** once triggered with **automatic continuation** between steps and **clear state display** throughout execution.

**Execution Model - Auto-Continue Workflow**:

This workflow runs autonomously through 4 steps:
1. Create Output Directory
2. Generate HTML Slides
3. Generate PowerPoint
4. Generate PDF

## Core Rules

1. **Start Immediately**: First action is TodoWrite initialization, second action is Step 1 execution
2. **No Preliminary Validation**: Start execution immediately (validation happens in Step 1)
3. **Parse Every Output**: Extract data (output_dir, pptx_file, pdf_file) for next step
4. **Auto-Continue via TodoList**: Check TodoList status and execute next pending step automatically
5. **Track Progress**: Update TodoWrite dynamically for each step
6. **⚠️ CONTINUOUS EXECUTION**: Do not stop until all 4 steps complete

## Execution Process

```
Input Parsing:
   └─ Extract template path from arguments
   └─ Validate template exists and is .md format
   └─ Extract project name from template filename

Step 1: Create Output Directory
   └─ Generate timestamp
   └─ Create directory: ./output/[Project]_[Timestamp]/
   └─ Output: output_dir path

Step 2: Generate HTML Slides
   └─ Read template.md
   └─ Parse template sections (12 sections)
   └─ Generate HTML slides (15 slides)
   └─ Apply viAct branding
   └─ Output: HTML files in output_dir/slides/

Step 3: Generate PowerPoint
   └─ Call pptx skill (html2pptx workflow)
   └─ Convert HTML → PPTX
   └─ Apply viAct branding (blue #00AEEF, white text)
   └─ Output: [Project]_proposal.pptx

Step 4: Generate PDF
   └─ Call pdf skill (pptx2pdf workflow)
   └─ Convert PPTX → PDF
   └─ Output: [Project]_proposal.pdf

Return:
   └─ Summary with file locations and slide count
```

## 4-Step Execution

### Step 0: Initialize TodoWrite (Mandatory)

```javascript
TodoWrite({
  todos: [
    {content: "Step 1: Create Output Directory", status: "pending", activeForm: "Creating output directory"},
    {content: "Step 2: Generate HTML Slides", status: "pending", activeForm: "Generating HTML slides"},
    {content: "Step 3: Generate PowerPoint", status: "pending", activeForm: "Generating PowerPoint"},
    {content: "Step 4: Generate PDF", status: "pending", activeForm: "Generating PDF"}
  ]
})
```

### Step 1: Create Output Directory

**Execute**:

```javascript
// Extract template path from arguments
const templatePath = args[0]; // First argument

// Validate template exists
const fileExists = fs.existsSync(templatePath);
if (!fileExists) {
  throw new Error(`Template file not found: ${templatePath}`);
}

// Validate .md format
if (!templatePath.endsWith('.md')) {
  throw new Error(`Template must be .md format: ${templatePath}`);
}

// Extract project name
const projectName = path.basename(templatePath, '.md');

// Generate timestamp
const timestamp = bash('date +%Y%m%d_%H%M%S').trim();

// Create output directory
const outputDir = `./output/${projectName}_${timestamp}/`;
bash(`mkdir -p "${outputDir}slides"`);

// Update TodoWrite
TodoWrite({
  todos: [
    {content: "Step 1: Create Output Directory", status: "completed", activeForm: "Creating output directory"},
    {content: "Step 2: Generate HTML Slides", status: "in_progress", activeForm: "Generating HTML slides"},
    {content: "Step 3: Generate PowerPoint", status: "pending", activeForm: "Generating PowerPoint"},
    {content: "Step 4: Generate PDF", status: "pending", activeForm: "Generating PDF"}
  ]
})

console.log(`[Step 1/4] Create Output Directory [✓ COMPLETED]`);
console.log(`✓ Created: ${outputDir}`);
```

**Parse Output**:
- Extract: `project_name` for next step
- Extract: `output_dir` for next step

**Auto-Continue**: Execute Step 2

---

### Step 2: Generate HTML Slides

**Execute**:

```javascript
// Read template
const templateContent = fs.readFileSync(templatePath, 'utf8');

// Parse template sections (12 sections)
const sections = parseTemplateSections(templateContent);

// Generate HTML slides using quotation_skill logic
const slidesDir = `${outputDir}slides/`;

// Slide 1: Cover slide
const coverSlide = generateCoverSlide(projectName, sections);
fs.writeFileSync(`${slidesDir}slide01_cover.html`, coverSlide);

// Slide 2: Project Requirement Statement
const prsSlide = generatePRSSlide(sections['project_requirement_statement']);
fs.writeFileSync(`${slidesDir}slide02_requirements.html`, prsSlide);

// Generate remaining slides (13 total sections mapped to 15 slides)
// ... (slide generation logic)

const slideCount = 15;

// Update TodoWrite
TodoWrite({
  todos: [
    {content: "Step 1: Create Output Directory", status: "completed", activeForm: "Creating output directory"},
    {content: "Step 2: Generate HTML Slides", status: "completed", activeForm: "Generating HTML slides"},
    {content: "Step 3: Generate PowerPoint", status: "in_progress", activeForm: "Generating PowerPoint"},
    {content: "Step 4: Generate PDF", status: "pending", activeForm: "Generating PDF"}
  ]
})

console.log(`[Step 2/4] Generate HTML Slides [✓ COMPLETED]`);
console.log(`✓ Generated ${slideCount} HTML slides`);
console.log(`✓ Applied viAct branding (blue #00AEEF, white text)`);
```

**Parse Output**:
- Extract: `slide_count`
- Extract: `slides_dir`

**Auto-Continue**: Execute Step 3

---

### Step 3: Generate PowerPoint

**Execute**:

```javascript
// Call pptx skill to convert HTML → PPTX
const pptxResult = SlashCommand({
  command: "/pptx html2pptx",
  arguments: [slidesDir]
});

// Parse result to get PPTX file path
const pptxFile = `${outputDir}${projectName}_proposal.pptx`;

// Update TodoWrite
TodoWrite({
  todos: [
    {content: "Step 1: Create Output Directory", status: "completed", activeForm: "Creating output directory"},
    {content: "Step 2: Generate HTML Slides", status: "completed", activeForm: "Generating HTML slides"},
    {content: "Step 3: Generate PowerPoint", status: "completed", activeForm: "Generating PowerPoint"},
    {content: "Step 4: Generate PDF", status: "in_progress", activeForm: "Generating PDF"}
  ]
})

console.log(`[Step 3/4] Generate PowerPoint [✓ COMPLETED]`);
console.log(`✓ Created: ${pptxFile}`);
console.log(`✓ ${slideCount} slides, 720x405px`);
```

**Parse Output**:
- Extract: `pptx_file_path`

**Auto-Continue**: Execute Step 4

---

### Step 4: Generate PDF

**Execute**:

```javascript
// Call pdf skill to convert PPTX → PDF
const pdfResult = SlashCommand({
  command: "/pdf pptx2pdf",
  arguments: [pptxFile]
});

// Parse result to get PDF file path
const pdfFile = `${outputDir}${projectName}_proposal.pdf`;

// Update TodoWrite
TodoWrite({
  todos: [
    {content: "Step 1: Create Output Directory", status: "completed", activeForm: "Creating output directory"},
    {content: "Step 2: Generate HTML Slides", status: "completed", activeForm: "Generating HTML slides"},
    {content: "Step 3: Generate PowerPoint", status: "completed", activeForm: "Generating PowerPoint"},
    {content: "Step 4: Generate PDF", status: "completed", activeForm: "Generating PDF"}
  ]
})

console.log(`[Step 4/4] Generate PDF [✓ COMPLETED]`);
console.log(`✓ Created: ${pdfFile}`);
```

**Auto-Continue**: All steps complete, return summary

---

## Return Summary

```javascript
console.log(``);
console.log(`✅ Slide Generation Complete!`);
console.log(``);
console.log(`📁 Template: ${templatePath}`);
console.log(`📊 Project: ${projectName}`);
console.log(``);
console.log(`Output Files:`);
console.log(`  • ${pptxFile} (${slideCount} slides)`);
console.log(`  • ${pdfFile} (${slideCount} pages)`);
console.log(``);
console.log(`📊 Statistics:`);
console.log(`  • Slides generated: ${slideCount}`);
console.log(`  • Dimensions: 720x405px`);
console.log(`  • Branding: viAct (blue #00AEEF, white text)`);
console.log(``);
console.log(`✨ Ready for delivery!`);
```

## Error Handling

| Error | Solution |
|-------|----------|
| Template not found | Show clear error with file path |
| Invalid format | "Template must be .md format (not .txt)" |
| Template has placeholders | "Template must be verified (no placeholders allowed)" |
| quotation_skill not found | "quotation_skill not available. Install from ~/.claude/skills/quotation_skill/" |
| pptx skill not found | "pptx skill not available" |
| pdf skill not found | "pdf skill not available" |

## Input Validation

**Pre-execution checks**:
```javascript
// Validate template exists
if (!fs.existsSync(templatePath)) {
  return `Error: Template file not found: ${templatePath}`;
}

// Validate .md format
if (!templatePath.endsWith('.md')) {
  return "Error: Template must be .md format (not .txt)";
}

// Validate no placeholders
const templateContent = fs.readFileSync(templatePath, 'utf8');
if (templateContent.includes('[PLACEHOLDER_') || templateContent.includes('[Value]')) {
  return "Error: Template must be verified (no placeholders allowed). Use /template to generate initial template.";
}
```

## Helper Functions

### parseTemplateSections

```javascript
function parseTemplateSections(content) {
  // Parse 12 sections from template
  const sections = {};

  // Section 1: Project Requirement Statement
  const prsMatch = content.match(/## 1\. Project Requirement Statement\n([\s\S]+?)\n## /);
  sections['project_requirement_statement'] = prsMatch ? prsMatch[1].trim() : '';

  // Section 2: Current Situation & Pain Points
  const painMatch = content.match(/## 2\. Current Situation & Pain Points\n([\s\S]+?)\n## /);
  sections['pain_points'] = painMatch ? painMatch[1].trim() : '';

  // ... parse remaining sections

  return sections;
}
```

### generateCoverSlide

```javascript
function generateCoverSlide(projectName, sections) {
  return `
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    font-family: Arial, sans-serif;
    background-color: #00AEEF;
    color: white;
    margin: 0;
    padding: 0;
    width: 1280px;
    height: 720px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .content {
    text-align: center;
  }
  h1 {
    font-size: 72px;
    margin: 0 0 40px 0;
  }
  h2 {
    font-size: 48px;
    margin: 0;
    font-weight: normal;
  }
</style>
</head>
<body>
  <div class="content">
    <h1>AI-Powered Video Analytics</h1>
    <h2>Technical Proposal</h2>
  </div>
</body>
</html>
  `.trim();
}
```

### generatePRSSlide

```javascript
function generatePRSSlide(prsContent) {
  // Parse PRS content and format as HTML slide
  // Use Template 2 from SLIDE_TEMPLATES.md
  // ... (implementation details in quotation_skill)
}
```

## Usage

```bash
# Basic usage
/quotation generate slide verified_template.md

# Alternative invocation (if registered as command)
/workflow:quotation-generate-slide "verified_template.md"
```

## Output Example

```
🎯 Slide Generation Started
📁 Template: verified_template.md
📊 Project: verified_template

[Step 1/4] Create Output Directory [✓ COMPLETED]
✓ Created: ./output/verified_template_20260126_235000/

[Step 2/4] Generate HTML Slides [✓ COMPLETED]
✓ Generated 15 HTML slides
✓ Applied viAct branding

[Step 3/4] Generate PowerPoint [✓ COMPLETED]
✓ Created: verified_template_proposal.pptx
✓ 15 slides, 720x405px

[Step 4/4] Generate PDF [✓ COMPLETED]
✓ Created: verified_template_proposal.pdf

✅ Slide Generation Complete!

📁 Output: ./output/verified_template_20260126_235000/
  • verified_template_proposal.pptx (15 slides)
  • verified_template_proposal.pdf (15 pages)

📊 Statistics:
  • Slides generated: 15
  • Dimensions: 720x405px
  • Branding: viAct (blue #00AEEF, white text)

✨ Ready for delivery!
```

## Integration with quotation_skill

This workflow orchestrates the quotation_skill components:

- **HTML Slide Generation**: Uses quotation_skill template parsing logic
- **viAct Branding**: Applies #00AEEF blue, white text, Arial font
- **Text Overflow Prevention**: Uses proper margins (0 120pt 85pt 40pt)
- **Slide Templates**: Uses 7 templates from quotation_skill/SLIDE_TEMPLATES.md
- **PPTX Generation**: Delegates to pptx skill
- **PDF Generation**: Delegates to pdf skill

**No modifications to quotation_skill** - This is a pure wrapper/orchestrator.

## Version History

**v1.0.0** (2025-01-26)
- Initial CCW workflow implementation
- 4-step auto-continue process
- Clear state display with TodoWrite
- Integration with quotation_skill, pptx, and pdf skills
- viAct branding applied
- Text overflow prevention
