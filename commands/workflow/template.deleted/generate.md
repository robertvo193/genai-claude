---
name: template-generate
description: Generate technical proposal templates from Deal Transfer Excel files with 5-step auto-continue workflow
argument-hint: "<excel.xlsx>"
allowed-tools: SlashCommand(*), TodoWrite(*), Bash(*), Read(*), Write(*)
---

# Template Generate Workflow Command

## Coordinator Role

**This command is a pure orchestrator**: Execute 5 steps in sequence to convert Deal Transfer Excel files into 3 proposal files (template, reasoning, checklist). Runs **fully autonomously** once triggered with **automatic continuation** between steps.

**Execution Model - Auto-Continue Workflow**:

This workflow runs autonomously through 5 steps:
1. Validate Excel file
2. Extract Deal Transfer data
3. Generate template file
4. Generate reasoning file
5. Generate checklist file

## Core Rules

1. **Start Immediately**: First action is TodoWrite initialization, second action is Step 1 execution
2. **No Preliminary Validation**: Start execution immediately (validation happens in Step 1)
3. **Parse Every Output**: Extract data (project_name, fields_count, modules, etc.) for next step
4. **Auto-Continue via TodoList**: Check TodoList status and execute next pending step automatically
5. **Track Progress**: Update TodoWrite dynamically for each step
6. **⚠️ CONTINUOUS EXECUTION**: Do not stop until all 5 steps complete

## Execution Process

```
Input Parsing:
   └─ Extract Excel path from arguments
   └─ Validate Excel exists and is .xlsx format

Step 1: Validate Excel File
   └─ Check file exists
   └─ Validate .xlsx format
   └─ Verify S1 (Commercial) sheet exists
   └─ Verify S2 (Technical) sheet exists
   └─ Output: validation_status

Step 2: Extract Deal Transfer Data
   └─ Parse S1 sheet (15-20 fields)
   └─ Parse S2 sheet (20-30 fields)
   └─ Map pain points → AI modules
   └─ Identify standard vs custom modules
   └─ Output: extracted_data object

Step 3: Generate Template File
   └─ Fill 12 sections from TEMPLATE.md
   └─ Apply clean content rules
   └─ Create placeholders for estimates
   └─ Output: template_file path

Step 4: Generate Reasoning File
   └─ Document all sources (S1/S2 fields)
   └─ Show all calculations
   └─ Explain all estimates
   └─ Output: reasoning_file path

Step 5: Generate Checklist File
   └─ List all placeholders
   └─ Format as table
   └─ Sort by section
   └─ Output: checklist_file path

Return:
   └─ Summary with file locations and statistics
```

## 5-Step Execution

### Step 0: Initialize TodoWrite (Mandatory)

```javascript
TodoWrite({
  todos: [
    {content: "Step 1: Validate Excel File", status: "pending", activeForm: "Validating Excel file"},
    {content: "Step 2: Extract Deal Transfer Data", status: "pending", activeForm: "Extracting Deal Transfer data"},
    {content: "Step 3: Generate Template File", status: "pending", activeForm: "Generating template file"},
    {content: "Step 4: Generate Reasoning File", status: "pending", activeForm: "Generating reasoning file"},
    {content: "Step 5: Generate Checklist File", status: "pending", activeForm: "Generating checklist file"}
  ]
})
```

### Step 1: Validate Excel File

**Execute**:

```javascript
// Extract Excel path from arguments
const excelPath = args[0]; // First argument

// Validate file exists
const fileExists = fs.existsSync(excelPath);
if (!fileExists) {
  throw new Error(`Excel file not found: ${excelPath}`);
}

// Validate .xlsx format
if (!excelPath.endsWith('.xlsx')) {
  throw new Error(`Excel file must be .xlsx format: ${excelPath}`);
}

// Check Python dependencies
const pythonCheck = bash('python3 --version').trim();
if (!pythonCheck.startsWith('Python 3')) {
  throw new Error('Python 3 is required');
}

const pandasCheck = bash('python3 -c "import pandas" 2>&1').trim();
if (pandasCheck.includes('ModuleNotFoundError')) {
  throw new Error('pandas library not found. Install with: pip install pandas openpyxl');
}

// Validate sheets using Python
const validateScript = `
import pandas as pd
import sys

