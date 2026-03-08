Describe a specific cloud service and its metadata.

The user's input is: $ARGUMENTS

Extract the service name from the user's input. It should be a lowercase, hyphenated string (e.g. "payment-platform").

Run this command from the project root:
```
python3 scripts/describe_service.py $SERVICE_NAME
```

The output is JSON with fields: service_name, description, owner, team, department, environment, region, aws_account_id, status, monthly_spend, resource_count.

Present the results as a well-formatted summary:
- **Service name** as a header
- Key metadata in a clean list format
- Highlight the **monthly spend** and **resource count** prominently
- Suggest the user try `/cloud-efficiency:get-underutilized-ec2`, `/cloud-efficiency:get-underutilized-rds`, or `/cloud-efficiency:get-underutilized-s3` filtered by this service to find savings
