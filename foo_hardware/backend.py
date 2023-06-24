from typing import List

from fastapi import FastAPI, HTTPException, status
from sqlmodel import Session, SQLModel, create_engine, select

from foo_hardware import models

sqlite_file_name = "../data/foo_hardware.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/user/", response_model=models.UserRead)
def create_user(user: models.UserCreate):
    with Session(engine) as session:
        db_user = models.User.from_orm(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


@app.get("/user/", response_model=List[models.UserRead])
def read_users():
    with Session(engine) as session:
        users = session.exec(select(models.User)).all()
        return users


@app.post("/hardware/", response_model=models.HardwareItemRead)
def create_hardware_item(hardware_item: models.HardwareItemCreate):
    with Session(engine) as session:
        owner = session.exec(
            select(models.User).where(models.User.id == hardware_item.owner_id)
        ).fetchall()
        if len(owner) != 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Found {len(owner)} owners with the given id"
                    f" '{hardware_item.owner_id}'; expected only one"
                ),
            )
        db_hardware_item = models.HardwareItem.from_orm(hardware_item)
        session.exec
        session.add(db_hardware_item)
        session.commit()
        session.refresh(db_hardware_item)
        return db_hardware_item


@app.get("/hardware/", response_model=List[models.HardwareItemRead])
def read_hardware_items():
    with Session(engine) as session:
        hardware_items = session.exec(select(models.HardwareItem)).all()
        return hardware_items


@app.delete("/hardware", response_model=models.HardwareItemRead)
def delete_hardware_item(hardware_item_id: int):
    with Session(engine) as session:
        user_to_delete = session.exec(
            select(models.HardwareItem).where(
                models.HardwareItem.id == hardware_item_id
            )
        ).first()
        if user_to_delete is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No hardware item with ID: {hardware_item_id} found",
            )
        session.delete(user_to_delete)
        session.commit()
        return user_to_delete
