# Google Drive Skill

Interact with Google Drive using PyDrive2. Supports uploading, downloading, searching, and managing files.

---

## Prerequisites

- Python 3.8+
- A Google Cloud project with the Drive API enabled
- OAuth 2.0 credentials (Desktop app type)

---

## Authentication Setup

### 1. Create Google Cloud credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project (or select an existing one)
3. Enable **Google Drive API**: APIs & Services → Enable APIs → search "Google Drive API"
4. Create credentials: APIs & Services → Credentials → Create Credentials → **OAuth 2.0 Client ID**
   - Application type: **Desktop app**
5. Download the JSON file and save it as `~/.gdrivelm/credentials.json`

### 2. Configure settings

Create the config directory and copy the settings template:

```bash
mkdir -p ~/.gdrivelm
cp ~/.claude/skills/google-drive/assets/settings_template.yaml ~/.gdrivelm/settings.yaml
```

The `settings.yaml` points to your credentials and token files:

```yaml
client_config_backend: file
client_config_file: ~/.gdrivelm/credentials.json

save_credentials: True
save_credentials_backend: file
save_credentials_file: ~/.gdrivelm/token.json

get_refresh_token: True

oauth_scope:
  - https://www.googleapis.com/auth/drive
  - https://www.googleapis.com/auth/drive.file
  - https://www.googleapis.com/auth/drive.metadata.readonly
```

### 3. Authorize (first-time only)

Run the helper script once to open the OAuth browser flow and generate `~/.gdrivelm/token.json`:

```bash
source ~/.claude/skills/google-drive/.venv/bin/activate
python ~/.claude/skills/google-drive/scripts/gdrive_helper.py search "test"
```

A browser window will open asking you to sign in with Google and grant Drive access. The token is saved automatically and refreshed on subsequent runs.

---

## Virtual Environment

The skill ships with a pre-configured `.venv`. Always use it — do **not** create a new one.

```bash
# Activate the skill venv
source ~/.claude/skills/google-drive/.venv/bin/activate

# Or activate all skills at once
source ~/.claude-skills-env.sh
```

To install dependencies manually if needed:

```bash
source ~/.claude/skills/google-drive/.venv/bin/activate
pip install -r ~/.claude/skills/google-drive/requirements.txt
```

---

## Quick Start

```python
import sys, os

skill_path = os.path.expanduser('~/.claude/skills/google-drive/scripts')
sys.path.insert(0, skill_path)

from gdrive_helper import authenticate, upload_file, download_file, search_files

drive = authenticate()

# Upload a file
result = upload_file(drive, '/path/to/report.pdf', title='Q1 Report')
print(f"Uploaded: {result['id']}")

# Search files
files = search_files(drive, "title contains 'report' and trashed = false")
for f in files:
    print(f"{f['title']} — {f['id']}")

# Download a file
download_file(drive, 'FILE_ID', '/tmp/report.pdf')
```

---

## File Structure

```
skills/google-drive/
├── SKILL.md                        # Full skill documentation (loaded by Claude)
├── README.md                       # This file — setup guide
├── requirements.txt                # Python dependencies
├── scripts/
│   ├── gdrive_helper.py            # Main helper: upload, download, search, etc.
│   └── gsheets_helper.py           # Google Sheets helper
└── assets/
    └── settings_template.yaml      # Template for ~/.gdrivelm/settings.yaml
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `credentials.json` not found | Download from Google Cloud Console and place at `~/.gdrivelm/credentials.json` |
| `token.json` not found | Run `authenticate()` once to trigger the browser OAuth flow |
| `Token expired` error | Delete `~/.gdrivelm/token.json` and re-run to re-authorize |
| `FileNotDownloadableError` on Google Docs | Use `file.GetContentString(mimetype='text/plain')` instead of direct download |
| `403 Permission denied` | Ensure the Google account has access to the file |

---

For full API reference and advanced usage, see [SKILL.md](SKILL.md).
