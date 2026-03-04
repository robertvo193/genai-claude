# CCW Workflow Plan: Quotation Skill Wrapper

## Goal

Create a CCW workflow that wraps `quotation_skill` to provide:
- **Simple command**: `/quotation generate slide <template.md>`
- **Clear state display**: Show workflow progress during execution
- **No modification to original quotation_skill**

## Current quotation_skill Workflow

```
Verified Proposal Template (markdown)
    ↓
[Step 0] Create Output Directory
    - Create: ./output/[Project]_[Timestamp]/
    ↓
[Step 1] Generate PowerPoint
    - Create HTML slides from template
    - Use pptx skill (html2pptx workflow)
    - Apply viAct branding
    - Output: [Project]_proposal.pptx
    ↓
[Step 2] Generate PDF
    - Use pdf skill (PPTX → PDF)
    - Output: [Project]_proposal.pdf
    ↓
[Complete] Both outputs ready
```

## Proposed CCW Workflow Structure

### File Location
`~/.claude/commands/workflow/quotation/generate-slide.md`

### YAML Frontmatter
```yaml
---
name: quotation-generate-slide
description: Generate PowerPoint and PDF from verified proposal templates with clear workflow state display
argument-hint: "<template.md>"
allowed-tools: SlashCommand(*), TodoWrite(*), Bash(*), Read(*), Write(*)
---
```

### 4-Step Auto-Continue Workflow

```javascript
// Step 0: Initialize TodoWrite (Mandatory)
TodoWrite({
  todos: [
    {content: "Step 1: Create Output Directory", status: "pending", activeForm: "Creating output directory"},
    {content: "Step 2: Generate HTML Slides", status: "pending", activeForm: "Generating HTML slides"},
    {content: "Step 3: Generate PowerPoint", status: "pending", activeForm: "Generating PowerPoint"},
    {content: "Step 4: Generate PDF", status: "pending", activeForm: "Generating PDF"}
  ]
})

// Step 1: Create Output Directory
console.log(`[Step 1/4] Create Output Directory`);
const projectName = path.basename(templatePath, '.md');
const timestamp = bash('date +%Y%m%d_%H%M%S').trim();
const outputDir = `./output/${projectName}_${timestamp}/`;
bash(`mkdir -p "${outputDir}"`);
console.log(`✓ Created: ${outputDir}`);

TodoWrite({ todos: [
  {content: "Step 1: Create Output Directory", status: "completed", activeForm: "Creating output directory"},
  {content: "Step 2: Generate HTML Slides", status: "in_progress", activeForm: "Generating HTML slides"},
  {content: "Step 3: Generate PowerPoint", status: "pending", activeForm: "Generating PowerPoint"},
  {content: "Step 4: Generate PDF", status: "pending", activeForm: "Generating PDF"}
]});

// Step 2: Generate HTML Slides (call quotation_skill)
console.log(`[Step 2/4] Generate HTML Slides`);
// Use quotation_skill to generate HTML
// Output: HTML slides in outputDir/slides/

TodoWrite({ todos: [
  {content: "Step 1: Create Output Directory", status: "completed", activeForm: "Creating output directory"},
  {content: "Step 2: Generate HTML Slides", status: "completed", activeForm: "Generating HTML slides"},
  {content: "Step 3: Generate PowerPoint", status: "in_progress", activeForm: "Generating PowerPoint"},
  {content: "Step 4: Generate PDF", status: "pending", activeForm: "Generating PDF"}
]});

// Step 3: Generate PowerPoint (call pptx skill)
console.log(`[Step 3/4] Generate PowerPoint`);
SlashCommand({ command: "/pptx html2pptx", arguments: [outputDir] });
// Output: project_proposal.pptx

TodoWrite({ todos: [
  {content: "Step 1: Create Output Directory", status: "completed", activeForm: "Creating output directory"},
  {content: "Step 2: Generate HTML Slides", status: "completed", activeForm: "Generating HTML slides"},
  {content: "Step 3: Generate PowerPoint", status: "completed", activeForm: "Generating PowerPoint"},
  {content: "Step 4: Generate PDF", status: "in_progress", activeForm: "Generating PDF"}
]});

// Step 4: Generate PDF (call pdf skill)
console.log(`[Step 4/4] Generate PDF`);
SlashCommand({ command: "/pdf pptx2pdf", arguments: [pptxPath] });
// Output: project_proposal.pdf

TodoWrite({ todos: [
  {content: "Step 1: Create Output Directory", status: "completed", activeForm: "Creating output directory"},
  {content: "Step 2: Generate HTML Slides", status: "completed", activeForm: "Generating HTML slides"},
  {content: "Step 3: Generate PowerPoint", status: "completed", activeForm: "Generating PowerPoint"},
  {content: "Step 4: Generate PDF", status: "completed", activeForm: "Generating PDF"}
]});

// Return summary
console.log(`✅ Slide Generation Complete!`);
console.log(`📁 Output: ${outputDir}`);
console.log(`  • ${projectName}_proposal.pptx`);
console.log(`  • ${projectName}_proposal.pdf`);
```

## Key Features

### 1. Clear State Display
Each step shows:
- `[Step X/4] Step Name`
- Progress indicator
- ✓ Checkmarks for completion
- File paths created

### 2. Auto-Continue Mechanism
- TodoWrite tracks progress
- Automatic progression between steps
- No user interaction needed during execution

### 3. Simple User Command
```bash
/quotation generate slide verified_template.md
```

### 4. Integration with Existing Skills
- Uses `quotation_skill` for HTML generation
- Calls `pptx` skill for PowerPoint
- Calls `pdf` skill for PDF conversion
- **No modification to original quotation_skill**

## Expected Output Example

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
  • verified_template_proposal.pptx
  • verified_template_proposal.pdf
```

## Implementation Notes

### File Structure
```
~/.claude/commands/workflow/quotation/
├── generate-slide.md    ← Main workflow file
└── (no other files needed)
```

### Dependencies
- quotation_skill: `~/.claude/skills/quotation_skill/`
- pptx skill: `~/.claude/skills/pptx/`
- pdf skill: `~/.claude/skills/pdf/`

### Error Handling
- Validate template exists
- Validate template has no placeholders
- Check quotation_skill available
- Check pptx skill available
- Check pdf skill available
- Clear error messages for each failure case

## Testing Plan

After implementation, test with:
1. `DT_cedo_template.md` (from previous template generation)
2. Verify 4 steps show clearly
3. Verify PPTX and PDF generated
4. Verify no modification to quotation_skill

## Next Step

Execute `/workflow:lite-execute` to implement this workflow design.
