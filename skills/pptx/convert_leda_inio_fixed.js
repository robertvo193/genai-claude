const html2pptx = require('./scripts/html2pptx.js');

const htmlFiles = [
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Fixed_v3_test/slides/slide01_title.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Fixed_v3_test/slides/slide02_requirements.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Fixed_v3_test/slides/slide03_scope.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Fixed_v3_test/slides/slide04_architecture.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Fixed_v3_test/slides/slide05_requirements_network.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Fixed_v3_test/slides/slide06_requirements_camera.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Fixed_v3_test/slides/slide07_requirements_workstations.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Fixed_v3_test/slides/slide08_timeline.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Fixed_v3_test/slides/slide09_module_1.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Fixed_v3_test/slides/slide10_module_2.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Fixed_v3_test/slides/slide11_module_3.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Fixed_v3_test/slides/slide12_module_4.html',
  '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Fixed_v3_test/slides/slide13_module_5.html'
];

const outputPath = '/home/philiptran/.vibe-kanban/worktrees/8331-2010/00_slide_proposal/output/Leda_Inio_Fixed_v3_test/Leda_Inio_proposal.pptx';

console.log('Converting HTML slides to PowerPoint...');
html2pptx.convertHtmlFilesToPptx(htmlFiles, outputPath)
  .then(() => {
    console.log('✓ PowerPoint created successfully');
  })
  .catch(err => {
    console.error('✗ Error:', err.message);
    process.exit(1);
  });
