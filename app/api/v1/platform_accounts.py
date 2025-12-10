from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.deps import get_current_user
from app.db.session import get_session
from app.crud.platform_account import (
    create_or_update_account,
    get_account_by_user_platform,
    get_accounts_for_user,
)
from app.schemas.platform import PlatformAccountCreate, PlatformAccountRead

router = APIRouter(prefix="/platform-accounts", tags=["platform-accounts"])


@router.get("/me", response_model=List[PlatformAccountRead])
def read_my_platform_accounts(
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    accounts = get_accounts_for_user(session, current_user.id)
    return accounts


@router.get("/me/{platform}", response_model=PlatformAccountRead)
def read_my_platform_account(
    platform: str,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    acc = get_account_by_user_platform(session, current_user.id, platform)
    if not acc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Platform account not found")
    return acc


@router.put("/me", response_model=PlatformAccountRead)
def upsert_my_platform_account(
    account_in: PlatformAccountCreate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    acc = create_or_update_account(session, current_user.id, account_in)
    return acc


@router.delete("/me/{platform}", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_platform_account(
    platform: str,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    acc = get_account_by_user_platform(session, current_user.id, platform)
    if not acc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Platform account not found")
    session.delete(acc)
    session.commit()
    return None
