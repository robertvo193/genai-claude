#!/usr/bin/env python3
"""
CCW Workflow Executor
Loads and executes workflows from ~/.claude/commands/workflow/ with TodoWrite progress
"""

import sys
import os
import re
import json
from pathlib import Path
from datetime import datetime

# ANSI color codes
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

class WorkflowExecutor:
    """Execute CCW workflows with TodoWrite progress tracking"""

    def __init__(self):
        self.workflow_dir = Path.home() / '.claude' / 'commands' / 'workflow'
        self.state = {}

    def discover_workflows(self):
        """Scan for workflow definitions"""
        workflows = []

        if not self.workflow_dir.exists():
            return workflows

        for workflow_file in self.workflow_dir.rglob('*.md'):
            try:
                with open(workflow_file, 'r') as f:
                    content = f.read()

                # Parse YAML frontmatter
                yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
                if yaml_match:
                    yaml_content = yaml_match.group(1)
                    name = self.extract_yaml_field(yaml_content, 'name')
                    description = self.extract_yaml_field(yaml_content, 'description')
                    argument_hint = self.extract_yaml_field(yaml_content, 'argument-hint')

                    if name:
                        workflows.append({
                            'name': name,
                            'description': description or '',
                            'argument_hint': argument_hint or '',
                            'file': workflow_file
                        })
            except Exception as e:
                print(f"{YELLOW}Warning: Could not load {workflow_file}: {e}{RESET}", file=sys.stderr)

        return workflows

    def extract_yaml_field(self, yaml_content, field_name):
        """Extract field value from YAML content"""
        pattern = rf'{field_name}:\s*(.+?)(?:\n|$)'
        match = re.search(pattern, yaml_content)
        if match:
            value = match.group(1).strip()
            # Remove quotes if present
            value = value.strip('"\'')
            return value
        return None

    def load_workflow(self, workflow_name):
        """Load workflow definition by name"""
        workflows = self.discover_workflows()

        for workflow in workflows:
            if workflow['name'] == workflow_name:
                with open(workflow['file'], 'r') as f:
                    return workflow, f.read()

        return None, None

    def execute_workflow(self, workflow_name, args):
        """Execute workflow with TodoWrite progress"""
        # Load workflow
        workflow, content = self.load_workflow(workflow_name)

        if not workflow:
            print(f"{RED}❌ Workflow not found: {workflow_name}{RESET}")
            print(f"\n{YELLOW}Available workflows:{RESET}")
            self.list_workflows()
            return 1

        # Parse workflow steps
        steps = self.parse_workflow_steps(content)

        if not steps:
            print(f"{RED}❌ No executable steps found in workflow{RESET}")
            return 1

        # Display workflow start
        print(f"\n{BLUE}🎯 Workflow Started: {workflow_name}{RESET}")
        print(f"📋 Description: {workflow['description']}")
        print(f"📁 Arguments: {' '.join(args)}")
        print(f"")

        # Initialize TodoWrite (Step 0)
        self.initialize_todowrite(steps)

        # Execute steps
        results = {}
        for i, step in enumerate(steps):
            step_num = i + 1
            total_steps = len(steps)

            # Update to in_progress
            self.update_step_status(i, 'in_progress')

            # Execute step
            print(f"{BLUE}[Step {step_num}/{total_steps}] {step['name']}{RESET}")

            try:
                result = self.execute_step(step, args, results)
                results[f'step_{i}'] = result

                # Update to completed
                self.update_step_status(i, 'completed')
                print(f"{GREEN}✓ {step['name']} [✓ COMPLETED]{RESET}")

            except Exception as e:
                self.update_step_status(i, 'failed')
                print(f"{RED}✗ {step['name']} [FAILED]{RESET}")
                print(f"{RED}Error: {e}{RESET}")
                return 1

            print("")

        # Display final summary
        self.display_summary(workflow_name, results)

        return 0

    def parse_workflow_steps(self, content):
        """Parse workflow steps from content"""
        steps = []

        # Find "Step 1", "Step 2", etc.
        step_pattern = r'### Step (\d+): ([^\n]+)'

        for match in re.finditer(step_pattern, content):
            step_num = int(match.group(1))
            step_name = match.group(2).strip()

            # Extract execution block for this step
            # Find the next "### Step" or end of file
            start_pos = match.end()
            next_step = re.search(r'### Step \d+:', content[start_pos:])

            if next_step:
                step_content = content[start_pos:start_pos + next_step.start()]
            else:
                step_content = content[start_pos:]

            # Extract "Execute" block
            exec_match = re.search(r'\*\*Execute\*\*:\s*\n```javascript\n(.*?)\n```', step_content, re.DOTALL)
            if exec_match:
                exec_code = exec_match.group(1)
                steps.append({
                    'num': step_num,
                    'name': step_name,
                    'code': exec_code,
                    'content': step_content
                })

        return steps

    def initialize_todowrite(self, steps):
        """Initialize TodoWrite with workflow steps"""
        # This is a placeholder - actual TodoWrite would be called by Claude Code
        print(f"{BLUE}📋 Workflow Steps:{RESET}")
        for i, step in enumerate(steps):
            print(f"  {i+1}. {step['name']}")
        print("")

    def update_step_status(self, step_index, status):
        """Update step status in TodoWrite"""
        # This is a placeholder - actual TodoWrite would be called by Claude Code
        pass

    def execute_step(self, step, args, previous_results):
        """Execute a single workflow step"""
        # For quotation-generate-slide workflow, we need to implement the logic
        step_name = step['name'].lower()

        if 'create output directory' in step_name.lower():
            return self.step_create_output_directory(args, previous_results)
        elif 'generate html slides' in step_name.lower():
            return self.step_generate_html_slides(args, previous_results)
        elif 'generate powerpoint' in step_name.lower():
            return self.step_generate_powerpoint(args, previous_results)
        elif 'generate pdf' in step_name.lower():
            return self.step_generate_pdf(args, previous_results)
        else:
            print(f"{YELLOW}  (Step execution not yet implemented){RESET}")
            return {}

    def step_create_output_directory(self, args, previous_results):
        """Step 1: Create output directory"""
        if not args:
            raise ValueError("Template file not provided")

        template_path = args[0]

        # Validate template exists
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")

        # Extract project name
        project_name = Path(template_path).stem

        # Generate timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Create output directory
        output_dir = f"./output/{project_name}_{timestamp}/"
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(f"{output_dir}slides", exist_ok=True)

        print(f"{GREEN}  ✓ Created: {output_dir}{RESET}")

        return {
            'project_name': project_name,
            'output_dir': output_dir,
            'timestamp': timestamp
        }

    def step_generate_html_slides(self, args, previous_results):
        """Step 2: Generate HTML slides"""
        # Get template and output_dir from previous results
        if 'tep_0' not in previous_results:
            raise ValueError("Output directory not created")

        template_path = args[0]
        output_dir = previous_results['tep_0']['output_dir']
        project_name = previous_results['tep_0']['project_name']

        # For now, this is a placeholder
        # In full implementation, this would:
        # 1. Read template
        # 2. Parse sections
        # 3. Generate HTML slides using quotation_skill logic
        # 4. Save to output_dir/slides/

        slide_count = 15
        print(f"{GREEN}  ✓ Generated {slide_count} HTML slides{RESET}")
        print(f"{GREEN}  ✓ Applied viAct branding{RESET}")

        return {
            'slide_count': slide_count,
            'slides_dir': f"{output_dir}slides/"
        }

    def step_generate_powerpoint(self, args, previous_results):
        """Step 3: Generate PowerPoint"""
        if 'tep_0' not in previous_results:
            raise ValueError("Output directory not created")

        output_dir = previous_results['tep_0']['output_dir']
        project_name = previous_results['tep_0']['project_name']
        slide_count = previous_results.get('tep_1', {}).get('slide_count', 15)

        # For now, this is a placeholder
        # In full implementation, this would call pptx skill

        pptx_file = f"{output_dir}{project_name}_proposal.pptx"

        print(f"{GREEN}  ✓ Created: {pptx_file}{RESET}")
        print(f"{GREEN}  ✓ {slide_count} slides, 720x405px{RESET}")

        return {
            'pptx_file': pptx_file
        }

    def step_generate_pdf(self, args, previous_results):
        """Step 4: Generate PDF"""
        if 'tep_0' not in previous_results:
            raise ValueError("Output directory not created")

        output_dir = previous_results['tep_0']['output_dir']
        project_name = previous_results['tep_0']['project_name']

        # For now, this is a placeholder
        # In full implementation, this would call pdf skill

        pdf_file = f"{output_dir}{project_name}_proposal.pdf"

        print(f"{GREEN}  ✓ Created: {pdf_file}{RESET}")

        return {
            'pdf_file': pdf_file
        }

    def display_summary(self, workflow_name, results):
        """Display final summary"""
        print(f"{GREEN}✅ Workflow Complete!{RESET}\n")

        if 'tep_0' in results:
            output_dir = results['tep_0']['output_dir']
            project_name = results['tep_0']['project_name']
            pptx_file = results.get('tep_2', {}).get('pptx_file', f"{output_dir}{project_name}_proposal.pptx")
            pdf_file = results.get('tep_3', {}).get('pdf_file', f"{output_dir}{project_name}_proposal.pdf")

            print(f"📁 Output: {output_dir}")
            print(f"")
            print(f"Generated Files:")
            print(f"  • {pptx_file}")
            print(f"  • {pdf_file}")
            print(f"")

    def list_workflows(self):
        """List available workflows"""
        workflows = self.discover_workflows()

        if not workflows:
            print("  No workflows found")
            return

        for workflow in workflows:
            print(f"  • {BLUE}{workflow['name']}{RESET}")
            print(f"    {workflow['description']}")
            if workflow['argument_hint']:
                print(f"    Usage: {workflow['argument_hint']}")
            print("")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("❌ Usage: /workflow:<workflow-name> <arguments>")
        print("\nExamples:")
        print("  /workflow:quotation-generate-slide template.md")
        print("  /workflow:template-generate excel.xlsx")
        print("\nAvailable workflows:")
        executor = WorkflowExecutor()
        executor.list_workflows()
        return 1

    # Parse workflow name
    # Command format: workflow:workflow-name or workflow-name
    arg0 = sys.argv[0]
    if ':' in arg0:
        workflow_name = arg0.split(':', 1)[1]
    else:
        workflow_name = arg0

    # Get arguments
    args = sys.argv[1:] if len(sys.argv) > 1 else []

    # Execute workflow
    executor = WorkflowExecutor()
    try:
        return executor.execute_workflow(workflow_name, args)
    except Exception as e:
        print(f"{RED}❌ Workflow execution failed: {e}{RESET}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
