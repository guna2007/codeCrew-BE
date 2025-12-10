from typing import Dict, Optional
from statistics import mean

from sqlmodel import Session, select

from app.crud.platform_account import get_accounts_for_user
from app.crud.snapshot import get_latest_snapshot
from app.models.platform_account import PlatformAccount
from app.models.snapshot import PlatformSnapshot


def get_latest_snapshots_for_user(session: Session, user_id: int):
    """
    Return dict keyed by platform with tuple (PlatformAccount, PlatformSnapshot | None)
    """
    result = {}
    accounts = get_accounts_for_user(session, user_id)
    for acc in accounts:
        snap = get_latest_snapshot(session, user_id, acc.platform)
        result[acc.platform] = (acc, snap)
    return result


def compute_summary(latest_snaps: Dict[str, tuple]) -> dict:
    """
    Compute a minimal summary:
      - total_problems_solved: sum of total_solved where present
      - platforms_connected: number of platforms present
      - avg_rating: mean of available ratings (if none, None)
    """
    total_solved = 0
    ratings = []
    for platform, (acc, snap) in latest_snaps.items():
        if snap and snap.total_solved:
            total_solved += snap.total_solved
        if snap and snap.rating is not None:
            ratings.append(snap.rating)

    avg_rating = round(mean(ratings), 2) if ratings else None

    return {
        "total_problems_solved": total_solved,
        "platforms_connected": len(latest_snaps),
        "avg_rating": avg_rating,
    }
