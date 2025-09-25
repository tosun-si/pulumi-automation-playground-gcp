FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    WORKDIR=/usr/local/src/app

WORKDIR $WORKDIR

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

COPY pulumi_apps $WORKDIR/pulumi_apps

FROM pulumi/pulumi-python:3.197.0

ENV WORKDIR=/usr/local/src/app
WORKDIR $WORKDIR

COPY --from=builder $WORKDIR $WORKDIR

ENV PATH="$WORKDIR/.venv/bin:$PATH"

RUN adduser --disabled-password --gecos '' --home /home/datasetscreatoruser datasetscreatoruser && \
    chown -R datasetscreatoruser $WORKDIR

USER datasetscreatoruser

ENTRYPOINT ["uvicorn"]
CMD ["pulumi_apps.automation_api.iaas.bq_datasets_tables_creation_api.main:app", "--host", "0.0.0.0", "--port", "8080"]
