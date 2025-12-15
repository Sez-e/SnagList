from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.services.user_service.app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
)
from backend.services.user_service.app.db.models import User
from backend.services.user_service.app.db.session import get_db
from backend.services.user_service.app.core.auth import create_access_token
from backend.services.user_service.app.core.security import (
    hash_password,
    verify_password,
)
from backend.services.user_service.app.core.roles import Roles

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
async def register_user(
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.email == payload.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    new_user = User(
        email=payload.email,
        name=payload.name,
        password_hash=hash_password(payload.password),
        roles=[Roles.OBSERVER],
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    access_token = create_access_token(
        user_id=str(new_user.id),
        roles=new_user.roles,
    )

    return TokenResponse(access_token=access_token)


@router.post("/login", response_model=TokenResponse)
async def login_user(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        user_id=str(user.id),
        roles=user.roles,
    )

    return TokenResponse(access_token=access_token)
