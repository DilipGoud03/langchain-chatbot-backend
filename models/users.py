from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.user_addresses import UserAddress


class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    password: str
    user_type: Optional[str] = ''


class ReadUser(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    user_type: Optional[str] = ''
    addresses: List[UserAddress] = []


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class LoggedInUser(BaseModel):
    id: int
    email: str
    name: str
    user_type: str

    class Config:
        from_attributes = True


class Meta(BaseModel):
    current_item: Optional[int]
    total_items: Optional[int]
    limit: Optional[int]
    page: Optional[int]


class UserList(BaseModel):
    meta: Meta
    users: List[ReadUser]
