#!/usr/bin/env python3
"""
viAct Outbound Orchestrator
Coordinates Google Sheets and Gmail for automated BD outreach.
"""

import os
import sys
import json
from datetime import datetime, timezone


# Resolve paths relative to this file's location
_SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILLS_ROOT = os.path.normpath(os.path.join(_SKILL_DIR, '..', '..'))

sys.path.insert(0, os.path.join(_SKILLS_ROOT, 'google-drive', 'scripts'))
sys.path.insert(0, os.path.join(_SKILLS_ROOT, 'gmail', 'skill'))
sys.path.insert(0, _SKILL_DIR)

try:
    from gsheets_helper import parse_spreadsheet_url, read_sheet_data, update_sheet_data
    from gmail_client import authenticate, send_email, reply_in_thread, has_recent_reply, find_thread_id
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all dependencies are installed:")
    print("  - google-drive: pip install -r ~/.claude/skills/google-drive/requirements.txt")
    print("  - gmail: pip install -r ~/.claude/skills/gmail/requirements.txt")
    print("  - orchestrator: pip install -r ~/.claude/skills/viact-outbound-orchestrator/requirements.txt")
    sys.exit(1)


CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'config_template.json')

# Statuses that block re-processing regardless of config
TERMINAL_STATUSES = {"Email Sent", "Client Replied"}


# ---------------------------------------------------------------------------
# Config & helpers
# ---------------------------------------------------------------------------

def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(
            f"Configuration file not found: {CONFIG_PATH}\n"
            "Please run: python3 ~/.claude/skills/viact-outbound-orchestrator/scripts/setup_config.py"
        )
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)


def column_letter_to_index(letter):
    result = 0
    for char in letter.upper():
        result = result * 26 + (ord(char) - ord('A') + 1)
    return result - 1


def extract_column_value(row, column_letter):
    col_index = column_letter_to_index(column_letter)
    if col_index < len(row):
        return str(row[col_index]).strip()
    return ""


def extract_lead_data(row, column_mappings):
    return {
        'lead_name':     extract_column_value(row, column_mappings.get('lead_name', 'B')),
        'company':       extract_column_value(row, column_mappings.get('company', 'T')),
        'deal_id':       extract_column_value(row, column_mappings.get('deal_id', 'A')),
        'email':         extract_column_value(row, column_mappings.get('email', 'AR')),
        'subject':       extract_column_value(row, column_mappings.get('subject', 'AL')),
        'drafted_email': extract_column_value(row, column_mappings.get('drafted_email', 'AM')),
        'hitl_approved': extract_column_value(row, column_mappings.get('hitl_approved', 'AN')),
        'status':        extract_column_value(row, column_mappings.get('status', 'AO')),
        'sent_timestamp':extract_column_value(row, column_mappings.get('sent_timestamp', 'AP')),
        'thread_id':     extract_column_value(row, column_mappings.get('message_id', 'AQ')),
    }


def is_approved(hitl_value, approved_values):
    return bool(hitl_value) and hitl_value in approved_values


def should_skip(status_value, skip_statuses):
    if not status_value:
        return False
    return status_value in TERMINAL_STATUSES or status_value in skip_statuses


def update_row_status(file_id, sheet_name, row_number, column_mappings,
                      status, message_id=None, timestamp=None):
    """Update status/thread_id/timestamp columns in a single batched API call."""
    updates = {column_mappings.get('status', 'AO'): status}
    if message_id is not None:
        updates[column_mappings.get('message_id', 'AQ')] = message_id
    if timestamp is not None:
        updates[column_mappings.get('sent_timestamp', 'AP')] = timestamp

    if len(updates) == 1:
        col, val = next(iter(updates.items()))
        update_sheet_data(file_id, f"{col}{row_number}", [[val]], sheet_name)
        return

    # Build a single range update spanning all changed columns
    col_indices = {col: column_letter_to_index(col) for col in updates}
    min_idx = min(col_indices.values())
    max_idx = max(col_indices.values())
    row_values = [''] * (max_idx - min_idx + 1)
    for col, val in updates.items():
        row_values[col_indices[col] - min_idx] = val
    min_col = next(c for c, i in col_indices.items() if i == min_idx)
    max_col = next(c for c, i in col_indices.items() if i == max_idx)
    update_sheet_data(file_id, f"{min_col}{row_number}:{max_col}{row_number}", [row_values], sheet_name)


