const PptxGenJS = require('pptxgenjs');
const html2pptx = require('./scripts/html2pptx.js');

const htmlFiles = ["/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/Leda_Inio/slides/slide01_title.html", "/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/Leda_Inio/slides/slide02_requirements.html"];
const outputPath = 'Leda_Inio/MultiAgent_Test2_proposal.pptx';

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