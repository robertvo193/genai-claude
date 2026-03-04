#!/usr/bin/env node
/**
 * Mermaid to PNG Converter for quotation_skill
 * Simple wrapper around mermaid-cli (mmdc)
 *
 * Usage: node mermaid_to_png.js <input.mmd> <output.png>
 */

const fs = require('fs');
const { execSync } = require('child_process');
const path = require('path');

function renderMermaidToPNG(inputMmd, outputPng) {
  /**
   * Convert Mermaid file to PNG using mmdc (mermaid-cli)
   *
   * Args:
   *   inputMmd: Path to input .mmd file
   *   outputPng: Path to output .png file
   */

  // Check if input file exists
  if (!fs.existsSync(inputMmd)) {
    throw new Error(`Input file not found: ${inputMmd}`);
  }

  // Ensure output directory exists
  const outputDir = path.dirname(outputPng);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  try {
    // Use mmdc to render Mermaid diagram
    // -b transparent: transparent background
    // -t dark: dark theme (matches viAct slides)
    const cmd = `mmdc -i "${inputMmd}" -o "${outputPng}" -b transparent -t dark`;

    console.log(`Rendering Mermaid diagram...`);
    console.log(`  Input:  ${inputMmd}`);
    console.log(`  Output: ${outputPng}`);

    execSync(cmd, { stdio: 'inherit' });

    console.log(`✓ Successfully created: ${outputPng}`);
    return outputPng;

  } catch (error) {
    // mmdc not found or failed
    console.error(`✗ Failed to render Mermaid diagram: ${error.message}`);
    console.error(`\nTo install mermaid-cli:`);
    console.error(`  npm install -g @mermaid-js/mermaid-cli`);
    console.error(`\nOr use npx (no installation needed):`);
    console.error(`  npx @mermaid-js/mermaid-cli -i "${inputMmd}" -o "${outputPng}" -b transparent -t dark`);

    // Create placeholder PNG
    console.warn(`\n⚠️ Creating placeholder image...`);

    const placeholderSVG = `
      <svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
        <rect width="800" height="600" fill="#1a1a1a"/>
        <text x="400" y="250" font-family="Arial" font-size="24" fill="#00AEEF" text-anchor="middle">
          System Architecture Diagram
        </text>
        <text x="400" y="300" font-family="Arial" font-size="16" fill="#FFFFFF" text-anchor="middle">
          Install mermaid-cli to render diagram
        </text>
        <text x="400" y="330" font-family="Arial" font-size="14" fill="#CCCCCC" text-anchor="middle">
          npm install -g @mermaid-js/mermaid-cli
        </text>
      </svg>
    `;

    // Save placeholder as PNG (convert SVG to PNG using basic approach)
    // Note: This is a simple placeholder - proper conversion would require sharp/graphicsmagick
    fs.writeFileSync(outputPng.replace('.png', '.svg'), placeholderSVG);
    console.log(`⚠️ Created placeholder SVG: ${outputPng.replace('.png', '.svg')}`);
    console.log(`⚠️ Please install mermaid-cli and re-run to generate PNG`);

    return null;
  }
}

// ============================================================================
// MAIN
// ============================================================================

if (require.main === module) {
  // Command line usage
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.log('Usage: node mermaid_to_png.js <input.mmd> <output.png>');
    console.log('');
    console.log('Example:');
    console.log('  node mermaid_to_png.js architecture.mmd architecture.png');
    process.exit(1);
  }

  const [inputMmd, outputPng] = args;

  try {
    renderMermaidToPNG(inputMmd, outputPng);
    process.exit(0);
  } catch (error) {
    console.error(error.message);
    process.exit(1);
  }
}

module.exports = { renderMermaidToPNG };
