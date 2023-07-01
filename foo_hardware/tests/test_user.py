from fastapi.testclient import TestClient
from foo_hardware.backend import app
from foo_hardware.tests.fixtures import (  # noqa: F401
    session_fixture,
    client_fixture,
    bootstrap_data_fixture,
)


def test_root_of_app():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200


def test_get_empty_users(client: TestClient):
    response = client.post("/user/", json={})
    app.dependency_overrides.clear()
    assert response.status_code == 422


def test_add_and_get_users2(bootstrap_data):
    client = bootstrap_data["client"]

    response = client.get("/user")
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 2
    p_pen = response.json()[0]
    assert p_pen["username"] == "Peter Pen"
    assert p_pen["password"] == "pass123"
