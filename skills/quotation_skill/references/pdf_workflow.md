# PDF Generation Workflow (using pdf skill)

## Overview

This guide explains how to generate PDF documents from PowerPoint presentations using the `pdf` skill.

## Prerequisites

- PowerPoint file already generated (`proposal.pptx`)
- `pdf` skill available at `~/.claude/skills/pdf/`
- Required dependencies: pypdf, pdfplumber, LibreOffice (for conversion)

## Conversion Methods

### Method 1: LibreOffice Conversion (Recommended)

LibreOffice provides the most reliable PPTX → PDF conversion.

```bash
# Using LibreOffice command-line
libreoffice --headless --convert-to pdf proposal.pptx
```

**Advantages**:
- Preserves formatting accurately
- Handles fonts and layouts correctly
- Maintains image quality
- Cross-platform compatibility

**Requirements**:
```bash
# Install LibreOffice (Ubuntu/Debian)
sudo apt-get install libreoffice

# Install LibreOffice (macOS)
brew install libreoffice

# Install LibreOffice (Windows)
# Download from libreoffice.org
```

### Method 2: Using Python Libraries

For programmatic conversion within Python scripts:

#### Using pypdf (metadata extraction)

```python
from pypdf import PdfReader, PdfWriter

# Read PDF metadata
reader = PdfReader("proposal.pdf")
print(f"Pages: {len(reader.pages)}")
print(f"Title: {reader.metadata.title}")
print(f"Author: {reader.metadata.author}")
```

#### Using pdfplumber (text/table extraction)

```python
import pdfplumber

# Extract text from PDF
with pdfplumber.open("proposal.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)

# Extract tables from PDF
with pdfplumber.open("proposal.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            print(table)
```

## Integration with quotation_skill

In State 3 (Output Generation), after generating PowerPoint:

### Step 1: Generate PowerPoint
Use `pptx` skill html2pptx workflow (see `pptx_workflow.md`)
Output: `proposal.pptx`

### Step 2: Convert to PDF

```bash
# Using LibreOffice (recommended)
libreoffice --headless --convert-to pdf proposal.pptx

# Output: proposal.pdf
```

### Step 3: Verify PDF

```python
import pypdf

# Verify PDF was created
reader = PdfReader("proposal.pdf")
print(f"✅ PDF created with {len(reader.pages)} pages")

# Verify page content
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if not text or len(text.strip()) < 50:
        print(f"⚠️  Warning: Page {i+1} has minimal text")
```

## Quality Checks

After PDF generation:

- ✅ File opens without errors
- ✅ All pages present
- ✅ Text selectable (not images)
- ✅ Formatting preserved from PPTX
- ✅ Images and diagrams visible
- ✅ Fonts rendered correctly
- ✅ No text overflow or clipping

## Troubleshooting

### "LibreOffice command not found"
**Solution**: Install LibreOffice
```bash
# Ubuntu/Debian
sudo apt-get install libreoffice

# macOS
brew install libreoffice
```

### "PDF has missing slides"
**Cause**: LibreOffice conversion error
**Solution**:
1. Check PowerPoint file integrity
2. Verify all slides render in PowerPoint
3. Try alternative conversion method

### "Text not selectable in PDF"
**Cause**: Text converted to images during conversion
**Solution**:
1. Check PowerPoint font usage (use standard fonts)
2. Verify LibreOffice version
3. Re-export PowerPoint with embedded fonts

### "Images low quality in PDF"
**Cause**: Compression during conversion
**Solution**:
1. Increase image resolution in PowerPoint
2. Check LibreOffice export settings
3. Use vector images when possible

### "PDF file size too large"
**Cause**: High-resolution images, embedded fonts
**Solution**:
1. Compress images in PowerPoint first
2. Optimize PDF after conversion
3. Remove unnecessary slides

## PDF Optimization

### Reduce File Size

