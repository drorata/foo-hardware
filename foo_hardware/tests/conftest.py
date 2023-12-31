import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from foo_hardware import models
from foo_hardware.backend import app, get_session
from foo_hardware.utils_test import SessionClient


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
    session.add(models.HardwareItem(kind=1, comment="some comment", owner_id=1))
    session.add(models.HardwareItem(kind=2, comment="some comment2", owner_id=1))
    session.add(models.HardwareItem(kind=1, comment="some comment3", owner_id=1))
    session.commit()
    yield SessionClient(session=session, client=client)
