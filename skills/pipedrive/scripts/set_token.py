#!/usr/bin/env python3
"""
Set Pipedrive API Token Helper
"""

import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
skill_dir = os.path.dirname(script_dir)
token_file = os.path.join(skill_dir, 'token')

if len(sys.argv) < 2:
    print("❌ Error: No token provided")
    print("\nUsage: python3 set_token.py YOUR_API_TOKEN")
    print("   or: /pipedrive set-token YOUR_API_TOKEN")
    print("\nTo get your API token:")
    print("1. Log in to https://viact.pipedrive.com")
    print("2. Go to Settings → Personal preferences → API")
    print("3. Copy your API token")
    sys.exit(1)

token = sys.argv[1].strip()

with open(token_file, 'w') as f:
    f.write(token)

print("✅ API token saved successfully")
print(f"   Location: {token_file}")
