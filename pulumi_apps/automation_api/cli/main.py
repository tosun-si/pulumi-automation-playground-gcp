import json
import logging
import os

import typer
from pulumi import automation as auto
from typing_extensions import Annotated

from pulumi_apps.automation_api.automation_env_vars import GOOGLE_PROJECT_KEY, GOOGLE_REGION_KEY, STACK_NAME_VALUE, \
    DATASETS_CONFIG_FILE_KEY, PULUMI_BACKEND_URL_KEY, PULUMI_BACKEND_URL_VALUE, PULUMI_CONFIG_PASSPHRASE_VALUE, \
    PULUMI_CONFIG_PASSPHRASE_KEY
from pulumi_apps.root import ROOT_DIR
from pulumi_apps.shared.bq_resources_creation.datasets_with_tables import get_dataset, get_table_with_partitioning, \
    get_table
from pulumi_apps.shared.bq_resources_creation.datasets_with_tables_config_file_loader import \
    get_datasets_with_tables_input

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = typer.Typer()

datasets_app = typer.Typer()
app.add_typer(datasets_app, name="dataset")


@datasets_app.command("create", help="Create DWH BQ datasets and tables")
def run_tests(
        project: Annotated[
            str,
            typer.Option(
                "--project",
                envvar=GOOGLE_PROJECT_KEY,
                help="GCP project ID."
            )
        ],
        region: Annotated[
            str,
            typer.Option(
                "--region",
                envvar=GOOGLE_REGION_KEY,
                help="GCP region."
            )
        ],
        dataset_config: Annotated[
            str,
            typer.Option(
                "--dataset-config",
                envvar=DATASETS_CONFIG_FILE_KEY,
                help="Path to configuration file."
            )
        ]):
    logger.info(f"####################### The CLI is invoked with params : ")

    logger.info(f"project : {project}")
    logger.info(f"region : {region}")
    logger.info(f"dataset-config : {dataset_config}")

    os.environ[GOOGLE_PROJECT_KEY] = project
    os.environ[GOOGLE_REGION_KEY] = region
    os.environ[PULUMI_BACKEND_URL_KEY] = PULUMI_BACKEND_URL_VALUE
    os.environ[PULUMI_CONFIG_PASSPHRASE_KEY] = PULUMI_CONFIG_PASSPHRASE_VALUE
    # os.environ[STACK_NAME_KEY] = STACK_NAME_VALUE

    stack = auto.create_or_select_stack(
        stack_name=STACK_NAME_VALUE,
        project_name="datasets_tables_automation_cli",
        program=lambda: pulumi_program(dataset_config)
    )

    logger.info("Installing plugins...")
    stack.workspace.install_plugin("gcp", "v8.41.1")
    logger.info("Plugins installed")

    logger.info("Setting up config")
    stack.set_config("gcp:project", auto.ConfigValue(value=project))
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


def pulumi_program(dataset_config: str):
    for dataset in get_datasets_with_tables_input(f"{ROOT_DIR}/{dataset_config}"):
        bq_dataset = get_dataset(dataset)

        for table in dataset.tables:
            (
                get_table_with_partitioning(bq_dataset, table) if table.partitionType is not None
                else get_table(bq_dataset, table)
            )


@app.command("help")
def help():
    print("Team league datasets and tables creation from the CLI in BigQuery")


def run():
    app()
