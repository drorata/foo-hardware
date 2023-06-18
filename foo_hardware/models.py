from typing import List, Optional

from sqlmodel import Column, Field, Relationship, SQLModel, String

from foo_hardware import constants


class UserBase(SQLModel):
    username: str = Field(sa_column=Column("username", String, unique=True))
    password: str
    items: List["HardwareItem"] = Relationship(back_populates="owner")


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int


class HardwareItemBase(SQLModel):
    kind: constants.HARDWARE_KINDS = Field(
        default=...,
        title="Type of hardware",
        description=(
            "Possible kinds are:"
            f" {[(e.name, e.value) for e in constants.HARDWARE_KINDS]}"
        ),
    )
    owner_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="items")
    comment: Optional[str]


class HardwareItem(HardwareItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class HardwareItemCreate(HardwareItemBase):
    class Config:
        pass


class HardwareItemRead(HardwareItemBase):
    id: int
