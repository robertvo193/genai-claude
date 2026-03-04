#!/usr/bin/env python3
"""
Training Progress Web Server
Simple Flask server to display training progress in real-time
"""

from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Progress file location
PROGRESS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'progress.json')

def read_progress():
    """Read progress from JSON file"""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        except:
            return None
    return None

@app.route('/')
def index():
    """Render progress dashboard"""
    progress = read_progress()
    return render_template('progress.html', progress=progress)

@app.route('/api/progress')
def api_progress():
    """Return progress as JSON"""
    progress = read_progress()
    return jsonify(progress or {})

@app.route('/api/progress/update', methods=['POST'])
def update_progress():
    """Update progress (called by training script)"""
    from flask import request
    data = request.get_json()

    # Add timestamp
    data['last_updated'] = datetime.now().isoformat()

    # Save to file
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    os.makedirs(template_dir, exist_ok=True)

    # Check if template exists, if not create it
    template_path = os.path.join(template_dir, 'progress.html')
    if not os.path.exists(template_path):
        create_template(template_path)

    print("🚀 Training Progress Server")
    print("   Open http://localhost:5000 in your browser")
    app.run(host='0.0.0.0', port=5000, debug=False)

def create_template(path):
    """Create the HTML template"""
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Training Progress - Auto Train</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
            max-width: 800px;
            width: 100%;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2em;
            margin-bottom: 10px;
        }

        .header p {
            opacity: 0.9;
            font-size: 0.9em;
        }

        .content {
            padding: 30px;
        }

        .status-card {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }

        .status-card h2 {
            font-size: 1.2em;
            margin-bottom: 15px;
            color: #333;
        }

        .progress-bar {
            width: 100%;
            height: 30px;
            background: #e9ecef;
            border-radius: 15px;
            overflow: hidden;
            margin: 20px 0;
            position: relative;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 0.85em;
        }

        .todo-list {
            list-style: none;
        }

        .todo-item {
            background: white;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }

        .todo-item:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }

        .todo-status {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            margin-right: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            flex-shrink: 0;
        }

        .todo-status.pending {
            background: #6c757d;
            color: white;
        }

        .todo-status.in_progress {
            background: #ffc107;
            color: #333;
            animation: pulse 1.5s infinite;
        }

        .todo-status.completed {
            background: #28a745;
            color: white;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }

        .todo-text {
            flex: 1;
            font-size: 0.95em;
            color: #333;
        }

        .todo-item.completed .todo-text {
            text-decoration: line-through;
            color: #999;
        }

        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .metric-card {
            background: white;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .metric-value {
            font-size: 1.8em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }

        .metric-label {
            font-size: 0.85em;
            color: #666;
        }

        .last-updated {
            text-align: center;
            color: #999;
            font-size: 0.85em;
            margin-top: 20px;
        }

        .no-data {
            text-align: center;
            padding: 40px;
            color: #999;
        }

        .no-data svg {
            width: 80px;
            height: 80px;
            margin-bottom: 20px;
            opacity: 0.3;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Auto Train Progress</h1>
            <p>Real-time training progress tracker</p>
        </div>

        <div class="content" id="content">
            {% if progress %}
            <div class="status-card">
                <h2>📊 Training Status</h2>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {{ progress.progress }}%">
                        {{ progress.progress }}%
                    </div>
                </div>
                <p><strong>Current Phase:</strong> {{ progress.current_phase }}</p>
                <p><strong>Use Case:</strong> {{ progress.use_case }}</p>
                <p><strong>Dataset:</strong> {{ progress.dataset_path }}</p>

                {% if progress.metrics %}
                <div class="metrics">
                    <div class="metric-card">
                        <div class="metric-value">{{ progress.metrics.images }}</div>
                        <div class="metric-label">Images</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{{ progress.metrics.classes }}</div>
                        <div class="metric-label">Classes</div>
                    </div>
                    {% if progress.metrics.epoch %}
                    <div class="metric-card">
                        <div class="metric-value">{{ progress.metrics.epoch }}</div>
                        <div class="metric-label">Epoch</div>
                    </div>
                    {% endif %}
                    {% if progress.metrics.map50 %}
                    <div class="metric-card">
                        <div class="metric-value">{{ progress.metrics.map50 }}</div>
                        <div class="metric-label">mAP50</div>
                    </div>
                    {% endif %}
                </div>
                {% endif %}
            </div>

            <div class="status-card">
                <h2>✓ Task Progress</h2>
                <ul class="todo-list">
                    {% for todo in progress.todos %}
                    <li class="todo-item {{ todo.status }}">
                        <div class="todo-status {{ todo.status }}">
                            {% if todo.status == 'completed' %}✓
                            {% elif todo.status == 'in_progress' %}⟳
                            {% else %}○
                            {% endif %}
                        </div>
                        <div class="todo-text">{{ todo.content }}</div>
                    </li>
                    {% endfor %}
                </ul>
            </div>

            <div class="last-updated">
                Last updated: {{ progress.last_updated }}
            </div>
            {% else %}
            <div class="no-data">
                <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
                <p>Waiting for training to start...</p>
                <p style="font-size: 0.9em; margin-top: 10px;">Run /auto-train command to begin</p>
            </div>
            {% endif %}
        </div>
    </div>

    <script>
        // Auto-refresh every 2 seconds
        setTimeout(function() {
            location.reload();
        }, 2000);
    </script>
</body>
</html>'''

    with open(path, 'w') as f:
        f.write(html)

    print(f"✅ Created template: {template_path}")
