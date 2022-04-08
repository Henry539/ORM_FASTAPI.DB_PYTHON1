from typing import List

from pydantic import BaseModel


class DataCreate(BaseModel):
    FULLNAME: str
    AGE: int
    SEX: str
    PHONE: int


class DataUser(DataCreate):
    ID_DATA: int
    USER_ID: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    ID: int
    USERNAME: str


class UserCreate(UserBase):
    PASSWORD: str

    class Config:
        orm_mode = True


class User(UserBase):
    STATUS: bool
    DATA_USER: List[DataUser] = []

    class Config:
        orm_mode = True
