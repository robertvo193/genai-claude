#!/usr/bin/env node

/**
 * Dependency Checker for template2slide-pro Skill
 *
 * This script ensures all required dependencies are installed and accessible
 * in the skill's local node_modules directory. It will:
 * 1. Check if node_modules exists
 * 2. Verify all required packages are installed
 * 3. Check Playwright browser installation
 * 4. Fix broken symlinks or incomplete installations
 * 5. Provide clear error messages with solutions
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SKILL_DIR = path.dirname(__dirname);
const SCRIPTS_DIR = path.join(SKILL_DIR, 'scripts');
const NODE_MODULES_DIR = path.join(SCRIPTS_DIR, 'node_modules');

// ANSI color codes for output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function logSuccess(message) {
  log(`✅ ${message}`, 'green');
}

function logError(message) {
  log(`❌ ${message}`, 'red');
}

function logWarning(message) {
  log(`⚠️  ${message}`, 'yellow');
}

function logInfo(message) {
  log(`ℹ️  ${message}`, 'cyan');
}

// Required packages with their import paths
const REQUIRED_PACKAGES = [
  { name: 'pptxgenjs', importPath: 'pptxgenjs', critical: true },
  { name: 'playwright', importPath: 'playwright', critical: true },
  { name: 'sharp', importPath: 'sharp', critical: true },
  { name: '@mermaid-js/mermaid-cli', importPath: '@mermaid-js/mermaid-cli', critical: true },
  { name: 'puppeteer', importPath: 'puppeteer', critical: false }
];

// Check if a directory exists
function dirExists(dirPath) {
  try {
    return fs.statSync(dirPath).isDirectory();
  } catch {
    return false;
  }
}

// Check if a file exists
function fileExists(filePath) {
  try {
    return fs.statSync(filePath).isFile();
  } catch {
    return false;
  }
}

// Check if a package is installed
function isPackageInstalled(packageName) {
  try {
    const packagePath = path.join(NODE_MODULES_DIR, packageName);
    const pkgJsonPath = path.join(packagePath, 'package.json');

    if (!dirExists(packagePath)) {
      return { installed: false, reason: 'Directory not found' };
    }

    if (!fileExists(pkgJsonPath)) {
      return { installed: false, reason: 'package.json not found' };
    }

    // Special check for playwright - verify lib/inprocess exists
    if (packageName === 'playwright') {
      const libDir = path.join(NODE_MODULES_DIR, 'playwright-core', 'lib');
      const inprocessFile = path.join(libDir, 'inprocess.js');

      if (!dirExists(libDir)) {
        return { installed: false, reason: 'playwright-core/lib directory missing' };
      }

      if (!fileExists(inprocessFile)) {
        return { installed: false, reason: 'playwright-core/lib/inprocess.js missing' };
      }
    }

    // Special check for mermaid-cli
    if (packageName === '@mermaid-js/mermaid-cli') {
      const cliPath = path.join(NODE_MODULES_DIR, '.bin', 'mmdc');
      const cliPathWin = path.join(NODE_MODULES_DIR, '.bin', 'mmdc.cmd');

      if (!fileExists(cliPath) && !fileExists(cliPathWin)) {
        return { installed: false, reason: 'mmdc binary not found' };
      }
    }

    return { installed: true };
  } catch (error) {
    return { installed: false, reason: error.message };
  }
}

// Check if Playwright browser is installed
function isPlaywrightBrowserInstalled() {
  try {
    const playwrightPath = path.join(NODE_MODULES_DIR, 'playwright');

    // Try to find chromium installation
    const playwrightDir = fs.readdirSync(playwrightPath);
    const localBrowsers = playwrightDir.find(d => d === '.local-browsers');

    if (!localBrowsers) {
      return { installed: false, reason: 'Playwright browsers not installed' };
    }

    // Check if chromium directory exists
    const localBrowsersPath = path.join(playwrightPath, '.local-browsers');
    const browsers = fs.readdirSync(localBrowsersPath);
    const chromiumInstall = browsers.find(b => b.startsWith('chromium-'));

    if (!chromiumInstall) {
      return { installed: false, reason: 'Chromium browser not installed' };
    }

    return { installed: true };
  } catch (error) {
    return { installed: false, reason: error.message };
  }
}

// Main check function
function checkDependencies() {
  logInfo('Checking template2slide-pro skill dependencies...\n');

  let allGood = true;
  let criticalMissing = [];

  // Check 1: Node.js version
  logInfo('Check 1: Node.js version');
  const nodeVersion = process.version;
  const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0]);

  if (majorVersion < 18) {
    logWarning(`Node.js version ${nodeVersion} detected. Recommended: Node.js 18+ or 20+`);
  } else {
    logSuccess(`Node.js version ${nodeVersion} OK`);
  }

  // Check 2: node_modules directory exists
  logInfo('\nCheck 2: Skill node_modules directory');
  if (!dirExists(NODE_MODULES_DIR)) {
    logError(`node_modules not found at: ${NODE_MODULES_DIR}`);
    logError('Run: cd ' + SCRIPTS_DIR + ' && npm install');
    return false;
  }
  logSuccess(`node_modules exists at: ${NODE_MODULES_DIR}`);

  // Check 3: Required packages
  logInfo('\nCheck 3: Required packages');
  for (const pkg of REQUIRED_PACKAGES) {
    const check = isPackageInstalled(pkg.name);

    if (check.installed) {
      logSuccess(`${pkg.name} installed`);
    } else {
      if (pkg.critical) {
        logError(`${pkg.name} MISSING - ${check.reason}`);
        criticalMissing.push(pkg.name);
      } else {
        logWarning(`${pkg.name} missing - ${check.reason}`);
      }
      allGood = false;
    }
  }

  // Check 4: Playwright browser
  logInfo('\nCheck 4: Playwright browser (Chromium)');
  const browserCheck = isPlaywrightBrowserInstalled();

  if (browserCheck.installed) {
    logSuccess('Chromium browser installed');
  } else {
    logWarning(`Chromium browser not installed - ${browserCheck.reason}`);
    logInfo('Run: cd ' + SCRIPTS_DIR + ' && npx playwright install chromium');
    allGood = false;
  }

  // Check 5: package.json
  logInfo('\nCheck 5: package.json');
  const packageJsonPath = path.join(SCRIPTS_DIR, 'package.json');
  if (!fileExists(packageJsonPath)) {
    logError(`package.json not found at: ${packageJsonPath}`);
    return false;
  }
  success('package.json exists');

  // Summary
  logInfo('\n' + '='.repeat(60));
  if (allGood) {
    logSuccess('All dependencies are properly installed!');
    logInfo('\nYou can now use the template2slide-pro skill.');
    return true;
  } else {
    logError('Dependency check failed!\n');

    if (criticalMissing.length > 0) {
      logError('Critical packages missing: ' + criticalMissing.join(', '));
      logInfo('\nTo fix all issues, run:');
      logInfo(`  cd ${SCRIPTS_DIR}`);
      logInfo('  npm install');
      logInfo('  npx playwright install chromium');
    }

    return false;
  }
}

// Auto-fix function
function fixDependencies() {
  logInfo('Attempting to fix dependency issues...\n');

  // Check if playwright is critically broken (missing lib/program)
  const playwrightPath = path.join(NODE_MODULES_DIR, 'playwright');
  const playwrightCoreLib = path.join(NODE_MODULES_DIR, 'playwright-core', 'lib');
  const criticallyBroken = !dirExists(playwrightCoreLib) ||
    !fileExists(path.join(playwrightCoreLib, 'inprocess.js')) ||
    !fileExists(path.join(NODE_MODULES_DIR, 'playwright', 'lib', 'program.js'));

  if (criticallyBroken) {
    logWarning('Playwright installation is critically broken. Performing clean reinstall...\n');

    const commands = [
      { cmd: `cd ${SCRIPTS_DIR} && find node_modules -name "playwright" -o -name "playwright-core" | head -5`, description: 'Checking playwright installation...' },
      { cmd: `cd ${SCRIPTS_DIR} && npm install playwright@latest --force`, description: 'Force reinstalling playwright...' },
      { cmd: `cd ${SCRIPTS_DIR} && npx playwright install chromium`, description: 'Installing Playwright Chromium browser...' }
    ];

    for (const { cmd, description } of commands) {
      logInfo(description);
      try {
        execSync(cmd, { stdio: 'inherit', timeout: 120000 });
        logSuccess('Done!');
      } catch (error) {
        logError(`Failed: ${error.message}`);
        logInfo('\nManual fix required:');
        logInfo(`  cd ${SCRIPTS_DIR}`);
        logInfo('  rm -rf node_modules/playwright node_modules/playwright-core node_modules/.bin/playwright node_modules/.bin/playwright-core');
        logInfo('  npm install');
        return false;
      }
    }
  } else {
    const commands = [
      { cmd: `cd ${SCRIPTS_DIR} && npm install`, description: 'Installing npm packages...' },
      { cmd: `cd ${SCRIPTS_DIR} && npx playwright install chromium`, description: 'Installing Playwright Chromium browser...' }
    ];

    for (const { cmd, description } of commands) {
      logInfo(description);
      try {
        execSync(cmd, { stdio: 'inherit', timeout: 120000 });
        logSuccess('Done!');
      } catch (error) {
        logError(`Failed: ${error.message}`);
        return false;
      }
    }
  }

  logSuccess('\nDependencies fixed! Running check again...');
  return checkDependencies();
}

// Main execution
const args = process.argv.slice(2);

if (args.includes('--fix') || args.includes('-f')) {
  fixDependencies();
} else {
  const ok = checkDependencies();
  process.exit(ok ? 0 : 1);
}

function success(msg) {
  logSuccess(msg);
}
