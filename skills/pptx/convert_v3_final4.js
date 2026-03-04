const PptxGenJS = require("pptxgenjs");
const html2pptx = require('./scripts/html2pptx.js');
const htmlFiles = [
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_v3_Final4/slides/slide01_title.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_v3_Final4/slides/slide02_requirements.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_v3_Final4/slides/slide03_scope.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_v3_Final4/slides/slide04_architecture.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_v3_Final4/slides/slide05_requirements_camera_network.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_v3_Final4/slides/slide06_requirements_dashboard.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_v3_Final4/slides/slide07_timeline.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_v3_Final4/slides/slide08_module_1.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_v3_Final4/slides/slide09_module_2.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_v3_Final4/slides/slide10_module_3.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_v3_Final4/slides/slide11_module_4.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_v3_Final4/slides/slide12_module_5.html'
];
const outputPath = '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_v3_Final4/Leda_Inio_v3_proposal.pptx';
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
