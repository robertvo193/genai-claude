#!/usr/bin/env python3
"""List all MLflow experiments."""

import argparse
import json
import sys
from datetime import datetime

import mlflow
from tabulate import tabulate


def list_experiments(view_type="active_only"):
    """List all experiments."""
    client = mlflow.tracking.MlflowClient()

    experiments = client.search_experiments(
        view_type=view_type
    )

    results = []
    for exp in experiments:
        # Get run count
        runs = client.search_runs(
            experiment_ids=[exp.experiment_id],
            max_results=1
        )
        run_count = len(client.search_runs(
            experiment_ids=[exp.experiment_id],
            max_results=10000
        ))

        results.append({
            "id": exp.experiment_id,
            "name": exp.name,
            "location": exp.artifact_location,
            "stage": exp.lifecycle_stage,
            "runs": run_count,
            "tags": dict(exp.tags) if exp.tags else {}
        })

    return results


def main():
    parser = argparse.ArgumentParser(
        description="List MLflow experiments",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--all", action="store_true", help="Include deleted experiments")
    parser.add_argument("--json", action="store_true", help="Output JSON")

    args = parser.parse_args()

    view_type = "ALL" if args.all else "ACTIVE_ONLY"

    experiments = list_experiments(view_type=view_type)

    if args.json:
        print(json.dumps(experiments, indent=2))
    else:
        if not experiments:
            print("No experiments found.")
            return

        headers = ["ID", "Name", "Runs", "Stage", "Tags"]
        rows = []
        for exp in experiments:
            tags_str = ", ".join([f"{k}:{v}" for k, v in exp['tags'].items()]) if exp['tags'] else ""
            rows.append([
                exp['id'][:8],
                exp['name'],
                exp['runs'],
                exp['stage'],
                tags_str
            ])

        print(tabulate(rows, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    main()
