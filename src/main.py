import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.settings import cl_settings
from src.endpoints import api_router


logging.basicConfig(
    level=cl_settings.LOGGING_LEVEL,
    format=cl_settings.LOGGING_FORMAT,
    style=cl_settings.LOGGING_STYLE,
)
# TODO un-comment lines below to debug sqlalchemy (for development purposes)
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
# logging.getLogger("sqlalchemy.pool").setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)


def init_app() -> FastAPI:
    app = FastAPI(
        title=cl_settings.PROJECT_NAME,
        openapi_url="/openapi.json",
        # openapi_url=cl_settings.OPENAPI_URL,
        # openapi_url=cl_settings.OPENAPI_PREFIX + cl_settings.OPENAPI_URL,
        # docs_url=cl_settings.DOCS_URL,
        # redoc_url=cl_settings.REDOC_URL.
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cl_settings.ALLOWED_ORIGINS,
        allow_credentials=cl_settings.IS_ALLOWED_CREDENTIALS,
        allow_methods=cl_settings.ALLOWED_METHODS,
        allow_headers=cl_settings.ALLOWED_HEADERS,
    )

    app.include_router(
        router=api_router,
        prefix="/api",
        # prefix=cl_settings.API_PREFIX,
    )

    return app

app : FastAPI = init_app()

@app.get("/")
def read_root():
    return {"Hello": "World"}



# able to simplify CMD on
# - `app` dockerfile
# - docker compose file - `app` service
# to `python main.py`
if __name__ == "__main__":
    uvicorn.run(
        # "< python module path which contains app variable >:< variable name of web app >"
        app="src.main:app",
        host=cl_settings.SERVER_HOST,
        port=cl_settings.SERVER_PORT,
        log_level=cl_settings.LOGGING_LEVEL,
        # for development
        reload=cl_settings.DEBUG,
        # for production
        # workers=cl_settings.SERVER_WORKERS,
    )
