---
name: quotation-generate
description: Generate PowerPoint and PDF from verified proposal templates with 4-step auto-continue workflow
argument-hint: "<template.md>"
allowed-tools: SlashCommand(*), TodoWrite(*), Bash(*), Read(*), Write(*)
---

# Quotation Generate Workflow Command

## Coordinator Role

**This command is a pure orchestrator**: Execute 4 steps in sequence to convert verified proposal templates into PowerPoint presentations and PDF documents. Runs **fully autonomously** once triggered with **automatic continuation** between steps.

**Execution Model - Auto-Continue Workflow**:

This workflow runs autonomously through 4 steps:
1. Create output directory
2. Generate HTML slides
3. Generate PowerPoint
4. Generate PDF

## Core Rules

1. **Start Immediately**: First action is TodoWrite initialization, second action is Step 1 execution
2. **No Preliminary Validation**: Start execution immediately (validation happens in Step 1)
3. **Parse Every Output**: Extract data (output_dir, slide_count, etc.) for next step
4. **Auto-Continue via TodoList**: Check TodoList status and execute next pending step automatically
5. **Track Progress**: Update TodoWrite dynamically for each step
6. **⚠️ CONTINUOUS EXECUTION**: Do not stop until all 4 steps complete

## Execution Process

```
Input Parsing:
   └─ Extract template path from arguments
   └─ Validate template exists and is .md format

Step 1: Create Output Directory
   └─ Create: ./output/[Project]_[Timestamp]/
   └─ Create: slides/ subdirectory
   └─ Output: output_dir path

Step 2: Generate HTML Slides
   └─ Parse template (12 sections)
   └─ Generate HTML files (using SLIDE_TEMPLATES.md)
   └─ Apply viAct branding
   └─ Generate architecture diagram (if needed)
   └─ Output: slides_dir path + slide_count

Step 3: Generate PowerPoint
   └─ Use pptx skill (html2pptx workflow)
   └─ Convert HTML → PowerPoint
   └─ Output: pptx_file path

Step 4: Generate PDF
   └─ Use pdf skill (LibreOffice)
   └─ Convert PPTX → PDF
   └─ Output: pdf_file path

Return:
   └─ Summary with file locations and completion status
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
// Extract project name from template path
const templatePath = args[0]; // First argument
const projectName = path.basename(templatePath, '.md').replace(/[_\s]+/g, '_');
const timestamp = bash('date +%Y%m%d_%H%M%S').trim();
const outputDir = `./output/${projectName}_${timestamp}/`;
const slidesDir = `${outputDir}slides/`;

// Create directories
bash(`mkdir -p "${slidesDir}"`);

// Validate creation
const success = bash(`test -d "${outputDir}" && echo "SUCCESS" || echo "FAILED"`).trim() === "SUCCESS";
if (!success) {
  throw new Error(`Failed to create output directory: ${outputDir}`);
}

// Update TodoWrite
TodoWrite({
  todos: [
    {content: "Step 1: Create Output Directory", status: "completed", activeForm: "Creating output directory"},
    {content: "Step 2: Generate HTML Slides", status: "in_progress", activeForm: "Generating HTML slides"},
    {content: "Step 3: Generate PowerPoint", status: "pending", activeForm: "Generating PowerPoint"},
    {content: "Step 4: Generate PDF", status": "pending", activeForm: "Generating PDF"}
  ]
})

console.log(`[Step 1/4] Create Output Directory [✓ COMPLETED]`);
console.log(`✓ Created: ${outputDir}`);
console.log(`✓ Created: slides/ subdirectory`);
```

**Parse Output**:
- Extract: `output_dir` path for next step

**Auto-Continue**: Execute Step 2

---

### Step 2: Generate HTML Slides

**Execute**:

```javascript
// Read template
const templatePath = args[0];
const templateContent = fs.readFileSync(templatePath, 'utf8');

// Read SLIDE_TEMPLATES.md
const slideTemplatesPath = '~/.claude/skills/quotation_skill/SLIDE_TEMPLATES.md';
const slideTemplates = fs.readFileSync(slideTemplatesPath, 'utf8');

// Parse template sections (12 sections)
const sections = parseTemplateSections(templateContent);

// Generate HTML slides
const htmlSlides = [];
sections.forEach((section, index) => {
  const slideNumber = String(index + 1).padStart(2, '0');
  const slideFileName = `slide${slideNumber}_${section.slug}.html`;

  // Select template based on section type
  const template = selectTemplate(section.type);

  // Generate HTML with viAct branding
  const html = generateHTML(section, template);

  // Save to slides directory
  const slidePath = `${slidesDir}${slideFileName}`;
  fs.writeFileSync(slidePath, html);

  htmlSlides.push(slideFileName);
});

// Generate architecture diagram if needed
if (sections.find(s => s.title === 'SYSTEM ARCHITECTURE')) {
  const scriptPath = '~/.claude/skills/quotation_skill/scripts/generate_architecture_diagram.py';
  bash(`cd ~/.claude/skills/quotation_skill && python scripts/generate_architecture_diagram.py`);
  bash(`mmdc -i architecture.mmd -o architecture.png -b transparent -t dark`);
}

// Update TodoWrite
TodoWrite({
  todos: [
    {content: "Step 1: Create Output Directory", status: "completed", activeForm: "Creating output directory"},
    {content: "Step 2: Generate HTML Slides", status: "completed", activeForm: "Generating HTML slides"},
    {content: "Step 3: Generate PowerPoint", status: "in_progress", activeForm: "Generating PowerPoint"},
    {content: "Step 4: Generate PDF", status": "pending", activeForm: "Generating PDF"}
  ]
})

console.log(`[Step 2/4] Generate HTML Slides [✓ COMPLETED]`);
console.log(`✓ Parsed ${sections.length} sections from template`);
console.log(`✓ Generated ${htmlSlides.length} HTML slides`);
console.log(`✓ Applied viAct branding`);
console.log(`✓ Generated architecture diagram`);
```

