---
name: train-model
description: Autonomous model training - natural language interface for training computer vision models (PPE detection, danger zone, safety monitoring). Auto-detects dataset, selects model, trains end-to-end.
argument-hint: "\"I want to train a model for <use-case> with dataset <path>\""
allowed-tools: TodoWrite(*), AskUserQuestion(*), Read(*), Write(*), Bash(*), Glob(*), Grep(*)
---

# Train Model Command - Autonomous Model Training

Train computer vision models using natural language. Works from ANY directory with any dataset.

## User Interface

```bash
# Simple usage (auto-detects dataset)
/train-model i want to train a model for PPE detection

# With explicit dataset
/train-model i want to train a model for danger zone detection with dataset ./linde-mexico-data

# With priority
/train-model i want to train a model for vest detection with accuracy priority

# With custom output
/train-model i want to train a model for helmet detection with dataset ./data output ./models
```

## 6-Phase Autonomous Workflow

### Phase 1: Intent Analysis

Parse user request to extract:
- **Use case**: What to detect (PPE, danger zone, vest, helmet, etc.)
- **Dataset path**: Where data is located (auto-detect if not specified)
- **Priority**: Speed vs accuracy (default: balanced)
- **Requirements**: Special constraints (real-time, edge deployment, etc.)

```python
# Intent parsing patterns
use_cases = {
    'PPE detection': ['ppe', 'safety equipment', 'protective gear'],
    'danger zone': ['danger zone', 'safety zone', 'restricted area'],
    'vest detection': ['vest', 'safety vest'],
    'helmet detection': ['helmet', 'hard hat', 'safety helmet'],
    'shoe detection': ['shoe', 'safety shoe', 'boot'],
    'glove detection': ['glove', 'safety glove']
}

# Dataset auto-detection
dataset_candidates = [
    './data',
    './dataset',
    './images',
    '../linde-mexico-data',
    '.'
]
```

### Phase 2: Dataset Survey

Automatically analyze dataset:
- **Format detection**: YOLO, COCO, Pascal VOC
- **Count images**: Total training/validation split
- **Class analysis**: Unique classes, distribution
- **Quality check**: Image sizes, aspect ratios, label validity

```bash
# Auto-detect dataset format
if [ -f "data.yaml" ]; then
    format="YOLO"
elif [ -d "annotations" ]; then
    format="COCO"
elif [ -d "labels" ]; then
    format="Pascal VOC"
fi

# Count images
num_images=$(find . -name "*.jpg" -o -name "*.png" | wc -l)

# Analyze classes
classes=$(ls labels/ | wc -l)
```

### Phase 3: Pipeline Design

Auto-select optimal configuration:

| Dataset Size | Priority | Model | Params | Speed |
|--------------|----------|-------|--------|-------|
| < 500 images | speed | YOLOv11n | 2.6M | Fastest |
| 500-5000 | balanced | YOLOv11s | 9.4M | Fast |
| > 5000 | accuracy | YOLOv11m | 20.1M | Medium |

```python
# Model selection logic
if priority == 'speed' or num_images < 500:
    model = 'yolo11n.pt'
elif priority == 'accuracy' or num_images > 5000:
    model = 'yolo11m.pt'
else:
    model = 'yolo11s.pt'

# Hyperparameter configuration
hyperparams = {
    'epochs': min(100, max(50, num_images // 10)),
    'batch': 16 if num_images < 1000 else 32,
    'imgsz': 640,
    'device': '0' if torch.cuda.is_available() else 'cpu'
}
```

### Phase 4: Execution Plan

Create detailed plan with:
- **Time estimate**: Based on dataset size and model
- **Resource check**: GPU availability, disk space
- **Training steps**: Data loading, model initialization, training loop
- **Validation**: mAP, precision, recall targets

```python
# Time estimation
time_per_epoch = 2  # minutes
total_time = epochs * time_per_epoch
print(f"Estimated training time: {total_time} minutes")

# Resource check
gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
if gpu_memory < 4:
    print("⚠️  Warning: Low GPU memory, reducing batch size")
    hyperparams['batch'] = 8
```

