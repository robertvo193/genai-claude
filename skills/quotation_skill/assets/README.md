# Assets Directory

This directory contains static assets used in generating quotation outputs.

## Purpose

Assets are files that are used in the output generation process but are not loaded into context. These include templates, images, configuration files, and other resources.

## Current Assets

### background.png
**Purpose**: Background image for PowerPoint slides
**Usage**: Applied as slide background in html2pptx workflow (State 3)
**Source**: Copied from `../template2slide/scripts/background.png`
**Size**: 1.3MB
**Format**: PNG image

This background image is used when generating PowerPoint presentations to maintain consistent viAct branding across all proposal slides.

## Referenced Assets (Not Copied)

These assets are located in other directories and referenced by the quotation skill:

### From dealtransfer2template/
**Location**: `../dealtransfer2template/`
**Purpose**: Content generation templates and references
**Files**:
- `TEMPLATE.md` - Proposal structure and field mappings
- `STANDARD_MODULES.md` - Standard AI module reference list
- `FIELD_NAMES_REFERENCE.md` - Deal Transfer field names (S1/S2)
- `Logic_for_Determining_List_of_AI_Modules_from_VA_usecases_and_Client_Painpoint.md` - Module inference logic
- `STANDARD_MODULES_COMMON.md` - Common module definitions
- `STANDARD_MODULES_byAI.md` - AI-generated module references

**Usage**: Referenced during State 1 (Content Generation) for:
- Extracting data from Deal Transfer Excel
- Mapping fields to proposal sections
- Identifying standard vs custom modules
- Inferring modules from vague use cases

### From pptx skill
**Location**: `~/.claude/skills/pptx/`
**Purpose**: PowerPoint generation
**Usage**: Invoked during State 3 (Output Generation)
**Key resources**:
- html2pptx workflow
- Design principles and color palettes
- Typography guidelines

### From pdf skill
**Location**: `~/.claude/skills/pdf/`
**Purpose**: PDF generation
**Usage**: Invoked during State 3 (Output Generation)
**Key resources**:
- PPTX → PDF conversion methods
- LibreOffice conversion
- pypdf library

## Why Some Assets Are Referenced vs Copied

### Copied Assets (in this directory)
- **Binary files** needed for output generation (e.g., background.png)
- **Small, static files** that won't change
- **Files required** during State 3 output generation

### Referenced Assets (in other directories)
- **Large documentation files** (templates, reference docs)
- **Files that may change** and should stay in source
- **Files used for reference only** during State 1-2
- **Skill files** that are invoked (pptx, pdf)

## Adding New Assets

To add a new asset to this directory:

1. **Determine asset type**:
   - Binary file (image, font) → Copy here
   - Documentation/template → Reference from source
   - Configuration file → Copy if small, reference if large

2. **For binary assets**:
   ```bash
   cp /path/to/asset.ext assets/
   ```

3. **Update this README**:
   - Add description under "Current Assets"
   - Document purpose, usage, source

4. **Update SKILL.md** (if needed):
   - Add reference to asset in appropriate workflow state
   - Document how/when to use the asset

## Asset Usage in Workflow

### State 1: Content Generation
**Assets used**: Referenced from `../dealtransfer2template/`
- TEMPLATE.md
- STANDARD_MODULES.md
- FIELD_NAMES_REFERENCE.md
- Module inference logic files

**No assets copied** - all referenced from source

### State 2: Review Workflow
**Assets used**: None
- Only uses scripts for template update

### State 3: Output Generation
**Assets used**:
- **Copied**: `background.png` (for PowerPoint slides)
- **Invoked skills**: pptx skill, pdf skill

## Best Practices

1. **Keep assets minimal**: Only copy what's needed for output generation
2. **Reference when possible**: Keep documentation and templates in source locations
3. **Document everything**: Update README when adding new assets
4. **Version control**: Track asset changes in git
5. **Size limits**: Avoid copying large files (>5MB) unless necessary

## Asset Maintenance

### Regular Updates
- Check `../template2slide/` for updated background images
- Sync `../dealtransfer2template/` reference docs if structure changes
- Update asset references when workflows change

### Cleanup
- Remove unused assets
- Archive old asset versions
- Keep README in sync with actual assets
