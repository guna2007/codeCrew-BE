from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel


class UserBase(SQLModel):
    email: str
    full_name: Optional[str] = None
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UserLogin(SQLModel):
    email: str
    password: str
