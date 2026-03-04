# MLflow Registry Quick Start

## Prerequisites

MLflow server must be running (configured with systemd):

```bash
# Check MLflow status
sudo systemctl status mlflow

# Set environment variable (add to ~/.bashrc for persistence)
export MLFLOW_TRACKING_URI=http://localhost:5001
```

## Verify Connection

```bash
python ~/.claude/skills/mlflow-registry/scripts/check_mlflow.py
```

Expected output:
```
MLflow Tracking URI: http://localhost:5001
✓ Connection successful
✓ Model Registry available
✓ Found 1 experiment(s)
✓ Found 0 registered model(s)
```

## Common Workflows

### 1. Dataset Versioning

```bash
# Log dataset
python ~/.claude/skills/mlflow-registry/scripts/log_dataset.py \
    --name "ppe-detection-v1" \
    --path "/data/ppe/train" \
    --tags "use_case:ppe,version:1.0,split:train"

# Get dataset URI
python ~/.claude/skills/mlflow-registry/scripts/get_dataset.py --name "ppe-detection-v1" --uri-only

# List all datasets
python ~/.claude/skills/mlflow-registry/scripts/list_datasets.py
```

### 2. Model Registry

After training completes and you have a `run_id`:

```bash
# Register model
python ~/.claude/skills/mlflow-registry/scripts/register_model.py \
    --run-id "abc123def456" \
    --name "yolo-ppe-detection" \
    --tags "use_case:ppe,dataset:ppe-detection-v1"

# List models
python ~/.claude/skills/mlflow-registry/scripts/list_models.py

# List versions
python ~/.claude/skills/mlflow-registry/scripts/list_models.py --name "yolo-ppe-detection"

# Get model URI for deployment
python ~/.claude/skills/mlflow-registry/scripts/get_model.py \
    --name "yolo-ppe-detection" \
    --stage "Production" \
    --uri-only

# Promote to production
python ~/.claude/skills/mlflow-registry/scripts/promote_model.py \
    --name "yolo-ppe-detection" \
    --version "1" \
    --stage "Production" \
    --archive-existing
```

### 3. Model Metadata

```bash
# Get training info
python ~/.claude/skills/mlflow-registry/scripts/model_info.py \
    --name "yolo-ppe-detection" \
    --version "1"
```

## Integration with Ray Workers

Your Ray worker should log to MLflow:

```python
# Ray worker script
import mlflow

def train_yolo(config):
    # MLflow auto-tracking from environment
    with mlflow.start_run() as run:
        # Log hyperparameters
        mlflow.log_params({
            "model": config["model"],
            "epochs": config["epochs"],
            "batch_size": config["batch_size"]
        })

        # Training loop
        for epoch in range(config["epochs"]):
            metrics = train_one_epoch()
            mlflow.log_metrics(metrics, step=epoch)

        # Log model artifact
        mlflow.log_artifact("runs/detect/train/weights/best.pt")

        # Return run_id for registration
        return run.info.run_id
```

After Ray job completes, register the model:
```bash
RUN_ID=$(ray job get-rays-job.py --last-run-id)
python register_model.py --run-id $RUN_ID --name "yolo-ppe"
```

## Using with Claude Code

The `mlflow-registry` skill is now available. Claude can:
- Manage dataset versions
- Register and query models
- Promote models between stages
- Get model metadata

Example prompts:
- "Register the latest run as model yolo-ppe-detection-v2"
- "Get the production model URI for yolo-ppe-detection"
- "Promote version 3 of yolo-ppe-detection to production"
- "Show me the training metrics for yolo-ppe-detection version 2"

## Troubleshooting

### Connection Error
```bash
# Check if MLflow server is running
curl http://localhost:5001/health

# Restart server
cd /home/philiptran/.claude/skills/mlflow-registry/scripts
bash setup_mlflow.sh
```

### Permission Errors
```bash
# Make scripts executable
chmod +x /home/philiptran/.claude/skills/mlflow-registry/scripts/*.py
chmod +x /home/philiptran/.claude/skills/mlflow-registry/scripts/*.sh
```

### Module Not Found
```bash
# Install tabulate
pip install tabulate

# Reinstall mlflow
pip install --upgrade 'mlflow>=2.18.0'
```
