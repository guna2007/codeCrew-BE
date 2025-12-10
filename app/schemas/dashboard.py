from typing import Dict, List, Optional
from sqlmodel import SQLModel
from datetime import datetime


class DashboardPlatform(SQLModel):
    platform: str
    handle: Optional[str] = None
    rating: Optional[int] = None
    max_rating: Optional[int] = None
    total_solved: Optional[int] = None
    contests_played: Optional[int] = None
    last_synced_at: Optional[datetime] = None
    snapshot_created_at: Optional[datetime] = None
    raw_data: Optional[str] = None


class DashboardSummary(SQLModel):
    total_problems_solved: int = 0
    platforms_connected: int = 0
    avg_rating: Optional[float] = None


class DashboardResponse(SQLModel):
    platforms: Dict[str, DashboardPlatform]
    summary: DashboardSummary
