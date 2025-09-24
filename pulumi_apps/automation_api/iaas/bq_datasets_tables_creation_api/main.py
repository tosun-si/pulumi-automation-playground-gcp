import json
import logging
import os

import uvicorn
from fastapi import FastAPI
from pulumi import automation as auto
from pydantic import BaseModel

from pulumi_apps.automation_api.automation_env_vars import GOOGLE_PROJECT_KEY, GOOGLE_REGION_KEY, \
    PULUMI_BACKEND_URL_KEY, PULUMI_BACKEND_URL_VALUE, PULUMI_CONFIG_PASSPHRASE_KEY, PULUMI_CONFIG_PASSPHRASE_VALUE, \
    STACK_NAME_VALUE
from pulumi_apps.shared.bq_resources_creation.dataset_table_input_objects import DatasetInput
from pulumi_apps.shared.bq_resources_creation.datasets_with_tables import get_dataset, get_table_with_partitioning, \
    get_table

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Request(BaseModel):
    datasets_with_tables_input: list[DatasetInput]


class Response(BaseModel):
    message: str


@app.post('/bigquery/teams_league/datasets/tables')
async def teams_league_datasets_service(request: Request):
    project_id = os.environ.get('PROJECT_ID', 'PROJECT_ID env var is not set.')
    region = os.environ.get('LOCATION', 'LOCATION env var is not set.')

    os.environ[GOOGLE_PROJECT_KEY] = project_id
    os.environ[GOOGLE_REGION_KEY] = region
    os.environ[PULUMI_BACKEND_URL_KEY] = PULUMI_BACKEND_URL_VALUE
    os.environ[PULUMI_CONFIG_PASSPHRASE_KEY] = PULUMI_CONFIG_PASSPHRASE_VALUE
    # os.environ[STACK_NAME_KEY] = STACK_NAME_VALUE

    stack = auto.create_or_select_stack(
        stack_name=STACK_NAME_VALUE,
        project_name="datasets_tables_automation_iaas",
        program=lambda: pulumi_program(request.datasets_with_tables_input)
    )

    logger.info("Installing plugins...")
    stack.workspace.install_plugin("gcp", "v8.41.1")
    logger.info("Plugins installed")

    logger.info("Setting up config")
    stack.set_config("gcp:project", auto.ConfigValue(value=project_id))
    stack.set_config("gcp:region", auto.ConfigValue(value=region))
    logger.info("Config set")

    logger.info("Refreshing stack...")
    stack.refresh(on_output=print)
    logger.info("Refresh complete")

    logger.info("#################### Creating the infra...")
    up_res = stack.up(
        on_output=print,
        color="always",
        show_secrets=False,
        diff=True
    )
    logger.info(f"Update summary: \n{json.dumps(up_res.summary.resource_changes, indent=4)}")

    return Response(
        message="Team league BigQuery datasets and tables created successfully ✅"
    )


def pulumi_program(datasets_with_tables_input: list[DatasetInput]):
    for dataset in datasets_with_tables_input:
        bq_dataset = get_dataset(dataset)

        for table in dataset.tables:
            (
                get_table_with_partitioning(bq_dataset, table) if table.partitionType is not None
                else get_table(bq_dataset, table)
            )


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
