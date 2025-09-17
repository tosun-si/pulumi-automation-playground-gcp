import json
import logging
import os

import uvicorn
from fastapi import FastAPI
from pulumi import automation as auto
from pydantic import BaseModel

from pulumi_apps.shared.bq_resources_creation.datasets_with_tables import get_dataset, get_table_with_partitioning, \
    get_table

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Request(BaseModel):
    datasets_with_tables_input: list[dict]


class Response(BaseModel):
    message: str


@app.post('/bigquery/teams_league/datasets/tables')
async def teams_league_service(request: Request):
    project_id = 'gb-poc-373711'
    region = 'europe-west1'
    stack_name = 'iaas_team_league_datasets_tables'

    stack = auto.create_or_select_stack(
        stack_name=stack_name,
        project_name=project_id,
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


def pulumi_program(datasets_with_tables_input: list[dict]):
    for dataset in datasets_with_tables_input:
        bq_dataset = get_dataset(dataset)

        for table in dataset["tables"]:
            (
                get_table_with_partitioning(bq_dataset, table) if table.get("partitionType") is not None
                else get_table(bq_dataset, table)
            )


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
