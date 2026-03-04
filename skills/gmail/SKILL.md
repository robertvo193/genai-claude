---
name: gmail
description: Send and receive emails via Gmail API with OAuth2 authentication. Use when you need to send emails, check for replies, or search messages. Supports thread checking to verify if clients have replied since a specific timestamp. Perfect for automated outreach workflows and email automation.
---

## Configuration

**Helper script location:**
```bash
# From within the skill directory
cd ~/.claude/skills/gmail
python scripts/setup_auth.py
```

**Authentication files** (use `~/.gmail-skill/` - expands to home directory):
- Credentials: `~/.gmail-skill/credentials.json`
- Token: `~/.gmail-skill/token_gmail.json` (auto-generated)
- Settings: `~/.gmail-skill/settings.yaml`

### Virtual Environment

**⚠️ Important**: This skill has its own virtual environment at:
```
~/.claude/skills/gmail/.venv
```

The `.venv` folder is **already set up** in the skill directory. When using this skill:
- ✅ Always use the existing `.venv` in `~/.claude/skills/gmail/`
- ❌ Do NOT create a new virtual environment
- ❌ Do NOT install dependencies in a different location

**Dependencies are pre-installed** in the skill's `.venv`. Just activate and use:
```bash
source ~/.claude/skills/gmail/.venv/bin/activate
```

Or activate all skills at once:
```bash
source ~/.claude-skills-env.sh
```

## Helper Script Usage

Use `scripts/gmail_client.py` for common email operations.

### Import and Use Functions

```python
import sys
import os

# Add skill directory to path (dynamic approach)
skill_path = os.path.expanduser('~/.claude/skills/gmail/skill')
sys.path.insert(0, skill_path)

from gmail_client import authenticate, send_email, has_recent_reply, search_messages

# Authenticate once
service = authenticate()

# Send email
message_id = send_email(service, "recipient@example.com", "Subject", "Email body")
print(f"Message ID: {message_id}")

# Check for recent replies
has_reply = has_recent_reply(service, "recipient@example.com", "Subject", "2024-01-01T00:00:00Z")
print(f"Has reply: {has_reply}")

# Search messages
messages = search_messages(service, "from:client@example.com")
for msg in messages:
    print(f"Message ID: {msg['id']}")
```

### Available Helper Functions

- `authenticate()` - Authenticate and return Gmail service object
- `send_email(service, to, subject, body, cc=None, bcc=None)` - Send email and return message ID
- `has_recent_reply(service, to, subject, since_timestamp)` - Check if recipient replied since timestamp
- `find_thread_id(service, to, subject)` - Find thread ID for a conversation
- `get_thread_messages(service, thread_id)` - Get all messages in a thread
- `search_messages(service, query, max_results=10)` - Search Gmail with query
- `get_message(service, message_id)` - Get message details

## Common Operations

### Send an Email

```python
from gmail_client import authenticate, send_email

service = authenticate()

# Simple email
message_id = send_email(
    service,
    to="recipient@example.com",
    subject="Meeting Request",
    body="Hi, let's schedule a meeting next week."
)
print(f"Sent: {message_id}")

# Email with CC and BCC
message_id = send_email(
    service,
    to="recipient@example.com",
    subject="Project Update",
    body="Here are the latest updates...",
    cc="manager@example.com",
    bcc="archive@example.com"
)
```

### Check for Client Replies

```python
from gmail_client import authenticate, has_recent_reply

service = authenticate()

# Check if client replied since we sent the draft
from datetime import datetime, timedelta
draft_timestamp = (datetime.now() - timedelta(days=7)).isoformat() + "Z"

has_reply = has_recent_reply(
    service,
    to="client@company.com",
    subject="Proposal for Project X",
    since_timestamp=draft_timestamp
)

if has_reply:
    print("Client has replied - don't send automated email")
else:
    print("No reply yet - safe to send")
```

### Find Email Thread

```python
from gmail_client import authenticate, find_thread_id, get_thread_messages

service = authenticate()

# Find the thread for a specific email
thread_id = find_thread_id(
    service,
    to="client@company.com",
    subject="Re: Proposal for Project X"
)

if thread_id:
    # Get all messages in the thread
    messages = get_thread_messages(service, thread_id)
    for msg in messages:
        sender = msg['from']
        date = msg['date']
        snippet = msg['snippet']
        print(f"[{date}] {sender}: {snippet}")
```

### Search Messages

