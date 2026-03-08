"""Find over-provisioned S3 buckets with potential cost savings."""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from api_client import fetch, error_output


def main():
    parser = argparse.ArgumentParser(description="Find over-provisioned S3 buckets")
    parser.add_argument("--service", type=str, help="Filter by service name")

    args = parser.parse_args()

    params = {
        "service": args.service,
    }

    data = fetch("s3", params)
    print(json.dumps({
        "buckets": data.get("buckets", []),
        "count": data.get("count", 0),
        "total_potential_annual_savings": data.get("total_potential_annual_savings", 0),
    }, indent=2))


if __name__ == "__main__":
    main()
