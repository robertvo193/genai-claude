# viAct Outbound Orchestrator Skill

A semi-autonomous BD outreach engine that connects **Pipedrive data (via Google Sheets)** to a **Gmail-capable Claude Agent**. It automates email sending with a mandatory **Human-in-the-Loop (HITL)** approval gate — keeping the personal touch while removing 90% of the friction.

---

## What This Skill Does

This is **Phase 1 of viAct's BD automation pipeline**. It bridges three systems:

```
Pipedrive / Google Sheets  →  HITL Review  →  Gmail  →  Status Update
  (leads + draft emails)       (BD Lead)      (send)     (sheet + Pipedrive)
```

### The Agent Architecture

#### 1. Reader Module
- Reads from Google Sheets: `Lead Name`, `Company`, `Pipedrive Deal ID`, `Sales Strategy`, `Drafted Email`
- **Filters only rows where `HITL_Approved = TRUE`** — nothing sends without human sign-off

#### 2. Context-Aware Gmail Module
- Before sending, checks the email thread for the lead
- If the **client has replied since the draft was created**, the agent **stops** and flags the row as `Manual Intervention Required` — preventing automated emails to leads who already responded

#### 3. Logger Module
- After sending: writes `Status = "Email Sent"`, `Sent Timestamp`, and Gmail `Thread ID` back to the sheet
- Thread ID enables future reply detection

---

## The BD Lead's Daily Workflow

### 09:00 AM — The "Green Light" Session
1. Open the Google Sheet — see overnight-generated leads and drafted emails
2. Skim the `Drafted Email` column
3. For approved emails: check `HITL_Approved = TRUE`
4. For emails needing a personal touch: edit the draft cell directly, then approve
5. The orchestrator wakes up, detects `TRUE` values, and sends at a human-like pace (~1 email every 3 minutes)

### 01:00 PM — The "Conflict Check"
- Review any rows flagged as `Manual Intervention Required`
- These are leads who replied while waiting for approval — take over manually

### 05:00 PM — Feedback & Optimization
- Review reply rates by strategy type
- Instruct Claude to tune the strategy generator based on what's working

---

## Prerequisites

This skill depends on two other skills being authenticated first:

| Skill | Purpose |
|---|---|
| `google-drive` | Read/write Google Sheets via PyDrive2 |
| `gmail` | Send emails and detect replies via Gmail API |

Complete their setup before proceeding:
- [skills/google-drive/README.md](../google-drive/README.md)
- [skills/gmail/README.md](../gmail/README.md)

---

## Setup

### Step 1: Authenticate Google Drive (Sheets access)

```bash
source ~/.claude/skills/google-drive/.venv/bin/activate
python ~/.claude/skills/google-drive/scripts/gdrive_helper.py search "test"
```

### Step 2: Authenticate Gmail

```bash
source ~/.claude/skills/gmail/.venv/bin/activate
python ~/.claude/skills/gmail/scripts/setup_auth.py
```

### Step 3: Configure the orchestrator

Run the interactive setup wizard — it will prompt for your spreadsheet URL and column mappings:

```bash
source ~/.claude/skills/viact-outbound-orchestrator/.venv/bin/activate
python ~/.claude/skills/viact-outbound-orchestrator/scripts/setup_config.py
```

