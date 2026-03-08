"""HTTP client for the cloud efficiency API. Stdlib only — no external deps."""

import json
import sys
import urllib.request
import urllib.error
import urllib.parse
from config import API_BASE_URL, API_VERSION, API_TIMEOUT


def error_output(message):
    """Print a JSON error to stdout and exit with code 1."""
    print(json.dumps({"error": True, "message": message}))
    sys.exit(1)


def fetch(endpoint, params=None):
    """Fetch JSON from the cloud efficiency API.

    Args:
        endpoint: API path after /api/{version}/ (e.g. "services", "ec2")
        params: Optional dict of query parameters

    Returns:
        Parsed JSON response as a dict/list.
    """
    url = f"{API_BASE_URL}/api/{API_VERSION}/{endpoint}"

    if params:
        filtered = {k: v for k, v in params.items() if v is not None}
        if filtered:
            url += "?" + urllib.parse.urlencode(filtered)

    req = urllib.request.Request(url)
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=API_TIMEOUT) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            error_output(f"Resource not found: {endpoint}")
        else:
            error_output(f"API returned HTTP {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        error_output(f"Cannot reach API server at {API_BASE_URL} — is the mock server running? ({e.reason})")
    except TimeoutError:
        error_output(f"API request timed out after {API_TIMEOUT}s")
    except json.JSONDecodeError:
        error_output("API returned invalid JSON")
