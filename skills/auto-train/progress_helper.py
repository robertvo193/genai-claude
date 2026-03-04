#!/usr/bin/env python3
"""
Progress Update Helper
Updates the progress.json file for the web UI
"""

import json
import os
import sys
from datetime import datetime

PROGRESS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'progress.json')

def update_progress(use_case, dataset_path, current_phase, progress, todos, metrics=None):
    """Update progress file"""
    data = {
        'use_case': use_case,
        'dataset_path': dataset_path,
        'current_phase': current_phase,
        'progress': progress,
        'todos': todos,
        'metrics': metrics or {},
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    with open(PROGRESS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✅ Progress updated: {progress}% - {current_phase}")

def get_progress():
    """Read current progress"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return None

if __name__ == '__main__':
    # Command-line interface for manual updates
    if len(sys.argv) < 5:
        print("Usage: progress_helper.py <use_case> <dataset> <phase> <progress> <todos_json>")
        print("Example:")
        print('  progress_helper.py "PPE detection" "/data" "Training" 45 \'[{"content":"Train model","status":"in_progress"}]\'')
        sys.exit(1)

    use_case = sys.argv[1]
    dataset_path = sys.argv[2]
    current_phase = sys.argv[3]
    progress = int(sys.argv[4])
    todos = json.loads(sys.argv[5])

    update_progress(use_case, dataset_path, current_phase, progress, todos)