### Phase 5: Model Training

Execute training with progress monitoring:
- **Data loading**: Auto-create data.yaml for YOLO
- **Model initialization**: Load pretrained weights
- **Training loop**: Monitor loss, mAP, learning rate
- **Checkpointing**: Save best model automatically

```python
from ultralytics import YOLO

# Create data.yaml
data_yaml = {
    'path': dataset_path,
    'train': 'images/train',
    'val': 'images/val',
    'names': {i: name for i, name in enumerate(classes)}
}

# Initialize model
model = YOLO(model_variant)

# Train with callbacks
results = model.train(
    data='data.yaml',
    epochs=epochs,
    batch=batch_size,
    imgsz=640,
    project=output_path,
    name='train',
    exist_ok=True
)
```

### Phase 6: Evaluation & Packaging

Evaluate performance and package results:
- **Metrics**: mAP@0.5, mAP@0.5:0.95, precision, recall
- **Visualization**: Confusion matrix, PR curves, sample predictions
- **Package**: Model weights + training report + usage guide

```python
# Evaluate
metrics = model.val()

# Generate report
report = {
    'mAP50': metrics.box.map50,
    'mAP50-95': metrics.box.map,
    'precision': metrics.box.mp,
    'recall': metrics.box.mr
}

# Package results
output_dir = f"{output_path}/trained_model_{timestamp}"
output_dir.mkdir()
shutil.copy(f'{output_path}/train/weights/best.pt', output_dir)

# Generate usage guide
with open(f'{output_dir}/README.md', 'w') as f:
    f.write(f"""
# Trained Model Report

## Use Case: {use_case}
## Dataset: {num_images} images, {len(classes)} classes
## Model: {model_variant}

## Performance Metrics
- mAP@0.5: {report['mAP50']:.3f}
- mAP@0.5:0.95: {report['mAP50-95']:.3f}
- Precision: {report['precision']:.3f}
- Recall: {report['recall']:.3f}

## Usage
```python
from ultralytics import YOLO
model = YOLO('best.pt')
results = model('image.jpg')
```
""")
```

## Complete Examples

### Example 1: PPE Detection (Auto-detect dataset)

```bash
/train-model i want to train a model for PPE detection
```

**System automatically**:
1. ✅ Detects dataset in `./linde-mexico-data`
2. ✅ Identifies YOLO format with 1200 images
3. ✅ Finds 6 classes: person, vest, no_vest, shoe, no_shoe, glove
4. ✅ Selects YOLOv11s (balanced for 1200 images)
5. ✅ Trains for 100 epochs (~3 hours on GPU)
6. ✅ Outputs to `./trained_model_20250129/`
   - `best.pt` - Best model weights
   - `README.md` - Usage guide
   - `results.png` - Training curves
   - `confusion_matrix.png` - Confusion matrix

### Example 2: Danger Zone Detection (Explicit dataset)

```bash
/train-model i want to train a model for danger zone detection with dataset ~/datasets/safety
```

**Output**:
```
🔍 Phase 1/6: Analyzing dataset...
   ✅ Found YOLO dataset at ~/datasets/safety
   ✅ 850 images, 2 classes (safe_zone, danger_zone)

🏗️  Phase 2/6: Designing pipeline...
   ✅ Model: YOLOv11s (9.4M params)
   ✅ Epochs: 85, Batch: 16, Image size: 640

📋 Phase 3/6: Creating plan...
   ✅ Estimated time: 2h 50min on GPU
   ✅ Required disk space: 2.1GB

⚙️  Phase 4/6: Training model...
   Epoch 10/85: mAP@0.5=0.42
   Epoch 20/85: mAP@0.5=0.58
   Epoch 30/85: mAP@0.5=0.67
   ...
   Epoch 85/85: mAP@0.5=0.81 ✅

📈 Phase 5/6: Evaluating results...
   ✅ mAP@0.5: 0.812
   ✅ Precision: 0.784
   ✅ Recall: 0.856

✅ Phase 6/6: Packaging results...
   ✅ Model saved to: ./trained_model_20250129/best.pt
   ✅ Report: ./trained_model_20250129/README.md
```