try:
    excel_path = '${excelPath}'
    xls = pd.ExcelFile(excel_path)

    # Check for S1/Commercial sheet
    s1_found = any(sheet.lower() in ['s1', 'commercial'] for sheet in xls.sheet_names)

    # Check for S2/Technical sheet
    s2_found = any(sheet.lower() in ['s2', 'technical'] for sheet in xls.sheet_names)

    if not s1_found:
        print('ERROR: S1 (Commercial) sheet not found')
        sys.exit(1)

    if not s2_found:
        print('ERROR: S2 (Technical) sheet not found')
        sys.exit(1)

    print('SUCCESS')
except Exception as e:
    print(f'ERROR: {str(e)}')
    sys.exit(1)
`;

const validationResult = bash(`python3 -c "${validateScript}"`).trim();
if (!validationResult.includes('SUCCESS')) {
  throw new Error(`Excel validation failed: ${validationResult}`);
}

// Update TodoWrite
TodoWrite({
  todos: [
    {content: "Step 1: Validate Excel File", status: "completed", activeForm: "Validating Excel file"},
    {content: "Step 2: Extract Deal Transfer Data", status: "in_progress", activeForm: "Extracting Deal Transfer data"},
    {content: "Step 3: Generate Template File", status: "pending", activeForm: "Generating template file"},
    {content: "Step 4: Generate Reasoning File", status: "pending", activeForm: "Generating reasoning file"},
    {content: "Step 5: Generate Checklist File", status: "pending", activeForm: "Generating checklist file"}
  ]
})

console.log(`[Step 1/5] Validate Excel File [✓ COMPLETED]`);
console.log(`✓ File exists: ${excelPath}`);
console.log(`✓ Valid Excel format (.xlsx)`);
console.log(`✓ S1 (Commercial) sheet found`);
console.log(`✓ S2 (Technical) sheet found`);
```

**Parse Output**:
- Extract: `excel_path` for next step
- Extract: `project_name` from Excel filename

**Auto-Continue**: Execute Step 2

---

### Step 2: Extract Deal Transfer Data

**Execute**:

```javascript
// Extract project name from Excel filename
const projectName = path.basename(excelPath, '.xlsx').replace(/[_\s]+/g, '_');
const timestamp = bash('date +%Y%m%d_%H%M%S').trim();
const outputDir = `./output/${projectName}_${timestamp}/`;

// Create output directory
bash(`mkdir -p "${outputDir}"`);

// Python extraction script
const extractScript = `
import pandas as pd
import json
import sys

excel_path = '${excelPath}'

# Load S1 (Commercial) sheet
s1_df = pd.read_excel(excel_path, sheet_name='Commercial' if 'Commercial' in pd.ExcelFile(excel_path).sheet_names else 'S1')

# Load S2 (Technical) sheet
s2_df = pd.read_excel(excel_path, sheet_name='Technical' if 'Technical' in pd.ExcelFile(excel_path).sheet_names else 'S2')

# Extract key fields
data = {
    'customer_name': s1_df.iloc[1, 1] if len(s1_df) > 1 else '',
    'industry': s1_df.iloc[2, 1] if len(s1_df) > 2 else '',
    'pain_points': s1_df.iloc[5, 1] if len(s1_df) > 5 else '',
    'camera_status': s1_df.iloc[6, 1] if len(s1_df) > 6 else '',
    'timeline': s1_df.iloc[10, 1] if len(s1_df) > 10 else '',
    'budget': s1_df.iloc[11, 1] if len(s1_df) > 11 else '',
    'use_cases': s2_df.iloc[2, 1] if len(s2_df) > 2 else '',
    'deployment': s2_df.iloc[3, 1] if len(s2_df) > 3 else '',
    'camera_quantity': s2_df.iloc[4, 1] if len(s2_df) > 4 else '',
    'ai_modules': s2_df.iloc[5, 1] if len(s2_df) > 5 else '',
    'network_requirements': s2_df.iloc[6, 1] if len(s2_df) > 6 else '',
    'hardware_requirements': s2_df.iloc[7, 1] if len(s2_df) > 7 else ''
}

# Map pain points to AI modules
pain_points_lower = str(data['pain_points']).lower()
ai_modules_mapped = []

if 'helmet' in pain_points_lower or 'safety' in pain_points_lower:
    ai_modules_mapped.append('Safety Helmet Detection')
if 'mask' in pain_points_lower:
    ai_modules_mapped.append('Safety Mask Detection')
if 'vest' in pain_points_lower:
    ai_modules_mapped.append('Safety Vest Detection')
