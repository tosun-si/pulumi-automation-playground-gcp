from typing import Optional

from pydantic import BaseModel


class TableInput(BaseModel):
    tableId: str
    tableSchemaPath: str
    partitionType: Optional[str] = None
    partitionField: Optional[str] = None
    clustering: Optional[list[str]] = None


class DatasetInput(BaseModel):
    datasetId: str
    datasetRegion: str
    datasetFriendlyName: str
    datasetDescription: str
    tables: list[TableInput]
