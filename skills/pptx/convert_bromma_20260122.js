const html2pptx = require('/home/philiptran/.claude/skills/pptx/scripts/html2pptx.js');
const pptxgenjs = require('pptxgenjs');
const path = require('path');
const fs = require('fs');

const slidesDir = '/home/philiptran/.vibe-kanban/worktrees/a185-quotation-skill/00_slide_proposal/output/Bromma_Malaysia_20260122_071651/slides';
const outputFile = '/home/philiptran/.vibe-kanban/worktrees/a185-quotation-skill/00_slide_proposal/output/Bromma_Malaysia_20260122_071651/Bromma_Malaysia_Proposal.pptx';

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
    console.log('✓ PowerPoint created successfully');
  } catch (error) {
    console.error('✗ Error:', error.message);
    process.exit(1);
  }
})();
