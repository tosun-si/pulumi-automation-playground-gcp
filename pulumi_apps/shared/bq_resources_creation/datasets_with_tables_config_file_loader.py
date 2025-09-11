import json
from typing import List, Dict

from pulumi_apps.root import ROOT_DIR


def _load_file_as_dicts(file_path: str) -> List[Dict]:
    with open(file_path) as file:
        return json.load(file)


def _load_file_as_string(file_path: str) -> str:
    with open(file_path) as file:
        return file.read()


def get_table_schema(table: Dict) -> str:
    table_schema_file_path = f'{ROOT_DIR} / {table["tableSchemaPath"]}'

    return _load_file_as_string(table_schema_file_path)


def get_datasets_with_tables_config(datasets_config_file_path) -> List[Dict]:
    datasets_tables_config_file_path = str(datasets_config_file_path)

    return _load_file_as_dicts(datasets_tables_config_file_path)
