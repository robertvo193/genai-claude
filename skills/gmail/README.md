# Gmail Skill

Send and receive emails via Gmail API with OAuth2 authentication. Supports sending, searching, thread checking, and reply detection.

---

## Prerequisites

- Python 3.8+
- A Google Cloud project with the Gmail API enabled
- OAuth 2.0 credentials (Desktop app type)

---

## Authentication Setup

### 1. Create Google Cloud credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project (or select an existing one)
3. Enable **Gmail API**: APIs & Services → Enable APIs → search "Gmail API"
4. Configure **OAuth consent screen**: APIs & Services → OAuth consent screen
   - User type: **External** (or Internal if using Google Workspace)
   - Add scopes: `gmail.send`, `gmail.readonly`
   - Add your email as a test user
5. Create credentials: APIs & Services → Credentials → Create Credentials → **OAuth 2.0 Client ID**
   - Application type: **Desktop app**
6. Download the JSON file and save it as `~/.gmail-skill/credentials.json`

### 2. Run the setup script (first-time only)

```bash
source ~/.claude/skills/gmail/.venv/bin/activate
python ~/.claude/skills/gmail/scripts/setup_auth.py
```

The script will:
- Verify `~/.gmail-skill/credentials.json` exists
- Open a browser for Google OAuth consent
- Save the token to `~/.gmail-skill/token_gmail.json`
- Confirm the authenticated Gmail address

### 3. Auth file locations

| File | Path | Description |
|---|---|---|
| Credentials | `~/.gmail-skill/credentials.json` | Downloaded from Google Cloud Console |
| Token | `~/.gmail-skill/token_gmail.json` | Auto-generated after first auth |

---

## Virtual Environment

The skill ships with a pre-configured `.venv`. Always use it — do **not** create a new one.

```bash
# Activate the skill venv
source ~/.claude/skills/gmail/.venv/bin/activate

# Or activate all skills at once
source ~/.claude-skills-env.sh
```

---

## Quick Start

```python
import sys, os

skill_path = os.path.expanduser('~/.claude/skills/gmail/skill')
sys.path.insert(0, skill_path)

from gmail_client import authenticate, send_email, has_recent_reply, search_messages

service = authenticate()

# Send an email
message_id = send_email(service, "recipient@example.com", "Hello", "Email body here")
print(f"Sent: {message_id}")

# Check if a contact has replied since a given time
has_reply = has_recent_reply(service, "client@company.com", "Proposal", "2024-01-01T00:00:00Z")
print(f"Has reply: {has_reply}")

# Search messages
messages = search_messages(service, "from:client@company.com newer_than:7d")
for msg in messages:
    print(msg['id'])
```

---

## File Structure

```
skills/gmail/
├── SKILL.md                        # Full skill documentation (loaded by Claude)
├── README.md                       # This file — setup guide
├── requirements.txt                # Python dependencies
├── scripts/
│   └── setup_auth.py               # OAuth2 first-time setup wizard
├── skill/
│   ├── __init__.py
│   └── gmail_client.py             # Core functions: send, search, thread check
└── assets/
    └── settings_template.yaml      # Template for OAuth config reference
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `credentials.json` not found | Download from Google Cloud Console and place at `~/.gmail-skill/credentials.json` |
| `invalid_grant: Token expired` | Delete `~/.gmail-skill/token_gmail.json` and re-run `setup_auth.py` |
| `403 Insufficient Permission` | Ensure `gmail.send` and `gmail.readonly` scopes are added and re-authenticate |
| `400 Bad Request` on send | Verify the recipient email address is valid |
| `429 Rate Limit` | Wait before retrying; Gmail API has per-user quotas |
| Browser doesn't open during auth | Run `setup_auth.py` in a terminal with a display, or use a machine with GUI access |

---

For full API reference and advanced usage, see [SKILL.md](SKILL.md).
