"""Mock API server for cloud efficiency data. Stdlib only — no external deps."""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def load_json(filename):
    with open(os.path.join(DATA_DIR, filename)) as f:
        return json.load(f)


class CloudAPIHandler(BaseHTTPRequestHandler):
    """Handles /api/v1/* routes for mock cloud efficiency data."""

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        params = parse_qs(parsed.query)

        routes = {
            "/api/v1/services": self.handle_list_services,
            "/api/v1/ec2": self.handle_ec2,
            "/api/v1/rds": self.handle_rds,
            "/api/v1/s3": self.handle_s3,
        }

        # Check for /api/v1/services/<name> pattern
        if path.startswith("/api/v1/services/") and path.count("/") == 4:
            service_name = path.split("/")[-1]
            self.handle_describe_service(service_name)
            return

        handler = routes.get(path)
        if handler:
            handler(params)
        else:
            self.send_json(404, {"error": True, "message": f"Not found: {path}"})

    def handle_list_services(self, params):
        services = load_json("services.json")
        self.send_json(200, {
            "services": [s["service_name"] for s in services],
            "count": len(services),
        })

    def handle_describe_service(self, name):
        services = load_json("services.json")
        match = next((s for s in services if s["service_name"] == name), None)
        if match:
            self.send_json(200, match)
        else:
            self.send_json(404, {"error": True, "message": f"Service '{name}' not found"})

    def handle_ec2(self, params):
        instances = load_json("ec2_instances.json")
        instances = self._filter(instances, params)
        total_savings = sum(i["potential_annual_savings"] for i in instances)
        self.send_json(200, {
            "instances": instances,
            "count": len(instances),
            "total_potential_annual_savings": total_savings,
        })

    def handle_rds(self, params):
        instances = load_json("rds_instances.json")
        instances = self._filter(instances, params)
        total_savings = sum(i["potential_annual_savings"] for i in instances)
        self.send_json(200, {
            "instances": instances,
            "count": len(instances),
            "total_potential_annual_savings": total_savings,
        })

    def handle_s3(self, params):
        buckets = load_json("s3_buckets.json")
        buckets = self._filter(buckets, params)
        total_savings = sum(b["potential_annual_savings"] for b in buckets)
        self.send_json(200, {
            "buckets": buckets,
            "count": len(buckets),
            "total_potential_annual_savings": total_savings,
        })

    def _filter(self, items, params):
        """Apply query parameter filters: service, cpu, memory."""
        service = params.get("service", [None])[0]
        if service:
            items = [i for i in items if i.get("service") == service]

        cpu_threshold = params.get("cpu", [None])[0]
        if cpu_threshold:
            items = [i for i in items if i.get("avg_cpu_pct", 0) <= float(cpu_threshold)]

        memory_threshold = params.get("memory", [None])[0]
        if memory_threshold:
            items = [i for i in items if i.get("avg_memory_pct", 0) <= float(memory_threshold)]

        return items

    def send_json(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def log_message(self, format, *args):
        """Quieter logging — single line per request."""
        print(f"[mock-api] {args[0]}" if args else "")


def main():
    port = int(os.environ.get("MOCK_SERVER_PORT", "8000"))
    server = HTTPServer(("127.0.0.1", port), CloudAPIHandler)
    print(f"Cloud Efficiency Mock API running on http://127.0.0.1:{port}")
    print(f"Endpoints:")
    print(f"  GET /api/v1/services")
    print(f"  GET /api/v1/services/<name>")
    print(f"  GET /api/v1/ec2?service=&cpu=&memory=")
    print(f"  GET /api/v1/rds?service=&cpu=&memory=")
    print(f"  GET /api/v1/s3?service=")
    print(f"\nPress Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
