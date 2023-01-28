import logging
from typing import Any

import decouple
from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class CLSettings(BaseSettings):

    PROJECT_NAME: str = decouple.config("PROJECT_NAME", cast=str)
    DEBUG : bool = decouple.config("DEBUG", cast=bool)

    POSTGRES_SCHEMA: str = decouple.config("POSTGRES_SCHEMA", cast=str)
    POSTGRES_USERNAME: str = decouple.config("POSTGRES_USERNAME", cast=str)
    POSTGRES_PASSWORD: str = decouple.config("POSTGRES_PASSWORD", cast=str)
    POSTGRES_HOST: str = decouple.config("POSTGRES_HOST", cast=str)
    POSTGRES_PORT: str = decouple.config("POSTGRES_PORT", cast=str)
    POSTGRES_DB: str = decouple.config("POSTGRES_DB", cast=str)

    # SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None
    # "postgresql+psycopg2://example_user:example_pwd@db:5432/example_db",

    SERVER_HOST : str = decouple.config("SERVER_HOST", cast=str)
    SERVER_PORT : int = decouple.config("SERVER_PORT", cast=int)
    SERVER_WORKERS : int = decouple.config("SERVER_WORKERS", cast=int)
    # LOGGERS: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    IS_ALLOWED_CREDENTIALS: bool = decouple.config("IS_ALLOWED_CREDENTIALS", cast=bool)
    ALLOWED_ORIGINS: list[AnyHttpUrl] = [
        "http://localhost",
        "http://127.0.0.1",
        "http://0.0.0.0",
    ]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    LOGGING_FORMAT : str = decouple.config("LOGGING_FORMAT", cast=str)
    LOGGING_STYLE : str = decouple.config("LOGGING_STYLE", cast=str)
    LOGGING_LEVEL : int = logging.INFO

    # API_PREFIX: str = "/api"
    # OPENAPI_URL: str = "/openapi.json"
    # OPENAPI_PREFIX: str = ""
    # DOCS_URL: str = "/docs"
    # REDOC_URL: str = "/redoc"


    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls,
        v: str | None,
        values: dict[str, Any],
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme=values.get("POSTGRES_SCHEMA", "postgresql"),
            user=values.get("POSTGRES_USERNAME"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


cl_settings : CLSettings = CLSettings()


logging.basicConfig(
    level=cl_settings.LOGGING_LEVEL,
    # level=logging.INFO,
    format=cl_settings.LOGGING_FORMAT,
    style=cl_settings.LOGGING_STYLE,
)
logger = logging.getLogger(__name__)
