const PptxGenJS = require("pptxgenjs");
const html2pptx = require('./scripts/html2pptx.js');

const htmlFiles = [
  '/home/philiptran/.vibe-kanban/worktrees/a185-quotation-skill/00_slide_proposal/output/Leda_Inio_20260121_002812/slides/slide01_cover.html',
  '/home/philiptran/.vibe-kanban/worktrees/a185-quotation-skill/00_slide_proposal/output/Leda_Inio_20260121_002812/slides/slide02_requirements.html',
  '/home/philiptran/.vibe-kanban/worktrees/a185-quotation-skill/00_slide_proposal/output/Leda_Inio_20260121_002812/slides/slide03_scope.html',
  '/home/philiptran/.vibe-kanban/worktrees/a185-quotation-skill/00_slide_proposal/output/Leda_Inio_20260121_002812/slides/slide04_architecture.html',
  '/home/philiptran/.vibe-kanban/worktrees/a185-quotation-skill/00_slide_proposal/output/Leda_Inio_20260121_002812/slides/slide05_requirements.html',
  '/home/philiptran/.vibe-kanban/worktrees/a185-quotation-skill/00_slide_proposal/output/Leda_Inio_20260121_002812/slides/slide06_training.html',
  '/home/philiptran/.vibe-kanban/worktrees/a185-quotation-skill/00_slide_proposal/output/Leda_Inio_20260121_002812/slides/slide07_timeline.html',
  '/home/philiptran/.vibe-kanban/worktrees/a185-quotation-skill/00_slide_proposal/output/Leda_Inio_20260121_002812/slides/slide08_module1.html',
  '/home/philiptran/.vibe-kanban/worktrees/a185-quotation-skill/00_slide_proposal/output/Leda_Inio_20260121_002812/slides/slide09_module2.html',
  '/home/philiptran/.vibe-kanban/worktrees/a185-quotation-skill/00_slide_proposal/output/Leda_Inio_20260121_002812/slides/slide10_module3.html',
  '/home/philiptran/.vibe-kanban/worktrees/a185-quotation-skill/00_slide_proposal/output/Leda_Inio_20260121_002812/slides/slide11_module4.html',
  '/home/philiptran/.vibe-kanban/worktrees/a185-quotation-skill/00_slide_proposal/output/Leda_Inio_20260121_002812/slides/slide12_module5.html'
];
const outputPath = '/home/philiptran/.vibe-kanban/worktrees/a185-quotation-skill/00_slide_proposal/output/Leda_Inio_20260121_002812/Leda_Inio_proposal.pptx';

async function convertSlides() {
  console.log('Creating PowerPoint...');
  const pptx = new PptxGenJS();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'viAct';
  pptx.title = 'Video Analytics Solution Proposal for Leda Inio';

  for (const htmlFile of htmlFiles) {
    console.log(`Processing: ${htmlFile}`);
    await html2pptx(htmlFile, pptx);
  }

  await pptx.writeFile({ fileName: outputPath });
  console.log(`✓ PowerPoint created: ${outputPath}`);
}

convertSlides().catch(err => {
  console.error('✗ Error:', err.message);
  process.exit(1);
});
