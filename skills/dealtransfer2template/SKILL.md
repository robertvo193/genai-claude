---
name: dealtransfer2template
description: Generate technical proposals from Deal Transfer Excel files and Knowledge base. Use when user provides Deal Transfer document or asks to generate proposal. Creates template, reasoning, and checklist files following viAct proposal structure.
---

# Deal Transfer to Template

Generate technical proposals from Deal Transfer Excel files (Commercial Sheet S1 and Technical Sheet S2) and Knowledge Base references.

## Workflow

1. Extract Deal Transfer data from Excel (S1 and S2 sheets)
2. Generate template file with clean proposal content
3. Generate reasoning file with source references and logic
4. Generate checklist file with placeholders for presale confirmation

## Output Files

Create three separate files:

1. **`[Project_Name]_template.md`**: Clean proposal content (no source references, no reasoning)
2. **`[Project_Name]_reasoning.md`**: Source references, mapping logic, and reasoning
3. **`[Project_Name]_checklist.md`**: Placeholders requiring presale confirmation

## Process

### Extract Deal Transfer Data

Extract from Excel using field names from `references/FIELD_NAMES_REFERENCE.md`:
- **Commercial Sheet (S1)**: Customer info, pain points, timeline, camera status
- **Technical Sheet (S2)**: Use cases, deployment method, requirements

**Extraction methods:**
- Run `python scripts/extract_deal_transfer.py <excel_file>`
- Or use pandas: `pd.read_excel(file, sheet_name='Commercial')` and `sheet_name='Technical'`

### Generate Template File

Fill all sections from `references/TEMPLATE.md` using extracted data.

**CRITICAL: Template file MUST contain ONLY clean proposal content**

