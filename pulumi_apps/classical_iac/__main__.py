from pulumi_apps.root import ROOT_DIR
from pulumi_apps.shared.bq_resources_creation.datasets_with_tables import get_dataset, get_table_with_partitioning, \
    get_table
from pulumi_apps.shared.bq_resources_creation.datasets_with_tables_config_file_loader import \
    get_datasets_with_tables_input

for dataset in get_datasets_with_tables_input(f"{ROOT_DIR}/classical_iac/config/datasets_with_tables.json"):
    bq_dataset = get_dataset(dataset)

    for table in dataset.tables:
        bq_table = (
            get_table_with_partitioning(bq_dataset, table) if table.partitionType is not None
            else get_table(bq_dataset, table)
        )
