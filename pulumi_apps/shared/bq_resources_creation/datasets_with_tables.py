import pulumi_gcp as gcp
from pulumi import ResourceOptions
from pulumi_gcp.bigquery import Dataset

from pulumi_apps.shared.bq_resources_creation.dataset_table_input_objects import TableInput, DatasetInput
from pulumi_apps.shared.bq_resources_creation.datasets_with_tables_config_file_loader import get_table_schema


def get_table(dataset: Dataset, table: TableInput):
    return gcp.bigquery.Table(
        table.tableId,
        deletion_protection=False,
        dataset_id=dataset.dataset_id,
        table_id=table.tableId,
        clusterings=table.clustering,
        schema=get_table_schema(table),
        opts=ResourceOptions(depends_on=[dataset])
    )


def get_table_with_partitioning(dataset: Dataset, table: TableInput):
    return gcp.bigquery.Table(
        table.tableId,
        deletion_protection=False,
        dataset_id=dataset.dataset_id,
        table_id=table.tableId,
        clusterings=table.clustering,
        time_partitioning=gcp.bigquery.TableTimePartitioningArgs(
            type=table.partitionType,
            field=table.partitionField,
        ),
        schema=get_table_schema(table),
        opts=ResourceOptions(depends_on=[dataset])
    )


def get_dataset(dataset: DatasetInput):
    dataset_id = dataset.datasetId

    return gcp.bigquery.Dataset(
        dataset_id,
        dataset_id=dataset_id,
        friendly_name=dataset.datasetFriendlyName,
        description=dataset.datasetDescription,
        location=dataset.datasetRegion
    )
