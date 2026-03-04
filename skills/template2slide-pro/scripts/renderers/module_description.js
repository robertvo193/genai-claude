const path = require('path');
const { escapeHtml, getBackgroundRelPath } = require('./shared');

// Extract Google Drive file ID from URL
function extractDriveId(url) {
  if (!url) return null;

  // Match patterns like:
  // - /d/FILE_ID/view
  // - /file/d/FILE_ID/view
  // - id=FILE_ID
  const patterns = [
    /\/d\/([a-zA-Z0-9_-]+)/,
    /\/file\/d\/([a-zA-Z0-9_-]+)/,
    /[?&]id=([a-zA-Z0-9_-]+)/
  ];

  for (const pattern of patterns) {
    const match = url.match(pattern);
    if (match && match[1]) {
      return match[1];
    }
  }

  return null;
}

// Convert Google Drive URL to embed URL
function getEmbedUrl(videoUrl) {
  if (!videoUrl) return null;

  // Check if it's a Google Drive URL
  const driveId = extractDriveId(videoUrl);
  if (driveId) {
    return `https://drive.google.com/file/d/${driveId}/preview`;
  }

  // Check if it's a YouTube URL
  const youtubeMatch = videoUrl.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]+)/);
  if (youtubeMatch) {
    return `https://www.youtube.com/embed/${youtubeMatch[1]}`;
  }

  // Return original URL if no pattern matched
  return videoUrl;
}

function generateModuleDescriptionHTML(slide, mediaPath, mediaType, htmlDir, assetsDir, constants, videoUrl = null) {
  const bgPath = getBackgroundRelPath(htmlDir, assetsDir);
  const content = slide.content || {};

  const { SLIDE_WIDTH, SLIDE_HEIGHT, ACCENT_COLOR, TEXT_COLOR } = constants;

  const mediaRelPath = mediaPath ? path.relative(htmlDir, mediaPath) : null;
  const isVideo = mediaType === 'video' || mediaType === 'video_manual_insert';

  // Determine if we should embed video directly
  const hasDownloadedVideo = mediaRelPath && isVideo;
  const hasVideoUrl = videoUrl && String(videoUrl).trim() !== '';
  const embedVideoUrl = hasVideoUrl ? getEmbedUrl(videoUrl) : null;
  const shouldEmbedVideo = !hasDownloadedVideo && embedVideoUrl;

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
  margin: 20pt 40pt 12pt 40pt;
  word-wrap: break-word;
  overflow-wrap: break-word;
  flex-shrink: 0;
}
.content-wrapper {
  flex: 1;
  display: flex;
  margin: 0 40pt 72pt 40pt;
  gap: 25pt;
  min-height: 0;
  overflow: hidden;
  padding-bottom: 0;
}
.text-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  overflow-y: auto;
  overflow-x: hidden;
}
.media-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 0;
  overflow: hidden;
  padding: 10pt;
}
.video-wrapper {
  width: 100%;
  aspect-ratio: 16 / 9;
  background: #000000;
  border: 2px solid ${ACCENT_COLOR};
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.video-wrapper iframe {
  width: 100%;
  height: 100%;
  border: none;
}
img, video {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
video {
  background: #000000;
}
.video-url-text {
  color: ${TEXT_COLOR};
  font-size: 8pt;
  line-height: 1.3;
  word-wrap: break-word;
  overflow-wrap: break-word;
  text-align: center;
  margin-top: 10pt;
  padding: 8pt;
  background: rgba(0, 174, 239, 0.1);
  border: 1px solid ${ACCENT_COLOR};
  border-radius: 4pt;
  max-width: 100%;
}
.video-url-label {
  color: ${ACCENT_COLOR};
  font-weight: bold;
  font-size: 9pt;
  margin-bottom: 5pt;
  text-transform: uppercase;
}
.section {
  margin-bottom: 8pt;
}
.section-label {
  color: ${ACCENT_COLOR};
  font-size: 13pt;
  font-weight: bold;
  margin-bottom: 2pt;
  word-wrap: break-word;
  overflow-wrap: break-word;
}
.section-text {
  color: ${TEXT_COLOR};
  font-size: 11pt;
  line-height: 1.25;
  word-wrap: break-word;
  overflow-wrap: break-word;
  margin: 0;
}
</style>
</head>
<body>
<h1 class="title">${escapeHtml(slide.title || '')}</h1>
<div class="content-wrapper">
  <div class="text-content">
    ${content.purpose ? `<div class="section">
      <p class="section-label">Purpose:</p>
      <p class="section-text">${escapeHtml(content.purpose)}</p>
    </div>` : ''}
    ${content.alert_logic ? `<div class="section">
      <p class="section-label">Alert Logic:</p>
      <p class="section-text">${escapeHtml(content.alert_logic)}</p>
    </div>` : ''}
    ${content.preconditions ? `<div class="section">
      <p class="section-label">Preconditions:</p>
      <p class="section-text">${escapeHtml(content.preconditions)}</p>
    </div>` : ''}
    ${content.data_requirements ? `<div class="section">
      <p class="section-label">Data Requirements:</p>
      <p class="section-text">${escapeHtml(content.data_requirements)}</p>
    </div>` : ''}
  </div>
  <div class="media-content">
    ${mediaRelPath ? (isVideo
      ? `<video src="${mediaRelPath}" controls data-media-path="${mediaRelPath}" data-media-type="video" style="max-width: 100%; max-height: 100%;"></video>`
      : `<img src="${mediaRelPath}" alt="${escapeHtml(slide.title)}" data-media-path="${mediaRelPath}" data-media-type="image" />`
    ) : hasVideoUrl ? (
      `<div class="video-url-text">
        <p class="video-url-label">Video URL</p>
        <p style="margin: 0; word-break: break-all;">${escapeHtml(videoUrl)}</p>
      </div>`
    ) : ''}
  </div>
</div>
</body>
</html>`;
}

module.exports = { generateModuleDescriptionHTML };



