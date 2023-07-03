from fastapi.testclient import TestClient

from foo_hardware.backend import app, get_user_from_id
from foo_hardware.utils_test import SessionClient


def test_root_of_app():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200


def test_add_user(bootstrap_data: SessionClient):
    client = bootstrap_data.client

    url = "/user/"
    headers = {"Content-Type": "application/json"}
    data = {
        "username": "great guy",
        "password": "here_is_a_password",
        "email": "some@email.com",
    }
    response = client.post(url, headers=headers, json=data)
    assert response.status_code == 200
    assert response.json()["username"] == "great guy"


def test_get_user_by_id(bootstrap_data: SessionClient):
    session = bootstrap_data.session
    user = get_user_from_id(session=session, user_id=1)
    assert user.username == "Peter Pen"


def test_get_empty_users(client: TestClient):
    response = client.post("/user/", json={})
    app.dependency_overrides.clear()
    assert response.status_code == 422


def test_add_and_get_users2(bootstrap_data: SessionClient):
    client = bootstrap_data.client

    response = client.get("/user")
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 2
    p_pen = response.json()[0]
    assert p_pen["username"] == "Peter Pen"
    assert p_pen["password"] == "pass123"
