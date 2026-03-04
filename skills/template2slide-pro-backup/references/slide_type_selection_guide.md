# Slide Type Selection Guide

## Overview

This guide provides intelligent decision-making logic for selecting appropriate slide types based on content characteristics. The agent should analyze each section and choose the optimal slide type dynamically.

## Core Principles

1. **Content-First Approach**: Analyze content characteristics, not just section names
2. **Flexibility**: Adapt slide type to content length and structure
3. **Readability**: Choose slide type that best presents information
4. **Consistency**: Maintain visual consistency across presentation

## Slide Type Decision Matrix

| Content Characteristics | Optimal Slide Type | Rationale |
|------------------------|-------------------|-----------|
| Title + minimal metadata | `title` | Clean, centered focus |
| Text-heavy with hierarchy | `content_bullets` | Bullet points for structure |
| Two distinct categories | `two_column` | Side-by-side comparison |
| Visual diagram needed | `diagram` | Large image/diagram display |
| Temporal sequence | `timeline` | Horizontal visualization |
| Individual item details | `module_description` | Text + media split |

## Detailed Slide Type Guidelines

### 1. Title Slide (`title`)

**Use When**:
- Cover page with project title
- Minimal metadata (client, date)
- Section divider slides (optional)

**Content Characteristics**:
- Primary: Large title text
- Secondary: Date, client name (optional)
- No body content

**Decision Logic**:
```python
if section_name == "Cover Page" or section_name == "COVER PAGE":
    return "title"
```

**Example**:
```markdown
## COVER PAGE
**Proposal Title:** Video Analytics Solution for Client
**Client Name:** ABC Corporation
**Date:** January 2026
```

---

### 2. Content Bullets Slide (`content_bullets`)

**Use When**:
- Hierarchical information (main points + sub-points)
- Lists, specifications, requirements
- Text-heavy content with clear structure
- Multiple related items

**Content Characteristics**:
- 5-15 bullet points
- Multiple levels (0, 1, 2)
- Key-value pairs (e.g., "Processor: Intel Xeon")
- Can be grouped logically

**Decision Logic**:
```python
def should_use_content_bullets(section_content):
    # Check for list-like structure
    has_bullet_points = count_items(section_content) >= 5
    has_hierarchy = detect_nested_structure(section_content)
    is_text_heavy = len(section_content) > 200 and len(section_content) < 1500

    return has_bullet_points or has_hierarchy or is_text_heavy

# Apply to sections
if section_name in ["Project Requirement", "System Requirements",
                   "User Interface", "Camera Specifications"]:
    if should_use_content_bullets(content):
        return "content_bullets"
```

**Examples**:

**Simple Bullet List**:
```markdown
## Project Requirement Statement
**Project:** AI-based video analytics
**Project Owner:** ABC Corp
**Duration:** 6 months
**Cameras:** 10
**AI Modules:**
- Helmet Detection
- Safety Vest Detection
- Fire Detection
```

**Hierarchical Content**:
```markdown
## System Requirements: AI Workstation
**Processor:** Intel Xeon
**GPU:** NVIDIA RTX 4070
**RAM:** 32GB DDR4
**Storage:**
- 500GB NVMe SSD (OS)
- 1TB SSD (Data)
**Network:** 10GbE NIC
```

**Key-Value Specifications**:
```markdown
## Network Requirements
**External Internet:**
- Minimum: 50 Mbps
- Purpose: System updates

**Internal Network:**
- Per-camera: 12 Mbps
- Total: 120 Mbps
- Switch: Gigabit Ethernet
```

**Combination Logic** (IMPORTANT):
```python
# Combine short related sections
network_items = count_items("Network Requirements")
camera_items = count_items("Camera Specifications")

if network_items <= 3 and camera_items <= 3:
    return "content_bullets"  # Combined slide
    title = "System Requirements: Network & Camera"
else:
    return "content_bullets"  # Separate slides
    # Two separate content_bullets slides
```

**When to Combine**:
- Both sections have ≤ 3 items each
- Content is related (infrastructure specifications)
- Combined slide is not overcrowded

**When to Separate**:
- Either section has > 6 items
- Content is complex or detailed
- Would result in text overflow

---

### 3. Two Column Slide (`two_column`)

**Use When**:
- Two distinct categories or perspectives
- Comparison or contrast needed
- Side-by-side information
- Responsibilities/roles split

**Content Characteristics**:
- Clear dichotomy (A vs B)
- Parallel structure
- Balanced content (not lopsided)

**Decision Logic**:
```python
if section_name == "Scope of Work" or section_name == "SCOPE OF WORK":
    return "two_column"

# Check for comparison structure
if has_two_clear_categories(content):
    category_ratio = calculate_balance(content)
    if 0.4 <= category_ratio <= 0.6:  # Balanced (40-60 split)
        return "two_column"
```

**Example**:
```markdown
## SCOPE OF WORK

### viAct Responsibilities
- Software licensing
- System deployment
- Technical support

### Client Responsibilities
- Hardware procurement
- Network infrastructure
- Site access
```

