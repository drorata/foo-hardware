import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from foo_hardware import models
from foo_hardware.backend import app, get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session  #


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="bootstrap_data")
def bootstrap_data_fixture(client: TestClient, session: Session):
    session.add(
        models.User(
            username="Peter Pen", password="pass123", email="peter@neverland.io"
        )
    )
    session.add(
        models.User(
            username="Captain Hook", password="pass456", email="hook@neverland.io"
        )
    )
    session.commit()
    yield {"client": client, "session": session}


def test_root_of_app():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200


def test_get_empty_users(client: TestClient):
    response = client.post("/user/", json={})
    app.dependency_overrides.clear()

    print(response.json())

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
