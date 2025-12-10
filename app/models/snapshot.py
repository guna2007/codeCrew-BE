from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class PlatformSnapshot(SQLModel, table=True):
    __tablename__ = "platform_snapshots"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    platform: str = Field(index=True)  # "leetcode", "codeforces", etc.

    rating: Optional[int] = None
    max_rating: Optional[int] = None
    total_solved: Optional[int] = None
    easy_solved: Optional[int] = None
    medium_solved: Optional[int] = None
    hard_solved: Optional[int] = None
    contests_played: Optional[int] = None

    # Raw JSON string of all stats returned from API (for debugging/future use)
    raw_data: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
