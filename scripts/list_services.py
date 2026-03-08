"""List all available cloud services."""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from api_client import fetch, error_output


def main():
    data = fetch("services")
    print(json.dumps({
        "services": data.get("services", []),
        "count": data.get("count", 0),
    }, indent=2))


if __name__ == "__main__":
    main()
