import logging
import random
# from decimal import Decimal

from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy import select, func
# from sqlalchemy.dialects.postgresql import array, ARRAY
# from sqlalchemy import Float
# from sqlalchemy import cast

from src.settings import cl_settings
from src.db import SessionLocal
from src.models import User, Audio


# TODO move logging setup to one module
logging.basicConfig(
    level=cl_settings.LOGGING_LEVEL,
    format=cl_settings.LOGGING_FORMAT,
    style=cl_settings.LOGGING_STYLE,
)
logger = logging.getLogger(__name__)


def initial_data(session: Session) -> None:
    fake = Faker()

    try:
        cursor_result = session.execute(
            select(func.count("*"))
            .select_from(User)
        )
        tuple_result = cursor_result.one()
        n = tuple_result[0]
        logger.info(f"users count {n=}")

        # insert users
        for _ in range(10):
            u = User(
                name=fake.name(),
                email=fake.email(),
                address=fake.address(),
                image=fake.image_url(),
            )
            session.add(u)

        cursor_result = session.execute(
            select(func.count("*"))
            .select_from(Audio)
        )
        tuple_result = cursor_result.one()
        n = tuple_result[0]
        logger.info(f"audio files count {n=}")

        # insert audio files
        for _ in range(10):
            # random_ticks : list[Decimal] = [
            #     Decimal(random.uniform(-10.0, -100.0))
            #     .quantize(Decimal('0.01'))
            #     for _ in range(15)
            # ]
            random_ticks : list[float] = [
                random.uniform(-10.0, -100.0)
                for _ in range(15)
            ]
            a = Audio(
                session_id=random.randint(2_000, 1_000_000),
                ticks=random_ticks,
                selected_tick=random.randint(0, 14),
                step_count=random.randint(0, 9),
            )
            session.add(a)
    except Exception as e:
        logger.error(e)
        raise e


def init() -> None:
    # Tables should be created with Alembic migrations
    # but if you don't want to use migrations,
    # delete tables, create new tables by un-commenting lines below
    # from app import Base, engine
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)

    with SessionLocal.begin() as session:
        initial_data(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
