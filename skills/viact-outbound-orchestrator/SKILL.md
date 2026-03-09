---
name: viact-outbound-orchestrator
description: Coordinates Google Sheets and Gmail for automated BD outreach with Human-in-the-Loop approval workflow. Reads approved leads from Google Sheets, sends emails via Gmail, checks for client replies, and updates sheet status.
---

## Configuration

**Setup script location:**
```bash
cd ~/.claude/skills/viact-outbound-orchestrator
python scripts/setup_config.py
```

**Configuration file** (use `~/.viact-orchestrator/` - expands to home directory):
- Config: `~/.viact-orchestrator/config.json`

### Virtual Environment

**⚠️ Important**: This skill has its own virtual environment at:
```
~/.claude/skills/viact-outbound-orchestrator/.venv
```

The `.venv` folder is **already set up** in the skill directory. When using this skill:
- ✅ Always use the existing `.venv` in `~/.claude/skills/viact-outbound-orchestrator/`
- ❌ Do NOT create a new virtual environment
- ❌ Do NOT install dependencies in a different location

**Dependencies are pre-installed** in the skill's `.venv`. Just activate and use:
```bash
source ~/.claude/skills/viact-outbound-orchestrator/.venv/bin/activate
```

## How It Works

The viAct Outbound Orchestrator automates your BD outreach workflow:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Read Google Sheet                                        │
│    - Parse spreadsheet URL to extract file ID               │
│    - Read all rows with column mappings                     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Filter Pending Approvals                                 │
│    - HITL_Approved = TRUE                                   │
│    - Status not in [Email Sent, Client Replied]             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Send Email via Gmail API                                 │
│    - New thread if no thread_id stored                      │
│    - Reply in thread if thread_id exists                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Update Google Sheet Status                               │
│    - Set Status = "Email Sent"                              │
│    - Add Sent Timestamp                                     │
│    - Add Thread ID                                          │
└─────────────────────────────────────────────────────────────┘
```

## Setup Instructions

### Step 1: Configure Google Sheets Access

Use the **google-drive skill** which includes Google Sheets support:

```bash
cd ~/.claude/skills/google-drive
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Configure Gmail Access

The orchestrator uses the **gmail skill** for email operations:

```bash
cd ~/.claude/skills/gmail
source .venv/bin/activate
pip install -r requirements.txt

# Run authentication setup
python scripts/setup_auth.py
```

### Step 3: Run Orchestrator Setup

```bash
cd ~/.claude/skills/viact-outbound-orchestrator
source .venv/bin/activate
pip install -r requirements.txt

# Run configuration setup
python scripts/setup_config.py
```

### Step 4: Configure openclaw Cron Jobs

```bash
bash ~/.claude/skills/viact-outbound-orchestrator/scripts/setup_cron.sh
```

This registers two cron jobs:
- **Send Pending Emails** — every 3 minutes
- **Check Client Replies** — every 10 minutes

## Configuration File Structure

Your `~/.viact-orchestrator/config.json` should look like:

```json
{
  "spreadsheet_url": "https://docs.google.com/spreadsheets/d/YOUR_ID/edit?gid=0#gid=0",
  "sheet_name": "Sheet1",
  "range": "A:AR",
  "column_mappings": {
    "lead_name": "B",
    "company": "T",
    "deal_id": "A",
    "email": "AR",
    "subject": "AL",
    "drafted_email": "AM",
    "hitl_approved": "AN",
    "status": "AO",
    "sent_timestamp": "AP",
    "message_id": "AQ"
  },
  "approved_values": ["TRUE", "true", "True", "YES", "yes", "Yes", "1"],
  "skip_statuses": ["Email Sent", "Client Replied", "Error"]
}
```

### Column Mappings

| Key | Description |
|-----|-------------|
| `lead_name` | Lead contact name |
| `company` | Company name |
| `deal_id` | Deal ID |
| `email` | Recipient email address |
| `subject` | Email subject |
| `drafted_email` | Drafted email content |
| `hitl_approved` | HITL approval status |
| `status` | Current status column |
| `sent_timestamp` | Sent timestamp (updated by orchestrator) |
| `message_id` | Gmail thread ID (updated by orchestrator) |

## Usage

### Run via Command Line

```bash
cd ~/.claude/skills/viact-outbound-orchestrator
source .venv/bin/activate

# Send approved emails
python skill/orchestrator.py send

# Check for client replies
python skill/orchestrator.py check-replies

# Check status
python skill/orchestrator.py status

# Sync Pipedrive leads to Google Sheet
python skill/sync_pipedrive_to_sheet.py --limit 100
```

### Run via Python

```python
import sys
sys.path.insert(0, '~/.claude/skills/viact-outbound-orchestrator/skill')

from orchestrator import send_pending_emails, check_client_replies
from sync_pipedrive_to_sheet import sync_pipedrive_to_sheet

results = send_pending_emails()
print(f"Emails sent: {results['emails_sent']}")

results = check_client_replies()
print(f"Replies found: {results['replied']}")

results = sync_pipedrive_to_sheet(limit=100)
print(f"Leads synced: {results['fetched']}")
```

## Available Functions
from sync_pipedrive_to_sheet import sync_pipedrive_to_sheet  # Sync Pipedrive leads to Google Sheet



from sync_pipedrive_to_sheet import sync_pipedrive_to_sheet  # Sync Pipedrive leads to Google Sheet

)
    send_pending_emails,     # Send emails for HITL-approved rows
    check_client_replies,    # Check for client replies on sent rows
    get_status,              # Get current status
    load_config,             # Load configuration
    column_letter_to_index,  # Convert A→0, B→1, etc.
    extract_column_value,    # Get value from row by column letter
    extract_lead_data,       # Extract lead data from row
    is_approved,             # Check if HITL approved
    should_skip,             # Check if should skip based on status
    update_row_status,        # Update sheet status (batched)
)
```

## Troubleshooting

### No Emails Being Sent

1. Check HITL_Approved column values (TRUE vs true vs True)
2. Verify Status column isn't in skip_statuses
3. Check config file path and contents
4. Review cron job logs for errors

### Client Replies Not Detected

1. Verify Gmail authentication is working
2. Check that thread_id is stored in the message_id column
3. Test `has_recent_reply()` function manually
4. Review Gmail thread structure

### Column Mapping Mismatch

Verify column mappings match your sheet layout and update `~/.viact-orchestrator/config.json` accordingly.

### Pipedrive Sync Function

The `sync_pipedrive_to_sheet()` function integrates your Pipedrive CRM with the Google Sheet:

**Features:**
- ✅ Fetches up to 100 newest leads from Pipedrive (sorted by update_time)
- ✅ Reads existing leads from the Google Sheet
- ✅ Uses upsert logic: updates existing leads by lead_id, adds new leads
- ✅ Maps Pipedrive lead fields to sheet columns automatically
- ✅ Sets default status to "Pending" for new leads
- ✅ Leaves email, drafted_email, and approval fields empty for manual review

**Field Mapping:**
| Pipedrive Field | Sheet Column | Description |
|----------------|---------------|-------------|
| id | A (deal_id) | Unique lead identifier for deduplication |
| title | B (lead_name) | Lead title/name |
| organization_name | T (company) | Company/organization name |
| - | AR (email) | Left empty (can be filled manually) |
| - | AL (subject) | Auto-generated: "Following up on: {title}" |
| - | AM (drafted_email) | Left empty (can be filled manually) |
| - | AN (hitl_approved) | Left empty (requires HITL approval) |
| - | AO (status) | Set to "Pending" for new leads |
| - | AP (sent_timestamp) | Left empty |
| - | AQ (message_id) | Left empty |

