from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from src.settings import cl_settings


engine = create_engine(
    # any change in URI, replicate in alembic `.ini` config file
    cl_settings.SQLALCHEMY_DATABASE_URI,
    # manage it on logging config
    # echo=True,
    # echo_pool="debug",
    future=True,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(engine)

Base = declarative_base()
