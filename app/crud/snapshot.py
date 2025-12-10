from typing import List, Optional

from sqlmodel import Session, select
from datetime import datetime

from app.models.snapshot import PlatformSnapshot
from app.schemas.snapshot import PlatformSnapshotCreate


def create_snapshot(session: Session, user_id: int, snap_in: PlatformSnapshotCreate) -> PlatformSnapshot:
    db = PlatformSnapshot(
        user_id=user_id,
        platform=snap_in.platform,
        rating=snap_in.rating,
        max_rating=snap_in.max_rating,
        total_solved=snap_in.total_solved,
        easy_solved=snap_in.easy_solved,
        medium_solved=snap_in.medium_solved,
        hard_solved=snap_in.hard_solved,
        contests_played=snap_in.contests_played,
        raw_data=snap_in.raw_data,
        created_at=datetime.utcnow(),
    )
    session.add(db)
    session.commit()
    session.refresh(db)
    return db


def get_snapshots_for_user(session: Session, user_id: int, platform: Optional[str] = None) -> List[PlatformSnapshot]:
    statement = select(PlatformSnapshot).where(PlatformSnapshot.user_id == user_id)
    if platform:
        statement = statement.where(PlatformSnapshot.platform == platform)
    statement = statement.order_by(PlatformSnapshot.created_at.desc())
    return session.exec(statement).all()


def get_latest_snapshot(session: Session, user_id: int, platform: str) -> Optional[PlatformSnapshot]:
    statement = (
        select(PlatformSnapshot)
        .where(PlatformSnapshot.user_id == user_id)
        .where(PlatformSnapshot.platform == platform)
        .order_by(PlatformSnapshot.created_at.desc())
    )
    return session.exec(statement).first()
