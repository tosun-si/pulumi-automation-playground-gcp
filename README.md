# pulumi-automation-playground-gcp

This project proposes code samples using Pulumi and the Pulumi Automation API, with infrastructure provisioned on Google Cloud.

It highlights the classical IaC approach and shows how the Pulumi Automation API brings powerful capabilities to manage infrastructure programmatically\
— using an API, CLI, or directly in code. This approach is especially well-suited for IaaS and PaaS scenarios

## Run the classical IaC with Terraform

**Init/Plan/Apply**:

Go the Terraform module:

```bash
cd terraform/datasets_and_tables
```

```bash
terraform init -backend-config="bucket=${TF_STATE_BUCKET}" -backend-config="prefix=${TF_STATE_PREFIX}/datasets_and_tables_iac_tf)"
terraform plan --out tfplan.out
terraform apply -auto-approve tfplan.out
```

## Run the classical IaC with Pulumi

### Preview/Up

```bash
pulumi preview --diff
pulumi up --diff --yes
```

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
      "datasetId": "team_league_raw_pulumi_iaas",
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
      "datasetId": "team_league_pulumi_iaas",
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

## Build the IaaS FastAPI app locally with Docker

```bash
docker buildx build \
    -f pulumi_apps/automation_api/iaas/bq_datasets_tables_creation_api/Dockerfile \
    -t $LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME:$IMAGE_TAG \
    .
```

## Run the IaaS FastAPI app locally with Docker

```bash
docker run --rm -it \
    -p 8080:8080 \
    -e PROJECT_ID="$PROJECT_ID" \
    -e LOCATION="$LOCATION" \
    -v "$HOME/.config/gcloud:/home/datasetscreatoruser/.config/gcloud:ro" \
    $LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME:$IMAGE_TAG
```

## Build and deploy the IaaS FastAPI in Cloud Run

```bash
gcloud builds submit \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --config deploy-iaas-in-cloud-run.yaml \
    --substitutions _REPO_NAME="$REPO_NAME",_SERVICE_NAME="$SERVICE_NAME",_IMAGE_TAG="$IMAGE_TAG" \
    --verbosity="debug" .
```

## Install the CLI app locally with UV and Typer

Add the package elements in the pyproject.toml file:

```text
[tool.setuptools]
packages = ["pulumi_apps"]

[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
```

And the script for the CLI:

```text
[project.scripts]
dwh = "pulumi_apps.automation_api.cli.main:run"
```

Install the CLI app:

```bash
uv pip install -e
```

Run the CLI locally:

```bash
dwh dataset create \
  --project ${PROJECT_ID} \
  --region ${LOCATION} \
  --dataset-config automation_api/cli/config/datasets_with_tables.json
```

