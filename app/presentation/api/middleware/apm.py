from fastapi import FastAPI

from elasticapm.contrib.starlette import ElasticAPM


def setup_apm_middleware(app: FastAPI) -> None:
    app.add_middleware(
        ElasticAPM,
    )  # настройки Elastic APM читаются из переменных окружения (динамически он их не увидит)
