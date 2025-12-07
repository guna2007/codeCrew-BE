from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.security import verify_password, create_access_token
from app.db.session import get_session
from app.schemas.user import UserCreate, UserRead, UserLogin
from app.schemas.token import Token
from app.crud.user import get_user_by_email, create_user

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, session: Session = Depends(get_session)) -> UserRead:
    existing = get_user_by_email(session, user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user = create_user(session, user_in)
    return UserRead(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.post("/login", response_model=Token)
def login(user_in: UserLogin, session: Session = Depends(get_session)) -> Token:
    user = get_user_by_email(session, user_in.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(subject=user.id)
    return Token(access_token=access_token, token_type="bearer")