**Alternative Two-Column Uses**:
- Before/After comparisons
- Option A vs Option B
- Current vs Proposed
- viAct vs Client (most common)
- On-Premise vs Cloud
- Hardware vs Software

**When NOT to Use**:
- Content is highly unbalanced (e.g., 1 item vs 10 items)
- No natural dichotomy exists
- Content fits better in bullet format

---

### 4. Diagram Slide (`diagram`)

**Use When**:
- Visual representation needed
- System architecture
- Flowcharts, network diagrams
- Complex relationships

**Content Characteristics**:
- Mermaid diagram code present
- References components/connections
- Visual is primary content

**Decision Logic**:
```python
if section_name == "System Architecture" or section_name == "SYSTEM ARCHITECTURE":
    return "diagram"

if contains_mermaid_code(content):
    return "diagram"

if describes_system_flow(content):
    return "diagram"
```

**Example**:
```markdown
## SYSTEM ARCHITECTURE

**Deployment Method:** On-Premise

**Components:**
- 10 IP Cameras
- NVR
- AI Inference Workstation
- Dashboard

**Flow:** Cameras → NVR → AI System → Dashboard → Alerts
```

**Diagram Generation**:
1. Extract deployment method (On-Premise/Cloud)
2. Identify components
3. Determine flow direction
4. Generate Mermaid code
5. Convert to PNG (transparent background)
6. Embed as full-width image

**Slide Structure**:
- Title: "Proposed System Architecture"
- Content: Large diagram image (80-90% of slide)
- Optional: Brief description text below diagram

---

### 5. Timeline Slide (`timeline`)

**Use When**:
- Sequential phases or milestones
- Temporal information
- Project schedule/roadmap

**Content Characteristics**:
- Named phases (T0, T1, T2, etc.)
- Events or activities per phase
- Dates or durations
- Sequential progression

**Decision Logic**:
```python
if section_name == "Implementation Plan" or section_name == "Timeline":
    return "timeline"

if detect_timeline_structure(content):
    # Look for: Phase T0, T1, T2 + events + dates
    return "timeline"
```

**Example**:
```markdown
## IMPLEMENTATION PLAN

### Phase T0: Project Award
- Contract signed
- Kickoff meeting
- Site survey

### Phase T1: Hardware Deployment (Weeks 1-2)
**Duration:** 2 weeks
- Camera installation
- Workstation setup
- Network configuration

### Phase T2: Software Deployment (Weeks 3-6)
**Duration:** 4 weeks
- Software installation
- AI model training
- System testing
```

**Timeline Visualization (FIXED)**:
- Horizontal timeline axis
- Milestones as markers on axis
- Staggered label heights (4 positions) to prevent overlap:
  - Position 1 (far-top): Event at -80pt, Phase/Date at -40pt
  - Position 2 (near-top): Event at -80pt, Phase/Date at -40pt
  - Position 3 (near-bottom): Event at +30pt, Phase/Date at +60pt
  - Position 4 (far-bottom): Event at +30pt, Phase/Date at +60pt
- Alternating above/below for even spacing

**Critical Requirements**:
- ✅ No text overlap
- ✅ All milestones visible
- ✅ Readable event names (word-wrap if needed)
- ✅ Clear phase identifiers (T0, T1, T2...)
- ✅ Date/duration information visible

---

### 6. Module Description Slide (`module_description`)

**Use When**:
- Individual module details
- Text + media combination
- Structured module information

**Content Characteristics**:
- Module name
- Module type (Standard/Custom)
- Purpose description
- Alert trigger logic
- Preconditions
- Detection criteria (if custom)
- Data requirements (if custom)
- Image or video URL

**Decision Logic**:
```python
if section_name.startswith("Module") or "MODULE" in section_name:
    return "module_description"

if has_module_structure(content):
    # Check for: purpose, alert_logic, preconditions
    return "module_description"
```

**Example**:
```markdown
### Module 1: Helmet Detection

**Module Type:** Standard

**Purpose Description:** Ensures compliance with safety regulations

**Alert Trigger Logic:** AI will capture people not wearing helmet

**Preconditions:** Camera distance 5-10 meters

**Video URL:** https://drive.google.com/file/d/...
```

**Slide Structure**:
- **Left side (50-60%)**:
  - Module name (title)
  - Module type (badge/label)
  - Purpose: Description
  - Alert Logic: Logic
  - Preconditions: Conditions
  - Detection Criteria: Criteria (if custom)

- **Right side (40-50%)**:
  - Video or image
  - Video priority: video_url → image_url → blank
  - Proper aspect ratio
  - Centered vertically

**One Slide Per Module**:
- ❌ Do NOT group multiple modules on one slide
- ✅ Each module gets its own dedicated slide
- ✅ Ensures sufficient space for details + media

---

## Advanced Decision Logic

### Section Combination Rules

**Network + Camera Requirements**:
```python
network_items = extract_items("Network Requirements")
camera_items = extract_items("Camera Specifications")

# Combine if both are short
if len(network_items) <= 3 and len(camera_items) <= 3:
    create_combined_slide(
        title="System Requirements: Network & Camera",
        left_section="Network Requirements",
        right_section="Camera Specifications",
        layout="two_column"  # or "content_bullets" with subheadings
    )
else:
    create_separate_slides()
```

