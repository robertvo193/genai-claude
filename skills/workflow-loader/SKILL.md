---
name: workflow
description: Execute CCW workflows from ~/.claude/commands/workflow/ directory with TodoWrite progress tracking and auto-continue
---

# Workflow Loader Skill

**Load and execute CCW workflows with clear progress display**

## Overview

This skill loads CCW workflow definitions from `~/.claude/commands/workflow/` and executes them with:
- TodoWrite progress tracking
- Auto-continue between steps
- Clear state display
- Error handling

## Usage

### Basic Syntax

```bash
/workflow:<workflow-name> <arguments>
```

### Examples

```bash
# Generate slides from template
/workflow:quotation-generate-slide Leda_Inio_template.md

# Generate template from Excel
/workflow:template-generate DT_cedo.xlsx

# List available workflows
/workflow:list
```

## How It Works

### Execution Flow

```
User Command: /workflow:quotation-generate-slide template.md
    ↓
[Step 1] Load Workflow Definition
    - Read: ~/.claude/commands/workflow/quotation/generate-slide.md
    - Parse YAML frontmatter
    - Extract workflow steps
    ↓
[Step 2] Initialize TodoWrite
    - Create task list from workflow steps
    - Display initial progress
    ↓
[Step 3] Execute Workflow Steps
    - For each step:
        • Mark as "in_progress"
        • Execute step logic
        • Mark as "completed"
        • Auto-continue to next step
    ↓
[Step 4] Return Results
    - Display final summary
    - Show output files
    - Report statistics
```

## Supported Workflows

### Quotation Workflows

| Workflow | Command | Purpose |
|----------|---------|---------|
| **quotation-generate-slide** | `/workflow:quotation-generate-slide <template.md>` | Generate PowerPoint + PDF from template |
| **quotation-generate** | `/workflow:quotation-generate <template.md>` | Alias for quotation-generate-slide |

### Template Workflows

| Workflow | Command | Purpose |
|----------|---------|---------|
| **template-generate** | `/workflow:template-generate <excel.xlsx>` | Generate template from Excel |
| **template-generate-deal** | `/workflow:template-generate-deal <excel.xlsx>` | Alias for template-generate |

## Workflow Definition Format

CCW workflow files use this format:

```yaml
---
name: workflow-name
description: Workflow description
argument-hint: "<argument-format>"
allowed-tools: SlashCommand(*), TodoWrite(*), Bash(*), Read(*), Write(*)
---

# Workflow Content

## Coordinator Role

**This command is a pure orchestrator**: Execute N steps in sequence...

## Core Rules

1. **Start Immediately**: First action is TodoWrite initialization
2. **No Preliminary Validation**: Start execution immediately
3. **Parse Every Output**: Extract data for next step
4. **Auto-Continue via TodoList**: Check TodoList status and execute next pending step
5. **Track Progress**: Update TodoWrite dynamically
6. **⚠️ CONTINUOUS EXECUTION**: Do not stop until all steps complete

## Execution Process

```
Step descriptions...
```

## N-Step Execution

### Step 0: Initialize TodoWrite (Mandatory)

### Step 1: First Step

**Execute**:

```javascript
<execution logic>
```

**Parse Output**:
- Extract: data for next step

**Auto-Continue**: Execute Step 2

...

## Return Summary

<output format>
```

## Progress Display

### TodoWrite Format

```javascript
TodoWrite({
  todos: [
    {content: "Step 1: Step Name", status: "completed", activeForm: "Executing step 1"},
    {content: "Step 2: Step Name", status: "in_progress", activeForm: "Executing step 2"},
    {content: "Step 3: Step Name", status: "pending", activeForm: "Executing step 3"}
  ]
})
```

### Console Output

```
[Step 1/4] Step Name [✓ COMPLETED]
✓ Result 1
✓ Result 2

[Step 2/4] Step Name [✓ COMPLETED]
✓ Result 3
```

## Error Handling

| Error Type | Handling |
|------------|----------|
| **Workflow not found** | Show error + list available workflows |
| **Invalid arguments** | Show usage + argument hint |
| **Step execution failed** | Show error + suggest fix |
| **File not found** | Show error + check current directory |

## Implementation Details

### Workflow Discovery

```python
def discover_workflows():
    """Scan ~/.claude/commands/workflow/ for workflow definitions"""
    workflow_dir = Path.home() / '.claude' / 'commands' / 'workflow'
    workflows = []

    for workflow_file in workflow_dir.rglob('*.md'):
        # Parse YAML frontmatter
        with open(workflow_file) as f:
            content = f.read()

        # Extract metadata
        yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            name = extract_yaml_field(yaml_content, 'name')
            description = extract_yaml_field(yaml_content, 'description')
            argument_hint = extract_yaml_field(yaml_content, 'argument-hint')

            workflows.append({
                'name': name,
                'description': description,
                'argument_hint': argument_hint,
                'file': workflow_file
            })

    return workflows
```

### Workflow Execution

```python
def execute_workflow(workflow_name, args):
    """Execute workflow with TodoWrite progress"""
    # 1. Load workflow definition
    workflow_file, content = load_workflow(workflow_name)

    # 2. Parse workflow steps
    steps = parse_workflow_steps(content)

    # 3. Initialize TodoWrite
    initialize_todowrite(steps)

    # 4. Execute each step
    for i, step in enumerate(steps):
        # Update status to in_progress
        update_step_status(i, 'in_progress')

        # Execute step logic
        result = execute_step(step, args)

        # Update status to completed
        update_step_status(i, 'completed')

        # Auto-continue to next step
        if i < len(steps) - 1:
            continue_to_next_step()

    # 5. Return results
    display_final_summary()
```

## Requirements

- CCW workflow definitions in `~/.claude/commands/workflow/`
- YAML frontmatter in each workflow file
- TodoWrite tool support
- SlashCommand tool support
- Bash, Read, Write tools

## Version History

**v1.0.0** (2025-01-26)
- Initial workflow loader implementation
- TodoWrite progress tracking
- Auto-continue mechanism
- Error handling
- Workflow discovery
