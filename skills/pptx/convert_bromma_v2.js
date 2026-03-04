const pptxgen = require('pptxgenjs');
const html2pptx = require('./scripts/html2pptx.js');
const fs = require('fs');
const path = require('path');

async function convertSlides() {
    const slidesDir = '/home/philiptran/.vibe-kanban/worktrees/0a55-create-skill/00_slide_proposal/output/Bromma_20260119_201952/slides';
    const outputFile = '/home/philiptran/.vibe-kanban/worktrees/0a55-create-skill/00_slide_proposal/output/Bromma_20260119_201952/Bromma_proposal_v2.pptx';

    const slideFiles = fs.readdirSync(slidesDir)
        .filter(f => f.endsWith('.html'))
        .sort();

    console.log(`Found ${slideFiles.length} slides to convert...`);

    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';

    for (const slideFile of slideFiles) {
        const htmlPath = path.join(slidesDir, slideFile);
        console.log(`Processing ${slideFile}...`);

        try {
            const { slide } = await html2pptx(htmlPath, pptx);
        } catch (error) {
            console.error(`  Error: ${error.message}`);
        }
    }

    await pptx.writeFile({ fileName: outputFile });
    console.log(`\n✅ Created: ${outputFile}`);
}

convertSlides().catch(console.error);
