const html2pptx = require('/home/philiptran/.claude/skills/pptx/scripts/html2pptx.js');
const pptxgenjs = require('pptxgenjs');
const path = require('path');
const fs = require('fs');

const slidesDir = '/home/philiptran/.vibe-kanban/worktrees/a185-quotation-skill/00_slide_proposal/output/Bromma_Malaysia_20260122_071651/slides_combined';
const outputFile = '/home/philiptran/.vibe-kanban/worktrees/a185-quotation-skill/00_slide_proposal/output/Bromma_Malaysia_20260122_071651/Bromma_Malaysia_Proposal_HTML_FINAL.pptx';

const htmlFiles = fs.readdirSync(slidesDir)
  .filter(f => f.endsWith('.html'))
  .sort()
  .map(f => path.join(slidesDir, f));

(async () => {
  try {
    const pptx = new pptxgenjs();
    pptx.layout = 'LAYOUT_16x9';

    console.log(`Converting ${htmlFiles.length} HTML slides to PowerPoint...`);

    for (const htmlFile of htmlFiles) {
      console.log(`  Processing ${path.basename(htmlFile)}...`);
      await html2pptx(htmlFile, pptx);
    }

    await pptx.writeFile({ fileName: outputFile });
    console.log('✓ PowerPoint created successfully with all backgrounds preserved!');
  } catch (error) {
    console.error('✗ Error:', error.message);
    process.exit(1);
  }
})();
