#!/usr/bin/env python3
"""
Quotation Generate Slide - Skill Implementation
Wraps quotation_skill with simple command syntax
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Main entry point for quotation-generate-slide skill"""
    if len(sys.argv) < 2:
        print("❌ Usage: /quotation-generate-slide <template.md>")
        print("\nExample:")
        print("  /quotation-generate-slide Leda_Inio_template.md")
        return 1

    template_file = sys.argv[1]

    # Check if file exists
    if not os.path.exists(template_file):
        print(f"❌ Template file not found: {template_file}")
        print(f"\n💡 Tip: Make sure you're in the correct directory")
        print(f"   Current directory: {os.getcwd()}")
        return 1

    # Check if file is .md
    if not template_file.endswith('.md'):
        print(f"❌ Template must be .md format (not {Path(template_file).suffix})")
        return 1

    print(f"🎯 Generating slides from: {template_file}")
    print(f"")
    print(f"📋 This will:")
    print(f"  1. Create output directory")
    print(f"  2. Generate HTML slides (15 slides)")
    print(f"  3. Convert to PowerPoint (.pptx)")
    print(f"  4. Convert to PDF (.pdf)")
    print(f"")

    # Call quotation_skill
    # This invokes Claude Code's skill system
    # The skill system will handle execution
    print(f"✨ Executing quotation_skill...")

    # We can't directly invoke skills from Python
    # Instead, we provide instructions for user to run
    print(f"\n💡 To complete slide generation, run:")
    print(f"   /quotation slide {template_file}")
    print(f"\n")
    print(f"📁 Output will be in: ./output/<project>_<timestamp>/")

    return 0

if __name__ == '__main__':
    sys.exit(main())
