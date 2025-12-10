from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.deps import get_current_user
from app.crud.platform_account import get_account_by_user_platform
from app.crud.snapshot import create_snapshot, get_snapshots_for_user
from app.db.session import get_session
from app.schemas.snapshot import PlatformSnapshotCreate, PlatformSnapshotRead
from app.services.codeforces import fetch_codeforces_profile

router = APIRouter(prefix="/sync", tags=["sync"])


@router.post("/platform/{platform}", response_model=PlatformSnapshotRead)
def sync_platform(
    platform: str,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Sync the given platform for current user. For now supports 'codeforces' only.
    """
    # find user's handle for this platform
    acc = get_account_by_user_platform(session, current_user.id, platform)
    if not acc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Platform account not found")

    handle = acc.handle

    if platform.lower() == "codeforces":
        data = fetch_codeforces_profile(handle)
        snap_in = PlatformSnapshotCreate(
            platform="codeforces",
            rating=data.get("rating"),
            max_rating=data.get("max_rating"),
            total_solved=data.get("total_solved"),
            contests_played=data.get("contests_played"),
            raw_data=data.get("raw_data"),
        )
        snap = create_snapshot(session, current_user.id, snap_in)
        # update last_synced_at on account
        acc.last_synced_at = snap.created_at
        session.add(acc)
        session.commit()
        session.refresh(acc)
        return snap

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported platform")
