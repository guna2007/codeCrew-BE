from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.deps import get_current_user
from app.crud.snapshot import get_snapshots_for_user
from app.db.session import get_session
from app.schemas.snapshot import PlatformSnapshotRead

router = APIRouter(prefix="/snapshots", tags=["snapshots"])


@router.get("/me", response_model=List[PlatformSnapshotRead])
def read_my_snapshots(
    platform: Optional[str] = None,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    snaps = get_snapshots_for_user(session, current_user.id, platform)
    return snaps
