const pptxgen = require('pptxgenjs');
const html2pptx = require('./scripts/html2pptx.js');
const fs = require('fs');
const path = require('path');

async function createPresentation() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'viAct';
  pptx.title = 'Leda Inio Safety Analytics Proposal';

  const slidesDir = '/home/philiptran/.vibe-kanban/worktrees/0847-test/proposal_skill/output/Leda_Inio_Safety_Analytics_20260127_060649/slides';
  const files = fs.readdirSync(slidesDir)
    .filter(f => f.endsWith('.html'))
    .sort();

  for (const file of files) {
    const filePath = path.join(slidesDir, file);
    console.log(`Processing: ${file}`);
    await html2pptx(filePath, pptx);
  }

  const outputPath = '/home/philiptran/.vibe-kanban/worktrees/0847-test/proposal_skill/output/Leda_Inio_Safety_Analytics_20260127_060649/Leda_Inio_Safety_Analytics_proposal.pptx';
  await pptx.writeFile({ fileName: outputPath });
  console.log(`\n✓ PowerPoint created: ${outputPath}`);
  console.log(`✓ Total slides: ${files.length}`);
}

createPresentation().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
