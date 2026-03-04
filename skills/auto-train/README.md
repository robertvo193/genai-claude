# Auto-Train Progress Dashboard

A simple web UI to track training progress in real-time when running `/auto-train`.

## Features

- 🚀 **Real-time progress tracking** - Auto-refreshes every 2 seconds
- 📊 **Visual progress bar** - See overall completion percentage
- ✓ **Task checklist** - Track completed, in-progress, and pending tasks
- 📈 **Live metrics** - Displays images, classes, epochs, mAP50, etc.
- 🎨 **Beautiful UI** - Modern, responsive design

## Quick Start

### 1. Start the Dashboard (Before Training)

Open a terminal and run:

```bash
~/.claude/skills/auto-train/start_dashboard.sh
```

Or manually:

```bash
cd ~/.claude/skills/auto-train
python3 progress_server.py
```

The dashboard will be available at: **http://localhost:5000**

### 2. Run Auto-Train

In another terminal, run your training command:

```bash
/auto-train "train danger zone detection with dataset-mexico-complete"
```

### 3. Watch Progress

Open http://localhost:5000 in your browser to see:
- Current phase (Parsing, Surveying, Preparing, Training, Packaging)
- Progress percentage
- Task checklist with status
- Live training metrics

## Usage

### Starting the Dashboard

```bash
# Option 1: Use the launcher script
~/.claude/skills/auto-train/start_dashboard.sh

# Option 2: Run directly with Python
cd ~/.claude/skills/auto-train
python3 progress_server.py
```

The dashboard will auto-refresh every 2 seconds to show the latest progress.

### Manually Updating Progress

You can manually update the progress for testing:

```bash
cd ~/.claude/skills/auto-train
python3 progress_helper.py \
  "Danger Zone Detection" \
  "dataset-mexico-complete" \
  "Training Model" \
  65 \
  '[{"content":"Parse request","status":"completed"},{"content":"Survey dataset","status":"completed"},{"content":"Train model","status":"in_progress"}]'
```

## Files

```
~/.claude/skills/auto-train/
├── progress_server.py       # Flask web server
├── progress_helper.py       # Progress update helper
├── start_dashboard.sh       # Quick launcher script
├── templates/
│   └── progress.html        # Web UI template (auto-created)
├── progress.json            # Current progress state (auto-created)
└── README.md                # This file
```

## Dashboard Features

### Status Indicators

- **⭕ Pending** - Task not started
- **⟳ In Progress** - Task currently running (animated)
- **✓ Completed** - Task finished

### Color Coding

- **Purple gradient** - Header and progress bar
- **Yellow** - In-progress tasks (pulsing animation)
- **Green** - Completed tasks
- **Gray** - Pending tasks

### Metrics Displayed

- **Images** - Total number of training images
- **Classes** - Number of object classes
- **Epoch** - Current training epoch (when training)
- **mAP50** - Current model accuracy (when training)

## Integration with Auto-Train

The auto-train workflow automatically updates progress.json during these phases:

1. **Parsing Request** (0-10%)
   - Extract use case, dataset path, requirements

2. **Surveying Dataset** (10-20%)
   - Count images, identify classes

3. **Preparing Data** (20-30%)
   - Create train/val/test splits

4. **Training Model** (30-90%)
   - Run YOLO training with live epoch/mAP updates

5. **Packaging Results** (90-100%)
   - Create final package with model and visualizations

## Troubleshooting

### Dashboard Not Loading

1. Check if Flask is installed:
   ```bash
   pip3 install flask
   ```

2. Check if port 5000 is available:
   ```bash
   lsof -i :5000
   ```

3. Try a different port:
   ```bash
   python3 progress_server.py
   # Edit progress_server.py: change port=5000 to port=5001
   ```

### Progress Not Updating

1. Check if progress.json exists:
   ```bash
   ls -l ~/.claude/skills/auto-train/progress.json
   ```

2. Verify auto-train is running:
   ```bash
   ps aux | grep auto-train
   ```

3. Check browser console for errors (F12)

## Example Output

When training is running, you'll see:

```
🚀 Auto Train Progress
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Training Status
████████████░░░░░░░░░░░  65%

Current Phase: Training Model
Use Case: Danger Zone Detection
Dataset: dataset-mexico-complete

Metrics:
┌─────────┬─────────┐
│ 1026    │ Images  │
│ 9       │ Classes │
│ 65/100  │ Epoch   │
│ 0.582   │ mAP50   │
└─────────┴─────────┘

✓ Task Progress
  ✓ Parse user request and validate dataset
  ✓ Survey dataset (count images, identify classes)
  ✓ Prepare train/val/test splits using yolo-finetune skill
  ⟳ Train YOLO model using yolo-finetune skill
  ○ Evaluate and package results

Last updated: 2025-01-30 08:15:30
```

## Requirements

- Python 3.6+
- Flask (`pip3 install flask`)
- Web browser (Chrome, Firefox, Safari, Edge)

## License

MIT License - Part of Claude Code Auto-Train Workflow
