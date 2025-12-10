from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel


class PlatformSnapshotCreate(SQLModel):
    platform: str
    rating: Optional[int] = None
    max_rating: Optional[int] = None
    total_solved: Optional[int] = None
    easy_solved: Optional[int] = None
    medium_solved: Optional[int] = None
    hard_solved: Optional[int] = None
    contests_played: Optional[int] = None
    raw_data: Optional[str] = None


class PlatformSnapshotRead(SQLModel):
    id: int
    user_id: int
    platform: str
    rating: Optional[int] = None
    max_rating: Optional[int] = None
    total_solved: Optional[int] = None
    easy_solved: Optional[int] = None
    medium_solved: Optional[int] = None
    hard_solved: Optional[int] = None
    contests_played: Optional[int] = None
    raw_data: Optional[str] = None
    created_at: datetime