**Template rules:**
- **ONLY proposal content** (text, numbers, descriptions that go to the client)
- **Clean, professional language** - no meta-commentary or explanations
- **Pure markdown format** - NO HTML tags (no `<br>`, `<br/>`, `<table>`, etc.)
- Use markdown formatting: bullet points (`-`), bold (`**text**`), headers (`##`), plain text
- Estimated values with placeholder IDs: `[Estimated Value] [PLACEHOLDER_ID]` (e.g., `30 Mbps [NETWORK_001]`)
- **NO source references** (no "S1 - Field name", "from S2", etc.)
- **NO reasoning explanations** (no "Based on...", "Logic: ...", "because...")
- **NO mapping details** (no "Extracted from...", "Calculated as...", "using...")
- **NO parentheses explaining sources** (e.g., avoid "(9 cameras)" unless it's the actual value)

**What BELONGS in Template:**
- ✅ Final values: "9 IP cameras"
- ✅ Descriptions: "Detects workers wearing safety helmets"
- ✅ Specifications: "1080p (1920×1080) minimum @ 25fps"
- ✅ Lists: Bullet points of modules, requirements, etc.

**What DOES NOT BELONG in Template:**
- ❌ Source references: "S1 - Customer overview", "from S2", "extracted from..."
- ❌ Reasoning: "Based on standard practices", "assuming client requires..."
- ❌ Explanations: "(9 cameras)", "(15 cameras × 8-10 Mbps)", "because S2 indicates..."
- ❌ Calculations shown: "120-150 Mbps (15 cameras × 8-10 Mbps per camera)"
- ❌ Meta-comments: "Note: Client already has cameras installed"

**CRITICAL: Project Requirement Statement Format**

Section 2 must use this exact format (all fields at same level using `**Field:**` format):

```
## 2. PROJECT REQUIREMENT STATEMENT

**Project:** AI-Powered Video Analytics for [Short Description of Main Objective]

**Project Owner:** [Client Name]

**Work Scope:** [Deployment method] AI system to [general objective]

**Project Duration:** [X months/years]

**Camera Number:** [X cameras]

**AI Modules per Camera:** [X modules per camera]

**AI Modules:**
1. [Module Name 1]
2. [Module Name 2]
...
```

**Key Requirements:**
- **Project field MUST be ONE SHORT SENTENCE** (e.g., "AI-Powered Video Analytics for Safety Compliance and Incident Prevention")
  - DO NOT use long descriptions with multiple sentences
  - Keep it concise like the examples: "AI-Powered Video Analytics Pilot for Safety Enhancement"
- **All fields MUST use `**Field:** Value` format** - NOT subheadings (`###`)
- **All fields are at the same hierarchical level** (no nesting, no subheadings)
- **Project Owner** must be extractable by parser (supports both `**Project Owner:**` and `**Client Name:**`)
- **DO NOT merge AI modules** - List each module separately
  - ❌ WRONG: "PPE Detection (Safety Helmet, Safety Mask, Safety Vest)"
  - ✅ CORRECT: "1. Safety Helmet Detection" / "2. Safety Mask Detection" / "3. Safety Vest Detection"
  - Each module from STANDARD_MODULES.md should be listed as a separate item
  - Exception: Only group under one module name if it's explicitly listed as a single module in STANDARD_MODULES.md (e.g., "PPE Detection" if it exists as one entry)

### Generate Reasoning File

Document ALL reasoning, sources, and logic that should NOT appear in the template:
- Source references (S1/S2 field names from `references/FIELD_NAMES_REFERENCE.md`)
- Mapping logic and calculations
- KB references used
- Reasoning for estimates
- Alternative options considered
- All "why" and "how" decisions

**Purpose of Reasoning File:**
- Complete audit trail of how template values were determined
- All meta-information, calculations, and sources
- Presale can review the reasoning behind each template value
- Transparency in decision-making process

### Generate Checklist File

For each placeholder, add entry:
- ID | Section | Item | Content estimated | presale's Answer

### Handle Missing Information

When information is missing:
1. Make reasonable estimates based on standard viAct practices, similar projects in KB, or industry standards
2. Format in template: `[Estimated Value] [PLACEHOLDER_ID]`
3. Document in reasoning file why it was estimated
4. Add to checklist for presale confirmation

## Resources

Load as needed:

- **`references/TEMPLATE.md`**: Proposal structure with source/guidance for each section
- **`references/STANDARD_MODULES.md`**: Standard AI modules list - check if module is standard or custom
- **`references/FIELD_NAMES_REFERENCE.md`**: Exact field names from S1 and S2 sheets
- **`references/Logic_for_Determining_List_of_AI_Modules_from_VA_usecases_and_Client_Painpoint.md`**: Logic for determining AI modules from vague use cases
- **`scripts/extract_deal_transfer.py`**: Extract and parse Deal Transfer Excel files
- **`scripts/validate_output.py`**: Validate generated proposal format

## Content Rules

### Template File - ONLY Client-Facing Content
- **ONLY proposal content** that would be sent to a client
- Pure markdown format - NO HTML tags (no `<br>`, `<br/>`, `<table>`, etc.)
- Use markdown formatting: bullet points, bold text, headers, plain text
- Show estimated values with placeholder IDs: `[Value] [ID]`
- **NO source references** (no "S1 -", "S2 -", "from KB", etc.)
- **NO reasoning** (no "because", "based on", "due to", etc.)
- **NO calculations shown** (just the final result)
- **NO meta-comments** (no "Note:", "Reminder:", etc.)
- **NO parentheses with explanations** (unless part of the actual value)

**Examples of GOOD Template Content:**
- ✅ "9 IP cameras"
- ✅ "120-150 Mbps [NETWORK_001]"
- ✅ "Detects workers wearing safety helmets"
- ✅ "Cloud-based AI system to monitor workplace safety compliance"

**Examples of BAD Template Content (these go in Reasoning, NOT Template):**
- ❌ "9 IP cameras (from S1)"
- ❌ "120-150 Mbps (15 cameras × 8-10 Mbps per camera)"
- ❌ "Detects workers wearing safety helmets (from STANDARD_MODULES.md)"
- ❌ "Cloud-based AI system to monitor workplace safety compliance (because S2 indicates cloud deployment)"
- ❌ "Note: Client already has cameras installed"

### Reasoning File - ALL Sources and Logic
- **ALL source references** (S1/S2 field names, KB references)
- **ALL mapping logic and calculations** (show the math)
- **ALL KB references** (document which KB articles were used)
- **ALL reasoning** (explain WHY each decision was made)
- **ALL explanations** for placeholders and estimates
- **Complete audit trail** for every value in the template

### Checklist File - Placeholders Only
- All placeholders with estimated values
- Format: ID | Section | Item | Content estimated | presale's Answer
- Brief explanation of why each placeholder was created
- Questions for presale confirmation

## Generation Guidelines

**IMPORTANT: Keep Template and Reasoning COMPLETELY SEPARATE**

1. **Template File = Client Proposal** (what the customer sees)
   - Clean, professional proposal
   - Final values only (no calculations shown)
   - No explanations of sources or reasoning
   - Ready to send to client

2. **Reasoning File = Internal Documentation** (what presale/internal team sees)
   - Complete audit trail
   - All sources, calculations, and logic
   - All "why" and "how" decisions
   - For internal review and validation

**Example Comparison:**

**In Template (what client sees):**
```
## 5. SYSTEM REQUIREMENTS

### Network Requirements

**Internet Bandwidth:**
- **Per-Camera Bandwidth**: 8-10 Mbps/camera
- **Total System Bandwidth**: 120-150 Mbps [NETWORK_001]
```

**In Reasoning (what internal team sees):**
```
## 5. SYSTEM REQUIREMENTS

### Network Requirements

**Source**: S2 - "Does client have stable internet connection?" = "Yes"
**Deployment**: Cloud (from S2)
**Calculation**:
- Per-camera bandwidth: 8-10 Mbps (standard for cloud streaming)
- Total: 8-10 Mbps × 15 cameras = 120-150 Mbps
- **Value**: "120-150 Mbps [NETWORK_001]"
**Reasoning**: Standard cloud bandwidth calculation based on KB references
**KB Reference**: "Network Requirements - Cloud Deployment"
```

---

**Core Principles:**

1. Extract from Deal Transfer first before making estimates
2. Never leave sections empty - make best estimate and use placeholder
3. Use standard module names from `references/STANDARD_MODULES.md` when available
4. Include Image URL and Video URL for standard modules (extract from `references/STANDARD_MODULES.md`, use URL if available or `""` if empty)
5. Convert pain points/VA use cases to AI modules (see `references/Logic_for_Determining_List_of_AI_Modules_from_VA_usecases_and_Client_Painpoint.md`)
6. Calculate timeline realistically - include ALL phases: T0, T1 (Hardware Deployment), T2 (Software Deployment), T3 (Integration & UAT)
   - **T1 is REQUIRED even if cameras already installed** (1-2 weeks for verification if cameras exist, 2-4 weeks if new installation)
7. Use concrete numbers and details
8. Maintain consistency - camera numbers, module counts consistent across sections
9. Document everything in reasoning file for traceability
10. Keep Work Scope concise - ONE short sentence: `[Deployment method] AI system to [general objective]` (do NOT list specific modules)
    - Example: "Cloud-based AI system to monitor workplace safety compliance in real time"
    - Example: "On-premise AI system to enhance operational efficiency and safety"
    - Keep it compact - avoid lengthy descriptions or detailed feature lists
11. **Keep Project field concise** - ONE short sentence summarizing the main objective (e.g., "AI-Powered Video Analytics for Safety Compliance and Incident Prevention")
    - Extract essence from pain points but keep it brief
    - Examples: "AI-Powered Video Analytics Pilot for Safety Enhancement", "AI-Powered Video Analytics for Safety Compliance and Workforce Monitoring"
12. **Use consistent field format** - All PROJECT REQUIREMENT STATEMENT fields must use `**Field:** Value` format at the same level
13. **DO NOT merge or group AI modules** - List each module separately as individual items
    - Check STANDARD_MODULES.md for exact module names
    - Each PPE item (Helmet, Mask, Vest) should be separate modules, not grouped as "PPE Detection"
    - Exception: Only use the exact module name if it exists as a single entry in STANDARD_MODULES.md
14. **Skip workstation specifications for Cloud deployment** - Only include Network and Camera specs
15. **Skip Power Requirements for Cloud deployment**
16. **Section 8 (User Interface & Reporting) - ONLY include if custom requirements exist**:
    - **Include Section 8 IF**: S2 - "Any customized dashboard?" has content (custom KPIs, multi-dashboard, custom reporting)
    - **Include Section 8 IF**: S2 - "How do they want to alert operators on-site?" mentions non-standard channels (VMS, on-site alarms, beyond Dashboard/Email/Telegram/SMS)
    - **Skip Section 8 IF**: S2 - "Any customized dashboard?" = "no" or blank AND alert channels are only standard (Dashboard, Email, Telegram)
17. **For Standard AI Modules - Extract ALL information from STANDARD_MODULES.md**:
    - Purpose Description
    - Alert Trigger Logic
    - Preconditions
    - Image URL (use exact URL from STANDARD_MODULES.md, or "" if empty)
    - Video URL (use exact URL from STANDARD_MODULES.md, or "" if not available)

## Quality Checks

**Template file:**
- All sections from `references/TEMPLATE.md` filled (EXCEPT Section 8 - see guideline #16)
- No sections completely empty
- Clean proposal language (no source references)
- Pure markdown format - NO HTML tags (no `<br>`, `<br/>`, `<table>`, etc.)
- Placeholder IDs present for uncertain items
- Module names match `references/STANDARD_MODULES.md` when standard
- Timeline includes ALL phases (T0, T1, T2, T3)
- Timeline calculations logical (consider camera status, standard vs custom modules)
- Architecture matches deployment method
- Responsibilities clearly divided
- Consistent numbers across sections
- **Standard AI Modules include ALL fields from STANDARD_MODULES.md**:
  - Purpose Description (exact text from KB)
  - Alert Trigger Logic (exact text from KB)
  - Preconditions (exact text from KB)
  - Image URL (exact URL from KB, or "" if empty)
  - Video URL (exact URL from KB, or "" if not available)
- **Section 8 included ONLY if custom requirements exist** (per guideline #16)
- **Project Requirement Statement uses correct format:**
  - Project field is ONE short sentence (not multi-sentence description)
  - All fields use `**Field:** Value` format (not `###` subheadings)
  - All fields at same hierarchical level
  - Project Owner field extractable by parser

**Reasoning file:**
- Every section has corresponding reasoning entry
- All S1/S2 references use field names from `references/FIELD_NAMES_REFERENCE.md`
- All KB references documented
- All calculations shown
- All placeholders explained

**Checklist file:**
- All placeholders from template listed
- Estimated values clearly shown
- Format matches required structure

## Next Steps

After generating files:
1. Presale reviews `[Project_Name]_checklist.md` and fills answers
2. Use `proposal-checklist-update` skill to update template with confirmed values
3. Proceed to next workflow step (e.g., slide-content-mapper)