### Example 3: Vest Detection (Accuracy priority)

```bash
/train-model i want to train a model for vest detection with accuracy priority dataset ./data/vest
```

**System selects YOLOv11m** for higher accuracy:
- 20.1M parameters
- 150 epochs
- Expected mAP@0.5: >0.90

### Example 4: Helmet Detection (Speed priority)

```bash
/train-model i want to train a model for helmet detection with speed priority
```

**System selects YOLOv11n** for fastest inference:
- 2.6M parameters
- 50 epochs
- Suitable for edge deployment

## Integration with Existing Workflows

### Use with CCW Workflows

```bash
# Plan training first
/workflow:plan "train YOLO model for PPE detection"

# Then execute training
/train-model i want to train a model for PPE detection

# Review results
/workflow:review-session-cycle --session="<training-session>"
```

### Use with Spec-Driven Development

```bash
# Create spec for custom training pipeline
/spec-create custom-ppe-trainer

# Execute training with custom configuration
/train-model i want to train with custom config.yaml
```

## Error Handling

### Dataset Not Found
```bash
/train-model i want to train a model for PPE detection

# System prompts:
# ⚠️  No dataset found in default locations.
# Please specify dataset path:
# > ./my-custom-dataset
```

### Insufficient Data
```bash
# If < 100 images detected
# ⚠️  Warning: Only 50 images found.
# This may result in poor model performance.
# Continue anyway? [y/N]
```

### GPU Not Available
```bash
# If no GPU detected
# ⚠️  No GPU found. Training on CPU (slow).
# Estimated time: 12 hours.
# Continue? [y/N]
```

## Best Practices

1. **Data Quality**: Ensure labels are accurate and consistent
2. **Data Quantity**: Minimum 100 images per class for acceptable results
3. **Data Split**: Use 80/20 train/validation split
4. **Class Balance**: Ensure balanced class distribution
5. **GPU Training**: Use GPU for datasets > 500 images

## Troubleshooting

### Training Stuck
- Check dataset format
- Verify label files exist
- Reduce batch size if GPU OOM

### Poor Performance
- Increase epochs
- Check data quality
- Use larger model (accuracy priority)
- Add more data

### Slow Training
- Use speed priority
- Reduce image size (imgsz=416)
- Use smaller model (YOLOv11n)

## Output Structure

```
trained_model_20250129_143025/
├── best.pt                    # Best model weights
├── last.pt                    # Last checkpoint
├── README.md                  # Usage guide
├── training_report.json       # Detailed metrics
├── results.png                # Training curves
├── confusion_matrix.png       # Confusion matrix
├── pr_curve.png               # Precision-Recall curve
└── sample_predictions/        # Sample predictions
    ├── image1.jpg
    ├── image2.jpg
    └── ...
```

## Advanced Usage

### Custom Training Configuration

Create `config.yaml`:
```yaml
model: yolo11m.pt
epochs: 150
batch: 32
imgsz: 640
device: 0
augment: true
hsv_h: 0.015
hsv_s: 0.7
hsv_v: 0.4
degrees: 0.0
translate: 0.1
scale: 0.5
flipud: 0.5
fliplr: 0.5
mosaic: 1.0
```

Use custom config:
```bash
/train-model i want to train with config config.yaml dataset ./data
```

### Transfer Learning

```bash
/train-model i want to fine-tune model pretrained.pt on dataset ./new-data
```

### Multi-GPU Training

```bash
/train-model i want to train on dataset ./data with 4 GPUs
```

## Related Commands

- `/ccw` - Main workflow orchestrator
- `/spec-create` - Create feature specification
- `/workflow:plan` - Plan implementation
- `/workflow:execute` - Execute plan

## Implementation Notes

This command orchestrates multiple AI agents:
1. **Survey Agent**: Dataset analysis
2. **Design Agent**: Model selection and configuration
3. **Planning Agent**: Execution planning
4. **Execution Agent**: Training execution
5. **Evaluation Agent**: Performance evaluation

All agents work autonomously - user only provides natural language request.
