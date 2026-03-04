---
name: auto-train
description: End-to-end autonomous YOLO model training. Parses natural language, auto-annotates if needed (SAM3 via annotate skill), prepares data splits, trains model (via yolo-finetune skill). Minimal human intervention.
argument-hint: "\"Train <use-case> detection with dataset <path>\""
allowed-tools: TodoWrite(*), AskUserQuestion(*), Read(*), Write(*), Bash(*), Glob(*), Grep(*), Skill(*)
---

# Autonomous YOLO Model Training Command

**Your Goal**: Train a YOLO model end-to-end based on user's natural language request using skills.

---

## EXECUTION WORKFLOW

You will execute this workflow from start to finish in a single session:

```
1. Parse user request
2. Create TODO list
3. Execute each TODO step-by-step
4. Report final results
```

---

## STEP 1: Parse User Request

**Extract from user input:**

```python
# User request example:
# "Train PPE detection with dataset /path/to/data"
# "Train danger zone detection with accuracy priority"
# "Train vest detection model"

Extract:
- use_case: What they want to detect (PPE, danger zone, vest, helmet, etc.)
- dataset_path: Where data is located (explicit or auto-detect)
- priority: speed/accuracy/balanced (default: balanced)
- classes: What objects to detect (infer from use_case)
```

**Common Use Cases and Classes:**

```python
use_case_mapping = {
    'PPE detection': ['helmet', 'vest', 'glove', 'shoe'],
    'danger zone': ['heavy_machinery', 'person', 'barrier'],
    'vest detection': ['vest', 'no_vest'],
    'helmet detection': ['helmet', 'no_helmet'],
    'heavy machinery': ['excavator', 'crane', 'bulldozer', 'truck'],
    'person detection': ['person']
}
```

**If dataset path not specified:**
```bash
# Auto-search common locations
for path in ./data ./dataset ./images . ..; do
    if [ -d "$path" ]; then
        dataset_path=$path
        break
    fi
done
```

---

## STEP 2: Validate Dataset

**Check dataset structure:**

```bash
# Does dataset exist?
ls -la <dataset_path>

# Count images
image_count=$(find <dataset_path> -name "*.jpg" -o -name "*.png" | wc -l)
echo "Found $image_count images"

# Check if labels exist
if [ -d "<dataset_path>/labels" ]; then
    echo "Dataset already annotated"
    has_labels=true
else
    echo "Dataset needs annotation"
    has_labels=false
fi
```

---

## STEP 3: Create TODO List

**Use TodoWrite tool to create your task list:**

```python
# If dataset already has labels:
TodoWrite({
    todos: [
        { content: "Parse user request and validate dataset", status: "completed", activeForm: "Parsing request" },
        { content: "Survey dataset (count images, identify classes)", status: "in_progress", activeForm: "Surveying dataset" },
        { content: "Prepare train/val/test splits using yolo-finetune skill", status: "pending", activeForm: "Preparing data splits" },
        { content: "Train YOLO model using yolo-finetune skill", status: "pending", activeForm: "Training model" },
        { content: "Evaluate and package results", status: "pending", activeForm: "Packaging results" }
    ]
})

# If dataset needs annotation:
TodoWrite({
    todos: [
        { content: "Parse user request and validate dataset", status: "completed", activeForm: "Parsing request" },
        { content: "Detect classes needed for annotation", status: "in_progress", activeForm: "Detecting classes" },
        { content: "Run SAM3 annotation using annotate skill", status: "pending", activeForm: "Annotating with SAM3" },
        { content: "Validate annotation output", status: "pending", activeForm: "Validating annotations" },
        { content: "Survey dataset (count images, identify classes)", status: "pending", activeForm: "Surveying dataset" },
        { content: "Prepare train/val/test splits using yolo-finetune skill", status: "pending", activeForm: "Preparing data splits" },
        { content: "Train YOLO model using yolo-finetune skill", status: "pending", activeForm: "Training model" },
        { content: "Evaluate and package results", status: "pending", activeForm: "Packaging results" }
    ]
})
```

---

## STEP 4: Execute TODOs (Step-by-Step)

### TODO: Survey Dataset

**DO THIS:**

