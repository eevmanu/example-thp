import logging

from tenacity import retry, stop_after_attempt, wait_fixed, after_log, before_log
from sqlalchemy import select

from src.settings import cl_settings
from src.db import SessionLocal


# TODO move logging setup to one module
logging.basicConfig(
    level=cl_settings.LOGGING_LEVEL,
    format=cl_settings.LOGGING_FORMAT,
    style=cl_settings.LOGGING_STYLE,
)
logger = logging.getLogger(__name__)

MAX_TRIES = 60 * 5  # 5 minutes
WAIT_SECONDS = 1


@retry(
    stop=stop_after_attempt(MAX_TRIES),
    wait=wait_fixed(WAIT_SECONDS),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        with SessionLocal.begin() as session:
            session.execute(select(1))
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Testing connection between app and db")
    init()
    logger.info("Connection tested")


if __name__ == "__main__":
    main()
