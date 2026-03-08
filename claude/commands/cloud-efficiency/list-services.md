List all available cloud services being monitored for efficiency.

Run this command from the project root:
```
python3 scripts/list_services.py
```

The output is JSON with this schema:
```json
{
  "services": ["service-a", "service-b"],
  "count": 2
}
```

Present the results as a clean numbered list of services with the total count. For each service name, briefly note that the user can run `/cloud-efficiency:describe-service <name>` to get details.
