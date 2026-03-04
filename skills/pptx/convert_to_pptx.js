const pptxgen = require('pptxgenjs');
const html2pptx = require('/home/philiptran/.claude/skills/pptx/scripts/html2pptx.js');
const fs = require('fs');
const path = require('path');

async function convertHtmlToPptx() {
  const slidesDir = process.argv[2];
  const outputDir = process.argv[3];
  const projectName = process.argv[4] || 'Presentation';

  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'viAct';
  pptx.company = 'viAct';
  pptx.subject = 'Video Analytics Solution Proposal';

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

  const outputPath = path.join(outputDir, `${projectName}_proposal.pptx`);
  await pptx.writeFile({ fileName: outputPath });
  console.log(`PowerPoint saved to: ${outputPath}`);
}

convertHtmlToPptx().catch(console.error);
