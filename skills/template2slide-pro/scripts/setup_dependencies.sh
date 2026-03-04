#!/bin/bash

# Dependency Setup Script for template2slide-pro Skill
# This script ensures all dependencies are properly installed

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "================================================"
echo "template2slide-pro Dependency Setup"
echo "================================================"
echo ""

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
  echo "❌ Node.js version $(node -v) detected. Node.js 18+ or 20+ required."
  exit 1
fi
echo "✅ Node.js version $(node -v) OK"
echo ""

# Step 1: Remove broken playwright installations if detected
echo "Step 1: Checking for broken playwright installation..."

if [ -d "node_modules/playwright" ] && [ ! -f "node_modules/playwright/lib/program.js" ]; then
  echo "⚠️  Broken playwright detected. Removing..."
  find node_modules -name "playwright" -type d -exec rm -rf {} + 2>/dev/null || true
  find node_modules -name "playwright-core" -type d -exec rm -rf {} + 2>/dev/null || true
  rm -f node_modules/.bin/playwright 2>/dev/null || true
  rm -f node_modules/.bin/playwright-core 2>/dev/null || true
  echo "✅ Broken playwright removed"
else
  echo "✅ Playwright installation OK or not present"
fi
echo ""

# Step 2: Install npm packages
echo "Step 2: Installing npm packages..."
npm install
echo "✅ npm packages installed"
echo ""

# Step 3: Install Playwright browser
echo "Step 3: Installing Playwright Chromium browser..."
npx playwright install chromium
echo "✅ Playwright Chromium installed"
echo ""

# Step 4: Verify installation
echo "================================================"
echo "Step 4: Verifying installation..."
node check_dependencies.js
echo ""

if [ $? -eq 0 ]; then
  echo "================================================"
  echo "✅ All dependencies installed successfully!"
  echo "================================================"
  exit 0
else
  echo "================================================"
  echo "❌ Dependency setup failed. Please check errors above."
  echo "================================================"
  exit 1
fi
