#!/usr/bin/env python3
"""List all datasets in MLflow."""

import argparse
import json
import sys
from tabulate import tabulate

import mlflow


def list_datasets():
    """List all datasets from MLflow."""
    client = mlflow.tracking.MlflowClient()

    # Search for dataset runs
    filter_string = "tag.mlflow.dataset.name != ''"
    runs = client.search_runs(
        experiment_ids=["0"],
        filter_string=filter_string,
        order_by=["attribute.start_time DESC"]
    )

    datasets = []
    seen_names = set()

    for run in runs:
        name = run.data.tags.get("mlflow.dataset.name", "unknown")

        # Skip duplicates
        if name in seen_names:
            continue
        seen_names.add(name)

        dataset_path = run.data.params.get("dataset_path", "unknown")
        logged_at = run.data.params.get("logged_at", "unknown")

        # Get tags
        tags = {k: v for k, v in run.data.tags.items() if k.startswith("dataset_")}
        tags = {k.replace("dataset_", ""): v for k, v in tags.items()}

        datasets.append({
            "name": name,
            "version": tags.get("version", "N/A"),
            "path": dataset_path,
            "logged_at": logged_at
        })

    return datasets


def main():
    parser = argparse.ArgumentParser(
        description="List all datasets in MLflow",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--quiet", action="store_true", help="Suppress table headers")

    args = parser.parse_args()

    datasets = list_datasets()

    if args.json:
        print(json.dumps(datasets, indent=2))
    else:
        if not datasets:
            print("No datasets found.")
            return

        headers = ["Name", "Version", "Path", "Logged At"]
        table = [
            [d["name"], d["version"], d["path"], d["logged_at"]]
            for d in datasets
        ]

        print(tabulate(table, headers=headers, tablefmt="grid" if not args.quiet else "plain"))


if __name__ == "__main__":
    main()
