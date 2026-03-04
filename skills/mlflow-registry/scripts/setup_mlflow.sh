#!/bin/bash
# Setup and start MLflow server for model registry and dataset versioning

set -e

# Default values
MLFLOW_PORT="${MLFLOW_PORT:-5001}"
MLFLOW_HOST="${MLFLOW_HOST:-0.0.0.0}"
MLFLOW_BACKEND_STORE="${MLFLOW_BACKEND_STORE:-./mlflow.db}"
MLFLOW_ARTIFACT_ROOT="${MLFLOW_ARTIFACT_ROOT:-./mlflow-artifacts}"
MLFLOW_DEFAULT_ARTIFACT_ROOT="${MLFLOW_DEFAULT_ARTIFACT_ROOT:-./mlflow-artifacts}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

echo_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

echo_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if mlflow is installed
check_mlflow() {
    if ! command -v mlflow &> /dev/null; then
        echo_error "MLflow is not installed!"
        echo "Install with: pip install 'mlflow>=2.18.0'"
        exit 1
    fi
    echo_info "MLflow found: $(mlflow --version)"
}

# Create directories
create_dirs() {
    echo_info "Creating MLflow directories..."
    mkdir -p "$(dirname "$MLFLOW_BACKEND_STORE")"
    mkdir -p "$MLFLOW_ARTIFACT_ROOT"
}

# Start MLflow server
start_mlflow() {
    echo_info "Starting MLflow server..."
    echo_info "Tracking URI: http://$MLFLOW_HOST:$MLFLOW_PORT"
    echo_info "Backend store: $MLFLOW_BACKEND_STORE"
    echo_info "Artifact root: $MLFLOW_ARTIFACT_ROOT"
    echo ""
    echo_warn "Press Ctrl+C to stop the server"
    echo ""

    export MLFLOW_TRACKING_URI="http://localhost:$MLFLOW_PORT"

    mlflow server \
        --backend-store-uri "$MLFLOW_BACKEND_STORE" \
        --default-artifact-root "$MLFLOW_DEFAULT_ARTIFACT_ROOT" \
        --host "$MLFLOW_HOST" \
        --port "$MLFLOW_PORT" \
        --serve-artifacts
}

# Main
main() {
    echo "=================================="
    echo "  MLflow Server Setup"
    echo "=================================="
    echo ""

    check_mlflow
    create_dirs
    start_mlflow
}

main
