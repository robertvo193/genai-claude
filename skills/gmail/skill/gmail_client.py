#!/usr/bin/env python3
"""
Gmail Client
Provides reusable functions for common Gmail operations.
"""

import os
import base64
import email
from email.message import EmailMessage
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/gmail.send',
             'https://www.googleapis.com/auth/gmail.readonly']


def authenticate(credentials_path=None, token_path=None):
    """
    Authenticate with Gmail API using OAuth2.

    Args:
        credentials_path (str): Path to credentials JSON file (optional)
        token_path (str): Path to token JSON file (optional)

    Returns:
        googleapiclient.discovery.Resource: Authenticated Gmail service object
    """
    # Default paths
    if credentials_path is None:
        credentials_path = os.path.expanduser('~/.gmail-skill/credentials.json')
    if token_path is None:
        token_path = os.path.expanduser('~/.gmail-skill/token_gmail.json')

    creds = None

    # Load existing token if available
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(
                    f"Credentials file not found: {credentials_path}\n"
                    "Please run setup_auth.py to set up OAuth2 credentials."
                )
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service


def send_email(service, to, subject, body, cc=None, bcc=None, reply_to=None):
    """
    Send a new email via Gmail API (starts a new thread).

    Args:
        service: Authenticated Gmail service object
        to (str): Recipient email address
        subject (str): Email subject
        body (str): Email body (plain text or HTML)
        cc (str): CC recipient (optional)
        bcc (str): BCC recipient (optional)
        reply_to (str): Reply-To address (optional)

    Returns:
        tuple: (message_id, thread_id) — for a new thread both values are equal

    Raises:
        HttpError: If API request fails
    """
    message = EmailMessage()
    message.set_content(body)
    message['to'] = to
    message['subject'] = subject

    if cc:
        message['cc'] = cc
    if bcc:
        message['bcc'] = bcc
    if reply_to:
        message['reply-to'] = reply_to

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        result = service.users().messages().send(
            userId='me',
            body={'raw': encoded_message}
        ).execute()
        return result['id'], result['threadId']
    except HttpError as e:
        raise Exception(f"Failed to send email: {e}")


def reply_in_thread(service, thread_id, to, subject, body):
    """
    Send a reply inside an existing Gmail thread (shows as a conversation).

    Fetches the last message in the thread to extract the RFC 2822 Message-ID
    needed for the In-Reply-To / References headers so Gmail groups it correctly.

    Args:
        service: Authenticated Gmail service object
        thread_id (str): Gmail thread ID (stored in sheet column AQ)
        to (str): Recipient email address
        subject (str): Reply subject (will have 'Re: ' prepended if missing)
        body (str): Reply body text

    Returns:
        tuple: (message_id, thread_id) of the sent reply

    Raises:
        Exception: If thread not found or send fails
    """
    # Fetch thread to get the RFC 2822 Message-ID of the last message
    thread = service.users().threads().get(
        userId='me',
        id=thread_id,
        format='metadata',
        metadataHeaders=['Message-ID', 'Subject']
    ).execute()

    messages = thread.get('messages', [])
    if not messages:
        raise Exception(f"Thread {thread_id} has no messages")

    last_msg = messages[-1]
    rfc_message_id = None
    for header in last_msg.get('payload', {}).get('headers', []):
        if header['name'].lower() == 'message-id':
            rfc_message_id = header['value']
            break

    # Build reply subject
    if not subject.lower().startswith('re:'):
        subject = f"Re: {subject}"

    # Build reply with threading headers
    message = EmailMessage()
    message.set_content(body)
    message['to'] = to
    message['subject'] = subject
    if rfc_message_id:
        message['In-Reply-To'] = rfc_message_id
        message['References'] = rfc_message_id

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        result = service.users().messages().send(
            userId='me',
            body={'raw': encoded_message, 'threadId': thread_id}
        ).execute()
        return result['id'], result['threadId']
    except HttpError as e:
        raise Exception(f"Failed to send reply: {e}")


def has_recent_reply(service, to, subject, since_timestamp, thread_id=None):
    """
    Check if recipient has replied to a subject since a given timestamp.

    Args:
        service: Authenticated Gmail service object
        to (str): Recipient email address to check
        subject (str): Email subject to match
        since_timestamp (str): ISO 8601 timestamp (e.g., "2024-01-01T00:00:00Z")
        thread_id (str): Known Gmail thread ID — skips the search API call if provided

    Returns:
        bool: True if recipient replied since timestamp, False otherwise
    """
    if thread_id is None:
        thread_id = find_thread_id(service, to, subject)

    if not thread_id:
        return False

    messages = get_thread_messages(service, thread_id)
    since_dt = datetime.fromisoformat(since_timestamp.replace('Z', '+00:00'))

    for msg in messages:
        sender = msg.get('from', '').lower()
        if to.lower() in sender:
            msg_date_str = msg.get('date', '')
            if msg_date_str:
                try:
                    msg_date = email.utils.parsedate_to_datetime(msg_date_str)
                    if msg_date and msg_date > since_dt:
                        return True
                except (ValueError, TypeError):
                    continue

    return False


