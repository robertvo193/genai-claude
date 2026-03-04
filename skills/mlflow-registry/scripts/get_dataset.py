#!/usr/bin/env python3
"""Get dataset URI and metadata from MLflow."""

import argparse
import json
import sys

import mlflow
from mlflow.store.artifact.utils import get_artifact_uri


def get_dataset_info(name, version=None):
    """Get dataset info by name and optional version."""
    client = mlflow.tracking.MlflowClient()

    # Search for dataset runs
    filter_string = f"tag.mlflow.dataset.name = '{name}'"
    runs = client.search_runs(
        experiment_ids=["0"],  # Default experiment
        filter_string=filter_string,
        order_by=["attribute.start_time DESC"]
    )

    if not runs:
        print(f"Error: Dataset '{name}' not found", file=sys.stderr)
        sys.exit(2)

    # Filter by version if specified
    if version:
        version_tag = f"dataset_version:{version}"
        runs = [r for r in runs if version_tag in r.data.tags]

    if not runs:
        print(f"Error: Dataset '{name}' version '{version}' not found", file=sys.stderr)
        sys.exit(2)

    # Get the latest (or specified) run
    run = runs[0]

    # Extract dataset info
    dataset_uri = f"runs:/{run.info.run_id}/dataset"
    dataset_path = run.data.params.get("dataset_path", "unknown")
    logged_at = run.data.params.get("logged_at", "unknown")

    # Get all tags
    tags = {k: v for k, v in run.data.tags.items() if k.startswith("dataset_")}
    tags = {k.replace("dataset_", ""): v for k, v in tags.items()}

    return {
        "name": name,
        "version": tags.get("version", "latest"),
        "path": dataset_path,
        "dataset_uri": dataset_uri,
        "run_id": run.info.run_id,
        "logged_at": logged_at,
        "tags": tags
    }


def main():
    parser = argparse.ArgumentParser(
        description="Get dataset URI from MLflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get latest version
  %(prog)s --name "ppe-v1"

  # Get specific version
  %(prog)s --name "ppe-v1" --version "1.0"

  # Get URI only (for shell scripts)
  %(prog)s --name "ppe-v1" --uri-only
        """
    )

    parser.add_argument("--name", required=True, help="Dataset name")
    parser.add_argument("--version", help="Dataset version")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--uri-only", action="store_true", help="Output only URI")
    parser.add_argument("--quiet", action="store_true", help="Suppress headers")

    args = parser.parse_args()

    info = get_dataset_info(args.name, args.version)

    if args.uri_only:
        print(info["dataset_uri"])
    elif args.json:
        print(json.dumps(info, indent=2))
    else:
        print(f"Dataset: {info['name']}")
        print(f"Version: {info['version']}")
        print(f"Path: {info['path']}")
        print(f"URI: {info['dataset_uri']}")
        print(f"Logged: {info['logged_at']}")
        if info['tags']:
            print("Tags:")
            for k, v in info['tags'].items():
                print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
