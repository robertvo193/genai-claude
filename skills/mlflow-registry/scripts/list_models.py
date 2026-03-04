#!/usr/bin/env python3
"""List models and versions in MLflow Model Registry."""

import argparse
import json
import sys
from tabulate import tabulate

import mlflow


def list_models(name=None):
    """List all models or specific model with versions."""
    client = mlflow.tracking.MlflowClient()

    if name:
        # List versions of specific model
        try:
            model = client.get_registered_model(name)
            versions = client.get_latest_versions(name)

            versions_info = []
            for v in versions:
                versions_info.append({
                    "name": name,
                    "version": v.version,
                    "stage": v.current_stage,
                    "status": v.status,
                    "run_id": v.run_id,
                    "created": v.creation_timestamp
                })

            return {"name": name, "versions": versions_info}

        except Exception as e:
            print(f"Error: Model '{name}' not found: {e}", file=sys.stderr)
            sys.exit(2)
    else:
        # List all registered models
        models = client.search_registered_models()

        result = []
        for model in models:
            versions = client.get_latest_models(model.name)
            result.append({
                "name": model.name,
                "description": model.description or "",
                "latest_versions": [v.version for v in model.latest_versions],
                "tags": model.tags
            })

        return result


def main():
    parser = argparse.ArgumentParser(
        description="List models in MLflow Model Registry",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all models
  %(prog)s

  # List all versions of a model
  %(prog)s --name "yolo-ppe-detection"
        """
    )

    parser.add_argument("--name", help="Model name (list versions)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--quiet", action="store_true", help="Suppress table headers")

    args = parser.parse_args()

    result = list_models(args.name)

    if args.json:
        print(json.dumps(result, indent=2))
    elif args.name:
        # Show versions of specific model
        if not result["versions"]:
            print(f"No versions found for model '{args.name}'")
            return

        headers = ["Version", "Stage", "Status", "Run ID"]
        table = [
            [v["version"], v["stage"], v["status"], v["run_id"][:8]]
            for v in result["versions"]
        ]
        print(tabulate(table, headers=headers, tablefmt="grid" if not args.quiet else "plain"))
    else:
        # Show all models
        if not result:
            print("No models found.")
            return

        headers = ["Name", "Latest Versions", "Description"]
        table = [
            [m["name"], ", ".join(m["latest_versions"]), m["description"][:50]]
            for m in result
        ]
        print(tabulate(table, headers=headers, tablefmt="grid" if not args.quiet else "plain"))


if __name__ == "__main__":
    main()
