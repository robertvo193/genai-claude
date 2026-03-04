const PptxGenJS = require("pptxgenjs");
const html2pptx = require('./scripts/html2pptx.js');
const htmlFiles = [
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Complete_Final/slides/slide01_title.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Complete_Final/slides/slide02_requirements.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Complete_Final/slides/slide03_scope.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Complete_Final/slides/slide04_architecture.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Complete_Final/slides/slide05_requirements_camera_network.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Complete_Final/slides/slide06_requirements_inference.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Complete_Final/slides/slide07_requirements_training.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Complete_Final/slides/slide08_requirements_dashboard.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Complete_Final/slides/slide09_timeline.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Complete_Final/slides/slide10_module_1.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Complete_Final/slides/slide11_module_2.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Complete_Final/slides/slide12_module_3.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Complete_Final/slides/slide13_module_4.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Complete_Final/slides/slide14_module_5.html'
];
const outputPath = '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Complete_Final/Leda_Inio_proposal.pptx';
async function convertSlides() {
  console.log('Creating PowerPoint...');
  const pptx = new PptxGenJS();
  pptx.layout = 'LAYOUT_16x9';
  for (const htmlFile of htmlFiles) {
    await html2pptx(htmlFile, pptx);
  }
  await pptx.writeFile({ fileName: outputPath });
  console.log('✓ PowerPoint created');
}
convertSlides().catch(err => { console.error('✗', err.message); process.exit(1); });
