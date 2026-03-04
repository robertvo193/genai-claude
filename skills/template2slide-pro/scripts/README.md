# Dependencies for template2slide-pro

## Status: ✅ Self-Contained

This skill includes its own `node_modules/` directory with all required dependencies.

## Initial Setup

The dependencies are pre-installed. If you need to reinstall or recover:

```bash
cd ~/.claude/skills/template2slide-pro/scripts
bash setup.sh
```

## Required Packages

- **pptxgenjs@^4.0.1** - PowerPoint generation library
- **playwright@^1.48.2** - Browser automation for HTML rendering
- **sharp@^0.34.5** - Image processing library
- **Chromium** - Playwright browser (installed via `npx playwright install chromium`)

## Architecture

All JavaScript files in this directory use **local requires**:

```javascript
// ✅ CORRECT - Uses local dependencies
const pptxgen = require('./node_modules/pptxgenjs');
const playwright = require('./node_modules/playwright');
const sharp = require('./node_modules/sharp');

// ❌ WRONG - Do not use global requires
const pptxgen = require('pptxgenjs');  // Assumes global installation
```

## Why Local Dependencies?

1. **Portability**: Skill works on any machine without setup
2. **Reliability**: Version-locked, no breaking changes
3. **Isolation**: No conflicts with other projects
4. **Offline**: Works without internet connection

## Troubleshooting

### "Cannot find module" errors

If you see module not found errors:

```bash
# Reinstall dependencies
rm -rf node_modules
bash setup.sh
```

### Playwright browser missing

```bash
# Install Chromium browser
npx playwright install chromium
```

### Permission errors

```bash
# Fix permissions
chmod +x setup.sh
chmod +x *.js
```

## Size Notes

The `node_modules/` directory is approximately **100-200 MB**. This is normal for Node.js projects and ensures the skill is self-contained.

## Version Information

See `package.json` for exact versions:
```bash
cat package.json | grep -A5 '"dependencies"'
```
