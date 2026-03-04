#!/usr/bin/env python3
"""Log training results to MLflow - creates run, logs metrics, model, and artifacts."""

import argparse
import json
import os
import sys
from datetime import datetime

import mlflow


def parse_key_value_pairs(pairs_str):
    """Parse 'key:value,key2:value2' format into dict."""
    if not pairs_str:
        return {}
    result = {}
    for pair in pairs_str.split(','):
        if ':' in pair:
            key, value = pair.split(':', 1)
            # Try to convert to float for numbers
            try:
                value = float(value)
                if value.is_integer():
                    value = int(value)
            except ValueError:
                pass  # Keep as string
            result[key.strip()] = value
    return result


def get_or_create_experiment(experiment_name):
    """Get existing experiment or create new one."""
    client = mlflow.tracking.MlflowClient()
    try:
        experiment = client.get_experiment_by_name(experiment_name)
        if experiment:
            return experiment.experiment_id
        # Create new experiment
        experiment_id = client.create_experiment(experiment_name)
        return experiment_id
    except Exception as e:
        print(f"Error accessing experiment: {e}", file=sys.stderr)
        # Fall back to default experiment
        return None


def log_training(
    run_name=None,
    experiment_name=None,
    metrics=None,
    params=None,
    tags=None,
    model_artifact=None,
    artifacts=None,
    description=None
):
    """Create MLflow run and log training results."""
    client = mlflow.tracking.MlflowClient()

    # Get experiment ID
    experiment_id = None
    if experiment_name:
        experiment_id = get_or_create_experiment(experiment_name)

    # Start run
    run = client.create_run(
        experiment_id=experiment_id,
        tags=tags,
        run_name=run_name
    )

    run_id = run.info.run_id

    # Log metrics
    if metrics:
        client.log_batch(
            run_id=run_id,
            metrics=[mlflow.entities.Metric(key=k, value=v, timestamp=int(datetime.now().timestamp() * 1000), step=0)
                    for k, v in metrics.items()],
            params=[],
            tags=[]
        )

    # Log params
    if params:
        client.log_batch(
            run_id=run_id,
            metrics=[],
            params=[mlflow.entities.Param(key=k, value=str(v)) for k, v in params.items()],
            tags=[]
        )

    # Log model artifact
    if model_artifact and os.path.exists(model_artifact):
        client.log_artifact(run_id, model_artifact, artifact_path="model")

    # Log additional artifacts
    if artifacts:
        for artifact_path in artifacts:
            if os.path.exists(artifact_path):
                client.log_artifact(run_id, artifact_path)

    # Set description
    if description:
        client.set_tag(run_id, "mlflow.note.content", description)

    # Get run info for output
    run_info = client.get_run(run_id)

    result = {
        "run_id": run_id,
        "run_name": run_info.info.run_name,
        "experiment_id": run_info.info.experiment_id,
        "experiment_name": experiment_name or "Default",
        "artifact_uri": run_info.info.artifact_uri,
        "metrics_logged": list(metrics.keys()) if metrics else [],
        "params_logged": list(params.keys()) if params else [],
        "artifacts_logged": ([model_artifact] + artifacts) if model_artifact or artifacts else [],
        "status": "success"
    }

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Log training results to MLflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Log training with metrics and model
  %(prog)s --run-name "yolo-ppe-training" \\
           --metrics "mAP50:0.85,precision:0.92" \\
           --model-artifact "best.pt"

  # Full example with experiment, params, tags
  %(prog)s --experiment-name "PPE-Detection" \\
           --run-name "yolo-ppe-v1" \\
           --params "epochs:100,batch:16" \\
           --metrics "mAP50:0.85,mAP95:0.72" \\
           --model-artifact "runs/detect/train/weights/best.pt" \\
           --artifacts "confusion_matrix.png,results.csv" \\
           --tags "use_case:ppe,dataset:v1"
        """
    )

    parser.add_argument("--run-name", help="Run name (auto-generated if not provided)")
    parser.add_argument("--experiment-name", help="Experiment name (uses Default if not provided)")
    parser.add_argument("--metrics", help="Metrics as 'key:value,key2:value2'")
    parser.add_argument("--params", help="Hyperparameters as 'key:value,key2:value2'")
    parser.add_argument("--tags", help="Tags as 'key:value,key2:value2'")
    parser.add_argument("--model-artifact", help="Path to model .pt file")
    parser.add_argument("--artifacts", help="Comma-separated list of additional artifact paths")
    parser.add_argument("--description", help="Run description")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--uri-only", action="store_true", help="Output only run ID")

    args = parser.parse_args()

    # Parse inputs
    metrics = parse_key_value_pairs(args.metrics)
    params = parse_key_value_pairs(args.params)
    tags = parse_key_value_pairs(args.tags)

    # Parse artifacts list
    artifacts = []
    if args.artifacts:
        artifacts = [a.strip() for a in args.artifacts.split(',') if a.strip()]

    # Validate at least one thing to log
    if not any([metrics, params, args.model_artifact, artifacts]):
        print("Error: Please provide at least --metrics, --params, --model-artifact, or --artifacts",
              file=sys.stderr)
        sys.exit(3)

    # Log training
    result = log_training(
        run_name=args.run_name,
        experiment_name=args.experiment_name,
        metrics=metrics,
        params=params,
        tags=tags,
        model_artifact=args.model_artifact,
        artifacts=artifacts,
        description=args.description
    )

    # Output
    if args.uri_only:
        print(result["run_id"])
    elif args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Run created successfully!")
        print(f"Run ID: {result['run_id']}")
        print(f"Run Name: {result['run_name']}")
        print(f"Experiment: {result['experiment_name']}")
        print(f"Artifact URI: {result['artifact_uri']}")
        if result['metrics_logged']:
            print(f"Metrics: {', '.join(result['metrics_logged'])}")
        if result['params_logged']:
            print(f"Params: {', '.join(result['params_logged'])}")
        if result['artifacts_logged']:
            print(f"Artifacts: {', '.join(result['artifacts_logged'])}")
        print()
        print(f"Register this model with:")
        print(f"  python register_model.py --run-id {result['run_id']} --name <model-name>")


if __name__ == "__main__":
    main()
