from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, SQLModel, create_engine, select

from foo_hardware import constants, models

sqlite_file_name = "../data/foo_hardware.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():  # pragma: no cover
    SQLModel.metadata.create_all(engine)


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.on_event("startup")
def on_startup():  # pragma: no cover
    create_db_and_tables()


@app.get("/")
def nothing_to_see_here():
    return "There's nothing to see here"


@app.post("/user", response_model=models.UserRead)
def create_user(*, session: Session = Depends(get_session), user: models.UserCreate):
    db_user = models.User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get("/user", response_model=List[models.UserRead])
def read_users(
    *,
    session: Session = Depends(get_session),
):
    users = session.exec(select(models.User)).all()
    return users


def get_user_from_id(session: Session, user_id: int) -> models.UserRead:
    owner = session.exec(
        select(models.User).where(models.User.id == user_id)
    ).fetchall()
    if len(owner) != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Found {len(owner)} owners with the given id"
                f" '{user_id}'; expected only one"
            ),
        )
    return owner[0]


def get_hardware_item_from_id(
    session: Session, hardware_item_id: int
) -> models.HardwareItem:
    item = session.exec(
        select(models.HardwareItem).where(models.HardwareItem.id == hardware_item_id)
    ).fetchall()
    if len(item) != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Found {len(item)} items with the given id"
                f" '{hardware_item_id}'; expected only one"
            ),
        )
    return item[0]


@app.post("/hardware", response_model=models.HardwareItemRead)
def create_hardware_item(
    *, session: Session = Depends(get_session), hardware_item: models.HardwareItemCreate
):
    get_user_from_id(session, hardware_item.owner_id)
    db_hardware_item = models.HardwareItem.from_orm(hardware_item)
    session.exec
    session.add(db_hardware_item)
    session.commit()
    session.refresh(db_hardware_item)
    return db_hardware_item


@app.get("/hardware", response_model=List[models.HardwareItemRead])
def read_hardware_items(
    *,
    session: Session = Depends(get_session),
):
    hardware_items = session.exec(select(models.HardwareItem)).all()
    return hardware_items


@app.delete("/hardware", response_model=models.HardwareItemRead)
def delete_hardware_item(
    *, session: Session = Depends(get_session), hardware_item_id: int
):
    hardware_item_to_delete = get_hardware_item_from_id(session, hardware_item_id)
    session.delete(hardware_item_to_delete)
    session.commit()
    return hardware_item_to_delete


@app.put("/hardware", response_model=models.HardwareItemRead)
def update_hardware_item(
    *,
    session: Session = Depends(get_session),
    hardware_item_id: int,
    owner_id: int = None,
    kind: constants.HARDWARE_KINDS = None,
    comment: str = None,
):
    hardware_item_to_update = get_hardware_item_from_id(session, hardware_item_id)

    if owner_id is not None:
        get_user_from_id(session, owner_id)
        hardware_item_to_update.owner_id = owner_id
    if kind is not None:
        hardware_item_to_update.kind = kind
    if comment is not None:
        hardware_item_to_update.comment = comment

    session.add(hardware_item_to_update)
    session.commit()
    session.refresh(hardware_item_to_update)

    return hardware_item_to_update
