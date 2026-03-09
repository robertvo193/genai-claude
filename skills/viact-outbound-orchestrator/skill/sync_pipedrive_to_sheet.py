#!/usr/bin/env python3
"""
Sync Pipedrive Leads to Google Sheet
Part of viAct Outbound Orchestrator
"""

import os
import sys

# Resolve paths relative to this file's location
_SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILLS_ROOT = os.path.normpath(os.path.join(_SKILL_DIR, '..', '..'))

sys.path.insert(0, os.path.join(_SKILLS_ROOT, 'google-drive', 'scripts'))
sys.path.insert(0, os.path.join(_SKILLS_ROOT, 'pipedrive', 'scripts'))
sys.path.insert(0, _SKILL_DIR)

try:
    from gsheets_helper import parse_spreadsheet_url, read_sheet_data, update_sheet_data
    from pipedrive import PipedriveClient
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


def column_letter_to_index(letter):
    result = 0
    for char in letter.upper():
        result = result * 26 + (ord(char) - ord('A') + 1)
    return result - 1


def load_config():
    """Load orchestrator config"""
    config_file = os.path.join(os.path.dirname(_SKILL_DIR), 'assets', 'config_template.json')
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file not found: {config_file}")

    import json
    with open(config_file, 'r') as f:
        return json.load(f)