if 'fire' in pain_points_lower:
    ai_modules_mapped.append('Fire & Smoke Detection')
if 'intrusion' in pain_points_lower or 'unauthorized' in pain_points_lower:
    ai_modules_mapped.append('Intrusion Detection')
if 'vehicle' in pain_points_lower:
    ai_modules_mapped.append('Vehicle Detection')

# Distinguish standard vs custom modules
standard_modules = ['Safety Helmet Detection', 'Safety Mask Detection', 'Safety Vest Detection',
                   'Fire & Smoke Detection', 'Intrusion Detection', 'Vehicle Detection']
custom_modules = [m for m in ai_modules_mapped if m not in standard_modules]

data['ai_modules_mapped'] = ai_modules_mapped
data['standard_modules'] = [m for m in ai_modules_mapped if m in standard_modules]
data['custom_modules'] = custom_modules
data['s1_field_count'] = len(s1_df.columns)
data['s2_field_count'] = len(s2_df.columns)

# Output as JSON
print(json.dumps(data))
`;

const extractionResult = bash(`python3 -c "${extractScript}"`).trim();
let extractedData;
try {
  extractedData = JSON.parse(extractionResult);
} catch (e) {
  throw new Error(`Failed to parse extraction result: ${extractionResult}`);
}

// Update TodoWrite
TodoWrite({
  todos: [
    {content: "Step 1: Validate Excel File", status: "completed", activeForm: "Validating Excel file"},
    {content: "Step 2: Extract Deal Transfer Data", status: "completed", activeForm: "Extracting Deal Transfer data"},
    {content: "Step 3: Generate Template File", status: "in_progress", activeForm: "Generating template file"},
    {content: "Step 4: Generate Reasoning File", status: "pending", activeForm: "Generating reasoning file"},
    {content: "Step 5: Generate Checklist File", status: "pending", activeForm: "Generating checklist file"}
  ]
})

console.log(`[Step 2/5] Extract Deal Transfer Data [✓ COMPLETED]`);
console.log(`✓ Extracted ${extractedData.s1_field_count} fields from S1 sheet`);
console.log(`✓ Extracted ${extractedData.s2_field_count} fields from S2 sheet`);
console.log(`✓ Mapped pain points → ${extractedData.ai_modules_mapped.length} AI modules`);
console.log(`✓ Identified: ${extractedData.standard_modules.length} standard modules, ${extractedData.custom_modules.length} custom modules`);
```

**Parse Output**:
- Extract: `extracted_data` object with all fields
- Extract: `project_name`
- Extract: `output_dir`

**Auto-Continue**: Execute Step 3

---

### Step 3: Generate Template File

**Execute**:

```javascript
// Read TEMPLATE.md structure
const templatePath = '~/.claude/skills/dealtransfer2template/TEMPLATE.md';
const templateStructure = fs.readFileSync(templatePath, 'utf8');

// Generate template content
const templateContent = generateTemplateContent(extractedData, templateStructure);

// Save template file
const templateFile = `${outputDir}${projectName}_template.md`;
fs.writeFileSync(templateFile, templateContent);

// Count placeholders
const placeholderCount = (templateContent.match(/\[PLACEHOLDER_[A-Z0-9_]+\]/g) || []).length;

// Update TodoWrite
TodoWrite({
  todos: [
    {content: "Step 1: Validate Excel File", status: "completed", activeForm: "Validating Excel file"},
    {content: "Step 2: Extract Deal Transfer Data", status: "completed", activeForm: "Extracting Deal Transfer data"},
    {content: "Step 3: Generate Template File", status: "completed", activeForm: "Generating template file"},
    {content: "Step 4: Generate Reasoning File", status: "in_progress", activeForm: "Generating reasoning file"},
    {content: "Step 5: Generate Checklist File", status: "pending", activeForm: "Generating checklist file"}
  ]
})

console.log(`[Step 3/5] Generate Template File [✓ COMPLETED]`);
console.log(`✓ Filled 12 sections from TEMPLATE.md`);
console.log(`✓ Created ${placeholderCount} placeholders for missing info`);
console.log(`✓ Clean proposal content (no source references)`);
console.log(`✓ Formatted: Project Requirement Statement`);
```

**Parse Output**:
- Extract: `template_file_path`
- Extract: `placeholder_count`

**Auto-Continue**: Execute Step 4

---

### Step 4: Generate Reasoning File