**Parse Output**:
- Extract: `slides_dir` path
- Extract: `slide_count` for summary

**Auto-Continue**: Execute Step 3

---

### Step 3: Generate PowerPoint

**Execute**:

```javascript
// Use pptx skill (html2pptx workflow)
const pptxSkillPath = '~/.claude/skills/pptx/';
const pptxOutputPath = `${outputDir}${projectName}_proposal.pptx`;

// Create Node.js script for conversion
const convertScript = `
const html2pptx = require('${pptxSkillPath}/scripts/html2pptx.js');
const pptxgenjs = require('pptxgenjs');
const path = require('path');
const fs = require('fs');

const slidesDir = path.resolve('${slidesDir}');
const outputFile = path.resolve('${pptxOutputPath}');

const htmlFiles = fs.readdirSync(slidesDir)
  .filter(f => f.endsWith('.html'))
  .sort()
  .map(f => path.join(slidesDir, f));

(async () => {
  try {
    const pptx = new pptxgenjs();
    pptx.layout = 'LAYOUT_16x9';

    for (const htmlFile of htmlFiles) {
      await html2pptx(htmlFile, pptx);
    }

    await pptx.writeFile({ fileName: outputFile });
    console.log('SUCCESS');
  } catch (error) {
    console.error('FAILED:', error.message);
    process.exit(1);
  }
})();
`;

// Save and run script
const scriptFile = `${outputDir}convert.js`;
fs.writeFileSync(scriptFile, convertScript);
bash(`cd ${pptxSkillPath} && node ${scriptFile}`);

// Validate output
const pptxExists = fs.existsSync(pptxOutputPath);
if (!pptxExists) {
  throw new Error(`PowerPoint generation failed: ${pptxOutputPath} not found`);
}

// Update TodoWrite
TodoWrite({
  todos: [
    {content: "Step 1: Create Output Directory", status: "completed", activeForm: "Creating output directory"},
    {content: "Step 2: Generate HTML Slides", status": "completed", activeForm: "Generating HTML slides"},
    {content: "Step 3: Generate PowerPoint", status: "completed", activeForm: "Generating PowerPoint"},
    {content: "Step 4: Generate PDF", status: "in_progress", activeForm: "Generating PDF"}
  ]
})

console.log(`[Step 3/4] Generate PowerPoint [✓ COMPLETED]`);
console.log(`✓ Converting HTML to PowerPoint...`);
console.log(`✓ Created: ${projectName}_proposal.pptx (${htmlSlides.length} slides)`);
```

**Parse Output**:
- Extract: `pptx_file_path` for next step

**Auto-Continue**: Execute Step 4

---

### Step 4: Generate PDF

**Execute**:

```javascript
// Use pdf skill (LibreOffice conversion)
const pdfOutputPath = `${outputDir}${projectName}_proposal.pdf`;

// Run LibreOffice conversion
bash(`libreoffice --headless --convert-to pdf --outdir "${outputDir}" "${pptxOutputPath}"`);

// Validate output
const pdfExists = fs.existsSync(pdfOutputPath);
if (!pdfExists) {
  throw new Error(`PDF generation failed: ${pdfOutputPath} not found`);
}

// Update TodoWrite
TodoWrite({
  todos: [
    {content: "Step 1: Create Output Directory", status": "completed", activeForm: "Creating output directory"},
    {content: "Step 2: Generate HTML Slides", status": "completed", activeForm: "Generating HTML slides"},
    {content: "Step 3: Generate PowerPoint", status": "completed", activeForm: "Generating PowerPoint"},
    {content: "Step 4: Generate PDF", status": "completed", activeForm": "Generating PDF"}
  ]
})

console.log(`[Step 4/4] Generate PDF [✓ COMPLETED]`);
console.log(`✓ Converting PowerPoint to PDF...`);
console.log(`✓ Created: ${projectName}_proposal.pdf (${htmlSlides.length} pages)`);
```

**Auto-Continue**: All steps complete, return summary

---

## Return Summary

