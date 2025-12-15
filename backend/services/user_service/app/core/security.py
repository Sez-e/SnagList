from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

MIN_PASSWORD_LENGTH = 8


def hash_password(plain_password: str) -> str:
    """
    Хэширование пароля
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверка пароля
    """
    return pwd_context.verify(plain_password, hashed_password)


def validate_password_policy(password: str) -> bool:
    """
    Проверка минимальных требований к паролю
    """
    if len(password) < MIN_PASSWORD_LENGTH:
        return False
    return True
