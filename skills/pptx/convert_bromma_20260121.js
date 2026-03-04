const html2pptx = require('/home/philiptran/.claude/skills/pptx/scripts/html2pptx.js');
const pptxgenjs = require('pptxgenjs');
const path = require('path');
const fs = require('fs');

const slidesDir = '/home/philiptran/.vibe-kanban/worktrees/a185-quotation-skill/00_slide_proposal/output/Bromma_Malaysia_20260121_105836/slides';
const outputFile = '/home/philiptran/.vibe-kanban/worktrees/a185-quotation-skill/00_slide_proposal/output/Bromma_Malaysia_20260121_105836/Bromma_Malaysia_Proposal.pptx';

// Get all HTML slide files sorted
const htmlFiles = fs.readdirSync(slidesDir)
  .filter(f => f.endsWith('.html'))
  .sort()
  .map(f => path.join(slidesDir, f));

(async () => {
  try {
    const pptx = new pptxgenjs();
    pptx.layout = 'LAYOUT_16x9';

    for (const htmlFile of htmlFiles) {
      console.log(`Processing ${path.basename(htmlFile)}...`);
      await html2pptx(htmlFile, pptx);
    }

    await pptx.writeFile(outputFile);
    console.log('✓ PowerPoint created successfully:', outputFile);
  } catch (error) {
    console.error('✗ Error creating PowerPoint:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
})();
