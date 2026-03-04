const { escapeHtml, getBackgroundRelPath, cleanTimelineEvent } = require('./shared');

function generateTimelineHTML(slide, htmlDir, assetsDir, constants) {
  const bgPath = getBackgroundRelPath(htmlDir, assetsDir);
  const milestones = slide.timeline?.milestones || [];

  const { SLIDE_WIDTH, SLIDE_HEIGHT, ACCENT_COLOR, TEXT_COLOR } = constants;

  let timelineHTML = '';
  const timelineStartX = 80;
  const timelineEndX = SLIDE_WIDTH - 80;
  const timelineY = SLIDE_HEIGHT / 2 + 50;
  const spacing = milestones.length > 1 ? (timelineEndX - timelineStartX) / (milestones.length - 1) : 0;

  // Simplify event text - only keep first line/short description
  function simplifyEventText(event) {
    if (!event) return '';
    // Split by newlines and take first line, or split by '-' and take first part
    const lines = event.split('\n');
    let simplified = lines[0].trim();

    // If the line contains 'Duration:', remove it
    simplified = simplified.replace(/- Duration:.*$/i, '').trim();
    // Remove trailing dashes or colons
    simplified = simplified.replace(/[-:]+$/, '').trim();

    // Limit to 30 characters
    if (simplified.length > 30) {
      simplified = simplified.substring(0, 28) + '...';
    }

    return simplified;
  }

  milestones.forEach((milestone, index) => {
    const x = timelineStartX + (index * spacing);
    const eventText = simplifyEventText(milestone.event);
    const phase = milestone.phase || '';
    const date = milestone.date ? cleanTimelineEvent(milestone.date) : '';

    const maxWidth = Math.min(180, spacing - 10);

    timelineHTML += `
      <div style="position: absolute; left: ${x}pt; top: ${timelineY}pt; transform: translateX(-50%);">
        <div style="width: 14pt; height: 14pt; background: ${ACCENT_COLOR}; border-radius: 50%; border: 3px solid ${TEXT_COLOR}; position: absolute; top: -7pt; left: -7pt;"></div>
        <div style="position: absolute; left: 0; top: 15pt; width: ${maxWidth}pt; text-align: center;">
          <p style="color: ${ACCENT_COLOR}; font-size: 16pt; font-weight: bold; margin: 0 0 8pt 0;">${escapeHtml(phase)}</p>
          <p style="color: ${TEXT_COLOR}; font-size: 12pt; line-height: 1.4; margin: 0 0 6pt 0; word-wrap: break-word; overflow-wrap: break-word;">${escapeHtml(eventText)}</p>
          ${date ? `<p style="color: #888888; font-size: 10pt; margin: 0; word-wrap: break-word; overflow-wrap: break-word;">${escapeHtml(date)}</p>` : ''}
        </div>
      </div>
    `;
  });

  return `<!DOCTYPE html>
<html>
<head>
<style>
html { background: #000000; }
body {
  width: ${SLIDE_WIDTH}pt;
  height: ${SLIDE_HEIGHT}pt;
  margin: 0;
  padding: 0;
  background-image: url('${bgPath}');
  background-size: cover;
  background-position: center;
  display: flex;
  flex-direction: column;
  font-family: Arial, Helvetica, sans-serif;
  overflow: hidden;
  min-height: 0;
  position: relative;
}
.title {
  color: ${ACCENT_COLOR};
  font-size: 28pt;
  font-weight: bold;
  text-transform: uppercase;
  margin: 25pt 40pt 15pt 40pt;
  word-wrap: break-word;
  overflow-wrap: break-word;
}
.timeline-container {
  flex: 1;
  position: relative;
  margin: 0 40pt 72pt 40pt;
  overflow: hidden;
  min-height: 0;
  padding-bottom: 0;
}
.timeline-line {
  position: absolute;
  left: ${timelineStartX}pt;
  width: ${timelineEndX - timelineStartX}pt;
  top: ${timelineY}pt;
  height: 2pt;
  background: ${ACCENT_COLOR};
}
</style>
</head>
<body>
<h1 class="title">${escapeHtml(slide.title || '')}</h1>
<div class="timeline-container">
  <div class="timeline-line"></div>
  ${timelineHTML}
</div>
</body>
</html>`;
}

module.exports = { generateTimelineHTML };



