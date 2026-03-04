# 📊 Command Comparison: `/quotation slide` vs `/quotation generate slide`

## Quick Answer

| Command | Status | How to Use |
|---------|--------|------------|
| `/quotation slide <template.md>` | ✅ **WORKS NOW** | Direct quotation_skill command |
| `/quotation generate slide <template.md>` | ⚠️ **DESIGN ONLY** | CCW workflow (not executable yet) |

---

## Detailed Comparison

### Command 1: `/quotation slide` ✅

**Type**: Skill Command
**Status**: **Fully Functional**
**Location**: `~/.claude/skills/quotation_skill/`
**Name**: `quotation`

#### What It Does

```
Template.md → HTML Slides → PowerPoint → PDF
```

#### Usage

```bash
/quotation slide Leda_Inio_template.md
```

#### Features

- ✅ **Works right now** - Fully implemented
- ✅ **Original quotation_skill** - Battle-tested
- ✅ **3-step process**:
  1. Create output directory
  2. Generate PowerPoint (HTML → PPTX)
  3. Generate PDF (PPTX → PDF)
- ✅ **viAct branding** - Blue #00AEEF, white text
- ✅ **Text overflow prevention** - Proper margins
- ✅ **High-quality output** - Professional slides

#### Progress Display

Shows basic progress:
- "Creating output directory..."
- "Generating HTML slides..."
- "Converting to PowerPoint..."
- "Converting to PDF..."

#### Output

```
./output/Leda_Inio_<timestamp>/
├── Leda_Inio_proposal.pptx
├── Leda_Inio_proposal.pdf
└── slides/ (HTML source files)
```

---

### Command 2: `/quotation generate slide` ⚠️

**Type**: CCW Workflow Command
**Status**: **Design Specification** (not executable)
**Location**: `~/.claude/commands/workflow/quotation/generate-slide.md`
**Name**: `quotation-generate-slide`

#### What It's Designed to Do

```
Template.md → [4 Auto-Continue Steps with TodoWrite] → PowerPoint + PDF
```

#### Planned Usage

```bash
/quotation generate slide Leda_Inio_template.md
```

#### Planned Features

- 🎨 **Better state display** - `[Step 1/4]`, `[Step 2/4]`, etc.
- 🔄 **Auto-continue mechanism** - TodoWrite-based progress
- 📊 **Clear progress indicators** - Checkmarks and percentages
- 🎯 **Simplified command** - More intuitive for end-users
- ⏸️ **State tracking** - Session management for resumption

#### Planned Progress Display

Would show enhanced progress:
```
[Step 1/4] Create Output Directory [✓ COMPLETED]
✓ Created: ./output/Leda_Inio_20260126_235000/

[Step 2/4] Generate HTML Slides [✓ COMPLETED]
✓ Generated 15 HTML slides
✓ Applied viAct branding

[Step 3/4] Generate PowerPoint [✓ COMPLETED]
✓ Created: Leda_Inio_proposal.pptx
✓ 15 slides, 720x405px

[Step 4/4] Generate PDF [✓ COMPLETED]
✓ Created: Leda_Inio_proposal.pdf
```

#### Current Status

❌ **Not yet executable** - It's a design document that:
- Describes how the workflow should work
- Specifies the 4-step process
- Defines TodoWrite integration
- Needs CCW framework integration to work

---

## Key Differences

| Aspect | `/quotation slide` | `/quotation generate slide` |
|--------|-------------------|---------------------------|
| **Status** | ✅ Works now | ⚠️ Design only |
| **Implementation** | quotation_skill (Python/shell) | CCW workflow (YAML + JS) |
| **Steps** | 3 steps | 4 steps (more granular) |
| **Progress Display** | Basic text | Enhanced TodoWrite states |
| **State Tracking** | None | TodoWrite + session management |
| **Command Syntax** | `/quotation slide` | `/quotation generate slide` |
| **Auto-Continue** | Manual execution | Automatic progression |
| **User Interaction** | May need intervention | Fully autonomous |

---

## 🚀 How to Use Globally

### Option 1: Use Working Command (Recommended)

**Command**: `/quotation slide <template.md>`

This works **globally right now** because:
- quotation_skill is in `~/.claude/skills/`
- Claude Code automatically loads skills from this directory
- The skill name is `quotation` (from SKILL.md frontmatter)

