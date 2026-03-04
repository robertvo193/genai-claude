"""
Ray Worker Template for MLflow Integration

This template shows how Ray workers should log to MLflow during training.
The mlflow-registry skill then handles dataset versioning and model registration.

Usage:
    1. Set MLFLOW_TRACKING_URI environment variable
    2. Ray worker logs metrics/params directly to MLflow
    3. After training, use mlflow-registry skill to register the model
"""

import mlflow
import os


def train_yolo_model(config, dataset_path):
    """
    YOLO training function that runs on Ray worker.

    Args:
        config: Training configuration (model, epochs, hyperparameters)
        dataset_path: Path to training dataset

    Returns:
        run_id: MLflow run ID for model registration
    """

    # MLflow auto-connects from MLFLOW_TRACKING_URI env var
    # Set this before submitting Ray job:
    # export MLFLOW_TRACKING_URI=http://localhost:5001

    with mlflow.start_run(run_name=f"{config['model']}-training") as run:
        # ============================================================
        # Step 1: Log training configuration
        # ============================================================
        mlflow.log_params({
            "model": config.get("model", "yolov8n"),
            "epochs": config.get("epochs", 100),
            "batch_size": config.get("batch_size", 16),
            "imgsz": config.get("imgsz", 640),
            "device": config.get("device", "0"),
            "workers": config.get("workers", 8),
            "dataset_path": dataset_path
        })

        # Log tags for filtering
        mlflow.set_tags({
            "use_case": config.get("use_case", "ppe-detection"),
            "dataset_name": config.get("dataset_name", "unknown"),
            "training_framework": "ultralytics"
        })

        # ============================================================
        # Step 2: Training loop
        # ============================================================
        print(f"Starting training: {config['model']} for {config['epochs']} epochs")

        # Your actual YOLO training code here
        # from ultralytics import YOLO
        # model = YOLO(config['model'])
        # results = model.train(
        #     data=dataset_path,
        #     epochs=config['epochs'],
        #     **config
        # )

        # Simulated training loop
        for epoch in range(config["epochs"]):
            # Simulate training
            metrics = {
                "train/loss": 1.0 - (epoch * 0.01),
                "val/mAP50": 0.5 + (epoch * 0.003),
                "val/mAP50-95": 0.3 + (epoch * 0.002)
            }

            # Log metrics for this epoch
            mlflow.log_metrics(metrics, step=epoch)

            if epoch % 10 == 0:
                print(f"Epoch {epoch}: mAP50 = {metrics['val/mAP50']:.3f}")

        # ============================================================
        # Step 3: Log model artifacts
        # ============================================================
        # Log the trained model weights
        # mlflow.log_artifact("runs/detect/train/weights/best.pt")
        # mlflow.log_artifact("runs/detect/train/weights/last.pt")

        # Log training results/plots
        # mlflow.log_artifact("runs/detect/train/results.csv")
        # mlflow.log_artifact("runs/detect/train/confusion_matrix.png")

        # ============================================================
        # Step 4: Return run_id for model registration
        # ============================================================
        run_id = run.info.run_id
        print(f"\nTraining completed!")
        print(f"Run ID: {run_id}")
        print(f"MLflow UI: {mlflow.get_tracking_uri()}/#/runs/{run_id}")

        return run_id


# ============================================================
# Ray Job Submission Example
# ============================================================

if __name__ == "__main__":
    # Example configuration
    config = {
        "model": "yolov8n.pt",
        "epochs": 100,
        "batch_size": 16,
        "imgsz": 640,
        "device": "0",
        "workers": 8,
        "use_case": "ppe-detection",
        "dataset_name": "ppe-detection-v1"
    }

    dataset_path = "/data/ppe/train.yaml"

    # Run training (on Ray worker or locally for testing)
    run_id = train_yolo_model(config, dataset_path)

    print(f"\n{'='*60}")
    print(f"Next steps:")
    print(f"{'='*60}")
    print(f"1. Register the model:")
    print(f"   python register_model.py --run-id {run_id} --name yolo-ppe-detection")
    print(f"\n2. Promote to production:")
    print(f"   python promote_model.py --name yolo-ppe-detection --version 1 --stage Production")
    print(f"{'='*60}")