def _load_sheet_rows(config):
    """Load all data rows from Google Sheet. Returns (file_id, sheet_name, column_mappings, rows)."""
    file_id = parse_spreadsheet_url(config.get('spreadsheet_url', ''))
    sheet_name = config.get('sheet_name', 'Sheet1')
    data_range = config.get('range', 'A:AR')
    column_mappings = config.get('column_mappings', {})

    rows = read_sheet_data(file_id, data_range, sheet_name)
    return file_id, sheet_name, column_mappings, rows


# ---------------------------------------------------------------------------
# Function 1: Send emails for HITL-approved rows
# ---------------------------------------------------------------------------

def send_pending_emails():
    """
    Read Google Sheet and send emails for all HITL-approved rows
    that have not yet been sent (status not in skip_statuses / TERMINAL_STATUSES).

    - If column AQ (thread_id) is empty  → send_email()       (new thread)
    - If column AQ (thread_id) has value → reply_in_thread()  (follow-up)

    Returns:
        dict: { processed, emails_sent, skipped, errors, error_details }
    """
    results = {'processed': 0, 'emails_sent': 0, 'skipped': 0, 'errors': 0, 'error_details': []}

    try:
        config = load_config()
        approved_values = config.get('approved_values', ['TRUE', 'true', 'True'])
        skip_statuses   = config.get('skip_statuses', ['Email Sent', 'Client Replied'])

        file_id, sheet_name, column_mappings, rows = _load_sheet_rows(config)

        if not rows or len(rows) < 2:
            print("No data found in sheet (or only header row exists)")
            return results

        pending = []
        for idx, row in enumerate(rows[1:], start=2):
            lead_data = extract_lead_data(row, column_mappings)

            if not is_approved(lead_data['hitl_approved'], approved_values):
                continue
            if should_skip(lead_data['status'], skip_statuses):
                results['skipped'] += 1
                continue

            pending.append((idx, lead_data))

        print(f"[send_pending_emails] {len(pending)} rows to process")
        if not pending:
            return results

        gmail_service = authenticate()

        for row_number, lead_data in pending:
            results['processed'] += 1
            try:
                # Use sheet's thread_id if present; only search Gmail if it's empty
                existing_thread_id = lead_data['thread_id'] or find_thread_id(
                    gmail_service, lead_data['email'], lead_data['subject']
                )
                if existing_thread_id:
                    print(f"  {lead_data['email']} — replying in thread {existing_thread_id}...")
                    _, thread_id = reply_in_thread(
                        gmail_service,
                        thread_id=existing_thread_id,
                        to=lead_data['email'],
                        subject=lead_data['subject'],
                        body=lead_data['drafted_email']
                    )
                    print(f"  {lead_data['email']} — reply sent (thread_id={thread_id})")
                else:
                    print(f"  {lead_data['email']} — sending new email...")
                    _, thread_id = send_email(
                        gmail_service,
                        to=lead_data['email'],
                        subject=lead_data['subject'],
                        body=lead_data['drafted_email']
                    )
                    print(f"  {lead_data['email']} — sent (thread_id={thread_id})")

                timestamp = datetime.now(timezone.utc).isoformat()
                update_row_status(file_id, sheet_name, row_number, column_mappings,
                                  status="Email Sent",
                                  message_id=thread_id,
                                  timestamp=timestamp)
                results['emails_sent'] += 1

            except Exception as e:
                error_msg = f"{lead_data['email']} — {e}"
                print(f"  ERROR: {error_msg}")
                update_row_status(file_id, sheet_name, row_number, column_mappings,
                                  status=f"Error: {e}")
                results['errors'] += 1
                results['error_details'].append(error_msg)

    except FileNotFoundError as e:
        print(f"Config error: {e}")
        results['errors'] += 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        results['errors'] += 1
        results['error_details'].append(str(e))

    return results


