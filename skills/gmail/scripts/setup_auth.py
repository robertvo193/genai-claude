#!/usr/bin/env python3
"""
Gmail Authentication Setup Script
Sets up OAuth2 credentials for Gmail API access.
"""

import os
import sys


def main():
    """Setup OAuth2 credentials for Gmail API."""

    print("=" * 60)
    print("Gmail Skill - OAuth2 Setup")
    print("=" * 60)
    print()

    # Define paths
    credentials_dir = os.path.expanduser('~/.gmail-skill')
    credentials_path = os.path.join(credentials_dir, 'credentials.json')
    token_path = os.path.join(credentials_dir, 'token_gmail.json')

    # Create credentials directory if it doesn't exist
    os.makedirs(credentials_dir, exist_ok=True)

    # Check if credentials already exist
    if os.path.exists(credentials_path):
        print(f"✓ Credentials file already exists: {credentials_path}")
        print()
        response = input("Do you want to re-authenticate? (y/N): ").strip().lower()
        if response != 'y':
            print("Setup cancelled. Existing credentials will be used.")
            return

    print()
    print("To set up Gmail API access, you need to:")
    print("1. Create a Google Cloud project")
    print("2. Enable the Gmail API")
    print("3. Create OAuth 2.0 credentials")
    print("4. Download the credentials JSON file")
    print()
    print("Detailed instructions:")
    print("https://developers.google.com/gmail/api/quickstart/python")
    print()

    # Check if credentials file exists
    if os.path.exists(credentials_path):
        print(f"Using existing credentials: {credentials_path}")
    else:
        print(f"Please place your credentials.json file at:")
        print(f"  {credentials_path}")
        print()

        response = input("Press Enter when you have placed credentials.json: ")
        if not os.path.exists(credentials_path):
            print(f"❌ Error: credentials.json not found at {credentials_path}")
            print("Setup cancelled.")
            sys.exit(1)

    print()
    print("Testing OAuth2 authentication...")
    print()

    # Try to authenticate
    try:
        # Add skill directory to path
        skill_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, skill_path)

        from gmail_client import authenticate

        service = authenticate()

        # Test the connection
        profile = service.users().getProfile(userId='me').execute()
        email_address = profile['emailAddress']

        print("✓ Authentication successful!")
        print()
        print(f"  Gmail account: {email_address}")
        print(f"  Token saved to: {token_path}")
        print()
        print("You can now use the Gmail skill!")
        print()

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print()
        print("Please ensure credentials.json is in the correct location:")
        print(f"  {credentials_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during authentication: {e}")
        print()
        print("Please check:")
        print("1. Your credentials.json file is valid")
        print("2. The Gmail API is enabled in your Google Cloud project")
        print("3. The OAuth2 consent screen is configured")
        sys.exit(1)


if __name__ == '__main__':
    main()
