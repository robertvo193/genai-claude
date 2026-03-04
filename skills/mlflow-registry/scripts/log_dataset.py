#!/usr/bin/env python3
"""Log dataset to MLflow with versioning and metadata."""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

import mlflow


def parse_tags(tags_str):
    """Parse tag string 'key:value,key2:value2' into dict."""
    if not tags_str:
        return {}
    tags = {}
    for tag in tags_str.split(','):
        if ':' in tag:
            key, value = tag.split(':', 1)
            tags[key.strip()] = value.strip()
    return tags


def log_dataset(name, path, description=None, tags=None):
    """Log dataset to MLflow and return dataset info."""
    tracking_uri = mlflow.get_tracking_uri()
    print(f"Connecting to MLflow at: {tracking_uri}", file=sys.stderr)

    # Validate path exists
    if not path.startswith(('s3://', 'gs://', 'dbfs://', 'http://', 'https://')):
        local_path = Path(path)
        if not local_path.exists():
            print(f"Error: Dataset path does not exist: {path}", file=sys.stderr)
            sys.exit(2)

    # Use mlflow.log_artifacts for dataset (simpler approach compatible with newer MLflow)
    with mlflow.start_run(run_name=f"dataset-{name}", nested=True):
        # Log dataset as artifact
        mlflow.log_artifacts(path, artifact_path="dataset")

        # Log metadata as params
        mlflow.log_param("dataset_name", name)
        mlflow.log_param("dataset_path", str(Path(path).absolute()))
        mlflow.log_param("logged_at", datetime.now().isoformat())

        # Count images
        train_imgs = len(list(Path(path).glob("images/train/*.jpg")))
        val_imgs = len(list(Path(path).glob("images/val/*.jpg")))
        mlflow.log_param("train_images", train_imgs)
        mlflow.log_param("val_images", val_imgs)

        # Log dataset summary
        summary = f"Dataset: {name}\n"
        summary += f"Path: {path}\n"
        summary += f"Train images: {train_imgs}\n"
        summary += f"Val images: {val_imgs}\n"
        if description:
            summary += f"Description: {description}\n"
        mlflow.log_text(summary, "dataset_summary.txt")

        if tags:
            for key, value in tags.items():
                mlflow.set_tag(f"dataset_{key}", value)

        run_id = mlflow.active_run().info.run_id

    # Construct dataset URI
    dataset_uri = f"runs:/{run_id}/dataset"

    print(f"Dataset logged successfully!")
    print(f"Name: {name}")
    print(f"Path: {path}")
    print(f"Run ID: {run_id}")
    print(f"Dataset URI: {dataset_uri}")

    return {
        "name": name,
        "path": path,
        "run_id": run_id,
        "dataset_uri": dataset_uri,
        "tags": tags or {}
    }


def main():
    parser = argparse.ArgumentParser(
        description="Log dataset to MLflow for versioning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Log local dataset
  %(prog)s --name "ppe-v1" --path "/data/ppe/train"

  # Log with tags
  %(prog)s --name "ppe-v1" --path "/data/ppe/train" \\
           --tags "use_case:ppe,version:1.0,split:train"

  # Log S3 dataset
  %(prog)s --name "imagenet-val" --path "s3://bucket/data/val" \\
           --description "ImageNet validation set"
        """
    )

    parser.add_argument("--name", required=True, help="Dataset name")
    parser.add_argument("--path", required=True, help="Dataset path (local or S3/GS)")
    parser.add_argument("--description", help="Dataset description")
    parser.add_argument("--tags", help="Tags as 'key:value,key2:value2'")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--uri-only", action="store_true", help="Output only dataset URI")

    args = parser.parse_args()

    tags = parse_tags(args.tags)

    result = log_dataset(args.name, args.path, args.description, tags)

    if args.uri_only:
        print(result["dataset_uri"])
    elif args.json:
        print(json.dumps(result, indent=2))
    else:
        # Human-readable already printed
        pass


if __name__ == "__main__":
    main()
