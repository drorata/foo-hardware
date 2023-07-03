from fastapi.testclient import TestClient
from pydantic import BaseModel
from sqlmodel import Session


class SessionClient(BaseModel):
    session: Session
    client: TestClient

    class Config:
        arbitrary_types_allowed = True