# ---------------------------------------------------------------------------
# Function 2: Check for client replies on already-sent rows
# ---------------------------------------------------------------------------

def check_client_replies():
    """
    Read Google Sheet and check every row with status="Email Sent" to see
    if the client has replied since the sent_timestamp.

    If a reply is detected → update status to "Client Replied".

    Returns:
        dict: { checked, replied, errors, error_details }
    """
    results = {'checked': 0, 'replied': 0, 'errors': 0, 'error_details': []}

    try:
        config = load_config()
        file_id, sheet_name, column_mappings, rows = _load_sheet_rows(config)

        if not rows or len(rows) < 2:
            print("No data found in sheet (or only header row exists)")
            return results

        # Only care about rows where we already sent an email
        sent_rows = []
        for idx, row in enumerate(rows[1:], start=2):
            lead_data = extract_lead_data(row, column_mappings)
            if lead_data['status'] == 'Email Sent':
                sent_rows.append((idx, lead_data))

        print(f"[check_client_replies] {len(sent_rows)} sent rows to check")
        if not sent_rows:
            return results

        gmail_service = authenticate()

        for row_number, lead_data in sent_rows:
            results['checked'] += 1
            try:
                # Use sent_timestamp so we only flag replies that arrived AFTER we sent
                since = lead_data['sent_timestamp'] or "1970-01-01T00:00:00Z"

                has_reply = has_recent_reply(
                    gmail_service,
                    to=lead_data['email'],
                    subject=lead_data['subject'],
                    since_timestamp=since,
                    thread_id=lead_data['thread_id'] or None,
                )

                if has_reply:
                    print(f"  {lead_data['email']} — client replied, updating status")
                    # Only update status; message_id column already has the thread_id from send time
                    update_row_status(file_id, sheet_name, row_number, column_mappings,
                                      status="Client Replied")
                    results['replied'] += 1
                else:
                    print(f"  {lead_data['email']} — no reply yet")

            except Exception as e:
                error_msg = f"{lead_data['email']} — {e}"
                print(f"  ERROR: {error_msg}")
                results['errors'] += 1
                results['error_details'].append(error_msg)

    except FileNotFoundError as e:
        print(f"Config error: {e}")
        results['errors'] += 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        results['errors'] += 1
        results['error_details'].append(str(e))

    return results


# ---------------------------------------------------------------------------
# Status helper
# ---------------------------------------------------------------------------

def get_status():
    return {
        'running': False,
        'last_check': datetime.now().isoformat(),
        'config_exists': os.path.exists(CONFIG_PATH)
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description='viAct Outbound Orchestrator')
    parser.add_argument('command', choices=['send', 'check-replies', 'status'])
    args = parser.parse_args()

    if args.command == 'send':
        print("=" * 60)
        print("viAct Outbound Orchestrator — Sending Pending Emails")
        print("=" * 60)
        r = send_pending_emails()
        print()
        print("=" * 60)
        print(f"  Processed:    {r['processed']}")
        print(f"  Emails sent:  {r['emails_sent']}")
        print(f"  Skipped:      {r['skipped']}")
        print(f"  Errors:       {r['errors']}")
        if r['error_details']:
            print("\nError details:")
            for err in r['error_details']:
                print(f"  - {err}")
        print("=" * 60)

    elif args.command == 'check-replies':
        print("=" * 60)
        print("viAct Outbound Orchestrator — Checking Client Replies")
        print("=" * 60)
        r = check_client_replies()
        print()
        print("=" * 60)
        print(f"  Checked:   {r['checked']}")
        print(f"  Replied:   {r['replied']}")
        print(f"  Errors:    {r['errors']}")
        if r['error_details']:
            print("\nError details:")
            for err in r['error_details']:
                print(f"  - {err}")
        print("=" * 60)

    elif args.command == 'status':
        s = get_status()
        print(f"Config exists: {s['config_exists']}")
        print(f"Last check:    {s['last_check']}")


if __name__ == '__main__':
    main()