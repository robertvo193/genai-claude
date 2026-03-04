# Architecture Diagram Generation Guide

## Overview

quotation_skill now includes **automatic architecture diagram generation** from template.md files.

## Workflow

```
template.md -> Extract Data -> Mermaid Code -> PNG -> HTML Slide -> PowerPoint
```

## Files Created

1. **scripts/generate_architecture_diagram.py** - Mermaid generator (Python)
2. **scripts/mermaid_to_png.js** - PNG converter (Node.js)

## Quick Start

### Step 1: Generate Mermaid Code

```python
from scripts.generate_architecture_diagram import SimpleArchitectureGenerator

generator = SimpleArchitectureGenerator(
    deployment_method='on-prem',
    num_cameras=9,
    ai_modules=['Helmet Detection', 'Safety Mask Detection', 'Hi-vis vest detection',
                'Fire & Smoke Detection', 'Human Down Detection']
)

mermaid_code = generator.generate()
```

### Step 2: Convert to PNG

```bash
mmdc -i architecture.mmd -o architecture.png -b transparent -t dark
```

### Step 3: Insert in HTML Slide

Use diagram template with image reference.

## Features

- No JSON, no regex - simple Python
- Compact mode for space-saving
- viAct branding colors
- Transparent background
- Dark theme

## Testing

✅ Tested with Leda Inio (9 cameras, 5 modules, on-premise)