**Usage**:
```bash
# From any directory
/quotation slide /path/to/Leda_Inio_template.md

# Example
cd ~/projects/leda
/quotation slide Leda_Inio_template.md
```

---

### Option 2: Wait for CCW Integration

The CCW workflow `/quotation generate slide` requires:
1. CCW framework to recognize `~/.claude/commands/workflow/` directory
2. SlashCommand integration to execute workflows
3. Proper session management setup

**This is not yet implemented** - it's a future enhancement.

---

## 💡 Recommendation

**For now, use**: `/quotation slide <template.md>`

**Reasons**:
1. ✅ **Works immediately** - No setup needed
2. ✅ **Tested and proven** - Original quotation_skill
3. ✅ **High quality output** - Professional slides
4. ✅ **Global availability** - Works from any directory

**Example**:
```bash
# Navigate to your template
cd /path/to/your/files

# Run the command
/quotation slide Leda_Inio_template.md

# Output:
# ✓ Leda_Inio_proposal.pptx
# ✓ Leda_Inio_proposal.pdf
```

---

## 📋 Complete Workflow Comparison

### Using `/quotation slide` (Current)

```bash
# Step 1: Generate template from Excel
/template DT_leda.xlsx

# Step 2: Fill placeholders (manual)
vim ./output/DT_leda_*/DT_leda_template.md

# Step 3: Generate slides
/quotation slide ./output/DT_leda_*/DT_leda_template.md

# Output:
# ./output/DT_leda_<timestamp>/DT_leda_proposal.pptx
# ./output/DT_leda_<timestamp>/DT_leda_proposal.pdf
```

### Using `/quotation generate slide` (Future)

```bash
# Same steps, but with better progress display:
/quotation generate slide ./output/DT_leda_*/DT_leda_template.md

# Would show:
# [Step 1/4] Create Output Directory [✓ COMPLETED]
# [Step 2/4] Generate HTML Slides [✓ COMPLETED]
# [Step 3/4] Generate PowerPoint [✓ COMPLETED]
# [Step 4/4] Generate PDF [✓ COMPLETED]
```

---

## 🎯 Summary

| Question | Answer |
|----------|---------|
| **Which command works now?** | `/quotation slide <template.md>` |
| **Which is simpler?** | Both are simple, but `/quotation slide` works now |
| **Which has better progress display?** | `/quotation generate slide` (when implemented) |
| **Can I use `/quotation slide` globally?** | ✅ Yes, from any directory |
| **Will `/quotation generate slide` work?** | ⚠️ Not yet, needs CCW integration |
| **What should I use?** | `/quotation slide <template.md>` (recommended) |

---

## 🔧 Technical Details

### Why `/quotation slide` Works Globally

**Skill Loading**:
```
~/.claude/skills/
├── quotation_skill/
│   └── SKILL.md  (name: quotation)
├── pptx/
│   └── SKILL.md  (name: pptx)
└── pdf/
    └── SKILL.md  (name: pdf)
```

Claude Code automatically:
1. Scans `~/.claude/skills/` directory
2. Reads SKILL.md from each subdirectory
3. Extracts `name` field from YAML frontmatter
4. Registers skill commands (`/quotation`, `/pptx`, `/pdf`)
5. Makes them available globally

### Why `/quotation generate slide` Doesn't Work Yet

**CCW Workflow Loading** (not fully implemented):
```
~/.claude/commands/workflow/
├── quotation/
│   └── generate-slide.md  (name: quotation-generate-slide)
```

CCW framework needs to:
1. Recognize workflows in `commands/workflow/`
2. Parse YAML frontmatter from workflow files
3. Register workflow commands with SlashCommand system
4. Execute workflows with TodoWrite integration
5. Handle state management and resumption

**This integration is not yet complete.**

---

## ✅ Final Recommendation

**Use this command**:

```bash
/quotation slide Leda_Inio_template.md
```

**Benefits**:
- ✅ Works globally right now
- ✅ No setup required
- ✅ Professional quality output
- ✅ Integrated with pptx and pdf skills
- ✅ Battle-tested and reliable

**Save `/quotation generate slide`** for future when CCW workflow integration is complete!
