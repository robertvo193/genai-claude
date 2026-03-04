#!/usr/bin/env python3
"""
Insert Available slides into generated presentation using OOXML unpack/pack approach

Usage:
    python insert_available_slides_ooxml.py <generated.pptx> <AvailableSlide11.pptx> <output.pptx>

Structure:
    1. Slide 1 from generated (Title Slide)
    2. Available Slides 2-10 (9 slides)
    3. Remaining slides from generated (Slides 2 onwards)
    4. Available Slides 11-25 (15 slides)
"""

import sys
import os
import shutil
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

# Register namespaces to preserve prefixes
NAMESPACES = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'ct': 'http://schemas.openxmlformats.org/package/2006/content-types'
}

for prefix, uri in NAMESPACES.items():
    ET.register_namespace(prefix, uri)

def insert_available_slides(generated_path, available_path, output_path):
    print("📊 Inserting Available slides using OOXML approach...\n")

    # Create temporary directories
    temp_dir = Path("temp_slide_insert")
    generated_dir = temp_dir / "generated"
    available_dir = temp_dir / "available"
    output_dir = temp_dir / "output"

    # Clean up any existing temp directory
    if temp_dir.exists():
        shutil.rmtree(temp_dir)

    for d in [generated_dir, available_dir, output_dir]:
        d.mkdir(parents=True)

    try:
        # Step 1: Unpack both presentations
        print("📦 Unpacking presentations...")
        unpack_pptx(generated_path, generated_dir)
        print(f"  ✓ Generated: {len(list((generated_dir / 'ppt' / 'slides').glob('*.xml')))} slides")

        unpack_pptx(available_path, available_dir)
        print(f"  ✓ Available: {len(list((available_dir / 'ppt' / 'slides').glob('*.xml')))} slides")

        # Step 2: Copy base structure to output
        print("\n📋 Setting up output structure...")
        copy_directory(generated_dir, output_dir)

        # Step 3: Build slide list
        print("\n🔗 Building slide order...")
        generated_slides = sorted((generated_dir / 'ppt' / 'slides').glob('slide*.xml'), key=lambda x: int(x.stem[5:]))
        available_slides = sorted((available_dir / 'ppt' / 'slides').glob('slide*.xml'), key=lambda x: int(x.stem[5:]))

        slide_mapping = []

        # Add generated slide 1 (title)
        slide_mapping.append(('generated', 1))

        # Add available slides 2-10 (indices 1-9)
        for i in range(1, min(10, len(available_slides) + 1)):
            slide_mapping.append(('available', i))

        # Add remaining generated slides (2 onwards)
        for i in range(2, len(generated_slides) + 1):
            slide_mapping.append(('generated', i))

        # Add available slides 11-25 (indices 10-24)
        for i in range(10, min(25, len(available_slides) + 1)):
            slide_mapping.append(('available', i))

        print(f"  Total slides to create: {len(slide_mapping)}")

        # Step 4: Copy slides and media
        print("\n📄 Copying slides and media...")
        output_slides_dir = output_dir / 'ppt' / 'slides'
        output_media_dir = output_dir / 'ppt' / 'media'
        media_offset = 0

        # Get current max media number
        if output_media_dir.exists():
            existing_media = list(output_media_dir.glob('*'))
            if existing_media:
                media_offset = max([int(f.stem.split('_')[-1].split('.')[0]) for f in existing_media if f.stem.split('_')[-1].split('.')[0].isdigit()] + [0])

        slide_id = 256
        slide_list = []

        for idx, (source, slide_num) in enumerate(slide_mapping, 1):
            if source == 'generated':
                src_slide = generated_dir / 'ppt' / 'slides' / f'slide{slide_num}.xml'
                src_rels = generated_dir / 'ppt' / 'slides' / '_rels' / f'slide{slide_num}.xml.rels'
            else:
                src_slide = available_dir / 'ppt' / 'slides' / f'slide{slide_num}.xml'
                src_rels = available_dir / 'ppt' / 'slides' / '_rels' / f'slide{slide_num}.xml.rels'

            # Copy slide XML
            dest_slide = output_slides_dir / f'slide{idx}.xml'
            shutil.copy2(src_slide, dest_slide)

            # Copy slide relationships
            dest_rels_dir = output_slides_dir / '_rels'
            dest_rels_dir.mkdir(exist_ok=True)
            dest_rels = dest_rels_dir / f'slide{idx}.xml.rels'

            if src_rels.exists():
                # Read and update relationships
                rels_tree = ET.parse(src_rels)
                rels_root = rels_tree.getroot()

                # Update media references if from available slides
                if source == 'available':
                    for rel in rels_root.findall('.//r:Relationship', NAMESPACES):
                        target = rel.get('Target')
                        if target.startswith('../media/'):
                            media_name = Path(target).name
                            # Copy media file
                            src_media = available_dir / 'ppt' / 'media' / media_name
                            if src_media.exists():
                                # Generate new media name with offset
                                media_ext = src_media.suffix
                                new_media_num = media_offset + 1
                                new_media_name = f"image{new_media_num}{media_ext}"
                                dest_media = output_media_dir / new_media_name
                                output_media_dir.mkdir(exist_ok=True, parents=True)
                                shutil.copy2(src_media, dest_media)
                                rel.set('Target', f'../media/{new_media_name}')
                                media_offset = new_media_num

                rels_tree.write(dest_rels, xml_declaration=True, encoding='UTF-8')

            slide_list.append(slide_id)
            slide_id += 1

            print(f"  ✓ Slide {idx}: {source} slide {slide_num}")

        # Step 5: Update presentation.xml and presentation.xml.rels
        print("\n📝 Updating presentation.xml and presentation.xml.rels...")
        update_presentation_files(output_dir, slide_list)

        # Step 7: Update [Content_Types].xml
        print("📝 Updating [Content_Types].xml...")
        update_content_types(output_dir, len(slide_mapping))

        # Step 8: Pack output
        print("\n📦 Packing output presentation...")
        pack_pptx(output_dir, output_path)

        print(f"\n✅ Successfully created presentation with {len(slide_mapping)} slides!")

    finally:
        # Clean up temp directory
        if temp_dir.exists():
            shutil.rmtree(temp_dir)


