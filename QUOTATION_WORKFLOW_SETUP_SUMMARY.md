# Quotation Workflow - Setup Complete

## ✅ Installation Summary

**Global CCW quotation workflow successfully installed and configured!**

### Files Created

```
~/.claude/
├── workflows/
│   └── quotation-generate.md          # 4-step workflow definition
├── commands/
│   ├── quotation.md                   # Command implementation
│   ├── quotation-quickref.md          # Quick reference card
│   └── QUOTATION_USER_GUIDE.md        # Complete user guide
└── workflows/.quotation/               # State directory (auto-created)
```

## 🎯 What You Can Do Now

### Generate Proposals (Simple Command)

```bash
/quotation generate slide <template.md>
```

**Example**:
```bash
/quotation generate slide Leda_Inio_template.md
```

### Check Status

```bash
/quotation status
```

### List Recent

```bash
/quotation list
```

## 📊 Workflow Overview

**4-Step Process** (Automated):

```
Step 1: Create Output Directory
  → ./output/[Project]_[Timestamp]/

Step 2: Generate HTML Slides
  → Parse template (12 sections)
  → Apply viAct branding
  → Prevent text overflow

Step 3: Generate PowerPoint
  → HTML → PPTX (via pptx skill)

Step 4: Generate PDF
  → PPTX → PDF (via pdf skill)
```

## 🎨 Features

### User-Facing
- ✅ Simple one-command interface
- ✅ Clear progress indicators (Step 1/4, 2/4, 3/4, 4/4)
- ✅ Visual status (🔄 in_progress, ✅ completed, ⏳ pending)
- ✅ Simple output (just file paths)

### Internal (Hidden)
- ✅ 7 HTML templates (from SLIDE_TEMPLATES.md)
- ✅ viAct branding (#00AEEF blue, white text)
- ✅ Text overflow prevention (smart layouts)
- ✅ Architecture diagram generation
- ✅ State management (JSON persistence)

## 📝 Requirements

### Input
- ✅ Verified proposal template (.md)
- ✅ No placeholders (no `[PLACEHOLDER_ID]`)
- ✅ 12 sections (standard viAct structure)

### Dependencies (Auto-Checked)
- ✅ pptx skill (`~/.claude/skills/pptx/`)
- ✅ pdf skill (`~/.claude/skills/pdf/`)
- ✅ LibreOffice (for PDF generation)

## 📂 Output Structure

```
./output/
└── [ProjectName]_[YYYYMMDD]_[HHMMSS]/
    ├── [Project]_proposal.pptx
    ├── [Project]_proposal.pdf
    └── slides/ (optional: HTML source)
```

## 🔧 Technical Details

### Templates Used (from SLIDE_TEMPLATES.md)

| Template | Use Case |
|----------|----------|
| Template 1 | Cover Page |
| Template 2 | Standard Content (bullets) |
| Template 3 | Two-Column Layout |
| Template 5 | AI Module Detail |
| Template 6 | Timeline/Phases |

### viAct Branding

- **Primary Color**: #00AEEF (viAct Blue)
- **Text Color**: #FFFFFF (White)
- **Font**: Arial, Helvetica, Verdana
- **Background**: `assets/background.png` (720×405px)
- **Margins**: `0 120pt 85pt 40pt` (prevents overflow)

### State Management

```json
{
  "session_id": "quotation-{timestamp}",
  "status": "in_progress" | "completed" | "failed",
  "template": "{template_path}",
  "project_name": "{project_name}",
  "output_dir": "./output/{project}_{timestamp}/",
  "steps": [
    { "step": 1, "name": "Create Output Directory", "status": "completed" },
    { "step": 2, "name": "Generate HTML Slides", "status": "completed" },
    { "step": 3, "name": "Generate PowerPoint", "status": "completed" },
    { "step": 4, "name": "Generate PDF", "status": "completed" }
  ],
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}
```

**Saved to**: `.workflow/.quotation/{session_id}/state.json`

## 🚀 Quick Start

### 1. Prepare Template

Ensure your template:
- ✅ Is markdown format (.md)
- ✅ Has no placeholders
- ✅ Has 12 sections

### 2. Run Command

```bash
/quotation generate slide Your_Template.md
```

### 3. Check Output

```bash
# View generated files
ls -la ./output/YourProject_20250126_163030/

# Open PowerPoint
libreoffice ./output/YourProject_20250126_163030/YourProject_proposal.pptx

# Open PDF
evince ./output/YourProject_20250126_163030/YourProject_proposal.pdf
```

## 📚 Documentation

| File | Description |
|------|-------------|
| `quotation-quickref.md` | Quick reference card |
| `QUOTATION_USER_GUIDE.md` | Complete user guide |
| `quotation-generate.md` | Workflow definition |
| `quotation.md` | Command implementation |

## 🐛 Troubleshooting

### Error: Template not found

**Solution**: Check file path is correct

### Error: Template has placeholders

**Solution**: Verify template first (remove all `[PLACEHOLDER_ID]` tags)

### Error: Skills not found

**Solution**: Install pptx and pdf skills
```bash
# Check if skills exist
ls ~/.claude/skills/pptx/
ls ~/.claude/skills/pdf/
```

### Error: PDF generation failed

**Solution**: Install LibreOffice
```bash
sudo apt install libreoffice
```

## 🎯 Success Criteria

- ✅ Command validates inputs (template, 12 sections, no placeholders)
- ✅ Workflow shows clear states (Step 1/4, 2/4, 3/4, 4/4)
- ✅ State persisted for status checking
- ✅ Errors shown clearly with helpful messages
- ✅ User only sees: command → progress (4 steps) → output location
- ✅ Output structure matches: `./output/[Project]_[Timestamp]/[Project]_proposal.{pptx,pdf}`

## 🔮 Future Enhancements

Possible future features:
- Custom output directory: `--output <path>`
- Parallel generation: Multiple templates at once
- Template validation: Built-in checker
- Batch mode: Process multiple templates
- Resume capability: Recover from failures

## 📞 Support

For issues or questions:
1. Check error messages (include solutions)
2. Read user guide: `QUOTATION_USER_GUIDE.md`
3. Review state files: `.workflow/.quotation/`
4. Validate template format
5. Verify dependencies installed

## ✨ Summary

**You now have a global quotation workflow that:**

1. ✅ Accepts simple command: `/quotation generate slide <template.md>`
2. ✅ Shows clear workflow states during execution
3. ✅ Hides technical complexity from end-users
4. ✅ Validates internally (template, dependencies, outputs)
5. ✅ Produces professional PowerPoint and PDF outputs
6. ✅ Tracks state and progress
7. ✅ Handles errors gracefully with clear messages

**Ready to use! Try it now:**

```bash
/quotation generate slide Your_Template.md
```

---

**Setup Date**: 2025-01-26
**CCW Version**: 6.3.48
**Installation**: Global (/home/philiptran)
**Workflow**: quotation-generate v1.0.0
