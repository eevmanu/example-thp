import logging
import re
from decimal import Decimal

from sqlalchemy import Column, Integer, Float, String
from sqlalchemy import UniqueConstraint, cast
from sqlalchemy.orm import validates
from sqlalchemy.dialects import postgresql
# from sqlalchemy.ext.mutable import MutableList

from src.settings import cl_settings
from src.db import Base


# TODO move logging setup to one module
logging.basicConfig(
    level=cl_settings.LOGGING_LEVEL,
    format=cl_settings.LOGGING_FORMAT,
    style=cl_settings.LOGGING_STYLE,
)
logger = logging.getLogger(__name__)


# TODO use uuidv7
# import sqlalchemy.dialects.postgresql
# from sqlalchemy import text
# PrimaryKeyType = sqlalchemy.dialects.postgresql.UUID
# https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#sqlalchemy.dialects.postgresql.UUID
# def makePrimaryKeyColumn(
#     pkType = PrimaryKeyType,
#     server_default = text('gen_random_uuid()'),
#     **kwargs,
# ):
#     return Column(
#         pkType(),
#         primary_key = True,
#         server_default = server_default,
#         **kwargs,
#     )


class User(Base):
    __tablename__ = "cl_user"

    id = Column(Integer, primary_key=True)
    # TODO use uuidv7
    # id = makePrimaryKeyColumn()

    name = Column(String(30), nullable=False)
    email = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)
    image = Column(String(100), nullable=False)

    def __repr__(self) -> str:
        return (
            "User("
            f"id={self.id!r}" + ","
            f"name={self.name!r}" + ","
            f"email={self.email!r}" + ","
            f"address={self.address!r}" + ","
            f"image={self.image!r}"
            ")"
        )

    @validates("name")
    def validates_name(self, key, value):
        if value == '':
            raise ValueError("ORM: failed user's name validation")
        return value

    @validates("email")
    def validates_email(self, key, value):
        if value == '':
            raise ValueError("ORM: failed user's email validation")
        EMAIL_REGEX_PATTERN=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        regex = re.compile(EMAIL_REGEX_PATTERN, re.IGNORECASE)
        match = regex.match(value)
        if not match:
            raise ValueError("ORM: user's email not comply regex")
        return value

    @validates("address")
    def validates_address(self, key, value):
        if value == '':
            raise ValueError("ORM: failed user's address validation")
        return value

    @validates("image")
    def validates_image(self, key, value):
        if value == '':
            raise ValueError("ORM: failed user's image URL validation")
        URL_REGEX_PATTERN=r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        regex = re.compile(URL_REGEX_PATTERN, re.IGNORECASE)
        match = regex.match(value)
        if not match:
            raise ValueError("ORM: user's image URL not comply regex")
        return value


class Audio(Base):
    __tablename__ = "cl_audio"

    id = Column(Integer, primary_key=True)
    # TODO use uuidv7
    # id = makePrimaryKeyColumn()

    session_id = Column(Integer, unique=True, nullable=False)
    # alternative, avoid creating an `id` field and use `session_id`

    ticks = Column(
        # MutableList.as_mutable(
            postgresql.ARRAY(Float),
            # postgresql.ARRAY(Numeric),
        # ),
        nullable=False,
    )
    selected_tick = Column(Integer, nullable=False)
    step_count = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('session_id', 'step_count'),
    )

    def __repr__(self) -> str:
        return (
            "Audio("
            f"session_id={self.session_id!r}" + ","
            f"ticks={self.ticks!r}" + ","
            f"selected_tick={self.selected_tick!r}" + ","
            f"step_count={self.step_count!r}"
            ")"
        )

    @validates("ticks")
    def validates_ticks(self, key, value):
        # logger.info(f"{type(key)=}")
        # logger.info(f"{type(value)=}")
        # logger.info(f"{value=}")
        # is value a list[float]
        if not isinstance(value, list):
            raise ValueError("ORM: not able to iterate ticks")
        if any([not isinstance(x, float) for x in value]):
            raise ValueError("ORM: failed audio's ticks validation")
        if len(value) != 15:
            raise ValueError("ORM: failed audio's ticks validation: ticks size")
        if any([(x < -100.0 or -10.0 < x) for x in value]):
            raise ValueError("ORM: failed audio's ticks validation: ticks wrong range")
        return value

    @validates("selected_tick")
    def validates_selected_tick(self, key, value):
        if not isinstance(value, int):
            raise ValueError("ORM: failed audio's selected_tick validation: type")
        if value < 0 or 14 < value:
            raise ValueError("ORM: failed audio's selected_tick validation: out of range")
        return value

    @validates("step_count")
    def validates_step_count(self, key, value):
        if not isinstance(value, int):
            raise ValueError("ORM: failed audio's step_count validation: type")
        if value < 0 or 9 < value:
            raise ValueError("ORM: failed audio's step_count validation: out of range")
        return value


# TODO apply CheckConstraint for validation constraints on User and Audio
