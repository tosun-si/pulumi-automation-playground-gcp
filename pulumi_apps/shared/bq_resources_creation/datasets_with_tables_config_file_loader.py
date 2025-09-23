import json

from pulumi_apps.root import ROOT_DIR
from pulumi_apps.shared.bq_resources_creation.dataset_table_input_objects import TableInput, DatasetInput


def _load_file_as_dicts(file_path: str) -> list[dict]:
    with open(file_path) as file:
        return json.load(file)


def _load_file_as_string(file_path: str) -> str:
    with open(file_path) as file:
        return file.read()


def get_table_schema(table: TableInput) -> str:
    table_schema_file_path = f'{ROOT_DIR}/{table.tableSchemaPath}'

    return _load_file_as_string(table_schema_file_path)


def get_datasets_with_tables_input(datasets_config_file_path: str) -> list[DatasetInput]:
    datasets_as_dicts: list[dict] = _load_file_as_dicts(datasets_config_file_path)

    return [DatasetInput(**dataset) for dataset in datasets_as_dicts]
