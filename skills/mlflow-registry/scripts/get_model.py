#!/usr/bin/env python3
"""Get model URI from Model Registry by stage or version."""

import argparse
import json
import sys

import mlflow


def get_model_uri(name, stage=None, version=None):
    """Get model URI from Model Registry."""
    client = mlflow.tracking.MlflowClient()

    if version:
        # Get by version
        model_version = client.get_model_version(name, version)
        model_uri = f"models:/{name}/{version}"
        return {
            "name": name,
            "version": version,
            "stage": model_version.current_stage,
            "uri": model_uri,
            "source": model_version.source,
            "status": model_version.status
        }
    elif stage:
        # Get by stage
        model_uri = f"models:/{name}/{stage}"
        # Get latest version in stage
        versions = client.get_latest_versions(name, stages=[stage])
        if not versions:
            print(f"Error: No model found in stage '{stage}'", file=sys.stderr)
            sys.exit(2)
        return {
            "name": name,
            "stage": stage,
            "version": versions[0].version,
            "uri": model_uri,
            "source": versions[0].source,
            "status": versions[0].status
        }
    else:
        # Default to Production stage
        return get_model_uri(name, stage="Production")


def main():
    parser = argparse.ArgumentParser(
        description="Get model URI from MLflow Model Registry",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get production model
  %(prog)s --name "yolo-ppe-detection" --stage "Production"

  # Get specific version
  %(prog)s --name "yolo-ppe-detection" --version "5"

  # Get URI only (for shell scripts)
  %(prog)s --name "yolo-ppe-detection" --stage "Production" --uri-only
        """
    )

    parser.add_argument("--name", required=True, help="Model name")
    parser.add_argument("--stage", help="Model stage (Production, Staging, Archived)")
    parser.add_argument("--version", help="Model version number")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--uri-only", action="store_true", help="Output only URI")
    parser.add_argument("--quiet", action="store_true", help="Suppress headers")

    args = parser.parse_args()

    if args.stage and args.version:
        print("Error: Use --stage OR --version, not both", file=sys.stderr)
        sys.exit(1)

    info = get_model_uri(args.name, args.stage, args.version)

    if args.uri_only:
        print(info["uri"])
    elif args.json:
        print(json.dumps(info, indent=2))
    else:
        print(f"Model: {info['name']}")
        print(f"Version: {info.get('version', 'N/A')}")
        print(f"Stage: {info.get('stage', 'N/A')}")
        print(f"URI: {info['uri']}")
        print(f"Source: {info['source']}")
        print(f"Status: {info['status']}")


if __name__ == "__main__":
    main()
