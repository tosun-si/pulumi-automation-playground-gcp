FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

COPY pulumi_apps /app/pulumi_apps

FROM pulumi/pulumi-python:3.197.0

WORKDIR /app

COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"

RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser /app

USER appuser

CMD ["uvicorn", "pulumi_apps.automation_api.iaas.bq_datasets_tables_creation_api.main:app", "--host", "0.0.0.0", "--port", "8080"]
