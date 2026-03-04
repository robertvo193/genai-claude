# Timeline Parsing Fix - Technical Documentation

## Problem Identification

The current timeline parsing in `map_to_slides.py` fails because:

1. **Regex Pattern Mismatch**: Code searches for `**Phase T0:**` (bold markdown)
2. **Template Format**: Templates use `### Phase T0:` (markdown heading format)
3. **Result**: No milestones extracted, timeline slide is empty

## Root Cause

In `map_to_slides.py` line 734:
```python
pattern1 = r'\*\*Phase\s+(T\d+):\s*([^*\n]+?)\*\*'
```

This pattern expects:
- `**Phase T0: Event Name**` (bold formatting)

But templates have:
- `### Phase T0: Event Name` (markdown heading)

## Solution

Update `_extract_timeline_milestones()` function to handle BOTH formats:

1. **Primary Pattern**: Markdown heading format `### Phase T0:`
2. **Fallback Pattern**: Bold format `**Phase T0:**`
3. **Flexible Extraction**: Extract phase, event name, duration, and activities

## Implementation

Add new pattern at the beginning of `_extract_timeline_milestones()`:

```python
def _extract_timeline_milestones(self, content: str) -> List[Dict[str, Any]]:
    """Extract timeline milestones from multiple formats"""
    milestones = []

    # Pattern 1: Markdown heading format: ### Phase T0: Event Name
    # This is the PRIMARY pattern for new templates
    pattern_heading = r'^###\s+Phase\s+(T\d+):\s*(.+?)$'
    matches_heading = list(re.finditer(pattern_heading, content, re.IGNORECASE | re.MULTILINE))

    if matches_heading:
        for match in matches_heading:
            phase = match.group(1).strip()
            event_name = match.group(2).strip()

            # Find content after this heading
            start_pos = match.end()

            # Find next heading (### Phase, ###, ##, ---) or end
            next_heading = re.search(r'^###', content[start_pos:], re.MULTILINE)
            next_section = re.search(r'^##', content[start_pos:], re.MULTILINE)
            next_separator = re.search(r'^---', content[start_pos:], re.MULTILINE)

            end_pos = len(content)
            if next_heading:
                end_pos = min(end_pos, start_pos + next_heading.start())
            if next_section and next_section.start() < end_pos:
                end_pos = start_pos + next_section.start()
            if next_separator and next_separator.start() < end_pos:
                end_pos = start_pos + next_separator.start()

            phase_content = content[start_pos:end_pos]

            # Extract duration (look for **Duration:** or **Duration:**
            duration = ""
            duration_match = re.search(r'\*\*Duration:?\*\*:\s*(.+?)(?:\n|$)', phase_content, re.IGNORECASE)
            if duration_match:
                duration = duration_match.group(1).strip()
            else:
                # Try to find duration in event name (e.g., "(Weeks 1-2)")
                duration_match = re.search(r'\((Weeks?\s*[\d-]+)\)', event_name, re.IGNORECASE)
                if duration_match:
                    duration = duration_match.group(1)

            # Construct date string
            date = ""
            if duration and phase != "T0":
                # Calculate relative to previous phase
                prev_phase = f"T{int(phase[1:]) - 1}" if phase[1:].isdigit() else "T0"
                date = f"{phase} = {prev_phase} + {duration}"
            elif phase == "T0":
                date = "Project Start"

            # Extract activities as notes
            activities_section = re.search(r'\*\*Activities:?\*\*', phase_content, re.IGNORECASE)
            notes = []
            if activities_section:
                # Get content after Activities heading
                activities_start = activities_section.end()
                activities_content = phase_content[activities_start:]

                # Extract bullet points
                for line in activities_content.split('\n'):
                    line = line.strip()
                    if line.startswith('-'):
                        note = re.sub(r'^-\s*\*\*', '', line)
                        note = re.sub(r'\*\*', '', note).strip()
                        if note:
                            notes.append(note)
                    elif line and not line.startswith('**') and not line.startswith('#'):
                        # Non-empty line that's not a heading
                        if note := re.sub(r'\*\*', '', line).strip():
                            notes.append(note)
            else:
                # Fallback: extract all bullet points as activities
                for line in phase_content.split('\n'):
                    line = line.strip()
                    if line.startswith('-') and not line.startswith('---'):
                        note = re.sub(r'^-\s*\*\*', '', line)
                        note = re.sub(r'\*\*', '', note).strip()
                        if note:
                            notes.append(note)

            milestones.append({
                "phase": phase,
                "event": event_name,
                "date": date,
                "notes": notes
            })

    # Fallback to existing patterns if heading format not found
    if not milestones:
        # Original patterns for **Phase T0:** format
        # ... (existing code)

    return milestones
```

## Testing

After fix, timeline parsing should work for:

✅ **Markdown Heading Format** (Bromma, Leda templates):
```markdown
### Phase T0: Project Award / Contract Signed
- Contract finalization
- Project kickoff meeting
```

✅ **Bold Format** (older templates):
```markdown
**Phase T0:** Project Award
- Contract finalization
```

## Expected Output

For Bromma template, should extract:

```json
{
  "phase": "T0",
  "event": "Project Award / Contract Signed",
  "date": "Project Start",
  "notes": ["Contract finalization", "Project kickoff meeting", "Technical site survey"]
},
{
  "phase": "T1",
  "event": "Hardware Deployment (Weeks 1-2)",
  "date": "T1 = T0 + 2 weeks",
  "notes": ["Verification of existing 15 IP cameras", "RTSP stream testing", ...]
},
{
  "phase": "T2",
  "event": "Software Deployment (Weeks 3-8)",
  "date": "T2 = T1 + 6 weeks",
  "notes": ["Cloud AI software deployment", ...]
},
{
  "phase": "T3",
  "event": "Integration & UAT (Weeks 9-12)",
  "date": "T3 = T2 + 4 weeks",
  "notes": ["System integration testing", ...]
}
```

## Files to Update

1. `/home/philiptran/.claude/skills/template2slide-pro/scripts/map_to_slides.py`
   - Function: `_extract_timeline_milestones()` (line 727)
   - Add markdown heading pattern support

2. `/home/philiptran/.claude/skills/template2slide-pro/SKILL.md`
   - Update workflow to include PDF generation

3. `/home/philiptran/.claude/skills/template2slide-pro/references/subagent0_slide_agent_v2.md`
   - Add PDF generation step
   - Update timeline parsing documentation

## Verification

After fix:
1. Run template2slide.py on Bromma_template.md
2. Check that milestones array is NOT empty
3. Verify timeline slide has proper content
4. Confirm all 4 phases (T0-T3) are displayed
5. Check anti-overlap logic is applied
