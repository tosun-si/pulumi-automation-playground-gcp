import json
import os

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from pulumi_apps.shared.bq_resources_creation.datasets_with_tables import get_dataset, get_table_with_partitioning, \
    get_table

app = FastAPI()


class Request(BaseModel):
    datasets_with_tables_input: str


class Response(BaseModel):
    message: str


@app.post('/bigquery/teams_league/datasets/tables')
async def teams_league_service(request: Request):
    datasets_with_tables: list[dict] = json.loads(request.datasets_with_tables_input)

    for dataset in datasets_with_tables:
        bq_dataset = get_dataset(dataset)

        for table in dataset["tables"]:
            (
                get_table_with_partitioning(bq_dataset, table) if table.get("partitionType") is not None
                else get_table(bq_dataset, table)
            )


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