def unpack_pptx(pptx_path, output_dir):
    """Unpack a PPTX file to a directory"""
    with zipfile.ZipFile(pptx_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)


def pack_pptx(input_dir, output_path):
    """Pack a directory to a PPTX file"""
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(input_dir)
                zip_ref.write(file_path, arcname)


def copy_directory(src, dst):
    """Copy directory recursively"""
    for item in src.glob('*'):
        if item.is_dir():
            shutil.copytree(item, dst / item.name, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dst / item.name)


def update_presentation_files(output_dir, slide_list):
    """Update both ppt/presentation.xml and ppt/_rels/presentation.xml.rels"""

    # Read the original rels file to understand the structure
    rels_file = output_dir / 'ppt' / '_rels' / 'presentation.xml.rels'

    # Read as text to preserve formatting
    with open(rels_file, 'r') as f:
        rels_content = f.read()

    # Parse to find the namespace
    rels_tree = ET.parse(rels_file)
    rels_root = rels_tree.getroot()

    # Determine which prefix is used for relationships
    rel_ns_uri = None
    used_prefix = None

    # Check existing Relationship elements to see what prefix they use
    for child in rels_root:
        if 'Relationship' in child.tag:
            # Extract the namespace URI from the tag
            if child.tag.startswith('{'):
                rel_ns_uri = child.tag.split('}')[0].strip('{')
            else:
                # No namespace, need to find from attributes
                pass

            # Find what prefix was used by checking root's xmlns declarations
            for attr_name, attr_value in rels_root.attrib.items():
                if attr_value == rel_ns_uri or (rel_ns_uri is None and 'schemas.openxmlformats.org/package/2006/relationships' in attr_value):
                    if attr_name.startswith('xmlns:'):
                        used_prefix = attr_name.split(':')[1]
                    elif attr_name == 'xmlns':
                        used_prefix = ''
                    break
            break

    # Default to ns0 if nothing found
    if used_prefix is None:
        used_prefix = 'ns0'

    # Now find all non-slide relationships
    all_rels = list(rels_root)
    non_slide_rels = []
    max_rid = 0

    for rel in all_rels:
        rel_type = rel.get('Type', '')
        if not rel_type.endswith('slide'):
            non_slide_rels.append(rel)
        rid = rel.get('Id', '')
        if rid.startswith('rId'):
            try:
                rid_num = int(rid[3:])
                if rid_num > max_rid:
                    max_rid = rid_num
            except:
                pass

    # Clear and rebuild
    rels_root.clear()

    # Re-add non-slide relationships
    for rel in non_slide_rels:
        rels_root.append(rel)

    # Add new slide relationships
    r_id_start = max_rid + 1
    r_id_to_slide = {}

    # Create Relationship elements with correct namespace
    rel_ns = '{http://schemas.openxmlformats.org/package/2006/relationships}' if used_prefix else ''

    for idx, slide_id in enumerate(slide_list, 0):
        r_id = r_id_start + idx
        rel = ET.Element(f'{rel_ns}Relationship')
        rel.set('Id', f'rId{r_id}')
        rel.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide')
        rel.set('Target', f'slides/slide{idx + 1}.xml')
        rels_root.append(rel)
        r_id_to_slide[slide_id] = r_id

    rels_tree.write(rels_file, xml_declaration=True, encoding='UTF-8')

    # Now update presentation.xml with the correct rIds
    pres_xml = output_dir / 'ppt' / 'presentation.xml'
    tree = ET.parse(pres_xml)
    root = tree.getroot()

    # Find sldIdLst element
    sld_id_lst = root.find('.//p:sldIdLst', NAMESPACES)
    if sld_id_lst is None:
        # Create new sldIdLst
        sld_id_lst = ET.Element(f'{{{NAMESPACES["p"]}}}sldIdLst')
        root.append(sld_id_lst)
    else:
        # Clear existing
        sld_id_lst.clear()

    # Add slide IDs with correct rIds
    for slide_id in slide_list:
        sld_id = ET.SubElement(sld_id_lst, f'{{{NAMESPACES["p"]}}}sldId')
        sld_id.set('id', str(slide_id))
        sld_id.set(f'{{{NAMESPACES["r"]}}}id', f'rId{r_id_to_slide[slide_id]}')

    tree.write(pres_xml, xml_declaration=True, encoding='UTF-8')


def update_content_types(output_dir, num_slides):
    """Update [Content_Types].xml"""
    types_file = output_dir / '[Content_Types].xml'
    tree = ET.parse(types_file)
    root = tree.getroot()

    # Remove existing slide overrides
    for override in root.findall('.//ct:Override', NAMESPACES):
        part_name = override.get('PartName', '')
        if '/ppt/slides/slide' in part_name:
            root.remove(override)

    # Add new slide overrides
    for i in range(1, num_slides + 1):
        override = ET.Element(f'{{{NAMESPACES["ct"]}}}Override')
        override.set('PartName', f'/ppt/slides/slide{i}.xml')
        override.set('ContentType', 'application/vnd.openxmlformats-officedocument.presentationml.slide+xml')
        root.append(override)

    tree.write(types_file, xml_declaration=True, encoding='UTF-8')


def main():
    if len(sys.argv) < 4:
        print("Usage: python insert_available_slides_ooxml.py <generated.pptx> <AvailableSlide11.pptx> <output.pptx>")
        sys.exit(1)

    generated_path = sys.argv[1]
    available_path = sys.argv[2]
    output_path = sys.argv[3]

    try:
        insert_available_slides(generated_path, available_path, output_path)
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
