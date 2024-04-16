from typing import List

from pydantic import BaseModel, Field


class UserData(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str


class CustomUsr(BaseModel):
    name: str


class CustomUsrData(BaseModel):
    bool: bool
    int: int
    float: float
    string: str
    array: List[str]
    Usr: CustomUsr


class UserOutSchema(BaseModel):
    data: UserData


class UserPageOutSchema(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[UserData]


class UserCreateOutSchema(BaseModel):
    id: str
    createdAt: str


class CustomUsrCreateOutSchema(BaseModel):
    id: str
    name: str
    job: str
    createdAt: str


class UserUpdateOutSchema(BaseModel):
    id: str
    name: str | None
    data: UserData | None
    updatedAt: str


class CustomUsrUpdateOutSchema(BaseModel):
    updatedAt: str
