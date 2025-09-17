# pulumi-automation-playground-gcp

This project proposes code samples using Pulumi and the Pulumi Automation API, with infrastructure provisioned on Google Cloud.

It highlights the classical IaC approach and shows how the Pulumi Automation API brings powerful capabilities to manage infrastructure programmatically\
— using an API, CLI, or directly in code. This approach is especially well-suited for IaaS and PaaS scenarios

## Run the IaaS FastAPI app locally

Install the Python packages with UV:

```bash
uv sync
```

Run the ASGI server with Uvicorn:

```bash
uvicorn pulumi_apps.automation_api.iaas.bq_datasets_tables_creation_api.main:app --reload --host 0.0.0.0 --port 8080
```

The request body and the request payload is:

```json
{
  "datasets_with_tables_input": [
    {
      "datasetId": "team_league_raw_pulumi",
      "datasetRegion": "EU",
      "datasetFriendlyName": "Team league Dataset containing raw data",
      "datasetDescription": "Team league raw Dataset description",
      "tables": [
        {
          "tableId": "team_stat_raw",
          "tableSchemaPath": "shared/bq_resources_creation/schema/team_league_raw/team_stat_raw.json"
        }
      ]
    },
    {
      "datasetId": "team_league_pulumi",
      "datasetRegion": "EU",
      "datasetFriendlyName": "Team league Dataset containing domain data",
      "datasetDescription": "Team league domain Dataset description",
      "tables": [
        {
          "tableId": "team_stat",
          "tableSchemaPath": "shared/bq_resources_creation/schema/team_league/team_stat.json",
          "partitionType": "DAY",
          "partitionField": "ingestionDate",
          "clustering": [
            "teamName",
            "teamSlogan"
          ]
        }
      ]
    }
  ]
}
```