---
name: pipedrive-export
description: Export Pipedrive deals with email threads to Excel and Google Sheets. Use when exporting CRM data, generating sales reports, or backing up deal communication history.
argument-hint: "[--days <n>] [--deal-id <id>] [--format <excel|sheets|both>] [--output <path>]"
---

# Pipedrive Export

Export Pipedrive deals with full email threads to Excel and/or Google Sheets.

## Execution

SKILL_DIR="$HOME/.claude/skills/pipedrive-export"
OUTPUT_DIR="${OUTPUT_DIR:-$(pwd)}"  # Default to current directory
cd "$SKILL_DIR" && PIPEDRIVE_API_TOKEN="$PIPEDRIVE_API_TOKEN" node --import tsx scripts/export.ts $ARGUMENTS --output "$OUTPUT_DIR"

## Quick Start

```bash
# Default: last 90 days, both Excel + Google Sheets, output to current directory
/pipedrive-export

# Last 7 days only
/pipedrive-export --days 7

# Export specific deal (bypasses date filter)
/pipedrive-export --deal-id 2054

# Excel only (no Google Sheets upload)
/pipedrive-export --format excel

# Custom output directory
/pipedrive-export --output ./my-exports
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--days <n>` | `90` | Days to look back for deals |
| `--deal-id <id>` | `null` | Export specific deal only |
| `--format <type>` | `both` | Output: `excel`, `sheets`, or `both` |
| `--output <path>` | `./query-results` | Output directory (current dir if not specified) |

## Output

- **Excel**: Summary sheet + per-deal sheets with email threads
- **Google Sheets**: Same as Excel, "anyone with link can edit" permission
- **JSON backup**: Complete data without truncation

## Requirements

- `PIPEDRIVE_API_TOKEN` in `~/.bashrc` (persisted)
- `~/.gdrivelm/` configured (for Google Sheets upload)
