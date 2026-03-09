#!/bin/bash
# Pipedrive Skill Setup Helper

echo "=========================================="
echo "Pipedrive Skill Setup"
echo "=========================================="
echo ""
echo "Your Pipedrive endpoint is configured to:"
echo "  https://viact.pipedrive.com"
echo ""

# Check if token file exists
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
TOKEN_FILE="$SKILL_DIR/token"

if [ -s "$TOKEN_FILE" ] && ! grep -q "^#" "$TOKEN_FILE"; then
    echo "✅ API token already configured"
    echo ""
    TOKEN=$(cat "$TOKEN_FILE" | tr -d '\n' | tr -d '\r')
    echo "Current token: ${TOKEN:0:20}..."
    echo ""
else
    echo "❌ API token not configured"
    echo ""
    echo "To get your Pipedrive API token:"
    echo ""
    echo "1. Log in to Pipedrive at:"
    echo "   https://viact.pipedrive.com"
    echo ""
    echo "2. Navigate to:"
    echo "   Settings → Personal preferences → API"
    echo ""
    echo "3. Copy your API token"
    echo ""
    echo "4. Run this command to set it:"
    echo "   /pipedrive set-token YOUR_TOKEN_HERE"
    echo ""
    echo "Or add it directly to: $TOKEN_FILE"
    echo ""
fi

echo "Configuration files:"
echo "  Company URL: $SKILL_DIR/company_url"
echo "  API Token:   $TOKEN_FILE"
echo ""
