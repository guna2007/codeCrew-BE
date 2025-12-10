from typing import Dict

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.deps import get_current_user
from app.crud.dashboard import get_latest_snapshots_for_user, compute_summary
from app.db.session import get_session
from app.schemas.dashboard import DashboardResponse, DashboardPlatform, DashboardSummary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/me", response_model=DashboardResponse)
def get_my_dashboard(current_user=Depends(get_current_user), session: Session = Depends(get_session)):
    latest = get_latest_snapshots_for_user(session, current_user.id)

    platforms_dict: Dict[str, DashboardPlatform] = {}
    for platform, (acc, snap) in latest.items():
        platforms_dict[platform] = DashboardPlatform(
            platform=platform,
            handle=acc.handle if acc else None,
            rating=snap.rating if snap else None,
            max_rating=snap.max_rating if snap else None,
            total_solved=snap.total_solved if snap else None,
            contests_played=snap.contests_played if snap else None,
            last_synced_at=acc.last_synced_at if acc else None,
            snapshot_created_at=snap.created_at if snap else None,
            raw_data=snap.raw_data if snap else None,
        )

    summary_data = compute_summary(latest)
    summary = DashboardSummary(**summary_data)

    return DashboardResponse(platforms=platforms_dict, summary=summary)
