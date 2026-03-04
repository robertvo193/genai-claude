#!/usr/bin/env python3
"""
viAct Outbound Orchestrator - Configuration Setup
Interactive setup script for creating the configuration file.
"""

import os
import json
import sys


def main():
    """Setup configuration file for viAct Outbound Orchestrator."""

    print("=" * 60)
    print("viAct Outbound Orchestrator - Configuration Setup")
    print("=" * 60)
    print()

    # Define paths
    config_dir = os.path.expanduser('~/.viact-orchestrator')
    config_path = os.path.join(config_dir, 'config.json')
    template_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        '..', 'assets', 'config_template.json'
    )

    # Create config directory if it doesn't exist
    os.makedirs(config_dir, exist_ok=True)

    # Check if config already exists
    if os.path.exists(config_path):
        print(f"✓ Configuration file already exists: {config_path}")
        print()
        response = input("Do you want to re-configure? (y/N): ").strip().lower()
        if response != 'y':
            print("Setup cancelled. Existing configuration will be used.")
            return

    # Load template
    with open(template_path, 'r') as f:
        config = json.load(f)

    print("Please provide the following information:")
    print()

    # Spreadsheet URL
    spreadsheet_url = input(f"Google Sheets URL [{config['spreadsheet_url']}]: ").strip()
    if spreadsheet_url:
        config['spreadsheet_url'] = spreadsheet_url

    # Sheet name
    sheet_name = input(f"Sheet name [{config['sheet_name']}]: ").strip()
    if sheet_name:
        config['sheet_name'] = sheet_name

    # Data range
    data_range = input(f"Data range [{config['range']}]: ").strip()
    if data_range:
        config['range'] = data_range

    print()
    print("Column Mappings (letters like A, B, C, etc.):")
    print()

    column_mappings = config.get('column_mappings', {})

    for key, default in column_mappings.items():
        value = input(f"  {key} column [{default}]: ").strip().upper()
        if value:
            column_mappings[key] = value

    config['column_mappings'] = column_mappings

    # Write configuration
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    print()
    print("✓ Configuration saved to:")
    print(f"  {config_path}")
    print()
    print("You can now run the orchestrator:")
    print("  python skill/orchestrator.py send")
    print("  python skill/orchestrator.py check-replies")
    print()


if __name__ == '__main__':
    main()