```bash
# Count images
image_count=$(find <dataset_path>/images -name "*.jpg" 2>/dev/null | wc -l)
echo "Image count: $image_count"

# Identify classes
if [ -f "<dataset_path>/classes.txt" ]; then
    classes=$(cat <dataset_path>/classes.txt | tr '\n' ', ')
    echo "Classes: $classes"
elif [ -f "<dataset_path>/data.yaml" ]; then
    # Parse from data.yaml
    grep -A 20 "names:" <dataset_path>/data.yaml
fi

# Check dataset format
if [ -f "<dataset_path>/data.yaml" ]; then
    format="YOLO"
else
    format="YOLO (no data.yaml)"
fi

echo "Dataset format: $format"
```

**THEN:** Mark as completed, move to next TODO

```python
TodoWrite({
    todos: [
        # ... previous completed ...
        { content: "Survey dataset (count images, identify classes)", status: "completed", activeForm: "Surveying dataset" },
        { content: "Prepare train/val/test splits using yolo-finetune skill", status: "in_progress", activeForm: "Preparing data splits" },
        # ... rest pending ...
    ]
})
```

---

### TODO: Prepare Data Splits (yolo-finetune skill)

**DO THIS:**

```bash
# Activate yolo environment (or appropriate env with ultralytics)
conda activate yolo  # or base, or whatever has ultralytics

# Run yolo-finetune prepare command
python ~/.claude/skills/yolo-finetune/skill/cli.py prepare \
    <dataset_path> \
    --output-dir ./prepared_dataset \
    --train-split 0.8 \
    --val-split 0.1 \
    --test-split 0.1
```

**Expected output:**
```
prepared_dataset/
├── train/
│   ├── images/
│   └── labels/
├── val/
│   ├── images/
│   └── labels/
├── test/
│   ├── images/
│   └── labels/
└── data.yaml
```

**IF SUCCESS:**

```python
# Update dataset_path to prepared version
dataset_path = "./prepared_dataset"

TodoWrite({
    todos: [
        # ... completed ...
        { content: "Prepare train/val/test splits using yolo-finetune skill", status: "completed", activeForm: "Preparing data splits" },
        { content: "Train YOLO model using yolo-finetune skill", status: "in_progress", activeForm: "Training model" },
        # ... pending ...
    ]
})
```

**IF FAILS:**
```bash
# Check error and retry with different parameters
# Or check if dataset needs preprocessing
```

---

### TODO: Train YOLO Model (yolo-finetune skill)

**DO THIS:**

```bash
# Determine model variant based on dataset size and priority
if [ "$image_count" -lt 500 ] || [ "$priority" == "speed" ]; then
    model_variant="yolo11n.pt"
    model_name="YOLOv11n (fastest)"
elif [ "$image_count" -gt 5000 ] || [ "$priority" == "accuracy" ]; then
    model_variant="yolo11s.pt"
    model_name="YOLOv11s (accurate)"
else
    model_variant="yolo11n.pt"
    model_name="YOLOv11n (balanced)"
fi

# Calculate epochs
epochs=$((image_count / 10))
if [ $epochs -lt 50 ]; then epochs=50; fi
if [ $epochs -gt 100 ]; then epochs=100; fi

echo "Training configuration:"
echo "  Model: $model_name"
echo "  Epochs: $epochs"
echo "  Dataset: $dataset_path"

# Run yolo-finetune train command
python ~/.claude/skills/yolo-finetune/skill/cli.py train \
    ./prepared_dataset/data.yaml \
    --output-dir ./yolo_model_output \
    --hyperparams ~/.claude/skills/yolo-finetune/runs/detect/tune/best_hyperparameters.yaml \
    --model $model_variant \
    --epochs $epochs \
    --batch-size 16 \
    --image-size 640 \
    --device 0
```

**WAIT for training to complete.**

**IF SUCCESS:**

```bash
# Check output
if [ -f "./yolo_model_output/train/weights/best.pt" ]; then
    echo "✅ Training successful"
    model_path="./yolo_model_output/train/weights/best.pt"
else
    echo "❌ Training failed"
    exit 1
fi
```

**THEN:** Mark as completed

```python
TodoWrite({
    todos: [
        # ... completed ...
        { content: "Train YOLO model using yolo-finetune skill", status: "completed", activeForm: "Training model" },
        { content: "Evaluate and package results", status: "in_progress", activeForm: "Packaging results" },
        # ... pending ...
    ]
})
```

---

### TODO: Evaluate and Package Results

**DO THIS:**

