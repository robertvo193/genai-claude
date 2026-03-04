#!/usr/bin/env python3
"""
Main orchestration script for template2slide skill
Converts verified proposal template to complete PowerPoint presentation

Usage:
    python3 template2slide.py <template_file.md> [output_dir]
"""

import sys
import json
from pathlib import Path

# Add script directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import modules - use existing robust functions
from generate_from_deal_transfer import generate_architecture_from_file
from map_to_slides import map_proposal_to_slides


def generate_architecture(template_file, output_dir):
    """Step 1: Generate architecture diagram from template"""
    print("\n" + "="*80)
    print("STEP 1: GENERATING ARCHITECTURE DIAGRAM")
    print("="*80)
    
    # Use the existing robust function that handles both proposal templates and deal transfers
    result = generate_architecture_from_file(str(template_file), str(output_dir))
    
    if result:
        arch_file = result["mermaid_file"]
        project_info = result["project_info"]
        print(f"✅ Architecture diagram saved to: {arch_file}")
        
        # Save project_info.json for later use by insert_reference_slides.py
        project_info_file = output_dir / f"{template_file.stem}_project_info.json"
        with open(project_info_file, 'w', encoding='utf-8') as f:
            json.dump(project_info, f, indent=2, ensure_ascii=False)
        print(f"✅ Project info saved to: {project_info_file}")
        
        return arch_file, project_info
    else:
        print("❌ Failed to generate architecture diagram")
        return None, None


def map_to_slides(template_file, architecture_file, output_dir):
    """Step 2: Map template content to slide structure"""
    print("\n" + "="*80)
    print("STEP 2: MAPPING CONTENT TO SLIDE STRUCTURE")
    print("="*80)
    
    # Use the map_proposal_to_slides function from map_to_slides.py
    result = map_proposal_to_slides(
        str(template_file),
        str(architecture_file) if architecture_file else None,
        str(output_dir) if output_dir else None
    )
    
    structure_file = Path(result["json_file"])
    slide_structure = result["slide_structure"]
    
    print(f"✅ Slide structure saved to: {structure_file}")
    print(f"   Total slides: {slide_structure.get('total_slides', 0)}")
    
    return structure_file


def generate_powerpoint(slide_structure_file, output_dir):
    """Step 3: Generate PowerPoint from slide structure"""
    print("\n" + "="*80)
    print("STEP 3: GENERATING POWERPOINT PRESENTATION")
    print("="*80)

    import subprocess

    # Load slide structure
    with open(slide_structure_file, 'r', encoding='utf-8') as f:
        slide_structure = json.load(f)

    project_name = slide_structure.get("project_name", "Proposal")
    pptx_file = output_dir / f"{project_name}_proposal.pptx"

    print(f"📊 Generating PowerPoint with {slide_structure.get('total_slides', 0)} slides...")

    # Run run_agent.sh to generate the PowerPoint (calls generate_from_json.js)
    try:
        result = subprocess.run(
            ['/home/philiptran/projects/00_slide_proposal/run_agent.sh', str(slide_structure_file)],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )

        if result.returncode == 0:
            print(result.stdout)
            print(f"✅ PowerPoint generated successfully: {pptx_file}")
        else:
            print(f"❌ PowerPoint generation failed:")
            print(result.stderr)
            print(f"Stdout: {result.stdout}")
            return None
    except subprocess.TimeoutExpired:
        print("❌ PowerPoint generation timed out after 5 minutes")
        return None
    except FileNotFoundError:
        print("❌ 'run_agent.sh' script not found at:")
        print("   /home/philiptran/projects/00_slide_proposal/run_agent.sh")
        print("   Please ensure the script exists and is executable.")
        return None
    except Exception as e:
        print(f"❌ Error generating PowerPoint: {e}")
        return None

    return pptx_file


