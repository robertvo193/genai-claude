#!/bin/bash
# Start the training progress dashboard

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Starting Training Progress Dashboard..."
echo ""
echo "   Dashboard will be available at: http://localhost:5000"
echo "   Press Ctrl+C to stop the server"
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "❌ Flask not found. Installing..."
    pip3 install flask
fi

# Start the server
python3 progress_server.py
