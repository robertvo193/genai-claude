#!/usr/bin/env python3
"""
Google Sheets Helper Script
Provides reusable functions for common Google Sheets operations.
Integrates with existing google-drive OAuth2 authentication.
"""

import os
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def parse_spreadsheet_url(url):
    """
    Extract Google Spreadsheet file ID from various URL formats.

    Args:
        url (str): Google Sheets URL (e.g., https://docs.google.com/spreadsheets/d/FILE_ID/edit?gid=0#gid=0)

    Returns:
        str: The spreadsheet file ID

    Raises:
        ValueError: If no file ID can be extracted from the URL

    Examples:
        >>> parse_spreadsheet_url("https://docs.google.com/spreadsheets/d/1abc123/edit")
        '1abc123'

        >>> parse_spreadsheet_url("https://docs.google.com/spreadsheets/d/1abc123/edit?gid=12345")
        '1abc123'

        >>> parse_spreadsheet_url("https://docs.google.com/spreadsheets/d/1abc123/edit?gid=12345#gid=12345")
        '1abc123'
    """
    # Pattern to match file ID in various Google Sheets URL formats
    # Matches: /d/{file_id}/ in the URL
    pattern = r'/d/([a-zA-Z0-9-_]+)'
    match = re.search(pattern, url)

    if not match:
        raise ValueError(f"Could not extract file ID from URL: {url}")

    file_id = match.group(1)
    return file_id


def authenticate_sheets(credentials_path=None, token_path=None):
    """
    Authenticate with Google Sheets API using OAuth2.

    Args:
        credentials_path (str): Path to credentials JSON file (optional)
        token_path (str): Path to token JSON file (optional)

    Returns:
        googleapiclient.discovery.Resource: Authenticated Sheets service object
    """
    # Default paths (can be overridden)
    if credentials_path is None:
        credentials_path = os.path.expanduser('~/.gmail-skill/credentials.json')
    if token_path is None:
        token_path = os.path.expanduser('~/.gmail-skill/token_sheets.json')

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
                    "Please set up OAuth2 credentials first."
                )
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    return service


def read_sheet_data(file_id, range_name, sheet_name=None):
    """
    Read data from a Google Sheet.

    Args:
        file_id (str): Spreadsheet file ID
        range_name (str): Range to read (e.g., "A1:Z100" or "Sheet1!A1:Z100")
        sheet_name (str): Sheet name (optional, prepended to range if provided)

    Returns:
        list: List of lists containing cell values

    Raises:
        HttpError: If API request fails
    """
    service = authenticate_sheets()

    # Build the full range if sheet_name is provided
    if sheet_name and '!' not in range_name:
        range_name = f"'{sheet_name}'!{range_name}"

    # Read values from the sheet
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=file_id, range=range_name).execute()

    values = result.get('values', [])
    return values


def update_sheet_data(file_id, range_name, values, sheet_name=None):
    """
    Update data in a Google Sheet.

    Args:
        file_id (str): Spreadsheet file ID
        range_name (str): Range to update (e.g., "A1:Z100")
        values (list): List of lists containing values to write
        sheet_name (str): Sheet name (optional, prepended to range if provided)

    Returns:
        int: Number of updated cells

    Raises:
        HttpError: If API request fails
    """
    service = authenticate_sheets()

    # Build the full range if sheet_name is provided
    if sheet_name and '!' not in range_name:
        range_name = f"'{sheet_name}'!{range_name}"

    body = {
        'values': values
    }

    sheet = service.spreadsheets()
    result = sheet.values().update(
        spreadsheetId=file_id,
        range=range_name,
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()

    return result.get('updatedCells', 0)



def append_sheet_data(file_id, range_name, values, sheet_name=None):
    """
    Append data to a Google Sheet.

    Args:
        file_id (str): Spreadsheet file ID
        range_name (str): Range to append to (e.g., "A1:Z100" or "Sheet1!A1")
        values (list): List of lists containing values to append
        sheet_name (str): Sheet name (optional, prepended to range if provided)

    Returns:
        dict: Response containing number of rows appended

    Raises:
        HttpError: If API request fails
    """
    service = authenticate_sheets()

    # Build the full range if sheet_name is provided
    if sheet_name and '!' not in range_name:
        range_name = f"'{sheet_name}'!{range_name}"

    body = {
        'values': values
    }

    sheet = service.spreadsheets()
    result = sheet.values().append(
        spreadsheetId=file_id,
        range=range_name,
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

    return result.get('updates', {})


def update_cell(file_id, column, row, value, sheet_name=None):
    """
    Update a single cell in a Google Sheet.

    Args:
        file_id (str): Spreadsheet file ID
        column (str): Column letter (e.g., "A", "B", "Z")
        row (int): Row number (1-indexed)
        value (str): Value to write
        sheet_name (str): Sheet name (optional)

    Returns:
        int: Number of updated cells (should be 1)
    """
    range_name = f"{column}{row}"
    return update_sheet_data(file_id, range_name, [[value]], sheet_name)


def get_cell(file_id, column, row, sheet_name=None):
    """
    Get a single cell value from a Google Sheet.

    Args:
        file_id (str): Spreadsheet file ID
        column (str): Column letter (e.g., "A", "B", "Z")
        row (int): Row number (1-indexed)
        sheet_name (str): Sheet name (optional)

    Returns:
        str: Cell value, or empty string if cell is empty
    """
    range_name = f"{column}{row}:{column}{row}"
    values = read_sheet_data(file_id, range_name, sheet_name)

    if values and values[0]:
        return values[0][0]
    return ""


def main():
    """CLI interface for testing"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: gsheets_helper.py <command> [args...]")
        print("\nCommands:")
        print("  parse_url <url>")
        print("  read <file_id> <range> [sheet_name]")
        print("  update <file_id> <range> <value> [sheet_name]")
        print("  cell <file_id> <column> <row> [sheet_name]")
        print("  append <file_id> <range> <value> [sheet_name]")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'parse_url':
        url = sys.argv[2]
        file_id = parse_spreadsheet_url(url)
        print(f"File ID: {file_id}")

    elif command == 'read':
        file_id = sys.argv[2]
        range_name = sys.argv[3]
        sheet_name = sys.argv[4] if len(sys.argv) > 4 else None

        values = read_sheet_data(file_id, range_name, sheet_name)
        print(f"Read {len(values)} rows:")
        for row in values:
            print(f"  {row}")

    elif command == 'update':
        file_id = sys.argv[2]
        range_name = sys.argv[3]
        value = sys.argv[4]
        sheet_name = sys.argv[5] if len(sys.argv) > 5 else None

        count = update_sheet_data(file_id, range_name, [[value]], sheet_name)
        print(f"Updated {count} cells")

    elif command == 'cell':
        file_id = sys.argv[2]
        column = sys.argv[3]
        row = int(sys.argv[4])
        sheet_name = sys.argv[5] if len(sys.argv) > 5 else None

        if len(sys.argv) > 6:
            value = sys.argv[6]
            count = update_cell(file_id, column, row, value, sheet_name)
            print(f"Updated {count} cells")
        else:
            value = get_cell(file_id, column, row, sheet_name)
            print(f"Cell value: {value}")

    elif command == 'append':
        file_id = sys.argv[2]
        range_name = sys.argv[3]
        value = sys.argv[4]
        sheet_name = sys.argv[5] if len(sys.argv) > 5 else None

        result = append_sheet_data(file_id, range_name, [[value]], sheet_name)
        print(f"Appended {result.get('updatedRows', 0)} rows")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
