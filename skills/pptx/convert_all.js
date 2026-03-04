const html2pptx = require('/home/philiptran/.claude/skills/pptx/scripts/html2pptx.js');
const pptxgenjs = require('pptxgenjs');
const fs = require('fs');

const slidesDir = '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Complete_20260120_200057/slides';
const htmlFiles = fs.readdirSync(slidesDir)
  .filter(f => f.endsWith('.html'))
  .sort()
  .map(f => `${slidesDir}/${f}`);

(async () => {
  try {
    const pptx = new pptxgenjs();
    pptx.layout = 'LAYOUT_16x9';

    for (const htmlFile of htmlFiles) {
      console.log(`Processing ${htmlFile}...`);
      await html2pptx(htmlFile, pptx);
    }

    await pptx.writeFile({ fileName: '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Complete_20260120_200057/Leda_Inio_proposal.pptx' });
    console.log('✓ PowerPoint created successfully');
  } catch (error) {
    console.error('✗ Error creating PowerPoint:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
})();