```python
from gmail_client import authenticate, search_messages

service = authenticate()

# Search for emails from a specific sender
messages = search_messages(service, "from:client@company.com")

# Search with multiple criteria
messages = search_messages(
    service,
    "from:client@company.com subject:urgent newer_than:7d"
)

# Get message details
for msg in messages:
    details = get_message(service, msg['id'])
    print(f"Subject: {details['subject']}")
    print(f"From: {details['from']}")
    print(f"Date: {details['date']}")
```

## Workflow Example: Human-in-the-Loop Outreach

```python
import sys
import os
from datetime import datetime, timedelta

skill_path = os.path.expanduser('~/.claude/skills/gmail/skill')
sys.path.insert(0, skill_path)

from gmail_client import authenticate, send_email, has_recent_reply

# Authenticate
service = authenticate()

# Lead data from your CRM/sheet
leads = [
    {
        'email': 'client1@company.com',
        'subject': 'Proposal for New Project',
        'body': 'Hi, I\'d like to discuss our proposal...',
        'draft_date': '2024-01-15T10:00:00Z',
        'approved': True
    },
    # ... more leads
]

for lead in leads:
    if not lead['approved']:
        continue

    # Check if client replied since draft
    has_reply = has_recent_reply(
        service,
        to=lead['email'],
        subject=lead['subject'],
        since_timestamp=lead['draft_date']
    )

    if has_reply:
        print(f"⚠️  {lead['email']} - Client replied, skip sending")
        continue

    # Send email
    try:
        message_id = send_email(
            service,
            to=lead['email'],
            subject=lead['subject'],
            body=lead['body']
        )
        print(f"✅ {lead['email']} - Sent: {message_id}")
    except Exception as e:
        print(f"❌ {lead['email']} - Error: {e}")
```

## Search Query Patterns

Common Gmail search patterns:
- `from:sender@example.com` - Emails from specific sender
- `to:recipient@example.com` - Emails to specific recipient
- `subject:keyword` - Emails with subject containing keyword
- `newer_than:7d` - Emails newer than 7 days
- `older_than:30d` - Emails older than 30 days
- `is:unread` - Unread emails
- `is:starred` - Starred emails
- `has:attachment` - Emails with attachments

Combine with spaces (AND):
```python
query = "from:client@example.com subject:urgent newer_than:7d"
```

## Error Handling

```python
from googleapiclient.errors import HttpError
from gmail_client import authenticate, send_email

service = authenticate()

try:
    message_id = send_email(
        service,
        to="recipient@example.com",
        subject="Test",
        body="Test email"
    )
    print(f"Sent: {message_id}")
except HttpError as e:
    if e.resp.status == 400:
        print("Bad request - check email address")
    elif e.resp.status == 401:
        print("Authentication failed - re-authenticate")
    elif e.resp.status == 429:
        print("Rate limit exceeded - wait and retry")
    else:
        print(f"API Error: {e}")
except Exception as e:
    print(f"Error: {e}")
```

## Common Pitfalls

### Pitfall 1: Authentication Token Expired

**Error Message:**
```
google.auth.exceptions.RefreshError: invalid_grant: Token has been expired or revoked
```

**Cause:** OAuth2 token expired or was revoked.

**Solution:** Run the setup script again:
```bash
cd ~/.claude/skills/gmail
python scripts/setup_auth.py
```

### Pitfall 2: Incorrect Timestamp Format

**Error Message:**
```
ValueError: Invalid timestamp format
```

**Cause:** Timestamp not in ISO 8601 format with 'Z' suffix.

**Solution:** Use proper ISO format:
```python
# ❌ WRONG
timestamp = "2024-01-01"

# ✅ CORRECT
timestamp = "2024-01-01T00:00:00Z"
# or
from datetime import datetime
timestamp = datetime.now().isoformat() + "Z"
```

### Pitfall 3: Thread Not Found

**Cause:** No matching thread exists for the given recipient and subject.

**Solution:** Handle the None return value:
```python
thread_id = find_thread_id(service, "email@example.com", "Subject")
if thread_id:
    messages = get_thread_messages(service, thread_id)
else:
    print("No thread found - this may be a new conversation")
```

## Performance Tips

1. **Authenticate once** - Reuse the service object across multiple operations
2. **Use search queries** - Filter messages before retrieving details
3. **Batch operations** - Process multiple emails in sequence with re-authentication
4. **Cache thread IDs** - Store thread IDs for repeated checks
5. **Limit results** - Use `max_results` parameter when searching

## Additional Resources

For more advanced Gmail API usage:
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Gmail Search Operators](https://support.google.com/mail/answer/7190)
