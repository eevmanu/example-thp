import logging
import re
# from decimal import Decimal
# import datetime
# import typing

from pydantic import BaseModel
# from pydantic import BaseConfig
from pydantic import EmailStr, AnyHttpUrl
from pydantic import validator

from src.settings import cl_settings


logging.basicConfig(
    level=cl_settings.LOGGING_LEVEL,
    format=cl_settings.LOGGING_FORMAT,
    style=cl_settings.LOGGING_STYLE,
)
logger = logging.getLogger(__name__)


# def format_datetime_into_isoformat(date_time: datetime.datetime) -> str:
#     return (
#         date_time.replace(
#             tzinfo=datetime.timezone.utc
#         )
#         .isoformat()
#         .replace("+00:00", "Z")
#     )

# def format_dict_key_to_camel_case(dict_key: str) -> str:
#     return "".join(
#         word
#         if idx == 0
#         else word.capitalize()
#         for idx, word in enumerate(dict_key.split("_"))
#     )

# custom BaseModel
# class CustomBaseModel(BaseModel):
#     class Config(BaseConfig):
#         orm_mode: bool = True
#         validate_assignment: bool = True
#         allow_population_by_field_name: bool = True
#         json_encoders: dict = {datetime.datetime: format_datetime_into_isoformat}
#         alias_generator: typing.Any = format_dict_key_to_camel_case


class UserIn(BaseModel):
    name: str
    email : EmailStr
    address : str
    image : AnyHttpUrl

    @validator("name")
    def validate_name(cls, v):
        # logger.info(f"{type(v)=}")
        if not isinstance(v, str):
            raise ValueError("SCHEMA: failed user's name validation (type)")
        if v.strip() == "":
            raise ValueError("SCHEMA: failed user's name validation (blank data)")
        return v

    @validator("email")
    def validate_email(cls, v):
        if v.strip() == "":
            raise ValueError("SCHEMA: failed user's email validation (blank data)")
        EMAIL_REGEX_PATTERN=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        regex = re.compile(EMAIL_REGEX_PATTERN, re.IGNORECASE)
        match = regex.match(v)
        if not match:
            raise ValueError("SCHEMA: user's email not comply regex")
        return v

    @validator("address")
    def validate_address(cls, v):
        if v.strip() == '':
            raise ValueError("SCHEMA: failed user's address validation")
        return v

    @validator("image")
    def validate_image(cls, v):
        if v.strip() == '':
            raise ValueError("SCHEMA: failed user's image validation")
        URL_REGEX_PATTERN=r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        regex = re.compile(URL_REGEX_PATTERN, re.IGNORECASE)
        match = regex.match(v)
        if not match:
            raise ValueError("SCHEMA: user's image URL not comply regex")
        return v


class UserSearchIn(BaseModel):
    id: int | None
    email: EmailStr | None
    address: str | None

    @validator("email")
    def validate_email(cls, v):
        # allow email as None
        if v is None:
            return v
        if v.strip() == "":
            raise ValueError("SCHEMA: failed user's email validation (blank data)")
        EMAIL_REGEX_PATTERN=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        regex = re.compile(EMAIL_REGEX_PATTERN, re.IGNORECASE)
        match = regex.match(v)
        if not match:
            raise ValueError("SCHEMA: user's email not comply regex")
        return v


class UserOut(BaseModel):
    id : int
    name : str
    email : EmailStr
    address : str
    image : AnyHttpUrl

    @validator("name")
    def validate_name(cls, v):
        # logger.info(f"{type(v)=}")
        if not isinstance(v, str):
            raise ValueError("SCHEMA: failed user's name validation (type)")
        if v.strip() == "":
            raise ValueError("SCHEMA: failed user's name validation (blank data)")
        return v

    @validator("email")
    def validate_email(cls, v):
        if v.strip() == "":
            raise ValueError("SCHEMA: failed user's email validation (blank data)")
        EMAIL_REGEX_PATTERN=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        regex = re.compile(EMAIL_REGEX_PATTERN, re.IGNORECASE)
        match = regex.match(v)
        if not match:
            raise ValueError("SCHEMA: user's email not comply regex")
        return v

    @validator("address")
    def validate_address(cls, v):
        if v.strip() == '':
            raise ValueError("SCHEMA: failed user's address validation")
        return v

    @validator("image")
    def validate_image(cls, v):
        if v.strip() == '':
            raise ValueError("SCHEMA: failed user's image validation")
        URL_REGEX_PATTERN=r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        regex = re.compile(URL_REGEX_PATTERN, re.IGNORECASE)
        match = regex.match(v)
        if not match:
            raise ValueError("SCHEMA: user's image URL not comply regex")
        return v

# audioout

class AudioIn(BaseModel):

    session_id : int
    ticks : list[float]
    selected_tick : int
    step_count : int


    @validator("ticks")
    def validate_ticks(cls, v):
        # logger.info(f"{type(v)=}")
        # logger.info(f"{v=}")
        if not isinstance(v, list):
            raise ValueError("SCHEMA: not able to iterate ticks")
        if any([not isinstance(x, float) for x in v]):
            raise ValueError("SCHEMA: failed audio's ticks validation")
        if len(v) != 15:
            raise ValueError("SCHEMA: failed audio's ticks validation: ticks size")
        if any([(x < -100.0 or -10.0 < x) for x in v]):
            raise ValueError("SCHEMA: failed audio's ticks validation: ticks wrong range")
        return v

    @validator("selected_tick")
    def validate_selected_tick(cls, v):
        if not isinstance(v, int):
            raise ValueError("SCHEMA: failed audio's selected_tick validation: type")
        if v < 0 or 14 < v:
            raise ValueError("SCHEMA: failed audio's selected_tick validation: out of range")
        return v

    @validator("step_count")
    def validate_step_count(cls, v):
        if not isinstance(v, int):
            raise ValueError("SCHEMA: failed audio's step_count validation: type")
        if v < 0 or 9 < v:
            raise ValueError("SCHEMA: failed audio's step_count validation: out of range")
        return v


class AudioOut(BaseModel):

    id : int
    session_id : int
    ticks : list[float]
    selected_tick : int
    step_count : int


    @validator("ticks")
    def validate_ticks(cls, v):
        # logger.info(f"{type(v)=}")
        # logger.info(f"{v=}")
        if not isinstance(v, list):
            raise ValueError("SCHEMA: not able to iterate ticks")
        if any([not isinstance(x, float) for x in v]):
            raise ValueError("SCHEMA: failed audio's ticks validation")
        if len(v) != 15:
            raise ValueError("SCHEMA: failed audio's ticks validation: ticks size")
        if any([(x < -100.0 or -10.0 < x) for x in v]):
            raise ValueError("SCHEMA: failed audio's ticks validation: ticks wrong range")
        return v

    @validator("selected_tick")
    def validate_selected_tick(cls, v):
        if not isinstance(v, int):
            raise ValueError("SCHEMA: failed audio's selected_tick validation: type")
        if v < 0 or 14 < v:
            raise ValueError("SCHEMA: failed audio's selected_tick validation: out of range")
        return v

    @validator("step_count")
    def validate_step_count(cls, v):
        if not isinstance(v, int):
            raise ValueError("SCHEMA: failed audio's step_count validation: type")
        if v < 0 or 9 < v:
            raise ValueError("SCHEMA: failed audio's step_count validation: out of range")
        return v


class AudioSearchIn(BaseModel):
    session_id: int | None