```bash
# Read training results
if [ -f "./yolo_model_output/train/results.csv" ]; then
    # Get last row (final epoch metrics)
    tail -n 1 ./yolo_model_output/train/results.csv
fi

# Create final package
final_package="./final_model_$(date +%Y%m%d_%H%M%S)"
mkdir -p $final_package

# Copy model and essential files
cp ./yolo_model_output/train/weights/best.pt $final_package/
cp ./yolo_model_output/train/results.csv $final_package/ 2>/dev/null || true
cp ./yolo_model_output/training_summary.yaml $final_package/ 2>/dev/null || true

# Copy visualization files
cp ./yolo_model_output/train/*.png $final_package/ 2>/dev/null || true

# Create README
cat > $final_package/README.md << EOF
# Trained YOLO Model

## Use Case: ${use_case}
## Dataset: ${dataset_path}
## Images: ${image_count}

## Training Configuration
- Model: ${model_name}
- Epochs: ${epochs}
- Batch size: 16
- Image size: 640
- Hyperparameters: Best from tuning runs

## Dataset Splits
- Train: 80%
- Validation: 10%
- Test: 10%

## Model Files
- best.pt: Best model weights (use this for inference)
- results.csv: Training metrics per epoch
- training_summary.yaml: Training configuration summary
- *.png: Training visualization plots

## Usage

\`\`\`python
from ultralytics import YOLO

# Load model
model = YOLO('${final_package}/best.pt')

# Run inference
results = model('image.jpg')

# View results
for r in results:
    r.show()
\`\`\`

## Training Command Used
\`\`\`bash
python ~/.claude/skills/yolo-finetune/skill/cli.py train \\
    ./prepared_dataset/data.yaml \\
    --output-dir ./yolo_model_output \\
    --hyperparameters ~/.claude/skills/yolo-finetune/runs/detect/tune/best_hyperparameters.yaml \\
    --model ${model_variant} \\
    --epochs ${epochs} \\
    --batch-size 16 \\
    --image-size 640
\`\`\`

Training date: $(date)
EOF

echo ""
echo "✅ Training complete!"
echo ""
echo "📦 Final package: $final_package"
echo ""
ls -lh $final_package/
```

**THEN:** Mark final TODO as completed

```python
TodoWrite({
    todos: [
        { content: "Parse user request and validate dataset", status: "completed", activeForm: "Parsing request" },
        { content: "Survey dataset (count images, identify classes)", status: "completed", activeForm: "Surveying dataset" },
        { content: "Prepare train/val/test splits using yolo-finetune skill", status: "completed", activeForm: "Preparing data splits" },
        { content: "Train YOLO model using yolo-finetune skill", status: "completed", activeForm: "Training model" },
        { content: "Evaluate and package results", status: "completed", activeForm: "Packaging results" }
    ]
})
```

---

## IF ANNOTATION IS NEEDED

### TODO: Run SAM3 Annotation

**ONLY IF: Dataset has no labels directory**

**DO THIS:**

```python
# Step 1: Determine classes from use_case
classes = use_case_mapping.get(use_case, ['person'])

# Step 2: Invoke annotate skill
Skill({
    skill: "annotate",
    args: f"folder {dataset_path}/images --classes {' '.join(classes)} --output ./annotate_ui/dataset --use-screen"
})
```

**WAIT for annotation to complete.**

**THEN:** Validate output

```bash
# Check annotation output
if [ -d "./annotate_ui/dataset/labels" ]; then
    echo "✅ Annotation successful"

    # Update dataset_path to annotated version
    dataset_path="./annotate_ui/dataset"

    # Mark TODOs as completed
    TodoWrite({
        todos: [
            # ... previous completed ...
            { content: "Run SAM3 annotation using annotate skill", status: "completed", activeForm: "Annotating with SAM3" },
            { content: "Validate annotation output", status: "completed", activeForm: "Validating annotations" },
            { content: "Survey dataset (count images, identify classes)", status: "in_progress", activeForm: "Surveying dataset" },
            # ... continue with rest of pipeline ...
        ]
    })
else
    echo "❌ Annotation failed"
    # Handle error
fi
```

---

## FINAL REPORT

After all TODOs are completed, output:

