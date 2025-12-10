from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel


class PlatformAccountBase(SQLModel):
    platform: str
    handle: str


class PlatformAccountCreate(PlatformAccountBase):
    pass


class PlatformAccountUpdate(SQLModel):
    handle: str


class PlatformAccountRead(PlatformAccountBase):
    id: int
    user_id: int
    is_active: bool
    last_synced_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
