"""Find underutilized EC2 instances with potential cost savings."""

import argparse
import json
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from api_client import fetch, error_output


def valid_date(s):
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return s
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: '{s}'. Use YYYY-MM-DD.")


def main():
    parser = argparse.ArgumentParser(description="Find underutilized EC2 instances")
    parser.add_argument("--service", type=str, help="Filter by service name")
    parser.add_argument("--cpu", type=float, default=20.0, help="CPU threshold %% (default: 20)")
    parser.add_argument("--memory", type=float, default=40.0, help="Memory threshold %% (default: 40)")
    parser.add_argument("--start-date", type=valid_date, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=valid_date, help="End date (YYYY-MM-DD)")

    args = parser.parse_args()

    params = {
        "service": args.service,
        "cpu": args.cpu,
        "memory": args.memory,
    }

    data = fetch("ec2", params)
    print(json.dumps({
        "instances": data.get("instances", []),
        "count": data.get("count", 0),
        "total_potential_annual_savings": data.get("total_potential_annual_savings", 0),
    }, indent=2))


if __name__ == "__main__":
    main()
