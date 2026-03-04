#!/usr/bin/env bash
# Setup openclaw cron jobs for ViAct Outbound Orchestrator.
# Run this script on any new VM after openclaw is installed.
# Safe to re-run — removes existing ViAct jobs before re-registering.
#
# Usage: bash setup_cron.sh

set -e

# ---------------------------------------------------------------------------
# Resolve openclaw binary
# ---------------------------------------------------------------------------
if command -v openclaw &>/dev/null; then
    OPENCLAW="openclaw"
elif [ -x "$HOME/.npm-global/bin/openclaw" ]; then
    OPENCLAW="$HOME/.npm-global/bin/openclaw"
elif ls "$HOME"/.nvm/versions/node/*/bin/openclaw &>/dev/null 2>&1; then
    OPENCLAW=$(ls "$HOME"/.nvm/versions/node/*/bin/openclaw | tail -1)
else
    echo "ERROR: openclaw binary not found. Install it first." >&2
    exit 1
fi

echo "Using openclaw at: $OPENCLAW"

# ---------------------------------------------------------------------------
# Remove all existing ViAct cron jobs (clean slate)
# ---------------------------------------------------------------------------
echo "Removing existing ViAct cron jobs..."
"$OPENCLAW" cron list 2>/dev/null \
    | awk '/^[0-9a-f-]{36}/ && /ViAct/ {print $1}' \
    | while read -r JOB_ID; do
        echo "  Removing $JOB_ID"
        "$OPENCLAW" cron rm "$JOB_ID" 2>/dev/null || true
      done

# ---------------------------------------------------------------------------
# Register two new jobs
# ---------------------------------------------------------------------------
SCRIPT_PATH="$HOME/.claude/skills/viact-outbound-orchestrator"
VENV="source $SCRIPT_PATH/.venv/bin/activate"
PY="python3 $SCRIPT_PATH/skill/orchestrator.py"

SEND_CMD="$VENV && $PY send"
CHECK_CMD="$VENV && $PY check-replies"

# Job 1: Send pending emails — every 3 minutes
echo "Registering: ViAct — Send Pending Emails (*/3 * * * *)"
"$OPENCLAW" cron add \
    --name "ViAct — Send Pending Emails" \
    --cron "*/3 * * * *" \
    --session isolated \
    --message "Run this shell command exactly and report output: bash -c '$SEND_CMD'" \
    --no-deliver

# Job 2: Check client replies — every 10 minutes
echo "Registering: ViAct — Check Client Replies (*/10 * * * *)"
"$OPENCLAW" cron add \
    --name "ViAct — Check Client Replies" \
    --cron "*/10 * * * *" \
    --session isolated \
    --message "Run this shell command exactly and report output: bash -c '$CHECK_CMD'" \
    --no-deliver

echo ""
echo "Done. Current cron jobs:"
"$OPENCLAW" cron list
