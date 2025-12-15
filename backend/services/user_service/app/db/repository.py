from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from .models import User  # noqa


async def create_user(
    db: AsyncSession,
    *,
    email: str,
    password_hash: str,
    name: Optional[str],
    roles: list[str],
) -> User:
    """
    Создание пользователя
    """
    user = User(
        email=email,
        password_hash=password_hash,
        name=name,
        roles=roles,
    )

    db.add(user)
    try:
        await db.flush()  # Получаем id без коммита
    except IntegrityError:
        raise

    return user


async def get_user_by_email(
    db: AsyncSession,
    email: str,
) -> Optional[User]:
    """
    Получение пользователя по email
    """
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


async def get_user_by_id(
    db: AsyncSession,
    user_id,
) -> Optional[User]:
    """
    Получение пользователя по id
    """
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def update_user(
    db: AsyncSession,
    user_id,
    *,
    name: Optional[str] = None,
    roles: Optional[list[str]] = None,
) -> Optional[User]:
    """
    Обновление пользователя
    """
    values = {}
    if name is not None:
        values["name"] = name
    if roles is not None:
        values["roles"] = roles

    if values:
        await db.execute(
            update(User)
            .where(User.id == user_id)
            .values(**values)
        )

    return await get_user_by_id(db, user_id)


async def delete_user(
    db: AsyncSession,
    user_id
) -> bool:
    """
    Удаление пользователя
    """
    result = await db.execute(
        delete(User).where(User.id == user_id)
    )
    return result.rowcount > 0


async def list_users(
    db: AsyncSession,
    *,
    offset: int = 0,
    limit: int = 20,
) -> List[User]:
    """
    Список пользователей
    """
    result = await db.execute(
        select(User)
        .offset(offset)
        .limit(limit)
        .order_by(User.created_at.desc())
    )
    return result.scalars().all()
