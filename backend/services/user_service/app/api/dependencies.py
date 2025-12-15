from typing import Set

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.services.user_service.app.core.auth import decode_access_token
from backend.services.user_service.app.core.permissions import ROLE_PERMISSIONS
from backend.services.user_service.app.db.session import get_db
from backend.services.user_service.app.db.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload = decode_access_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id: str = payload.get("sub")
    roles: list[str] = payload.get("roles", [])

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    user.roles = roles
    return user


def get_user_permissions(roles: list[str]) -> Set[str]:
    permissions: Set[str] = set()

    for role in roles:
        permissions |= ROLE_PERMISSIONS.get(role, set())

    return permissions


def require_permission(permission: str):
    async def checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        permissions = get_user_permissions(current_user.roles)

        if permission not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

        return current_user

    return checker
