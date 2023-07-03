import pytest
from fastapi import HTTPException
from sqlmodel import select

from foo_hardware import models
from foo_hardware.backend import get_hardware_item_from_id
from foo_hardware.utils_test import SessionClient


def test_get_item_from_id(bootstrap_data: SessionClient):
    session = bootstrap_data.session
    item = get_hardware_item_from_id(session=session, hardware_item_id=1)
    assert item.kind == 1
    assert item.comment == "some comment"


def test_get_item_from_wrong_id(bootstrap_data: SessionClient):
    session = bootstrap_data.session
    with pytest.raises(HTTPException):
        get_hardware_item_from_id(session=session, hardware_item_id=123)


def test_add_hardware_with_invalid_user(bootstrap_data: SessionClient):
    client = bootstrap_data.client

    url = "/hardware"
    headers = {"Content-Type": "application/json"}
    data = {"owner_id": "1111", "kind": "1"}
    response = client.post(url, headers=headers, json=data)
    assert response.status_code == 404


def test_create_hardware_item(bootstrap_data: SessionClient):
    client = bootstrap_data.client
    hardware_item_data = {"owner_id": 1, "kind": 1, "comment": "great stuff"}
    headers = {"Content-Type": "application/json"}

    response = client.post("/hardware", headers=headers, json=hardware_item_data)
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["comment"] == "great stuff"


def test_get_hardware_items(bootstrap_data: SessionClient):
    client = bootstrap_data.client

    response = client.get("/hardware")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 3


def test_delet_hardware_item(bootstrap_data: SessionClient):
    client = bootstrap_data.client
    response = client.delete("/hardware?hardware_item_id=1")
    assert response.status_code == 200

    response = client.get("/hardware")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 2


def test_update_item_owner(bootstrap_data: SessionClient):
    client = bootstrap_data.client
    session = bootstrap_data.session

    hardware_item_id = 1

    hardware_item = session.exec(
        select(models.HardwareItem).where(models.HardwareItem.id == hardware_item_id)
    ).fetchall()[0]
    assert hardware_item.owner_id == 1

    response = client.put(
        "/hardware?hardware_item_id=1&owner_id=2",
    )
    assert response.status_code == 200
    hardware_item = session.exec(
        select(models.HardwareItem).where(models.HardwareItem.id == hardware_item_id)
    ).fetchall()[0]
    assert hardware_item.owner_id == 2


def test_update_item_kind(bootstrap_data: SessionClient):
    client = bootstrap_data.client
    session = bootstrap_data.session

    hardware_item_id = 1

    hardware_item = session.exec(
        select(models.HardwareItem).where(models.HardwareItem.id == hardware_item_id)
    ).fetchall()[0]
    assert hardware_item.kind == 1

    response = client.put(
        "/hardware?hardware_item_id=1&kind=2",
    )
    assert response.status_code == 200
    hardware_item = session.exec(
        select(models.HardwareItem).where(models.HardwareItem.id == hardware_item_id)
    ).fetchall()[0]
    assert hardware_item.kind == 2


def test_update_item_comment(bootstrap_data: SessionClient):
    client = bootstrap_data.client
    session = bootstrap_data.session

    hardware_item_id = 1

    hardware_item = session.exec(
        select(models.HardwareItem).where(models.HardwareItem.id == hardware_item_id)
    ).fetchall()[0]
    assert hardware_item.comment == "some comment"

    response = client.put(
        "/hardware?hardware_item_id=1&comment=foo bar",
    )
    assert response.status_code == 200
    hardware_item = session.exec(
        select(models.HardwareItem).where(models.HardwareItem.id == hardware_item_id)
    ).fetchall()[0]
    assert hardware_item.comment == "foo bar"