**Workstation Specifications**:
```python
workstations = ["AI Training", "AI Inference", "Dashboard"]
total_specs = sum([count_items(ws) for ws in workstations])

# Combine all workstations if total specs ≤ 8
if total_specs <= 8:
    create_combined_slide(
        title="System Requirements: Workstations",
        layout="content_bullets",  # Group by workstation type
        sections=workstations
    )
else:
    # Create separate slides or group strategically
    if training_specs + inference_specs <= 10:
        combine_training_and_inference()
```

### Content Length Classification

```python
def classify_content_length(content):
    item_count = count_items(content)
    char_count = len(content)

    if item_count <= 3:
        return "short"
    elif item_count <= 6:
        return "medium"
    else:
        return "long"

# Apply classification
length = classify_content_length(section_content)

if length == "short":
    # Consider combining with another short section
    consider_combination()
elif length == "medium":
    # Standard slide
    create_standard_slide()
else:  # long
    # May need multiple slides or condensed formatting
    consider_multi_slide()
```

### Adaptive Layout Selection

```python
def select_optimal_layout(section_name, content):
    content_type = analyze_content_type(content)
    content_length = classify_content_length(content)
    has_media = check_for_media(content)

    # Decision tree
    if section_name == "Cover Page":
        return "title"

    elif section_name == "Scope of Work":
        return "two_column"

    elif section_name == "System Architecture":
        return "diagram"

    elif section_name == "Implementation Plan":
        return "timeline"

    elif section_name.startswith("Module"):
        return "module_description"

    elif content_type == "comparison" and is_balanced(content):
        return "two_column"

    elif has_media and content_length == "short":
        return "module_description"  # Even for non-modules

    elif content_type == "list" or content_type == "hierarchical":
        if should_combine_with_neighbor(section_name):
            return "combined_content_bullets"
        else:
            return "content_bullets"

    else:
        return "content_bullets"  # Default
```

---

## Special Cases

### Empty or Minimal Content

```python
if is_empty_or_minimal(content):
    # Option 1: Skip the slide entirely
    skip_slide()

    # Option 2: Merge with adjacent section
    merge_with_adjacent()

    # Option 3: Create minimal bullet slide
    create_minimal_slide()
```

### Very Long Content

```python
if is_very_long(content):  # > 15 items or > 2000 chars
    # Option 1: Split into multiple slides
    split_into_multiple_slides()

    # Option 2: Condense formatting
    use_condensed_format()

    # Option 3: Group by subcategory
    group_and_condense()
```

### Mixed Content Types

```python
if has_mixed_content_types(content):
    # Contains bullets + table + diagram

    # Choose primary type based on dominance
    primary_type = identify_dominant_type(content)

    # Incorporate secondary types
    if primary_type == "diagram":
        # Add bullet summary below diagram
        create_diagram_with_bullets()
    elif primary_type == "bullets":
        # Add small inline diagram
        create_bullets_with_mini_diagram()
```

---

## Decision Checklist

For each section, ask:

1. **What is the primary content type?**
   - Text hierarchy → `content_bullets`
   - Two categories → `two_column`
   - Visual diagram → `diagram`
   - Timeline → `timeline`
   - Module details → `module_description`

2. **How long is the content?**
   - Short (≤3 items) → Consider combining
   - Medium (4-6 items) → Standard slide
   - Long (>6 items) → May need multiple slides

3. **Is there a natural split?**
   - Yes (viAct vs Client) → `two_column`
   - No → Use single column format

4. **Are there media elements?**
   - Yes → `module_description` or `diagram`
   - No → Text-based slide type

5. **Should this combine with adjacent section?**
   - Both short and related → Combine
   - One long or unrelated → Keep separate

---

## Example Flow

```
Input: Template with 7 sections

Section 1: Cover Page
  → Analyze: Title + metadata
  → Decision: title

Section 2: Project Requirement
  → Analyze: 10 bullet points, hierarchical
  → Decision: content_bullets

Section 3: Scope of Work
  → Analyze: viAct vs Client split
  → Decision: two_column

Section 4: System Architecture
  → Analyze: Describes components + flow
  → Decision: diagram

Section 5: System Requirements
  → Analyze: Network (3 items) + Camera (2 items)
  → Decision: Combined content_bullets (short content)

Section 6: Implementation Plan
  → Analyze: T0, T1, T2 phases with events
  → Decision: timeline

Section 7: Proposed Modules (5 modules)
  → Analyze: 5 individual modules with media
  → Decision: 5 × module_description (one per module)

Total: 10 slides (not including title)
```

---

## Quality Checks

After selecting slide types, verify:

- ✅ All sections assigned a slide type
- ✅ No orphaned content
- ✅ Logical flow of information
- ✅ Balanced presentation (not too text-heavy in one area)
- ✅ Appropriate slide count (typically 12-20 for full proposal)
- ✅ Media assets available for chosen slide types
- ✅ Timeline has anti-overlap protection
- ✅ Combined sections are truly related
