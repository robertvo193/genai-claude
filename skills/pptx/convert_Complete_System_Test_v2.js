const PptxGenJS = require('pptxgenjs');
const html2pptx = require('./scripts/html2pptx.js');

const htmlFiles = ["/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/Leda_Inio_Final/slides/slide01_title.html", "/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/Leda_Inio_Final/slides/slide02_requirements.html", "/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/Leda_Inio_Final/slides/slide03_scope.html", "/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/Leda_Inio_Final/slides/slide04_architecture.html", "/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/Leda_Inio_Final/slides/slide05_timeline.html", "/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/Leda_Inio_Final/slides/slide06_module1.html", "/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/Leda_Inio_Final/slides/slide07_module2.html", "/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/Leda_Inio_Final/slides/slide08_module3.html", "/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/Leda_Inio_Final/slides/slide09_module4.html", "/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/Leda_Inio_Final/slides/slide10_module5.html", "/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/Leda_Inio_Final/slides/slide11_inference_ws.html", "/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/Leda_Inio_Final/slides/slide12_training_ws.html", "/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/Leda_Inio_Final/slides/slide13_dashboard_ws.html"];
const outputPath = '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/Leda_Inio_Final/Complete_System_Test_v2_proposal.pptx';

async function convertSlides() {
  console.log(`Converting ${htmlFiles.length} HTML slides to PowerPoint...`);
  const pptx = new PptxGenJS();
  pptx.layout = 'LAYOUT_16x9';

  for (const htmlFile of htmlFiles) {
    const basename = htmlFile.split('/').pop();
    console.log(`  Processing ${basename}...`);
    await html2pptx(htmlFile, pptx);
  }

  await pptx.writeFile({ fileName: outputPath });
  console.log(`✓ PowerPoint created: ${outputPath}`);
}

convertSlides().catch(err => {
  console.error('✗ Error:', err.message);
  process.exit(1);
});