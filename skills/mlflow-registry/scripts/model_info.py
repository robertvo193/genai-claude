#!/usr/bin/env python3
"""Get detailed model information including training metadata."""

import argparse
import json
import sys
from datetime import datetime

import mlflow


def get_model_info(name, version):
    """Get detailed model information."""
    client = mlflow.tracking.MlflowClient()

    # Get model version
    try:
        model_version = client.get_model_version(name, version)
    except Exception as e:
        print(f"Error: Model {name} version {version} not found: {e}", file=sys.stderr)
        sys.exit(2)

    # Get run details
    try:
        run = client.get_run(model_version.run_id)
    except Exception as e:
        print(f"Error: Run {model_version.run_id} not found: {e}", file=sys.stderr)
        sys.exit(2)

    # Extract info
    info = {
        "model": {
            "name": name,
            "version": version,
            "stage": model_version.current_stage,
            "status": model_version.status,
            "source": model_version.source,
            "run_id": model_version.run_id,
            "description": model_version.description or ""
        },
        "training": {
            "params": dict(run.data.params),
            "metrics": dict(run.data.metrics),
            "tags": dict(run.data.tags)
        },
        "timestamp": {
            "created": datetime.fromtimestamp(model_version.creation_timestamp).isoformat(),
            "last_updated": datetime.fromtimestamp(model_version.last_updated_timestamp).isoformat()
        }
    }

    # Format for display
    print(f"Model: {info['model']['name']}")
    print(f"Version: {info['model']['version']}")
    print(f"Stage: {info['model']['stage']}")
    print(f"Status: {info['model']['status']}")
    print(f"Run ID: {info['model']['run_id']}")
    print(f"Created: {info['timestamp']['created']}")
    print()

    if info['model']['description']:
        print(f"Description: {info['model']['description']}")
        print()

    print("Training Parameters:")
    for k, v in info['training']['params'].items():
        print(f"  {k}: {v}")
    print()

    print("Validation Metrics:")
    for k, v in info['training']['metrics'].items():
        print(f"  {k}: {v}")
    print()

    # Extract dataset info from tags
    dataset_tags = {k: v for k, v in info['training']['tags'].items() if 'dataset' in k.lower()}
    if dataset_tags:
        print("Dataset:")
        for k, v in dataset_tags.items():
            print(f"  {k}: {v}")

    return info


def main():
    parser = argparse.ArgumentParser(
        description="Get detailed model information from MLflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get model info
  %(prog)s --name "yolo-ppe-detection" --version "1"

  # Get model info as JSON
  %(prog)s --name "yolo-ppe-detection" --version "1" --json
        """
    )

    parser.add_argument("--name", required=True, help="Model name")
    parser.add_argument("--version", required=True, help="Model version number")
    parser.add_argument("--json", action="store_true", help="Output JSON")

    args = parser.parse_args()

    info = get_model_info(args.name, args.version)

    if args.json:
        print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
