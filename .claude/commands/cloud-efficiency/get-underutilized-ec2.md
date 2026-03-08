Find underutilized EC2 instances with right-sizing recommendations and projected annual savings.

The user's input is: $ARGUMENTS

Parse the following from the user's natural language input:
- **--service** (optional): Service name to filter by (e.g. "payment-platform")
- **--cpu** (optional, default 20): CPU utilization threshold percentage — instances below this are flagged
- **--memory** (optional, default 40): Memory utilization threshold percentage — instances below this are flagged
- **--start-date** (optional): Start date in YYYY-MM-DD format
- **--end-date** (optional): End date in YYYY-MM-DD format

Build and run the command from the project root:
```
python3 scripts/get_underutilized_ec2.py [--service SERVICE] [--cpu CPU] [--memory MEMORY] [--start-date DATE] [--end-date DATE]
```

The output is JSON:
```json
{
  "instances": [
    {
      "instance_id": "i-xxx",
      "instance_name": "name",
      "service": "service-name",
      "instance_type": "c5.4xlarge",
      "vcpus": 16,
      "memory_gb": 32,
      "avg_cpu_pct": 4.2,
      "max_cpu_pct": 11.8,
      "avg_memory_pct": 8.6,
      "monthly_cost": 4896.00,
      "recommended_type": "c5.large",
      "recommended_monthly_cost": 612.00,
      "potential_annual_savings": 51408.00
    }
  ],
  "count": 1,
  "total_potential_annual_savings": 51408.00
}
```

Present results as a formatted table with columns:
| Instance | Service | Current Type | Avg CPU | Avg Mem | Monthly Cost | Recommended | Savings/yr |

After the table, include a **Summary** section with:
- Total instances flagged
- **Total potential annual savings** (bold, formatted as currency)
- The worst offenders (lowest CPU/memory utilization)
- A brief recommendation for each instance (e.g. "Downsize from c5.4xlarge to c5.large — using only 4% of 16 vCPUs")

Make the savings numbers stand out. This data should make the cost waste obvious at a glance.
