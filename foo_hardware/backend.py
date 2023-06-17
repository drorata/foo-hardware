from typing import List

from fastapi import FastAPI
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
        print("XXXXXXXXXXX")
        print(f"ZZ: {hardware_item.owner_id}")
        find_user = select(models.User).where(models.User.id == hardware_item.owner_id)
        res = session.exec(find_user)
        print(f"YYY: {res}")
        print("XXXXXXXXXXX")
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
