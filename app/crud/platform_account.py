from datetime import datetime
from typing import List, Optional

from sqlmodel import Session, select

from app.models.platform_account import PlatformAccount
from app.schemas.platform import PlatformAccountCreate, PlatformAccountUpdate


def get_accounts_for_user(session: Session, user_id: int) -> List[PlatformAccount]:
    statement = select(PlatformAccount).where(PlatformAccount.user_id == user_id)
    return session.exec(statement).all()


def get_account_by_user_platform(
    session: Session, user_id: int, platform: str
) -> Optional[PlatformAccount]:
    statement = (
        select(PlatformAccount)
        .where(PlatformAccount.user_id == user_id)
        .where(PlatformAccount.platform == platform)
    )
    return session.exec(statement).first()


def create_account(session: Session, user_id: int, account_in: PlatformAccountCreate) -> PlatformAccount:
    db_obj = PlatformAccount(
        user_id=user_id,
        platform=account_in.platform,
        handle=account_in.handle,
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_account(session: Session, db_obj: PlatformAccount, account_in: PlatformAccountUpdate) -> PlatformAccount:
    db_obj.handle = account_in.handle
    db_obj.updated_at = datetime.utcnow()
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def create_or_update_account(
    session: Session, user_id: int, account_in: PlatformAccountCreate
) -> PlatformAccount:
    existing = get_account_by_user_platform(session, user_id, account_in.platform)
    if existing:
        return update_account(session, existing, PlatformAccountUpdate(handle=account_in.handle))
    return create_account(session, user_id, account_in)