```
✅ MODEL TRAINING COMPLETE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Use Case: {use_case}
📁 Dataset: {original_dataset_path}
🖼️  Images: {image_count}
🏷️  Classes: {classes}

🔧 Training Configuration:
  Model: {model_name}
  Epochs: {epochs}
  Batch: 16
  Image Size: 640px
  Hyperparameters: Best from tuning runs

📁 Dataset Splits:
  Train: 80%
  Val: 10%
  Test: 10%

📈 Performance:
  (See results.csv in final package for detailed metrics)

📦 Output: {final_package}
   ├── best.pt (model weights)
   ├── results.csv (training metrics)
   ├── training_summary.yaml (config summary)
   ├── *.png (visualization plots)
   └── README.md (usage guide)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Quick Start:
```python
from ultralytics import YOLO
model = YOLO('{final_package}/best.pt')
results = model('your_image.jpg')
```
```

---

## ERROR HANDLING

### Dataset Not Found
```
1. Try auto-searching: ./data ./dataset ./images . ..
2. If not found, use AskUserQuestion:
   AskUserQuestion({
     questions: [{
       question: "Dataset not found. Please provide the path to your dataset:",
       header: "Dataset",
       options: [
         { label: "I'll provide path", description: "Enter full path to dataset" }
       ],
       multiSelect: false
     }]
   })
3. Update dataset_path and continue
```

### yolo-finetune Prepare Fails
```
1. Check dataset has images/ and labels/ directories
2. Verify YOLO format (classes.txt or data.yaml exists)
3. Check ultralytics is installed in environment
4. Try activating different environment (base, yolo, etc.)
```

### yolo-finetune Train Fails (GPU OOM)
```
1. Reduce batch_size: --batch-size 8
2. Retry training
3. If still fails, reduce image size: --image-size 480
4. Retry again
5. If still fails, use CPU: --device cpu
```

### Annotation Fails
```
1. Check error message from annotate skill
2. Try reducing number of classes
3. Try without --use-screen flag
4. Ask user to verify classes are appropriate
```

---

## IMPLEMENTATION NOTES

1. **Always use TodoWrite** to track progress
2. **Mark one TODO at a time** - complete it before moving to next
3. **Use Skill tool** for annotation (annotate skill)
4. **Use yolo-finetune skill** for prepare and train (NOT raw ultralytics)
5. **Report progress** after each major step
6. **Create clear output structure** with README and usage examples

---

## SKILLS USED

### annotate skill
- **Use when**: Dataset has no labels directory
- **Purpose**: SAM3 detection + YOLO format conversion
- **Invocation**: `Skill({ skill: "annotate", args: "folder <path> --classes <c1> <c2> --output <dir> --use-screen" })`
- **Output**: YOLO dataset with labels/

### yolo-finetune skill
- **Use when**: Dataset is ready for training
- **Purpose**: Prepare data splits and train YOLO model
- **Commands**:
  - `prepare`: Create train/val/test splits
  - `train`: Train YOLO with best hyperparameters
- **Invocation via Bash**:
  ```bash
  python ~/.claude/skills/yolo-finetune/skill/cli.py prepare <dataset> --output-dir ./prepared
  python ~/.claude/skills/yolo-finetune/skill/cli.py train ./prepared/data.yaml --output-dir ./model --epochs 100
  ```

---

## QUICK EXAMPLES

### Example 1: Pre-annotated Dataset
```bash
/auto-train "Train PPE detection with dataset /home/philiptran/linde-mexico-data/linde-mexico-task908"
```

**Expected flow:**
1. Parse request → use_case="PPE detection", dataset_path specified
2. Validate → labels exist, skip annotation
3. Survey → 526 images, 6 classes
4. Prepare → yolo-finetune prepare creates train/val/test splits
5. Train → yolo-finetune train with best hyperparameters
6. Package → ./final_model_*/
7. Report → metrics and usage

### Example 2: Needs Annotation
```bash
/auto-train "Train danger zone detection with dataset ./construction-site"
```

**Expected flow:**
1. Parse request → use_case="danger zone", classes=['heavy_machinery', 'person', 'barrier']
2. Validate → no labels, need annotation
3. Annotate → annotate skill (SAM3 + YOLO conversion)
4. Survey → check annotated dataset
5. Prepare → yolo-finetune prepare
6. Train → yolo-finetune train
7. Package → ./final_model_*/
8. Report → metrics and usage

### Example 3: With Priority
```bash
/auto-train "Train vest detection with accuracy priority dataset ./data/vest"
```

**Expected flow:**
1. Parse request → priority="accuracy"
2. Select larger model (yolo11s.pt)
3. More epochs (up to 150)
4. Train with yolo-finetune
