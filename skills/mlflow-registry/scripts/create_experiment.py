#!/usr/bin/env python3
"""Create a new MLflow experiment."""

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


def create_experiment(name, description=None, tags=None, artifact_location=None):
    """Create a new MLflow experiment."""
    client = mlflow.tracking.MlflowClient()

    # Check if experiment already exists
    existing = client.get_experiment_by_name(name)
    if existing:
        result = {
            "name": name,
            "experiment_id": existing.experiment_id,
            "artifact_location": existing.artifact_location,
            "status": "already_exists"
        }
        return result

    # Create new experiment
    experiment_id = client.create_experiment(
        name=name,
        artifact_location=artifact_location,
        tags=tags
    )

    # Set description (API changed in newer MLflow versions)
    if description:
        try:
            client.update_experiment(experiment_id, description)
        except AttributeError:
            # MLflow 2.x+ uses different API
            client.set_experiment_description(experiment_id, description)

    # Get experiment info
    experiment = client.get_experiment(experiment_id)

    result = {
        "name": name,
        "experiment_id": experiment_id,
        "artifact_location": experiment.artifact_location,
        "status": "created"
    }

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Create MLflow experiment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create experiment
  %(prog)s --name "PPE-Detection"

  # Create with description
  %(prog)s --name "PPE-Detection" --description "PPE object detection experiments"

  # Create with tags
  %(prog)s --name "PPE-Detection" --tags "team:vision,project:ppe"
        """
    )

    parser.add_argument("--name", required=True, help="Experiment name")
    parser.add_argument("--description", help="Experiment description")
    parser.add_argument("--tags", help="Tags as 'key:value,key2:value2'")
    parser.add_argument("--artifact-location", help="Custom artifact location")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--id-only", action="store_true", help="Output only experiment ID")

    args = parser.parse_args()

    tags = parse_tags(args.tags)

    result = create_experiment(
        name=args.name,
        description=args.description,
        tags=tags,
        artifact_location=args.artifact_location
    )

    if args.id_only:
        print(result["experiment_id"])
    elif args.json:
        print(json.dumps(result, indent=2))
    else:
        status_msg = "already exists" if result["status"] == "already_exists" else "created successfully"
        print(f"Experiment {status_msg}!")
        print(f"Name: {result['name']}")
        print(f"Experiment ID: {result['experiment_id']}")
        print(f"Artifact Location: {result['artifact_location']}")


if __name__ == "__main__":
    main()
