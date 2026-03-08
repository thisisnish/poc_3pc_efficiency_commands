"""Describe a specific cloud service."""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from api_client import fetch, error_output


def main():
    if len(sys.argv) < 2:
        error_output("Usage: python3 describe_service.py <service_name>")

    service_name = sys.argv[1].strip().lower()
    data = fetch(f"services/{service_name}")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
