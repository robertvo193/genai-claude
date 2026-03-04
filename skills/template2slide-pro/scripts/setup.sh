#!/bin/bash
# Auto-install dependencies for template2slide-pro skill
# This script ensures all required Node.js packages are available locally

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🔧 Setting up template2slide-pro dependencies..."
echo ""

# Check if node_modules exists
if [ -d "node_modules" ] && [ -f "node_modules/pptxgenjs/package.json" ]; then
    echo "✅ Dependencies already installed."
    echo ""
    echo "Installed packages:"
    echo "  - pptxgenjs: $(ls node_modules/pptxgenjs/package.json >/dev/null 2>&1 && echo '✓' || echo '✗')"
    echo "  - playwright: $(ls node_modules/playwright/package.json >/dev/null 2>&1 && echo '✓' || echo '✗')"
    echo "  - sharp: $(ls node_modules/sharp/package.json >/dev/null 2>&1 && echo '✓' || echo '✗')"
    echo ""
    echo "To reinstall from scratch, run:"
    echo "  rm -rf node_modules && bash setup.sh"
    exit 0
fi

echo "📦 Installing Node.js packages..."
npm install --silent

echo "🌐 Installing Playwright Chromium browser..."
npx playwright install chromium --silent

echo ""
echo "✅ Setup complete!"
echo ""
echo "All dependencies are now available locally in this skill."
