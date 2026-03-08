"""Configuration for cloud efficiency API client."""

import os

API_BASE_URL = os.environ.get("CLOUD_API_BASE_URL", "http://127.0.0.1:8000")
API_VERSION = os.environ.get("CLOUD_API_VERSION", "v1")
API_TIMEOUT = int(os.environ.get("CLOUD_API_TIMEOUT", "30"))
