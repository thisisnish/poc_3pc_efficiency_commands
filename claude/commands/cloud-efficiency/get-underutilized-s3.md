Find over-provisioned S3 buckets with storage optimization recommendations and projected annual savings.

The user's input is: $ARGUMENTS

Parse the following from the user's natural language input:
- **--service** (optional): Service name to filter by

Build and run the command from the project root:
```
python3 scripts/get_underutilized_s3.py [--service SERVICE]
```

The output is JSON:
```json
{
  "buckets": [
    {
      "bucket_name": "analytics-data-lake-raw",
      "service": "user-analytics",
      "total_size_gb": 12400.0,
      "object_count": 64200000,
      "current_storage_class": "STANDARD",
      "pct_objects_not_accessed_90d": 91.2,
      "pct_objects_not_accessed_180d": 84.8,
      "versioning_enabled": true,
      "version_overhead_gb": 3100.0,
      "lifecycle_policy": false,
      "monthly_cost": 9920.00,
      "recommended_storage_class": "INTELLIGENT_TIERING",
      "recommended_lifecycle": "Move objects >60d to GLACIER, delete versions >14d",
      "recommended_monthly_cost": 1980.00,
      "potential_annual_savings": 95280.00
    }
  ],
  "count": 1,
  "total_potential_annual_savings": 95280.00
}
```

Present results as a formatted table with columns:
| Bucket | Service | Size (GB) | Storage Class | % Unaccessed (90d) | Versioning Overhead | Monthly Cost | Recommended Class | Savings/yr |

After the table, include a **Summary** section with:
- Total buckets flagged
- **Total potential annual savings** (bold, formatted as currency)
- Key findings highlighted:
  - Buckets with NO lifecycle policy (this is a red flag — call it out)
  - Stale data percentages (e.g. "91% of 64M objects haven't been accessed in 90 days — still on STANDARD storage")
  - Version bloat (e.g. "3.1TB of version overhead with no expiration policy")
- Specific lifecycle policy recommendations for each bucket

S3 costs are death by a thousand cuts — make each bucket's waste crystal clear with actionable next steps.
