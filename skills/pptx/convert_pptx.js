const pptxgen = require('pptxgenjs');
const html2pptx = require('/home/philiptran/.claude/skills/pptx/scripts/html2pptx.js');
const fs = require('fs');
const path = require('path');

async function convertHtmlToPptx() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'viAct';
  pptx.company = 'viAct';
  pptx.subject = 'Video Analytics Solution Proposal';

  const slidesDir = '/home/philiptran/.vibe-kanban/worktrees/a197-quotation/00_slide_proposal/output/Leda_Inio_20260115_052013/slides';

  // Get all slide files sorted
  const slideFiles = fs.readdirSync(slidesDir)
    .filter(f => f.endsWith('.html') && f.startsWith('slide'))
    .sort();

  console.log(`Processing ${slideFiles.length} slides...`);

  for (const slideFile of slideFiles) {
    const slidePath = path.join(slidesDir, slideFile);
    console.log(`Adding ${slideFile}...`);

    try {
      await html2pptx(slidePath, pptx);
    } catch (error) {
      console.error(`Error processing ${slideFile}:`, error.message);
      throw error;
    }
  }

  const outputPath = '/home/philiptran/.vibe-kanban/worktrees/a197-quotation/00_slide_proposal/output/Leda_Inio_20260115_052013/Leda_Inio_proposal.pptx';
  await pptx.writeFile({ fileName: outputPath });
  console.log(`PowerPoint saved to: ${outputPath}`);
}

convertHtmlToPptx().catch(console.error);