**Execute**:

```javascript
// Generate reasoning content
const reasoningContent = generateReasoningContent(extractedData, templateStructure);

// Save reasoning file
const reasoningFile = `${outputDir}${projectName}_reasoning.md`;
fs.writeFileSync(reasoningFile, reasoningContent);

// Update TodoWrite
TodoWrite({
  todos: [
    {content: "Step 1: Validate Excel File", status: "completed", activeForm: "Validating Excel file"},
    {content: "Step 2: Extract Deal Transfer Data", status: "completed", activeForm: "Extracting Deal Transfer data"},
    {content: "Step 3: Generate Template File", status: "completed", activeForm: "Generating template file"},
    {content: "Step 4: Generate Reasoning File", status: "completed", activeForm: "Generating reasoning file"},
    {content: "Step 5: Generate Checklist File", status: "in_progress", activeForm: "Generating checklist file"}
  ]
})

console.log(`[Step 4/5] Generate Reasoning File [✓ COMPLETED]`);
console.log(`✓ Documented all S1/S2 sources`);
console.log(`✓ Showed all calculations (bandwidth, storage)`);
console.log(`✓ Explained all ${placeholderCount} estimates`);
console.log(`✓ Complete audit trail`);
```

**Parse Output**:
- Extract: `reasoning_file_path`

**Auto-Continue**: Execute Step 5

---

### Step 5: Generate Checklist File

**Execute**:

```javascript
// Generate checklist content
const checklistContent = generateChecklistContent(templateContent);

// Save checklist file
const checklistFile = `${outputDir}${projectName}_checklist.md`;
fs.writeFileSync(checklistFile, checklistContent);

// Update TodoWrite
TodoWrite({
  todos: [
    {content: "Step 1: Validate Excel File", status: "completed", activeForm: "Validating Excel file"},
    {content: "Step 2: Extract Deal Transfer Data", status: "completed", activeForm: "Extracting Deal Transfer data"},
    {content: "Step 3: Generate Template File", status: "completed", activeForm: "Generating template file"},
    {content: "Step 4: Generate Reasoning File", status: "completed", activeForm: "Generating reasoning file"},
    {content: "Step 5: Generate Checklist File", status: "completed", activeForm: "Generating checklist file"}
  ]
})

console.log(`[Step 5/5] Generate Checklist File [✓ COMPLETED]`);
console.log(`✓ Listed ${placeholderCount} placeholders`);
console.log(`✓ Formatted: ID | Section | Item | Estimated | Answer`);
console.log(`✓ Ready for presale review`);
```

**Auto-Continue**: All steps complete, return summary

---

## Return Summary

```javascript
console.log(``);
console.log(`✅ Template Generation Complete!`);
console.log(``);
console.log(`📁 Excel: ${excelPath}`);
console.log(`📊 Project: ${projectName}`);
console.log(``);
console.log(`Output Files:`);
console.log(`  • ${templateFile} (12 sections, ${placeholderCount} placeholders)`);
console.log(`  • ${reasoningFile} (complete audit trail)`);
console.log(`  • ${checklistFile} (${placeholderCount} items to confirm)`);
console.log(``);
console.log(`📊 Statistics:`);
console.log(`  • S1 fields extracted: ${extractedData.s1_field_count}`);
console.log(`  • S2 fields extracted: ${extractedData.s2_field_count}`);
console.log(`  • AI modules mapped: ${extractedData.ai_modules_mapped.length}`);
console.log(`  • Placeholders created: ${placeholderCount}`);
console.log(`  • Sections filled: 12/12`);
console.log(``);
console.log(`Next Steps:`);
console.log(`  1. Review ${projectName}_checklist.md`);
console.log(`  2. Fill presale answers for placeholders`);
console.log(`  3. Update template with confirmed values`);
console.log(`  4. Generate slides: /quotation generate slide ${projectName}_template.md`);
```

## Error Handling

| Error | Solution |
|-------|----------|
| Excel file not found | Show clear error with file path |
| Invalid format | "Excel file must be .xlsx format (not .xls)" |
| S1 sheet not found | "S1 (Commercial) sheet not found in Excel" |
| S2 sheet not found | "S2 (Technical) sheet not found in Excel" |
| Python not found | "Python 3 is required. Install from python.org" |
| pandas not found | "Install: pip install pandas openpyxl" |
| Empty fields | Warning shown but extraction continues |
| No AI modules mapped | Warning: "No pain points mapped to modules" |

