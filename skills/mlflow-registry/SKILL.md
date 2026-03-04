---
name: mlflow-registry
description: MLflow Model Registry and Dataset Versioning for orchestration. Use when managing MLflow models (register, promote, query) or datasets (version, tag, retrieve). Integrates with Ray/training workflows - Ray workers handle training metrics, this skill handles orchestration.
license: MIT
---

# MLflow Registry & Dataset Versioning

Skill for managing MLflow Model Registry and Dataset Versioning. Focuses on orchestration-layer operations, not training-loop logging (handled by Ray workers).

## Prerequisites

```bash
# Install MLflow
pip install mlflow

# Start MLflow server
mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root ./mlflow-artifacts \
    --host 0.0.0.0 \
    --port 5001
```

Set environment variable:
```bash
export MLFLOW_TRACKING_URI=http://localhost:5001
```

## Quick Reference

### Experiments
- `scripts/create_experiment.py <name>` - Create experiment
- `scripts/list_experiments.py` - List all experiments

### Training Logging
- `scripts/log_training.py` - Create run, log metrics + model + artifacts (returns run_id)

### Dataset Versioning
- `scripts/log_dataset.py <dataset_name> <dataset_path>` - Log dataset version
- `scripts/get_dataset.py <dataset_name> [--version <ver>]` - Get dataset URI
- `scripts/list_datasets.py` - List all datasets

### Model Registry
- `scripts/register_model.py <run_id> <model_name>` - Register model from run
- `scripts/get_model.py <model_name> [--stage <stage>]` - Get model URI
- `scripts/promote_model.py <model_name> <version> <stage>` - Transition stage
- `scripts/list_models.py` - List registered models
- `scripts/model_info.py <model_name> <version>` - Get model metadata

---

## Experiments

### Create Experiment

Organize runs by creating experiments first:

```bash
# Create experiment
python scripts/create_experiment.py --name "PPE-Detection"

# Create with description and tags
python scripts/create_experiment.py \
    --name "PPE-Detection" \
    --description "PPE object detection experiments" \
    --tags "team:vision,project:ppe"
```

### List Experiments

```bash
# List active experiments
python scripts/list_experiments.py

# Include deleted experiments
python scripts/list_experiments.py --all
```

---

## Training Logging

### Log Training Results

After training completes, log everything to MLflow:

```bash
python scripts/log_training.py \
    --experiment-name "PPE-Detection" \
    --run-name "yolo-ppe-v1" \
    --params "epochs:100,batch:16,imgsz:640" \
    --metrics "mAP50:0.85,mAP95:0.72,precision:0.92,f1:0.90" \
    --model-artifact "runs/detect/train/weights/best.pt" \
    --artifacts "confusion_matrix.png,results.csv" \
    --tags "use_case:ppe,dataset:ppe-v1"
```

**Returns:** `run_id` for model registration

### Minimal Example

```bash
# Just log model + metrics
python scripts/log_training.py \
    --metrics "mAP50:0.85" \
    --model-artifact "best.pt"
```

---

## Dataset Versioning

### Log Dataset

```bash
python scripts/log_dataset.py \
    --name "ppe-detection-v1" \
    --path "/data/ppe/train" \
    --description "PPE detection training dataset" \
    --tags "use_case:ppe,version:1.0,split:train"
```

**Returns:** Dataset URI for use in training scripts

### Get Dataset

```bash
# Get latest version
python scripts/get_dataset.py --name "ppe-detection-v1"

# Get specific version
python scripts/get_dataset.py --name "ppe-detection-v1" --version "3"
```

**Returns:** Dataset path and metadata

### List Datasets

```bash
python scripts/list_datasets.py
```

**Returns:** All registered datasets with versions

---

## Model Registry

### Register Model

After Ray training completes, register the model:

```bash
python scripts/register_model.py \
    --run-id "abc123def456" \
    --name "yolo-ppe-detection" \
    --description "YOLOv8n for PPE detection" \
    --tags "use_case:ppe,dataset:ppe-detection-v1"
```

**Returns:** Model version info

### Get Model URI

Get model URI for deployment/inference:

```bash
# Get production model
python scripts/get_model.py \
    --name "yolo-ppe-detection" \
    --stage "Production"

# Get specific version
python scripts/get_model.py \
    --name "yolo-ppe-detection" \
    --version "5"
```

**Returns:** Model URI (e.g., `s3://mlflow/5/model.pt`)

### Promote Model

Transition model through stages:

```bash
python scripts/promote_model.py \
    --name "yolo-ppe-detection" \
    --version "3" \
    --stage "Production" \
    --archive-existing
```

