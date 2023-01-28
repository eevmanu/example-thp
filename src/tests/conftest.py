from typing import Generator

import pytest
from fastapi.testclient import TestClient
# from faker import Faker

from src.db import SessionLocal
from src.main import app


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c

# TODO use faker as pytest fixture
# @pytest.fixture(scope="module")
# def generate_data() -> Generator:
#     fake = Faker()
#     # how to create a yield?