def generate_pdf(pptx_file, output_dir):
    """Step 4: Generate PDF from PowerPoint using pdf skill or LibreOffice"""
    print("\n" + "="*80)
    print("STEP 4: GENERATING PDF FROM POWERPOINT")
    print("="*80)

    try:
        pdf_file = pptx_file.with_suffix('.pdf')

        # Try using LibreOffice (soffice) if available
        import subprocess
        import shutil

        # Method 1: LibreOffice
        libreoffice_paths = [
            'libreoffice',
            '/usr/bin/libreoffice',
            '/Applications/LibreOffice.app/Contents/MacOS/soffice',
            'soffice'
        ]

        soffice_cmd = None
        for path in libreoffice_paths:
            if shutil.which(path):
                soffice_cmd = path
                break

        if soffice_cmd:
            print(f"📄 Converting PPTX to PDF using {soffice_cmd}...")
            result = subprocess.run(
                [soffice_cmd, '--headless', '--convert-to', 'pdf',
                 '--outdir', str(output_dir), str(pptx_file)],
                capture_output=True,
                text=True,
                timeout=120  # 2 minutes timeout
            )

            if result.returncode == 0 and pdf_file.exists():
                print(f"✅ PDF generated successfully: {pdf_file}")
                return pdf_file
            else:
                print(f"⚠️  LibreOffice conversion failed:")
                print(result.stderr)
        else:
            print("⚠️  LibreOffice not found. Trying alternative method...")

        # Method 2: Use Python-based conversion (unoconv if available)
        if shutil.which('unoconv'):
            print("📄 Converting PPTX to PDF using unoconv...")
            result = subprocess.run(
                ['unoconv', '-f', 'pdf', '-o', str(pdf_file), str(pptx_file)],
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0 and pdf_file.exists():
                print(f"✅ PDF generated successfully: {pdf_file}")
                return pdf_file

        # Method 3: Inform user about manual conversion
        print(f"\n⚠️  Automatic PDF generation not available.")
        print(f"   PPTX file: {pptx_file}")
        print(f"   Expected PDF: {pdf_file}")
        print(f"\n   Manual conversion options:")
        print(f"   1. Open PPTX in LibreOffice/Office → File → Export as PDF")
        print(f"   2. Install LibreOffice: sudo apt-get install libreoffice")

        return pdf_file  # Return expected path even if not created

    except subprocess.TimeoutExpired:
        print("❌ PDF generation timed out after 2 minutes")
        return None
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return None


def main():
    """Main orchestration function"""
    if len(sys.argv) < 2:
        print("Usage: python3 template2slide.py <template_file.md> [output_dir]")
        sys.exit(1)
    
    template_file = Path(sys.argv[1])
    if not template_file.exists():
        print(f"Error: Template file not found: {template_file}")
        sys.exit(1)
    
    # Set output directory
    if len(sys.argv) >= 3:
        output_dir = Path(sys.argv[2])
    else:
        output_dir = template_file.parent / "output"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("="*80)
    print("TEMPLATE TO SLIDE CONVERSION")
    print("="*80)
    print(f"Template: {template_file}")
    print(f"Output: {output_dir}")
    print("="*80)
    
    try:
        # Step 1: Generate architecture
        arch_file, project_info = generate_architecture(template_file, output_dir)

        if not arch_file:
            print("❌ Architecture generation failed. Exiting.")
            sys.exit(1)

        # Step 2: Map to slides
        structure_file = map_to_slides(template_file, arch_file, output_dir)

        if not structure_file:
            print("❌ Slide mapping failed. Exiting.")
            sys.exit(1)

        # Step 3: Generate PowerPoint
        pptx_file = generate_powerpoint(structure_file, output_dir)

        if not pptx_file:
            print("❌ PowerPoint generation failed. Exiting.")
            sys.exit(1)

        # Step 4: Generate PDF from PowerPoint
        pdf_file = generate_pdf(pptx_file, output_dir)

        print("\n" + "="*80)
        print("✅ CONVERSION COMPLETE")
        print("="*80)
        print(f"Architecture diagram: {arch_file}")
        print(f"Slide structure: {structure_file}")
        print(f"PowerPoint: {pptx_file}")
        if pdf_file and pdf_file.exists():
            print(f"PDF: {pdf_file}")
        print("\nNext steps:")
        print("1. Review the generated PowerPoint presentation")
        print("2. Review the generated PDF (if available)")
        print("3. Make any necessary adjustments")
        print("4. Share with presales for final review")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

