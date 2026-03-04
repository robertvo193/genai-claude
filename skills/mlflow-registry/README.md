# MLflow Registry Skill

MLflow Model Registry and Dataset Versioning skill for Claude Code.

## Overview

This skill provides:
- **Dataset Versioning**: Track and version training datasets
- **Model Registry**: Register, manage, and promote ML models
- **Integration Ready**: Works with Ray.io training workflows

## What This Skill Does

✅ **Does:**
- Log and query dataset versions
- Register trained models to Model Registry
- Promote models between stages (Staging → Production)
- Get model URIs for deployment
- Query model metadata (params, metrics, dataset)

❌ **Does NOT:**
- Handle training loop logging (Ray workers do this directly)
- Replace the official MLflow MCP (which is for LLM traces)
- Provide real-time training monitoring

## Quick Start

1. **Install MLflow**
   ```bash
   pip install 'mlflow>=2.18.0' tabulate
   ```

2. **Start MLflow server**
   ```bash
   cd scripts
   bash setup_mlflow.sh
   ```

3. **Set environment variable**
   ```bash
   export MLFLOW_TRACKING_URI=http://localhost:5001
   ```

4. **Verify connection**
   ```bash
   python scripts/check_mlflow.py
   ```

See [QUICKSTART.md](QUICKSTART.md) for detailed usage examples.

## Scripts

### Dataset Versioning
| Script | Description |
|--------|-------------|
| `log_dataset.py` | Log dataset with versioning |
| `get_dataset.py` | Get dataset URI by name/version |
| `list_datasets.py` | List all datasets |

### Model Registry
| Script | Description |
|--------|-------------|
| `register_model.py` | Register model from run |
| `get_model.py` | Get model URI by stage/version |
| `promote_model.py` | Promote model to different stage |
| `list_models.py` | List models and versions |
| `model_info.py` | Get model training metadata |

### Utilities
| Script | Description |
|--------|-------------|
| `setup_mlflow.sh` | Start MLflow server |
| `check_mlflow.py` | Check MLflow connection |

## Usage Examples

### Dataset Versioning
```bash
# Log dataset
python scripts/log_dataset.py \
    --name "ppe-detection-v1" \
    --path "/data/ppe/train" \
    --tags "use_case:ppe,version:1.0"

# Get dataset URI
python scripts/get_dataset.py --name "ppe-detection-v1" --uri-only
```

### Model Registry
```bash
# Register model (after Ray training)
python scripts/register_model.py \
    --run-id "abc123" \
    --name "yolo-ppe-detection" \
    --tags "dataset:ppe-detection-v1"

# Get production model
python scripts/get_model.py \
    --name "yolo-ppe-detection" \
    --stage "Production" \
    --uri-only

# Promote to production
python scripts/promote_model.py \
    --name "yolo-ppe-detection" \
    --version "1" \
    --stage "Production" \
    --archive-existing
```

## Integration with Ray Workers

Ray workers log to MLflow directly:

```python
# Ray worker template
import mlflow
import os

def train_yolo(config):
    # Auto-connect from MLFLOW_TRACKING_URI
    with mlflow.start_run() as run:
        # Log hyperparameters
        mlflow.log_params(config)

        # Training loop
        for epoch in range(config["epochs"]):
            metrics = train_one_epoch()
            mlflow.log_metrics(metrics, step=epoch)

        # Log model
        mlflow.log_artifact("runs/detect/train/weights/best.pt")

        # Return run_id for registration
        return run.info.run_id
```

After Ray training completes, use this skill to register:
```bash
RUN_ID=$(ray job status --job-id $JOB_ID --output json | jq .run_id)
python scripts/register_model.py --run-id $RUN_ID --name "yolo-ppe"
```

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ Vibe Kanban │ ──→ │   Ray.io     │ ──→ │  MLflow     │
│  (Tasks)    │     │  (Training)  │     │ (Registry)  │
└─────────────┘     └──────────────┘     └─────────────┘
                          │                      ▲
                          │                      │
                          ├─ Logs metrics ──────┤
                          │  (direct API)        │
                          │                      │
                          └──────────────────────┘
                           This skill orchestrates
                           dataset + model registration
```

## Official MLflow MCP vs This Skill

| Feature | Official MLflow MCP | This Skill |
|---------|---------------------|------------|
| Purpose | LLM trace observability | Model registry + datasets |
| Tools | `search_traces`, `log_feedback` | `register_model`, `log_dataset` |
| Use case | GenAI applications | Traditional ML (YOLO, SAM3) |
| Training loop | Not applicable | Ray handles directly |

This skill is **complementary** to the official MLflow MCP, not a replacement.

## License

MIT
