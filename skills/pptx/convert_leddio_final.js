const html2pptx = require('./scripts/html2pptx.js');
const pptxgenjs = require('pptxgenjs');

const htmlFiles = [
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Final_20260120_213814/slides/slide01_title.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Final_20260120_213814/slides/slide02_requirements.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Final_20260120_213814/slides/slide03_scope.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Final_20260120_213814/slides/slide04_architecture.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Final_20260120_213814/slides/slide05_requirements_network.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Final_20260120_213814/slides/slide06_requirements_camera.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Final_20260120_213814/slides/slide07_requirements_workstations.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Final_20260120_213814/slides/slide08_timeline.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Final_20260120_213814/slides/slide09_module_1.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Final_20260120_213814/slides/slide10_module_2.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Final_20260120_213814/slides/slide11_module_3.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Final_20260120_213814/slides/slide12_module_4.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Final_20260120_213814/slides/slide13_module_5.html'
];

(async () => {
  try {
    const pptx = new pptxgenjs();
    pptx.layout = 'LAYOUT_16x9';

    for (const htmlFile of htmlFiles) {
      console.log(`Processing ${htmlFile}...`);
      await html2pptx(htmlFile, pptx);
    }

    await pptx.writeFile('/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Final_20260120_213814/Leda_Inio_Final_proposal.pptx');
    console.log('✓ PowerPoint created successfully');
  } catch (error) {
    console.error('✗ Error creating PowerPoint:', error.message);
    process.exit(1);
  }
})();
