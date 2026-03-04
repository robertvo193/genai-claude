#!/usr/bin/env python3
"""
Template Generation Skill - Simplified End-User Interface
Generates proposal templates from Deal Transfer Excel files
"""

import sys
import os
import subprocess
import json
from pathlib import Path

def main():
    """Main entry point for template skill"""
    if len(sys.argv) < 2:
        print("❌ Usage: /template <excel_file.xlsx>")
        print("\nExample:")
        print("  /template DT_cedo.xlsx")
        return 1

    excel_file = sys.argv[1]

    # Check if file exists
    if not os.path.exists(excel_file):
        print(f"❌ Excel file not found: {excel_file}")
        print(f"\n💡 Tip: Make sure you're in the correct directory")
        print(f"   Current directory: {os.getcwd()}")
        return 1

    # Get the script path
    script_dir = Path(__file__).parent.parent / 'dealtransfer2template' / 'bin'
    generate_script = script_dir / 'generate_template.py'

    if not generate_script.exists():
        print(f"❌ Script not found: {generate_script}")
        return 1

    # Run the actual generation script
    try:
        result = subprocess.run(
            [sys.executable, str(generate_script), excel_file],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )

        # Print output
        print(result.stdout)

        if result.returncode != 0:
            print(result.stderr, file=sys.stderr)
            return 1

        # Parse JSON output if available
        try:
            lines = result.stdout.strip().split('\n')
            json_start = -1
            for i, line in enumerate(lines):
                if line.strip().startswith('{'):
                    json_start = i
                    break

            if json_start >= 0:
                json_text = '\n'.join(lines[json_start:])
                data = json.loads(json_text)

                if data.get('status') == 'success':
                    print(f"\n🎉 Success! Files generated in:")
                    print(f"   {data['output_dir']}")
                    print(f"\n📝 Quick access:")
                    print(f"   Template:  {data['files']['template']}")
                    print(f"   Reasoning: {data['files']['reasoning']}")
                    print(f"   Checklist: {data['files']['checklist']}")
                    print(f"\n📊 {data['statistics']['placeholders']} placeholders to fill")
                    print(f"   {data['statistics']['ai_modules']} AI modules detected")

        except json.JSONDecodeError:
            pass  # JSON parsing optional

        return 0

    except subprocess.TimeoutExpired:
        print("❌ Error: Script execution timeout (>5 minutes)")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
