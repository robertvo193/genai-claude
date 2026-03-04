const { escapeHtml, getBackgroundRelPath, cleanTimelineEvent } = require('./shared');

function generateTimelineHTML(slide, htmlDir, assetsDir, constants) {
  const bgPath = getBackgroundRelPath(htmlDir, assetsDir);
  const milestones = slide.timeline?.milestones || [];

  const { SLIDE_WIDTH, SLIDE_HEIGHT, ACCENT_COLOR, TEXT_COLOR } = constants;

  // Determine if two-column layout should be used
  // Use two-column if: explicitly requested, OR many milestones (>=4) with lots of text
  const useTwoColumnLayout = slide.timeline?.useTwoColumn ||
    (milestones.length >= 4 && milestones.some(m =>
      (m.event || '').length > 50 || (m.event || '').split('\n').length > 2
    ));

  // TWO-COLUMN LAYOUT
  if (useTwoColumnLayout) {
    return generateTwoColumnTimeline(slide, htmlDir, assetsDir, constants, milestones);
  }

  // HORIZONTAL TIMELINE LAYOUT (original)
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

// Two-column timeline layout for better space utilization with many milestones
function generateTwoColumnTimeline(slide, htmlDir, assetsDir, constants, milestones) {
  const bgPath = getBackgroundRelPath(htmlDir, assetsDir);
  const { SLIDE_WIDTH, SLIDE_HEIGHT, ACCENT_COLOR, TEXT_COLOR } = constants;

  // Split milestones into two columns
  const midPoint = Math.ceil(milestones.length / 2);
  const leftPhases = milestones.slice(0, midPoint);
  const rightPhases = milestones.slice(midPoint);

  function renderMilestone(milestone) {
    const phase = milestone.phase || '';
    const date = milestone.date ? cleanTimelineEvent(milestone.date) : '';
    const eventItems = (milestone.event || '')
      .split('\n')
      .map(line => line.trim())
      .filter(line => line.length > 0);

    const itemsHTML = eventItems.map(item =>
      `<li style="margin-bottom: 3pt;">${escapeHtml(item.replace(/^[-•]\s*/, ''))}</li>`
    ).join('');

    return `
      <div class="phase">
        ${date ? `<p class="phase-time">${escapeHtml(date)}</p>` : ''}
        <p class="phase-name">${escapeHtml(phase)}</p>
        <ul class="activities">
          ${itemsHTML}
        </ul>
      </div>
    `;
  }

  const leftColumnHTML = leftPhases.map(renderMilestone).join('');
  const rightColumnHTML = rightPhases.map(renderMilestone).join('');

  // Calculate total duration if available
  const duration = slide.timeline?.totalDuration || '';

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
}
.title {
  color: ${ACCENT_COLOR};
  font-size: 26pt;
  font-weight: bold;
  text-transform: uppercase;
  margin: 15pt 40pt 8pt 40pt;
  word-wrap: break-word;
  overflow-wrap: break-word;
}
.duration {
  color: ${TEXT_COLOR};
  font-size: 12pt;
  margin: 0 40pt 10pt 40pt;
}
.timeline {
  flex: 1;
  display: flex;
  gap: 35pt;
  padding: 0 40pt 45pt 40pt;
  overflow: hidden;
  min-height: 0;
}
.column {
  flex: 1;
  overflow-y: auto;
  min-height: 0;
}
.phase {
  margin-bottom: 12pt;
  padding-left: 12pt;
  border-left: 3px solid ${ACCENT_COLOR};
}
.phase-time {
  color: ${TEXT_COLOR};
  font-size: 10pt;
  margin: 0 0 4pt 0;
}
.phase-name {
  color: ${ACCENT_COLOR};
  font-size: 11pt;
  font-weight: bold;
  margin: 0 0 5pt 0;
}
.activities {
  color: ${TEXT_COLOR};
  font-size: 9pt;
  line-height: 1.4;
  margin: 0;
  padding: 0;
  list-style-type: none;
}
.activities li {
  margin-bottom: 3pt;
}
</style>
</head>
<body>
<h1 class="title">${escapeHtml(slide.title || '')}</h1>
${duration ? `<p class="duration">Project Duration: ${escapeHtml(duration)}</p>` : ''}
<div class="timeline">
  <div class="column">
    ${leftColumnHTML}
  </div>
  <div class="column">
    ${rightColumnHTML}
  </div>
</div>
</body>
</html>`;
}

module.exports = { generateTimelineHTML };