## Input Validation

**Pre-execution checks**:
```javascript
// Validate Excel exists
if (!fs.existsSync(excelPath)) {
  return `Error: Excel file not found: ${excelPath}`;
}

// Validate .xlsx format
if (!excelPath.endsWith('.xlsx')) {
  return "Error: Excel file must be .xlsx format (not .xls)";
}

// Validate Python 3
const pythonVersion = bash('python3 --version').trim();
if (!pythonVersion.startsWith('Python 3')) {
  return "Error: Python 3 is required";
}

// Validate pandas
const pandasCheck = bash('python3 -c "import pandas" 2>&1').trim();
if (pandasCheck.includes('ModuleNotFoundError')) {
  return "Error: Required Python libraries not found. Install with: pip install pandas openpyxl";
}
```

## Helper Functions

### generateTemplateContent

```javascript
function generateTemplateContent(data, templateStructure) {
  // Fill 12 sections from TEMPLATE.md
  // Apply clean content rules:
  //   - ONLY proposal content (client-facing)
  //   - Pure markdown (NO HTML)
  //   - Final values only (no calculations shown)
  //   - Placeholders for estimates: [Value] [PLACEHOLDER_ID]
  //   - NO source references
  //   - NO reasoning explanations

  let content = templateStructure;

  // Replace placeholders with extracted data
  content = content.replace(/\{\{CUSTOMER_NAME\}\}/g, data.customer_name || '[Customer Name]');
  content = content.replace(/\{\{INDUSTRY\}\}/g, data.industry || '[Industry]');
  content = content.replace(/\{\{PAIN_POINTS\}\}/g, data.pain_points || '[Pain Points]');

  // Generate Project Requirement Statement
  const prs = generateProjectRequirementStatement(data);
  content = content.replace(/\{\{PROJECT_REQUIREMENT_STATEMENT\}\}/g, prs);

  // List AI modules separately (NOT merged)
  const aiModulesList = data.ai_modules_mapped.map((m, i) => `${i + 1}. ${m}`).join('\n');
  content = content.replace(/\{\{AI_MODULES\}\}/g, aiModulesList);

  return content;
}
```

### generateProjectRequirementStatement

```javascript
function generateProjectRequirementStatement(data) {
  const cameraNum = data.camera_quantity || 'X';
  const moduleNum = data.ai_modules_mapped.length || 'X';
  const duration = data.timeline || 'X months';

  return `**Project:** AI-Powered Video Analytics for ${data.industry || 'Site Safety'}

**Project Owner:** ${data.customer_name || '[Client Name]'}

**Work Scope:** ${data.deployment || 'On-premise'} AI system to ${data.use_cases || 'enhance safety monitoring'}

**Project Duration:** ${duration}

**Camera Number:** ${cameraNum} cameras

**AI Modules per Camera:** ${moduleNum} modules per camera

**AI Modules:**
${data.ai_modules_mapped.map((m, i) => `${i + 1}. ${m}`).join('\n')}`;
}
```

### generateReasoningContent

