Find underutilized RDS instances with right-sizing recommendations and projected annual savings.

The user's input is: $ARGUMENTS

Parse the following from the user's natural language input:
- **--service** (optional): Service name to filter by
- **--cpu** (optional, default 20): CPU utilization threshold percentage
- **--memory** (optional, default 40): Memory utilization threshold percentage
- **--start-date** (optional): Start date in YYYY-MM-DD format
- **--end-date** (optional): End date in YYYY-MM-DD format

Build and run the command from the project root:
```
python3 scripts/get_underutilized_rds.py [--service SERVICE] [--cpu CPU] [--memory MEMORY] [--start-date DATE] [--end-date DATE]
```

The output is JSON:
```json
{
  "instances": [
    {
      "db_instance_id": "pay-db-prod-primary",
      "service": "payment-platform",
      "engine": "PostgreSQL 15.4",
      "instance_class": "db.r6g.4xlarge",
      "allocated_storage_gb": 2000,
      "used_storage_gb": 340,
      "storage_utilization_pct": 17.0,
      "provisioned_iops": 10000,
      "avg_iops_used": 620,
      "iops_utilization_pct": 6.2,
      "avg_cpu_pct": 5.8,
      "avg_db_connections": 18,
      "max_allowed_connections": 5000,
      "connection_utilization_pct": 0.84,
      "monthly_cost": 8942.00,
      "recommended_class": "db.r6g.large",
      "recommended_monthly_cost": 1680.00,
      "potential_annual_savings": 87144.00
    }
  ],
  "count": 1,
  "total_potential_annual_savings": 87144.00
}
```

Present results as a formatted table with columns:
| RDS Instance | Service | Engine | Current Class | Avg CPU | Storage Used | IOPS Used | Monthly Cost | Recommended | Savings/yr |

After the table, include a **Summary** section with:
- Total RDS instances flagged
- **Total potential annual savings** (bold, formatted as currency)
- Key inefficiencies highlighted:
  - Storage over-provisioning (e.g. "2TB allocated, only 340GB used — 83% wasted")
  - IOPS over-provisioning (e.g. "10,000 IOPS provisioned, avg 620 used — 94% wasted")
  - Connection pool waste (e.g. "5,000 max connections, avg 18 used")
- Right-sizing recommendations for each instance

Make the waste metrics impossible to ignore. RDS is often the biggest hidden cost — make that clear.
