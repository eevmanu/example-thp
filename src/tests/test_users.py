from http import HTTPStatus

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.crud import user_crud
from src.schema import UserIn


def test_hello_world(
    client: TestClient
) -> None:
    r = client.get("/")
    assert r.status_code == 200


def test_get_users(
    client: TestClient
) -> None:
    r = client.get("/api/users")
    assert r.status_code == 200
    # TODO validate structure of first entity
    # TODO validate structure of all entities


def test_get_user(
    client: TestClient,
    db : Session,
) -> None:
    # TODO replace by a faker pytest fixture
    from faker import Faker
    fake = Faker()

    # TODO move to fixture
    in_data : dict = {
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address(),
        "image": fake.image_url(),
    }
    user_in = UserIn(
        name=in_data["name"],
        email=in_data["email"],
        address=in_data["address"],
        image=in_data["image"],
    )
    user_in = user_crud.create(db, user_in)


    r = client.get(f"/api/users/{user_in.id}")
    out_data = r.json()
    assert r.status_code == 200
    assert user_in.id == out_data["id"]
    assert all(in_data[k] == out_data[k] for k in in_data if k in out_data)


def test_create_user(
    client: TestClient,
    db : Session,
) -> None:
    # TODO move to fixture
    in_data : dict = {
        "name": "name1",
        "email": "name1@gmail.com",
        "address": "address1",
        "image": "https://i.imgur.com/name1.png",
    }


    r = client.post(
        "/api/users",
        json=in_data,
    )
    out_data = r.json()
    assert r.status_code == 200
    assert all(in_data[k] == out_data[k] for k in in_data if k in out_data)


    r = client.get(f"/api/users/{out_data['id']}")
    out_data = r.json()
    assert r.status_code == 200
    assert all(in_data[k] == out_data[k] for k in in_data if k in out_data)


def test_full_update_user(
    client: TestClient,
    db : Session,
):
    # TODO move to fixture
    in_data : dict = {
        "name": "name1",
        "email": "name1@gmail.com",
        "address": "address1",
        "image": "https://i.imgur.com/name1.png",
    }
    r = client.post(
        "/api/users",
        json=in_data,
    )
    out_data = r.json()
    assert r.status_code == 200
    # assert all(in_data[k] == out_data[k] for k in in_data if k in out_data)
    r = client.get(f"/api/users/{out_data['id']}")
    out_data = r.json()
    assert r.status_code == 200
    assert all(in_data[k] == out_data[k] for k in in_data if k in out_data)


    in_up_data : dict = {
        "name": "name2",
        "email": "name2@gmail.com",
        "address": "address2",
        "image": "https://i.imgur.com/name2.png",
    }


    r = client.put(
        f"/api/users/{out_data['id']}",
        json=in_up_data,
    )
    out_data = r.json()
    assert r.status_code == 200
    assert all(in_up_data[k] == out_data[k] for k in in_up_data if k in out_data)
    # assert all(in_data[k] != out_data[k] for k in in_data if k in out_data)


def test_delete_user(
    client: TestClient,
    db : Session,
):
    # TODO move to fixture
    in_data : dict = {
        "name": "name1",
        "email": "name1@gmail.com",
        "address": "address1",
        "image": "https://i.imgur.com/name1.png",
    }
    r = client.post(
        "/api/users",
        json=in_data,
    )
    out_data = r.json()
    assert r.status_code == HTTPStatus.OK

    r = client.delete(f"/api/users/{out_data['id']}")
    assert r.status_code == HTTPStatus.OK

    r = client.get(f"/api/users/{out_data['id']}")
    assert r.status_code == HTTPStatus.NOT_FOUND


def test_search_user_by_email(
    client: TestClient,
    db : Session,
):
    # TODO move to fixture
    in_data : dict = {
        "name": "name1",
        "email": "name1@gmail.com",
        "address": "address1",
        "image": "https://i.imgur.com/name1.png",
    }
    r = client.post(
        "/api/users",
        json=in_data,
    )
    out_data = r.json()
    assert r.status_code == HTTPStatus.OK

    in_search_data : dict = {
        "email": out_data["email"],
    }

    r = client.post(
        "/api/users/search",
        json=in_search_data,
    )
    out_data = r.json()
    assert r.status_code == HTTPStatus.OK
    assert in_data["email"] == out_data[0]["email"]


def test_search_user_by_address(
    client: TestClient,
    db : Session,
):
    # TODO move to fixture
    in_data : dict = {
        "name": "name1",
        "email": "name1@gmail.com",
        "address": "address1",
        "image": "https://i.imgur.com/name1.png",
    }
    r = client.post(
        "/api/users",
        json=in_data,
    )
    out_data = r.json()
    assert r.status_code == HTTPStatus.OK

    in_search_data : dict = {
        "address": out_data["address"],
    }

    r = client.post(
        "/api/users/search",
        json=in_search_data,
    )
    out_data = r.json()
    assert r.status_code == HTTPStatus.OK
    assert in_data["address"] == out_data[0]["address"]


# TODO replicate tests for audio files