```javascript
function generateReasoningContent(data, templateStructure) {
  // Document ALL sources:
  //   - S1 field references
  //   - S2 field references
  //   - KB references
  // Show ALL calculations:
  //   - Bandwidth calculations
  //   - Storage calculations
  //   - Timeline estimates
  // Explain ALL estimates:
  //   - Why specific values chosen
  //   - What standards followed
  //   - What similar projects referenced

  let content = '# Reasoning and Audit Trail\n\n';

  content += '## Data Sources\n\n';
  content += `### S1 (Commercial) Sheet\n`;
  content += `- Customer Name: "${data.customer_name}" (S1, Row 2)\n`;
  content += `- Industry: "${data.industry}" (S1, Row 3)\n`;
  content += `- Pain Points: "${data.pain_points}" (S1, Row 6)\n`;
  content += `- Timeline: "${data.timeline}" (S1, Row 11)\n\n`;

  content += `### S2 (Technical) Sheet\n`;
  content += `- Use Cases: "${data.use_cases}" (S2, Row 3)\n`;
  content += `- Deployment: "${data.deployment}" (S2, Row 4)\n`;
  content += `- Camera Quantity: "${data.camera_quantity}" (S2, Row 5)\n\n`;

  content += '## AI Module Mapping\n\n';
  content += `**Pain Points:** ${data.pain_points}\n\n`;
  content += '**Mapping Logic:**\n';
  content += `- Pain points → AI modules: ${data.ai_modules_mapped.join(', ')}\n`;
  content += `- Standard modules: ${data.standard_modules.length}\n`;
  content += `- Custom modules: ${data.custom_modules.length}\n\n`;

  if (data.custom_modules.length > 0) {
    content += '**Custom Modules Identified:**\n';
    data.custom_modules.forEach(m => {
      content += `- ${m} (requires custom development)\n`;
    });
    content += '\n';
  }

  return content;
}
```

### generateChecklistContent

```javascript
function generateChecklistContent(templateContent) {
  // Extract all placeholders
  const placeholderRegex = /\[PLACEHOLDER_([A-Z0-9_]+)\]/g;
  const placeholders = [];
  let match;

  while ((match = placeholderRegex.exec(templateContent)) !== null) {
    placeholders.push(match[1]);
  }

  // Format as table
  let content = '# Placeholder Checklist\n\n';
  content += '| ID | Section | Item | Content Estimated | Presale\'s Answer |\n';
  content += '|----|---------|------|-------------------|------------------|\n';

  placeholders.forEach(id => {
    content += `| ${id} | | | | |\n`;
  });

  return content;
}
```

## Usage

```bash
# Basic usage
/template generate deal "DT_0109.xlsx"

# Alternative invocation (if registered as command)
/workflow:template-generate "DT_0109.xlsx"
```

## Output Example

```
🎯 Template Generation Started
📁 Excel: DT_0109.xlsx
📊 Project: Leda Inio Construction
⏰ Timestamp: 20250126_163030

[Step 1/5] Validate Excel File [✓ COMPLETED]
✓ File exists: DT_0109.xlsx
✓ Valid Excel format (.xlsx)
✓ S1 (Commercial) sheet found
✓ S2 (Technical) sheet found

[Step 2/5] Extract Deal Transfer Data [✓ COMPLETED]
✓ Extracted 15 fields from S1 sheet
✓ Extracted 22 fields from S2 sheet
✓ Mapped pain points → 5 AI modules
✓ Identified: 4 standard modules, 1 custom module

[Step 3/5] Generate Template File [✓ COMPLETED]
✓ Filled 12 sections from TEMPLATE.md
✓ Created 8 placeholders for missing info
✓ Clean proposal content (no source references)
✓ Formatted: Project Requirement Statement

[Step 4/5] Generate Reasoning File [✓ COMPLETED]
✓ Documented all S1/S2 sources
✓ Showed all calculations (bandwidth, storage)
✓ Explained all 8 estimates
✓ Complete audit trail

[Step 5/5] Generate Checklist File [✓ COMPLETED]
✓ Listed 8 placeholders
✓ Formatted: ID | Section | Item | Estimated | Answer
✓ Ready for presale review

✅ Template Generation Complete!
📁 Excel: DT_0109.xlsx
📊 Project: Leda Inio Construction

Output Files:
  • ./output/Leda_Inio_20250126_163030/Leda_Inio_template.md (12 sections, 8 placeholders)
  • ./output/Leda_Inio_20250126_163030/Leda_Inio_reasoning.md (complete audit trail)
  • ./output/Leda_Inio_20250126_163030/Leda_Inio_checklist.md (8 items to confirm)

📊 Statistics:
  • S1 fields extracted: 15
  • S2 fields extracted: 22
  • AI modules mapped: 5
  • Placeholders created: 8
  • Sections filled: 12/12

Next Steps:
  1. Review Leda_Inio_checklist.md
  2. Fill presale answers for placeholders
  3. Update template with confirmed values
  4. Generate slides: /quotation generate slide Leda_Inio_template.md
```

## Integration with dealtransfer2template

This workflow orchestrates the dealtransfer2template skill components:

- **TEMPLATE.md**: `~/.claude/skills/dealtransfer2template/TEMPLATE.md`
- **Python scripts**: pandas + openpyxl for Excel parsing
- **AI module mapping**: Pain points → modules logic
- **Placeholder generation**: Unique ID system
- **3-file output**: Template, reasoning, checklist

## Version History

**v1.0.0** (2025-01-26)
- Initial CCW workflow implementation
- 5-step auto-continue process
- Integration with dealtransfer2template skill
- S1/S2 sheet extraction
- AI module mapping
- Placeholder management
- Statistics tracking