This creates `~/.viact-orchestrator/config.json`. You can also create/edit it manually (see [Configuration](#configuration) below).

### Step 4: Register automated cron jobs (optional)

Requires `openclaw` to be installed:

```bash
bash ~/.claude/skills/viact-outbound-orchestrator/scripts/setup_cron.sh
```

Registers two recurring jobs:

| Job | Schedule | Purpose |
|---|---|---|
| Send Pending Emails | Every 3 min | Sends newly approved emails |
| Check Client Replies | Every 10 min | Detects replies and updates sheet |

---

## Configuration

Config file: `~/.viact-orchestrator/config.json`

```json
{
  "spreadsheet_url": "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit",
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
  "approved_values": ["TRUE", "true", "True", "YES", "yes", "1"],
  "skip_statuses": ["Email Sent", "Client Replied", "Error"]
}
```

### Column Mappings Reference

| Key | Description | Who fills it |
|---|---|---|
| `lead_name` | Lead contact name | Human / AI |
| `company` | Company name | Human / AI |
| `deal_id` | Pipedrive Deal ID | Pipedrive sync |
| `email` | Recipient email address | Human / AI |
| `subject` | Email subject line | Human / AI |
| `drafted_email` | Full email body | AI (reviewed by human) |
| `hitl_approved` | Set `TRUE` to approve sending | **Human reviewer only** |
| `status` | Current send status | Orchestrator |
| `sent_timestamp` | ISO timestamp of when sent | Orchestrator |
| `message_id` | Gmail Thread ID (for reply tracking) | Orchestrator |

### Status Values

| Status | Meaning |
|---|---|
| *(empty)* | Not yet processed |
| `Email Sent` | Successfully sent, awaiting reply |
| `Client Replied` | Client responded — handle manually |
| `Manual Intervention Required` | Client replied before send — skip automation |
| `Error` | Send failed — check logs |

---

## Usage

### Command Line

```bash
source ~/.claude/skills/viact-outbound-orchestrator/.venv/bin/activate

# Send all approved, unsent emails
python ~/.claude/skills/viact-outbound-orchestrator/skill/orchestrator.py send

# Check for client replies on sent emails
python ~/.claude/skills/viact-outbound-orchestrator/skill/orchestrator.py check-replies

# Show current status summary
python ~/.claude/skills/viact-outbound-orchestrator/skill/orchestrator.py status
```

### Python API

```python
import sys, os

skill_path = os.path.expanduser('~/.claude/skills/viact-outbound-orchestrator/skill')
sys.path.insert(0, skill_path)

from orchestrator import send_pending_emails, check_client_replies, get_status

# Send approved emails
result = send_pending_emails()
print(f"Sent: {result['emails_sent']}, Skipped: {result['skipped']}, Errors: {result['errors']}")

# Check for replies
result = check_client_replies()
print(f"Replies found: {result['replied']}")

# Get status overview
status = get_status()
print(status)
```

---

## File Structure

```
skills/viact-outbound-orchestrator/
├── SKILL.md                        # Full skill documentation (loaded by Claude)
├── README.md                       # This file — setup & usage guide
├── requirements.txt                # Python dependencies
├── scripts/
│   ├── setup_config.py             # Interactive config wizard
│   └── setup_cron.sh               # Register openclaw cron jobs
├── skill/
│   ├── __init__.py
│   └── orchestrator.py             # Core logic: send, check-replies, status
└── assets/
    └── config_template.json        # Default config template
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| No emails being sent | Check `HITL_Approved` column value is in `approved_values` list in config |
| Emails re-sent to same lead | Ensure `status` column is mapped correctly and shows `Email Sent` |
| Reply not detected | Verify `message_id` (Thread ID) was written to the sheet after first send |
| `config.json` not found | Run `setup_config.py` or manually create `~/.viact-orchestrator/config.json` |
| Column mismatch errors | Update `column_mappings` letters to match your actual sheet layout |
| Gmail auth failure | Re-run `~/.claude/skills/gmail/scripts/setup_auth.py` |
| Google Sheets auth failure | Re-run `gdrive_helper.py` to refresh the Drive OAuth token |
| `openclaw` not found | Install openclaw before running `setup_cron.sh` |

---

## Next Steps / Phase 2

Once this is stable, the natural evolution is:

- **Replace the static `Drafted Email` column** with a live Claude API call that generates the draft on demand inside the sheet
- **Add Pipedrive deal stage updates** — move deals to `"Outreach Sent"` automatically after email is sent
- **Reply-rate analytics tab** — track which strategy types get the best response rates and feed that back into prompt tuning

---

For full API reference and function signatures, see [SKILL.md](SKILL.md).