def find_thread_id(service, to, subject):
    """
    Find the thread ID for an email conversation with a specific recipient and subject.

    Args:
        service: Authenticated Gmail service object
        to (str): Recipient email address
        subject (str): Email subject

    Returns:
        str: Thread ID if found, None otherwise
    """
    # Search for messages with matching subject
    # Remove "Re:" and "Fwd:" prefixes for better matching
    clean_subject = subject
    for prefix in ['Re:', 'Fwd:', 'RE:', 'FWD:']:
        if clean_subject.startswith(prefix):
            clean_subject = clean_subject[len(prefix):].strip()

    # Build search query
    query = f'to:{to} subject:"{clean_subject}"'

    try:
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=10
        ).execute()

        messages = results.get('messages', [])

        if messages:
            # Get the most recent message and return its thread ID
            message_id = messages[0]['id']
            message = service.users().messages().get(
                userId='me',
                id=message_id,
                format='minimal'
            ).execute()

            return message.get('threadId')

    except HttpError:
        pass

    return None


def get_thread_messages(service, thread_id):
    """
    Get all messages in a Gmail thread.

    Args:
        service: Authenticated Gmail service object
        thread_id (str): Gmail thread ID

    Returns:
        list: List of message dictionaries with 'id', 'from', 'date', 'subject', 'snippet'
    """
    try:
        thread = service.users().threads().get(
            userId='me',
            id=thread_id,
            format='metadata',
            metadataHeaders=['From', 'Date', 'Subject']
        ).execute()

        messages = thread.get('messages', [])

        # Extract relevant information from each message
        message_list = []
        for msg in messages:
            headers = {}
            for header in msg.get('payload', {}).get('headers', []):
                headers[header['name'].lower()] = header['value']

            message_list.append({
                'id': msg['id'],
                'threadId': msg.get('threadId'),
                'from': headers.get('from', ''),
                'date': headers.get('date', ''),
                'subject': headers.get('subject', ''),
                'snippet': msg.get('snippet', '')
            })

        return message_list

    except HttpError as e:
        raise Exception(f"Failed to get thread: {e}")


def search_messages(service, query, max_results=10):
    """
    Search for Gmail messages matching a query.

    Args:
        service: Authenticated Gmail service object
        query (str): Gmail search query (e.g., "from:sender@example.com")
        max_results (int): Maximum number of results to return

    Returns:
        list: List of message dictionaries with 'id' and 'threadId'
    """
    try:
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()

        messages = results.get('messages', [])

        return messages

    except HttpError as e:
        raise Exception(f"Failed to search messages: {e}")


def get_message(service, message_id):
    """
    Get full details of a Gmail message.

    Args:
        service: Authenticated Gmail service object
        message_id (str): Gmail message ID

    Returns:
        dict: Message dictionary with 'id', 'threadId', 'from', 'to', 'subject',
              'date', 'body', 'snippet'
    """
    try:
        message = service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()

        # Extract headers
        headers = {}
        for header in message.get('payload', {}).get('headers', []):
            headers[header['name'].lower()] = header['value']

        # Extract body
        body = ''
        payload = message.get('payload', {})

        if 'body' in payload and 'data' in payload['body']:
            # Single part message
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        elif 'parts' in payload:
            # Multipart message - get the text/plain part
            for part in payload['parts']:
                if part.get('mimeType') == 'text/plain':
                    if 'body' in part and 'data' in part['body']:
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        break

        return {
            'id': message['id'],
            'threadId': message.get('threadId'),
            'from': headers.get('from', ''),
            'to': headers.get('to', ''),
            'subject': headers.get('subject', ''),
            'date': headers.get('date', ''),
            'body': body,
            'snippet': message.get('snippet', '')
        }

    except HttpError as e:
        raise Exception(f"Failed to get message: {e}")


def main():
    """CLI interface for testing"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: gmail_client.py <command> [args...]")
        print("\nCommands:")
        print("  send <to> <subject> <body>")
        print("  check_reply <to> <subject> <timestamp>")
        print("  find_thread <to> <subject>")
        print("  get_thread <thread_id>")
        print("  search <query>")
        print("  get_message <message_id>")
        sys.exit(1)

    command = sys.argv[1]
    service = authenticate()

    if command == 'send':
        to = sys.argv[2]
        subject = sys.argv[3]
        body = sys.argv[4]

        message_id = send_email(service, to, subject, body)
        print(f"Sent: {message_id}")

    elif command == 'check_reply':
        to = sys.argv[2]
        subject = sys.argv[3]
        timestamp = sys.argv[4]

        has_reply = has_recent_reply(service, to, subject, timestamp)
        print(f"Has reply: {has_reply}")

    elif command == 'find_thread':
        to = sys.argv[2]
        subject = sys.argv[3]

        thread_id = find_thread_id(service, to, subject)
        print(f"Thread ID: {thread_id}")

    elif command == 'get_thread':
        thread_id = sys.argv[2]

        messages = get_thread_messages(service, thread_id)
        print(f"Thread has {len(messages)} messages:")
        for msg in messages:
            print(f"  [{msg['date']}] {msg['from']}: {msg['snippet'][:50]}")

    elif command == 'search':
        query = sys.argv[2]

        messages = search_messages(service, query)
        print(f"Found {len(messages)} messages:")
        for msg in messages:
            print(f"  ID: {msg['id']}, Thread: {msg['threadId']}")

    elif command == 'get_message':
        message_id = sys.argv[2]

        message = get_message(service, message_id)
        print(f"From: {message['from']}")
        print(f"To: {message['to']}")
        print(f"Subject: {message['subject']}")
        print(f"Date: {message['date']}")
        print(f"\nBody:\n{message['body']}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