**Stages:** `None` → `Staging` → `Production` → `Archived`

### List Models

```bash
# List all models
python scripts/list_models.py

# List versions of specific model
python scripts/list_models.py --name "yolo-ppe-detection"
```

### Get Model Info

Get training metadata (params, metrics, dataset):

```bash
python scripts/model_info.py \
    --name "yolo-ppe-detection" \
    --version "5"
```

**Returns:**
- Training parameters
- Validation metrics
- Linked dataset version
- Artifact location

---

## Integration with Ray Workers

Ray workers should log directly to MLflow using Python API:

```python
# Ray worker script (runs on cluster)
import mlflow

def train_yolo(config):
    with mlflow.start_run() as run:
        # Log hyperparameters
        mlflow.log_params(config)

        # Training loop
        for epoch in range(epochs):
            metrics = train_one_epoch()
            mlflow.log_metrics(metrics, step=epoch)

        # Log model artifact
        mlflow.log_artifact("runs/detect/train/weights/best.pt")

        # Return run_id for registration
        return run.info.run_id
```

After training completes, use skill to register:
```bash
python scripts/register_model.py --run-id $RUN_ID --name "yolo-ppe"
```

---

## Common Workflows

### 0. Setup Experiment

```bash
# Create experiment to organize runs
python scripts/create_experiment.py \
    --name "PPE-Detection" \
    --description "PPE object detection experiments" \
    --tags "team:vision,project:ppe"
```

### 1. Prepare Training Data

```bash
# 1. Log dataset
python scripts/log_dataset.py \
    --name "ppe-detection-v2" \
    --path "/data/ppe/v2" \
    --tags "use_case:ppe,version:2.0"

# 2. Get dataset URI for training script
DATASET_URI=$(python scripts/get_dataset.py --name "ppe-detection-v2" --uri-only)

# 3. Pass to Ray training
ray submit training_job.py --dataset $DATASET_URI
```

### 2. Log Training Results

```bash
# After training completes
python scripts/log_training.py \
    --experiment-name "PPE-Detection" \
    --run-name "yolo-ppe-v2" \
    --params "epochs:100,batch:16" \
    --metrics "mAP50:0.85,precision:0.92" \
    --model-artifact "best.pt" \
    --tags "dataset:ppe-detection-v2"

# Returns RUN_ID for next step
```

### 3. Register Trained Model

```bash
# 1. From log_training output or Ray training
RUN_ID="abc123..."

# 2. Register model
python scripts/register_model.py \
    --run-id $RUN_ID \
    --name "yolo-ppe-detection" \
    --tags "dataset:ppe-detection-v2"

# 3. Promote to staging
python scripts/promote_model.py \
    --name "yolo-ppe-detection" \
    --version "1" \
    --stage "Staging"
```

### 4. Deploy Model

```bash
# 1. Get production model URI
MODEL_URI=$(python scripts/get_model.py \
    --name "yolo-ppe-detection" \
    --stage "Production" \
    --uri-only)

# 2. Deploy to inference
python deploy_inference.py --model $MODEL_URI
```

---

## Script Reference

### Environment Variables

All scripts respect:
- `MLFLOW_TRACKING_URI` - MLflow server URL (default: `http://localhost:5001`)
- `MLFLOW_REGISTRY_URI` - Model registry URI (default: same as tracking URI)

### Output Formats

- **Default:** Human-readable table
- `--json`: JSON output for parsing
- `--uri-only`: Return only URI (for shell pipes)
- `--quiet`: Suppress headers/prompts

### Error Handling

Scripts exit with codes:
- `0`: Success
- `1`: MLflow connection error
- `2`: Resource not found
- `3`: Validation error

---

## Troubleshooting

### Connection Issues
```bash
# Check MLflow server
curl http://localhost:5001/health

# Verify tracking URI
echo $MLFLOW_TRACKING_URI
```

### Dataset Not Found
```bash
# List all datasets to find correct name
python scripts/list_datasets.py
```

### Model Version Conflicts
```bash
# Check existing versions
python scripts/list_models.py --name "yolo-ppe"

# Archive old version before promoting new one
python scripts/promote_model.py --name "yolo-ppe" --version "4" --stage "Archived"
```

---

## References

- [MLflow Model Registry Docs](https://mlflow.org/docs/latest/model-registry.html)
- [MLflow Dataset API](https://mlflow.org/docs/latest/datasets.html)
- [MLflow Python API](https://mlflow.org/docs/latest/python_api/index.html)
