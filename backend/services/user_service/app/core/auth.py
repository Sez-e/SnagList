from datetime import datetime, timedelta
from typing import Optional, List

import jwt

from .config import settings  # noqa


ALGORITHM = "HS256"


def create_access_token(
    *,
    user_id: str,
    roles: List[str],
    expires_delta: Optional[timedelta] = None,
) -> str:
    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    )

    payload = {
        "sub": user_id,
        "roles": roles,
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=ALGORITHM,
    )

    return token


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[ALGORITHM],
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")

    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
