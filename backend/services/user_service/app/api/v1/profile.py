from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.services.user_service.app.schemas.user import UserUpdate, UserResponse
from backend.services.user_service.app.db.models import User
from backend.services.user_service.app.db.session import get_db
from backend.services.user_service.app.core.security import hash_password
from backend.services.user_service.app.api.dependencies import get_current_user

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/", response_model=UserResponse)
async def update_profile(
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated = False

    if payload.name is not None:
        current_user.name = payload.name
        updated = True

    if payload.password is not None:
        current_user.password_hash = hash_password(payload.password)
        updated = True

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields to update",
        )

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return current_user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await db.delete(current_user)
    await db.commit()
    return None