```bash
# Using Ghostscript (install first)
sudo apt-get install ghostscript

# Compress PDF
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 \
   -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH \
   -sOutputFile=proposal_compressed.pdf proposal.pdf
```

### Merge Multiple PDFs

```python
from pypdf import PdfWriter

merger = PdfWriter()
merger.append("proposal_part1.pdf")
merger.append("proposal_part2.pdf")
merger.write("proposal_complete.pdf")
merger.close()
```

### Split PDF

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("proposal.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as f:
        writer.write(f)
```

## Extracting Content from PDF

### Extract All Text

```python
import pdfplumber

with pdfplumber.open("proposal.pdf") as pdf:
    full_text = ""
    for page in pdf.pages:
        full_text += page.extract_text() + "\n"

    with open("proposal_text.txt", "w") as f:
        f.write(full_text)
```

### Extract Tables

```python
import pdfplumber

with pdfplumber.open("proposal.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        if tables:
            print(f"Page {i+1} has {len(tables)} table(s)")
```

### Extract Metadata

```python
from pypdf import PdfReader

reader = PdfReader("proposal.pdf")
meta = reader.metadata

print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
print(f"Producer: {meta.producer}")
print(f"Creation Date: {meta.creation_date}")
```

## Advanced: Add Metadata to PDF

```python
from pypdf import PdfReader, PdfWriter

# Read existing PDF
reader = PdfReader("proposal.pdf")
writer = PdfWriter()

# Add all pages
for page in reader.pages:
    writer.add_page(page)

# Add metadata
writer.add_metadata({
    "/Title": "Video Analytics Solution Proposal for Client",
    "/Author": "viAct",
    "/Subject": "AI-Powered Video Analytics Proposal",
    "/Creator": "quotation_skill",
    "/Producer": "LibreOffice"
})

# Save with metadata
with open("proposal_with_metadata.pdf", "wb") as f:
    writer.write(f)
```

## Complete Workflow Example

```bash
#!/bin/bash
# complete_pdf_generation.sh

echo "Step 1: Generate PowerPoint (using pptx skill)"
# (Assuming proposal.pptx already created)

echo "Step 2: Convert to PDF"
libreoffice --headless --convert-to pdf proposal.pptx

echo "Step 3: Verify PDF"
python3 << EOF
import pypdf
try:
    reader = pypdf.PdfReader("proposal.pdf")
    print(f"✅ PDF created with {len(reader.pages)} pages")
    print(f"✅ Title: {reader.metadata.title}")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
EOF

if [ $? -eq 0 ]; then
    echo "✅ PDF generation complete"
    echo "Output: proposal.pdf"
else
    echo "❌ PDF generation failed"
    exit 1
fi
```

## Best Practices

1. **Use LibreOffice for conversion** - Most reliable PPTX → PDF conversion
2. **Verify PowerPoint first** - Ensure PPTX is correct before converting
3. **Check PDF page count** - Should match PowerPoint slide count
4. **Test text selection** - Ensure text is selectable, not images
5. **Optimize file size** - Compress if needed for email/sharing
6. **Add metadata** - Include title, author, subject for searchability
7. **Keep backups** - Save original PowerPoint alongside PDF

## Output Files

After State 3 (Output Generation):

```
project/
├── proposal.pptx          # PowerPoint presentation
├── proposal.pdf           # PDF document
└── proposal_final.md      # Source template (for reference)
```

## References

- `~/.claude/skills/pdf/SKILL.md` - Complete pdf skill documentation
- `~/.claude/skills/pdf/REFERENCE.md` - Advanced PDF operations
- LibreOffice documentation: https://help.libreoffice.org/

## Summary

The PDF generation workflow is straightforward:
1. Generate PowerPoint (using pptx skill)
2. Convert to PDF (using LibreOffice or pdf skill)
3. Verify and optimize (using pypdf/pdfplumber)

Both PDF and PowerPoint are delivered as final outputs to complete the quotation workflow.
