#!/usr/bin/env python3
"""Promote/transition model to different stage in Model Registry."""

import argparse
import json
import sys

import mlflow


def promote_model(name, version, stage, archive_existing=False):
    """Transition model version to a new stage."""
    client = mlflow.tracking.MlflowClient()

    # Get current model version
    try:
        model_version = client.get_model_version(name, version)
    except Exception as e:
        print(f"Error: Model {name} version {version} not found: {e}", file=sys.stderr)
        sys.exit(2)

    old_stage = model_version.current_stage

    # Archive existing models in target stage
    if archive_existing and stage != "Archived":
        existing_versions = client.get_latest_versions(name, stages=[stage])
        for existing in existing_versions:
            if existing.version != version:
                print(f"Archiving existing version {existing.version} in stage {stage}", file=sys.stderr)
                client.transition_model_version_stage(
                    name=name,
                    version=existing.version,
                    stage="Archived"
                )

    # Transition to new stage
    client.transition_model_version_stage(
        name=name,
        version=version,
        stage=stage
    )

    # Get updated model version
    model_version = client.get_model_version(name, version)

    result = {
        "name": name,
        "version": version,
        "old_stage": old_stage,
        "new_stage": stage,
        "uri": f"models:/{name}/{stage}",
        "status": model_version.status
    }

    print(f"Model promoted successfully!")
    print(f"Name: {result['name']}")
    print(f"Version: {result['version']}")
    print(f"Stage: {result['old_stage']} → {result['new_stage']}")
    print(f"Model URI: {result['uri']}")
    print(f"Status: {result['status']}")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Promote model to different stage in MLflow Model Registry",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Promote to Staging
  %(prog)s --name "yolo-ppe-detection" --version "1" --stage "Staging"

  # Promote to Production and archive old production model
  %(prog)s --name "yolo-ppe-detection" --version "2" --stage "Production" \\
           --archive-existing

  # Archive model
  %(prog)s --name "yolo-ppe-detection" --version "1" --stage "Archived"

Valid stages: None, Staging, Production, Archived
        """
    )

    parser.add_argument("--name", required=True, help="Model name")
    parser.add_argument("--version", required=True, help="Model version number")
    parser.add_argument("--stage", required=True,
                       choices=["None", "Staging", "Production", "Archived"],
                       help="Target stage")
    parser.add_argument("--archive-existing", action="store_true",
                       help="Archive existing models in target stage")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--quiet", action="store_true", help="Suppress success messages")

    args = parser.parse_args()

    result = promote_model(args.name, args.version, args.stage, args.archive_existing)

    if args.json:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
