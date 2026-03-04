    def _extract_timeline_milestones(self, content: str) -> List[Dict[str, Any]]:
        """Extract timeline milestones from multiple formats

        Supports:
        1. Markdown heading: ### Phase T0: Event Name
        2. Bold format: **Phase T0:** Event Name
        3. Various date/duration formats
        """
        milestones = []

        # Pattern 1: Markdown heading format - PRIMARY PATTERN for new templates
        # Format: ### Phase T0: Event Name
        # This is what Bromma and Leda templates use
        pattern_heading = r'^###\s+Phase\s+(T\d+):\s*(.+?)$'
        matches_heading = list(re.finditer(pattern_heading, content, re.IGNORECASE | re.MULTILINE))

        if matches_heading:
            for match in matches_heading:
                phase = match.group(1).strip()
                event_name = match.group(2).strip()

                # Find content after this heading
                start_pos = match.end()

                # Find next heading (### Phase, ###, ##, ---) or end of content
                next_phase_heading = re.search(r'^###\s+Phase\s+T\d+', content[start_pos:], re.MULTILINE)
                next_heading = re.search(r'^###', content[start_pos:], re.MULTILINE)
                next_section = re.search(r'^##', content[start_pos:], re.MULTILINE)
                next_separator = re.search(r'^---', content[start_pos:], re.MULTILINE)

                end_pos = len(content)
                if next_phase_heading:
                    end_pos = start_pos + next_phase_heading.start()
                elif next_heading:
                    end_pos = start_pos + next_heading.start()
                elif next_section:
                    end_pos = start_pos + next_section.start()
                elif next_separator:
                    end_pos = start_pos + next_separator.start()

                phase_content = content[start_pos:end_pos]

                # Extract duration - look for **Duration:** or **Duration:**
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

                # Extract activities/notes
                # Look for **Activities:** section
                activities_section = re.search(r'\*\*Activities:?\*\*', phase_content, re.IGNORECASE)
                notes = []

                if activities_section:
                    # Get content after Activities heading
                    activities_start = activities_section.end()
                    activities_content = phase_content[activities_start:]

                    # Extract bullet points
                    for line in activities_content.split('\n'):
                        line = line.strip()
                        if line.startswith('-') and not line.startswith('---'):
                            note = re.sub(r'^-\s*\*\*', '', line)
                            note = re.sub(r'\*\*', '', note).strip()
                            if note:
                                notes.append(note)
                        elif line and not line.startswith('**') and not line.startswith('#'):
                            # Non-empty line that's not a heading
                            note = re.sub(r'\*\*', '', line).strip()
                            if note and note not in notes:
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

        # Fallback: Original patterns for **Phase T0:** format (older templates)
        if not milestones:
            # Pattern 2: **Phase T0: Project Award** (with colon inside bold, event name in same bold)
            pattern1 = r'\*\*Phase\s+(T\d+):\s*([^*\n]+?)\*\*'
            matches1 = list(re.finditer(pattern1, content, re.IGNORECASE | re.MULTILINE))

            if not matches1:
                # Pattern 3: **Phase T0:** Event Name (colon inside bold, event on same or next line)
                pattern2 = r'\*\*Phase\s+(T\d+):\*\*\s*(.+?)(?=\*\*Phase|\*\*Total|---|\Z)'
                matches1 = list(re.finditer(pattern2, content, re.IGNORECASE | re.DOTALL))

            if not matches1:
                # Pattern 4: **Phase T0**: Event Name (colon outside bold)
                pattern3 = r'\*\*Phase\s+(T\d+)\*\*:\s*(.+?)(?=\n\*\*Phase|\n\*\*Total|\n---|\Z)'
                matches1 = list(re.finditer(pattern3, content, re.IGNORECASE | re.MULTILINE | re.DOTALL))

            for match in matches1:
                phase = match.group(1).strip()
                event_name = match.group(2).strip()

                # Find the section content after this phase header
                start_pos = match.end()
                # Look for next phase (with **Phase) or end of section
                # Also check for **Total Duration** or separator (---)
                next_phase = re.search(r'\*\*Phase\s+T\d+', content[start_pos:], re.IGNORECASE)
                next_duration = re.search(r'\*\*Total Duration', content[start_pos:], re.IGNORECASE)
                next_separator = re.search(r'\n\s*---\s*\n', content[start_pos:], re.IGNORECASE)

                end_pos = len(content)
                if next_phase:
                    end_pos = start_pos + next_phase.start()
                elif next_duration:
                    end_pos = start_pos + next_duration.start()
                elif next_separator:
                    end_pos = start_pos + next_separator.start()

                phase_content = content[start_pos:end_pos]

                # Extract date/duration - try multiple formats
                date = ""
                # Format 1: T1 = T0 + x weeks (full format)
                date_match = re.search(rf'{phase}\s*=\s*T\d+\s*\+\s*(.+?)(?:\n|$|\)|,|\.)', event_name + '\n' + phase_content, re.IGNORECASE)
                if date_match:
                    date = f"{phase} = {date_match.group(1).strip()}"
                else:
                    # Format 2: (T0 + x weeks) or T0 + x weeks
                    date_match = re.search(r'\(?\s*T\d+\s*\+\s*(.+?)\s*\)?', event_name + '\n' + phase_content, re.IGNORECASE)
                    if date_match:
                        prev_phase = f"T{int(phase[1:]) - 1}" if phase[1:].isdigit() else "T0"
                        date = f"{phase} = {prev_phase} + {date_match.group(1).strip()}"
                    else:
                        # Format 3: Just duration (e.g., "2-4 weeks") - construct full format
                        duration_match = re.search(r'(\d+\s*[-–]\s*\d+|\d+)\s*(weeks?|days?|months?)', phase_content, re.IGNORECASE)
                        if duration_match and phase != "T0":
                            prev_phase = f"T{int(phase[1:]) - 1}" if phase[1:].isdigit() else "T0"
                            date = f"{phase} = {prev_phase} + {duration_match.group(0).strip()}"

                # Extract notes (bullet points) from phase content
                notes = []
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

        # Last resort: **Phase T0** Event Name (colon outside bold, no colon after Phase)
        if not milestones:
            pattern2 = r'\*\*Phase\s+(T\d+)\*\*[:\s]+(.+?)(?:\n|\*\*)'
            matches2 = re.finditer(pattern2, content, re.IGNORECASE | re.DOTALL)

            for match in matches2:
                phase = match.group(1).strip()
                description = match.group(2).strip()

                # Extract date/duration - try multiple formats
                date = ""
                date_match = re.search(rf'{phase}\s*=\s*T\d+\s*\+\s*(.+?)(?:\n|$|\)|,|\.)', description, re.IGNORECASE)
                if date_match:
                    date = f"{phase} = {date_match.group(1).strip()}"
                else:
                    date_match = re.search(r'\(?\s*T\d+\s*\+\s*(.+?)\s*\)?', description, re.IGNORECASE)
                    if date_match:
                        prev_phase = f"T{int(phase[1:]) - 1}" if phase[1:].isdigit() else "T0"
                        date = f"{phase} = {prev_phase} + {date_match.group(1).strip()}"

                milestones.append({
                    "phase": phase,
                    "event": description.split('\n')[0] if '\n' in description else description,
                    "date": date,
                    "notes": []
                })

        return milestones
