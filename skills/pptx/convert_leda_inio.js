const html2pptx = require('/home/philiptran/.claude/skills/pptx/scripts/html2pptx.js');
const pptxgenjs = require('pptxgenjs');

const htmlFiles = [
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_20260120_192208/slides/slide01_title.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_20260120_192208/slides/slide02_requirements.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_20260120_192208/slides/slide03_scope.html'
];

(async () => {
  try {
    const pptx = new pptxgenjs();
    pptx.layout = 'LAYOUT_16x9';

    for (const htmlFile of htmlFiles) {
      console.log(`Processing ${htmlFile}...`);
      await html2pptx(htmlFile, pptx);
    }

    await pptx.writeFile('/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_20260120_192208/Leda_Inio_proposal.pptx');
    console.log('✓ PowerPoint created successfully');
  } catch (error) {
    console.error('✗ Error creating PowerPoint:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
})();
