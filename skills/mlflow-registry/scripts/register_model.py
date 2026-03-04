#!/usr/bin/env python3
"""Register MLflow model to Model Registry."""

import argparse
import json
import sys

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


def register_model(run_id, name, description=None, tags=None):
    """Register model from run to Model Registry."""
    client = mlflow.tracking.MlflowClient()

    # Verify run exists
    try:
        run = client.get_run(run_id)
    except Exception as e:
        print(f"Error: Run {run_id} not found: {e}", file=sys.stderr)
        sys.exit(2)

    # Construct model URI
    model_uri = f"runs:/{run_id}/model"

    # Register model
    model_version = mlflow.register_model(
        model_uri=model_uri,
        name=name
    )

    # Add description
    if description:
        client.update_model_version(
            name=name,
            version=model_version.version,
            description=description
        )

    # Add tags
    if tags:
        for key, value in tags.items():
            client.set_registered_model_tag(name, key, value)

    # Get model info
    model_info = client.get_model_version(name, model_version.version)

    result = {
        "name": name,
        "version": model_version.version,
        "run_id": run_id,
        "model_uri": f"models:/{name}/{model_version.version}",
        "source": model_info.source,
        "status": model_info.status,
        "tags": tags or {}
    }

    print(f"Model registered successfully!")
    print(f"Name: {result['name']}")
    print(f"Version: {result['version']}")
    print(f"Run ID: {result['run_id']}")
    print(f"Model URI: {result['model_uri']}")
    print(f"Status: {result['status']}")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Register MLflow model to Model Registry",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Register model from run
  %(prog)s --run-id "abc123" --name "yolo-ppe-detection"

  # Register with metadata
  %(prog)s --run-id "abc123" --name "yolo-ppe" \\
           --description "YOLOv8n for PPE detection" \\
           --tags "use_case:ppe,dataset:ppe-v1"
        """
    )

    parser.add_argument("--run-id", required=True, help="MLflow run ID")
    parser.add_argument("--name", required=True, help="Model name")
    parser.add_argument("--description", help="Model description")
    parser.add_argument("--tags", help="Tags as 'key:value,key2:value2'")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--uri-only", action="store_true", help="Output only model URI")

    args = parser.parse_args()

    tags = parse_tags(args.tags)

    result = register_model(args.run_id, args.name, args.description, tags)

    if args.uri_only:
        print(result["model_uri"])
    elif args.json:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
