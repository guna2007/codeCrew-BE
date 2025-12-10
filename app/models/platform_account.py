from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class PlatformAccount(SQLModel, table=True):
    __tablename__ = "platform_accounts"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)  # FK to users.id (logical)
    platform: str = Field(index=True)  # "leetcode", "codeforces", etc.
    handle: str

    is_active: bool = Field(default=True)
    last_synced_at: Optional[datetime] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
