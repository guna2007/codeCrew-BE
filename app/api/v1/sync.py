from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.deps import get_current_user
from app.crud.platform_account import (
    get_account_by_user_platform,
    get_accounts_for_user,
)
from app.crud.snapshot import create_snapshot
from app.db.session import get_session
from app.schemas.snapshot import PlatformSnapshotCreate, PlatformSnapshotRead
from app.services.codeforces import fetch_codeforces_profile

router = APIRouter(prefix="/sync", tags=["sync"])

# Keep existing single-platform sync (unchanged)
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


# NEW: sync all connected platforms for current user
@router.post("/me", response_model=List[Dict[str, Any]])
def sync_all_my_platforms(
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Sync all connected platforms for the current user.
    - For now only 'codeforces' performs a real sync (others return 'unsupported').
    - Skips platforms that were synced very recently (30s cooldown).
    Returns a list of per-platform results:
      { platform, handle, status: 'synced'|'skipped'|'unsupported'|'error', details }
    """
    results: List[Dict[str, Any]] = []
    cooldown_seconds = 30  # simple throttle to avoid accidental repeated syncs

    accounts = get_accounts_for_user(session, current_user.id)
    if not accounts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No platform accounts found for user")

    for acc in accounts:
        platform = acc.platform.lower()
        handle = acc.handle
        entry: Dict[str, Any] = {"platform": platform, "handle": handle, "status": None, "details": None}
        try:
            # Simple cooldown check
            if acc.last_synced_at:
                delta = datetime.utcnow() - acc.last_synced_at
                if delta.total_seconds() < cooldown_seconds:
                    entry["status"] = "skipped"
                    entry["details"] = f"Recently synced ({int(delta.total_seconds())}s ago). Cooldown {cooldown_seconds}s."
                    results.append(entry)
                    continue

            if platform == "codeforces":
                # perform the fetch & snapshot
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
                # update last_synced_at on account to snapshot timestamp
                acc.last_synced_at = snap.created_at
                session.add(acc)
                session.commit()
                session.refresh(acc)

                entry["status"] = "synced"
                entry["details"] = {"snapshot_id": snap.id, "created_at": snap.created_at.isoformat()}
            else:
                # unsupported platform for now
                entry["status"] = "unsupported"
                entry["details"] = "Sync not implemented for this platform yet"
        except Exception as exc:
            # do not fail whole loop; capture the error per-platform
            entry["status"] = "error"
            entry["details"] = str(exc)

        results.append(entry)

    return results
