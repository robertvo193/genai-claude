const PptxGenJS = require("pptxgenjs");
const html2pptx = require('./scripts/html2pptx.js');

const htmlFiles = [
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Comparison_Fixed/slides/slide01_title.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Comparison_Fixed/slides/slide02_requirements.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Comparison_Fixed/slides/slide03_scope.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Comparison_Fixed/slides/slide04_architecture.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Comparison_Fixed/slides/slide05_requirements_network.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Comparison_Fixed/slides/slide06_requirements_camera.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Comparison_Fixed/slides/slide07_requirements_workstations.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Comparison_Fixed/slides/slide08_timeline.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Comparison_Fixed/slides/slide09_module_1.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Comparison_Fixed/slides/slide10_module_2.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Comparison_Fixed/slides/slide11_module_3.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Comparison_Fixed/slides/slide12_module_4.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Comparison_Fixed/slides/slide13_module_5.html'
];

const outputPath = '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Comparison_Fixed/Leda_Inio_proposal.pptx';

async function convertSlides() {
  console.log('Creating PowerPoint presentation...');
  const pptx = new PptxGenJS();
  pptx.layout = 'LAYOUT_16x9';
  
  for (const htmlFile of htmlFiles) {
    const basename = htmlFile.split('/').pop();
    console.log(`  Processing ${basename}...`);
    await html2pptx(htmlFile, pptx);
  }
  
  console.log('Writing file...');
  await pptx.writeFile({ fileName: outputPath });
  console.log('✓ PowerPoint created successfully');
}

convertSlides().catch(err => {
  console.error('✗ Error:', err.message);
  process.exit(1);
});