def sync_pipedrive_to_sheet(limit: int = 100):
    """
    Sync Pipedrive leads to the orchestrator Google Sheet.

    Fetches the N newest leads from Pipedrive and adds/updates them in the sheet.
    Uses an upsert logic: if a lead already exists (by lead_id), update it;
    otherwise, add it as a new row.

    Returns:
        dict: { fetched, added, updated, errors, error_details }
    """
    results = {'fetched': 0, 'added': 0, 'updated': 0, 'errors': 0, 'error_details': []}

    try:
        print("=" * 60)
        print("viAct Outbound Orchestrator — Sync Pipedrive Leads")
        print("=" * 60)

        # Load config
        config = load_config()
        file_id = parse_spreadsheet_url(config.get('spreadsheet_url', ''))
        sheet_name = config.get('sheet_name', 'Sheet1')
        column_mappings = config.get('column_mappings', {})

        # Read existing sheet data
        print(f"\n📖 Reading Google Sheet: {config.get('spreadsheet_url', '')}")
        data_range = config.get('range', 'A:AR')
        rows = read_sheet_data(file_id, data_range, sheet_name)

        print(f"[sync_pipedrive_to_sheet] Fetching {limit} newest leads from Pipedrive...")

        # Fetch leads from Pipedrive
        pipedrive_dir = os.path.join(_SKILLS_ROOT, 'pipedrive')
        if not os.path.exists(pipedrive_dir):
            raise FileNotFoundError(f"Pipedrive skill not found at {pipedrive_dir}")

        # Get Pipedrive credentials
        token_file = os.path.join(pipedrive_dir, 'token')
        url_file = os.path.join(pipedrive_dir, 'company_url')

        if not os.path.exists(token_file) or not os.path.exists(url_file):
            raise FileNotFoundError("Pipedrive credentials not found. Please configure pipedrive skill.")

        with open(token_file, 'r') as f:
            api_token = f.read().strip()
        with open(url_file, 'r') as f:
            company_url = f.read().strip()

        # Create Pipedrive client and fetch leads
        print(f"[sync_pipedrive_to_sheet] Connecting to Pipedrive at {company_url}...")
        client = PipedriveClient(api_token, company_url)
        leads = client.list_leads(sort_by='update_time', sort_order='desc', limit=limit)

        results['fetched'] = len(leads)
        print(f"[sync_pipedrive_to_sheet] ✅ Fetched {len(leads)} leads from Pipedrive")

        if not leads:
            print("[sync_pipedrive_to_sheet] No leads to sync")
            return results

        # Build a lookup of existing leads by lead_id (from column A = deal_id)
        existing_leads = {}
        deal_id_idx = column_letter_to_index(column_mappings.get('deal_id', 'A'))

        for idx, row in enumerate(rows[1:], start=2):  # Skip header row
            if deal_id_idx < len(row):
                lead_id = str(row[deal_id_idx]).strip()
                if lead_id:
                    existing_leads[lead_id] = {'row_idx': idx, 'row': row}

        print(f"[sync_pipedrive_to_sheet] 📊 Found {len(existing_leads)} existing leads in sheet")

        # Get column indices for all mapped columns
        column_indices = {
            'deal_id': column_letter_to_index(column_mappings.get('deal_id', 'A')),
            'lead_name': column_letter_to_index(column_mappings.get('lead_name', 'B')),
            'company': column_letter_to_index(column_mappings.get('company', 'T')),
            'email': column_letter_to_index(column_mappings.get('email', 'AR')),
            'subject': column_letter_to_index(column_mappings.get('subject', 'AL')),
            'drafted_email': column_letter_to_index(column_mappings.get('drafted_email', 'AM')),
            'hitl_approved': column_letter_to_index(column_mappings.get('hitl_approved', 'AN')),
            'status': column_letter_to_index(column_mappings.get('status', 'AO')),
            'sent_timestamp': column_letter_to_index(column_mappings.get('sent_timestamp', 'AP')),
            'message_id': column_letter_to_index(column_mappings.get('message_id', 'AQ')),
        }

        # Prepare update batches
        updates = []

        for lead in leads:
            try:
                lead_id = str(lead.get('id', ''))
                lead_title = lead.get('title', 'New Lead from Pipedrive')

                # Build row data matching the sheet structure
                max_col = max(column_indices.values()) + 1
                row_data = [''] * max_col

                # Map Pipedrive lead data to sheet columns
                row_data[column_indices['deal_id']] = lead_id
                row_data[column_indices['lead_name']] = lead_title
                row_data[column_indices['company']] = lead.get('organization_name', '')

                # Pipedrive leads don't have email directly, but might have person_id
                # We'll leave email empty for now - it can be filled in later
                row_data[column_indices['email']] = ''

                row_data[column_indices['subject']] = f"Following up on: {lead_title}"
                row_data[column_indices['drafted_email']] = ''  # Leave empty for now
                row_data[column_indices['hitl_approved']] = ''  # Not approved yet
                row_data[column_indices['status']] = 'Pending'  # Default status
                row_data[column_indices['sent_timestamp']] = ''
                row_data[column_indices['message_id']] = ''

                # Check if lead already exists
                if lead_id in existing_leads:
                    # Update existing lead
                    row_idx = existing_leads[lead_id]['row_idx']
                    updates.append((row_idx, row_data))
                    results['updated'] += 1
                    print(f"  📝 Row {row_idx}: Updating lead '{lead_title}' (ID: {lead_id})")
                else:
                    # Add new lead
                    updates.append((None, row_data))  # None indicates new row
                    results['added'] += 1
                    print(f"  ➕ New row: Adding lead '{lead_title}' (ID: {lead_id})")

            except Exception as e:
                error_msg = f"Lead {lead.get('id', 'unknown')} — {e}"
                print(f"  ❌ ERROR: {error_msg}")
                results['errors'] += 1
                results['error_details'].append(error_msg)

        if not updates:
            print("[sync_pipedrive_to_sheet] No updates to apply")
            return results

        # Apply updates in batches
        print(f"\n[sync_pipedrive_to_sheet] Applying {len(updates)} updates...")

        # Separate new rows from updates
        new_rows = [row for row_idx, row in updates if row_idx is None]
        update_rows = [(row_idx, row) for row_idx, row in updates if row_idx is not None]

        # Add new rows if any
        if new_rows:
            try:
                # Calculate the range for new rows
                start_row = len(rows) + 1
                end_row = start_row + len(new_rows) - 1
                range_spec = f"A{start_row}:AR{end_row}"
                update_sheet_data(file_id, range_spec, new_rows, sheet_name)
                print(f"  ✅ Added {len(new_rows)} new rows")
            except Exception as e:
                print(f"  ❌ ERROR adding new rows: {e}")
                results['errors'] += 1
                results['error_details'].append(f"Error adding new rows: {e}")

        # Update existing rows if any
        for row_idx, row in update_rows:
            try:
                # Update each row individually (more precise)
                update_sheet_data(file_id, f"A{row_idx}:AR{row_idx}", [row], sheet_name)
                print(f"  ✅ Updated row {row_idx}")
            except Exception as e:
                print(f"  ❌ ERROR updating row {row_idx}: {e}")
                results['errors'] += 1
                results['error_details'].append(f"Error updating row {row_idx}: {e}")

        print("\n" + "=" * 60)
        print("Sync Summary")
        print("=" * 60)
        print(f"  Fetched from Pipedrive: {results['fetched']}")
        print(f"  Added to sheet:          {results['added']}")
        print(f"  Updated in sheet:        {results['updated']}")
        print(f"  Errors:                 {results['errors']}")
        if results['error_details']:
            print("\nError details:")
            for err in results['error_details']:
                print(f"  - {err}")
        print("=" * 60)

    except FileNotFoundError as e:
        print(f"❌ Config error: {e}")
        results['errors'] += 1
        results['error_details'].append(str(e))
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        results['errors'] += 1
        results['error_details'].append(str(e))

    return results


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Sync Pipedrive Leads to Google Sheet')
    parser.add_argument('--limit', type=int, default=100,
                       help='Number of leads to fetch (default: 100)')

    args = parser.parse_args()

    results = sync_pipedrive_to_sheet(limit=args.limit)

    if results['errors'] > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
