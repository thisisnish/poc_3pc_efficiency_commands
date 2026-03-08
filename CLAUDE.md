# Cloud Efficiency Commands

Claude Code slash commands for AWS cloud cost optimization and efficiency insights.

## Architecture
- `.claude/commands/cloud-efficiency/` — slash command markdown files
- `scripts/` — Python stdlib-only client scripts (no external deps)
- `mock_server/` — Local HTTP server with mock AWS data

## Running
1. Start mock server: `python3 mock_server/server.py`
2. Use slash commands: `/cloud-efficiency:list-services`, etc.

## Conventions
- Python stdlib only — no pip installs required
- Errors output as `{"error": true, "message": "..."}` to stdout + exit 1
- Scripts output JSON to stdout; Claude summarizes for user
