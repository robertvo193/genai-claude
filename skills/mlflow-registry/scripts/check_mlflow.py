#!/usr/bin/env python3
"""Check MLflow connection and health."""

import sys
import mlflow
from mlflow.tracking import MlflowClient


def check_mlflow():
    """Check MLflow connection and print status."""
    tracking_uri = mlflow.get_tracking_uri()
    print(f"MLflow Tracking URI: {tracking_uri}")

    try:
        client = MlflowClient()

        # Test connection
        experiments = client.search_experiments(max_results=1)
        print("✓ Connection successful")

        # Check registry
        try:
            models = client.search_registered_models(max_results=1)
            print("✓ Model Registry available")
        except Exception as e:
            print(f"✗ Model Registry error: {e}")

        # List experiments
        experiments = client.search_experiments()
        print(f"✓ Found {len(experiments)} experiment(s)")

        # List models
        try:
            models = client.search_registered_models()
            print(f"✓ Found {len(models)} registered model(s)")
        except:
            pass

        return 0

    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(check_mlflow())