```javascript
console.log(``);
console.log(`✅ Quotation Generation Complete!`);
console.log(``);
console.log(`📁 Template: ${templatePath}`);
console.log(`📊 Project: ${projectName}`);
console.log(``);
console.log(`Output Files:`);
console.log(`  • ${pptxOutputPath} (${htmlSlides.length} slides)`);
console.log(`  • ${pdfOutputPath} (${htmlSlides.length} pages)`);
console.log(``);
console.log(`📂 All files in: ${outputDir}`);
console.log(`  └── slides/ (${htmlSlides.length} HTML source files)`);
```

## Error Handling

| Error | Solution |
|-------|----------|
| Template not found | Show clear error with file path |
| Template not .md | "Template must be markdown (.md) format" |
| Has placeholders | "Template must be verified first (no [PLACEHOLDER_ID])" |
| pptx skill not found | "Install pptx skill: ~/.claude/skills/pptx/" |
| LibreOffice not found | "Install LibreOffice: sudo apt install libreoffice" |
| HTML text overflow | "Use two-column layout (Template 3) or split into 2 slides" |
| Background not showing | "Background MUST use absolute file:// URL" |

## Input Validation

**Pre-execution checks**:
```javascript
// Validate template exists
if (!fs.existsSync(templatePath)) {
  return `Error: Template file not found: ${templatePath}`;
}

// Validate markdown format
if (!templatePath.endsWith('.md')) {
  return "Error: Template must be markdown (.md) format";
}

// Validate no placeholders
const templateContent = fs.readFileSync(templatePath, 'utf8');
const hasPlaceholders = /\[PLACEHOLDER_[A-Z0-9_+\]/.test(templateContent);
if (hasPlaceholders) {
  return "Error: Template contains placeholders. Template must be verified first.";
}
```

## Helper Functions

### parseTemplateSections

```javascript
function parseTemplateSections(templateContent) {
  const sections = [];
  const sectionRegex = /^##\s+(\d+)\.\s+(.+)$/gm;
  let match;

  while ((match = sectionRegex.exec(templateContent)) !== null) {
    sections.push({
      number: parseInt(match[1]),
      title: match[2].trim(),
      content: extractSectionContent(templateContent, match[2]),
      type: determineSectionType(match[2])
    });
  }

  return sections;
}
```

### selectTemplate

```javascript
function selectTemplate(sectionType) {
  const templateMap = {
    'cover': 'Template 1',
    'content': 'Template 2',
    'two-column': 'Template 3',
    'ai-module': 'Template 5',
    'timeline': 'Template 6'
  };

  return templateMap[sectionType] || 'Template 2';
}
```

### generateHTML

```javascript
function generateHTML(section, template) {
  // Load template from SLIDE_TEMPLATES.md
  // Replace placeholders with section content
  // Apply viAct branding
  // Ensure correct margins (0 120pt 85pt 40pt)
  // Return complete HTML
}
```

## Usage

```bash
# Basic usage
/workflow:quotation-generate "Leda_Inio_template.md"

# Alternative invocation (if registered as command)
/quotation-generate "Leda_Inio_template.md"
```

## Output Example

```
🎯 Quotation Generation Started
📁 Template: Leda_Inio_template.md
📊 Project: Leda_Inio

[Step 1/4] Create Output Directory [🔄 IN PROGRESS]
✓ Created: ./output/Leda_Inio_20250126_163030/
✓ Created: slides/ subdirectory

[Step 2/4] Generate HTML Slides [🔄 IN PROGRESS]
✓ Parsed 12 sections from template
✓ Generated 15 HTML slides
✓ Applied viAct branding
✓ Generated architecture diagram

[Step 3/4] Generate PowerPoint [🔄 IN PROGRESS]
✓ Converting HTML to PowerPoint...
✓ Created: Leda_Inio_proposal.pptx (15 slides)

[Step 4/4] Generate PDF [🔄 IN PROGRESS]
✓ Converting PowerPoint to PDF...
✓ Created: Leda_Inio_proposal.pdf (15 pages)

✅ Quotation Generation Complete!
📁 Template: Leda_Inio_template.md
📊 Project: Leda_Inio

Output Files:
  • ./output/Leda_Inio_20250126_163030/Leda_Inio_proposal.pptx (15 slides)
  • ./output/Leda_Inio_20250126_163030/Leda_Inio_proposal.pdf (15 pages)

📂 All files in: ./output/Leda_Inio_20250126_163030/
  └── slides/ (15 HTML source files)
```

## Integration with quotation_skill

This workflow orchestrates the quotation_skill components:

- **SLIDE_TEMPLATES.md**: `~/.claude/skills/quotation_skill/SLIDE_TEMPLATES.md`
- **Background image**: `~/.claude/skills/quotation_skill/assets/background.png`
- **Diagram generator**: `~/.claude/skills/quotation_skill/scripts/generate_architecture_diagram.py`
- **pptx skill**: `~/.claude/skills/pptx/`
- **pdf skill**: LibreOffice (system tool)

## Version History

**v1.0.0** (2025-01-26)
- Initial CCW workflow implementation
- 4-step auto-continue process
- Integration with quotation_skill
- viAct branding applied
- Architecture diagram generation
- Text overflow prevention
