# Cloud Efficiency Commands

**Claude Code slash commands for AWS cloud cost optimization** — find over-provisioned EC2, RDS, and S3 resources with right-sizing recommendations and projected annual savings.

```
  /cloud-efficiency:get-underutilized-ec2  →  $386,985/yr in EC2 savings found
  /cloud-efficiency:get-underutilized-rds  →  $201,864/yr in RDS savings found
  /cloud-efficiency:get-underutilized-s3   →  $215,112/yr in S3 savings found
  ─────────────────────────────────────────────────────────────────
  Total identified savings                    $803,961/yr
```

## What is this?

A set of [Claude Code slash commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands) that connect to a cloud efficiency API and return actionable cost optimization insights — right inside your terminal.

**No dashboards. No context-switching. Just ask Claude.**

```
You:    /cloud-efficiency:get-underutilized-ec2 show me all ec2 waste for payment-platform
Claude: Found 2 underutilized EC2 instances for payment-platform...
        ┌──────────────────┬────────────┬──────────┬──────────┬─────────────┐
        │ Instance         │ Type       │ Avg CPU  │ Cost/mo  │ Savings/yr  │
        ├──────────────────┼────────────┼──────────┼──────────┼─────────────┤
        │ pay-api-prod-01  │ c5.4xlarge │ 4.2%     │ $4,896   │ $51,408     │
        │ pay-api-prod-02  │ c5.4xlarge │ 3.8%     │ $4,896   │ $51,408     │
        └──────────────────┴────────────┴──────────┴──────────┴─────────────┘
        Recommendation: Downsize both to c5.large — you're using <5% of 16 vCPUs.
```

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/3pc_efficiency_commands.git
cd 3pc_efficiency_commands
```

### 2. Start the mock API server

```bash
python3 mock_server/server.py
```

### 3. Open Claude Code in the project directory

```bash
claude
```

### 4. Run slash commands

| Command | What it does |
|---------|-------------|
| `/cloud-efficiency:list-services` | List all monitored cloud services |
| `/cloud-efficiency:describe-service payment-platform` | Get service metadata and spend |
| `/cloud-efficiency:get-underutilized-ec2` | Find underutilized EC2 instances |
| `/cloud-efficiency:get-underutilized-rds` | Find underutilized RDS instances |
| `/cloud-efficiency:get-underutilized-s3` | Find over-provisioned S3 buckets |

## Commands in Detail

### `/cloud-efficiency:list-services`

Lists all cloud services being monitored. No arguments needed.

### `/cloud-efficiency:describe-service`

Get detailed metadata for a service — owner, team, region, monthly spend, resource count.

```
/cloud-efficiency:describe-service user-analytics
```

### `/cloud-efficiency:get-underutilized-ec2`

Find EC2 instances running below CPU/memory thresholds with right-sizing recommendations.

```
# Natural language — Claude parses the filters
/cloud-efficiency:get-underutilized-ec2 show me ec2 waste for user-analytics with cpu below 15%

# All instances below default thresholds (20% CPU, 40% memory)
/cloud-efficiency:get-underutilized-ec2 show me all underutilized instances
```

### `/cloud-efficiency:get-underutilized-rds`

Find RDS instances with over-provisioned compute, storage, IOPS, and connections.

```
/cloud-efficiency:get-underutilized-rds find rds waste across all services
```

### `/cloud-efficiency:get-underutilized-s3`

Find S3 buckets on wrong storage classes, missing lifecycle policies, and version bloat.

```
/cloud-efficiency:get-underutilized-s3 show me s3 optimization opportunities for content-delivery
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Claude Code                                                │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Slash Commands (.claude/commands/cloud-efficiency/)   │  │
│  │  • list-services.md      • get-underutilized-ec2.md   │  │
│  │  • describe-service.md   • get-underutilized-rds.md   │  │
│  │                          • get-underutilized-s3.md    │  │
│  └──────────────────────┬────────────────────────────────┘  │
│                         │ executes                          │
│  ┌──────────────────────▼────────────────────────────────┐  │
│  │  Python Scripts (scripts/)                            │  │
│  │  • api_client.py → HTTP client (stdlib only)          │  │
│  │  • list_services.py, describe_service.py              │  │
│  │  • get_underutilized_ec2/rds/s3.py                    │  │
│  └──────────────────────┬────────────────────────────────┘  │
└─────────────────────────┼───────────────────────────────────┘
                          │ HTTP GET /api/v1/*
                          ▼
              ┌───────────────────────┐
              │  Cloud Efficiency API  │
              │  (mock_server/)       │
              │  Serves from JSON     │
              │  data files           │
              └───────────────────────┘
```

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `CLOUD_API_BASE_URL` | `http://127.0.0.1:8000` | API server URL |
| `CLOUD_API_VERSION` | `v1` | API version |
| `CLOUD_API_TIMEOUT` | `30` | Request timeout in seconds |
| `MOCK_SERVER_PORT` | `8000` | Port for mock server |

## File Structure

```
3pc_efficiency_commands/
├── .claude/
│   ├── commands/cloud-efficiency/   # Slash command definitions
│   │   ├── list-services.md
│   │   ├── describe-service.md
│   │   ├── get-underutilized-ec2.md
│   │   ├── get-underutilized-rds.md
│   │   └── get-underutilized-s3.md
│   └── settings.local.json         # Permission allowlist
├── scripts/                         # Python client scripts (stdlib only)
│   ├── config.py
│   ├── api_client.py
│   ├── list_services.py
│   ├── describe_service.py
│   ├── get_underutilized_ec2.py
│   ├── get_underutilized_rds.py
│   └── get_underutilized_s3.py
├── mock_server/                     # Local HTTP server + mock data
│   ├── server.py
│   └── data/
│       ├── services.json
│       ├── ec2_instances.json
│       ├── rds_instances.json
│       └── s3_buckets.json
├── CLAUDE.md                        # Project instructions for Claude
├── README.md
└── .gitignore
```

## Design Principles

- **Zero external dependencies** — Python stdlib only, no `pip install` needed
- **Scripts output JSON** — Claude interprets and formats the results conversationally
- **Natural language input** — Slash commands accept plain English, Claude parses the filters
- **Separation of concerns** — Commands define presentation, scripts handle API calls, server handles data

## Extending to Real APIs

To connect to a real cloud cost API (e.g., AWS Cost Explorer, CloudHealth, Spot.io):

1. Replace `mock_server/` with your real API endpoint
2. Update `scripts/config.py` with your API URL
3. Add authentication in `scripts/api_client.py` (API keys, OAuth, etc.)
4. The slash commands work unchanged — they only care about the JSON schema

## License

MIT
